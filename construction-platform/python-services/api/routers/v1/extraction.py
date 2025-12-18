from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Dict, Any
import logging
from datetime import datetime
import pandas as pd
import io
import fitz  # PyMuPDF
import tempfile
import os
import math
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor

from services.pdf_processing import process_pdf_page
from services.excel_processing import process_excel_sheet, deduplicate_cad_items
from utils.caching_helpers import get_cache_key, get_cached_result, set_cached_result
from utils.metrics import (
    pdf_processing_counter, 
    excel_processing_counter, 
    document_processing_time, 
    materials_detected_histogram
)
from config import MATERIAL_KEYWORDS
try:
    from routers.v1 import materials as mat_router
    API_VERSIONING_AVAILABLE = True
except ImportError:
    API_VERSIONING_AVAILABLE = False

router = APIRouter(
    prefix="/extraction",
    tags=["extraction"]
)

logger = logging.getLogger(__name__)

# Import dependencies (assuming some of these might need to be passed or imported from specific locations)
# For now, we will assume redis_client and others are available via dependency injection or simple imports if they were global.


@router.post("/pdf")
async def extract_pdf_data(file: UploadFile = File(...)):
    """Extract construction data from PDF files"""
    start_time = datetime.now()
    
    try:
        content = await file.read()
        
        # Cache logic would go here.
        # For this refactor, I will simplify and focus on the extraction logic moving to service.
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
            
        try:
            logger.info(f"Opening PDF from disk: {tmp_path}")
            doc = fitz.open(tmp_path)
            
            page_results = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Usng the imported service function
                result = process_pdf_page(page, page_num, MATERIAL_KEYWORDS)
                page_results.append(result)
            
            extracted_data = []
            construction_items = []
            
            for result in page_results:
                extracted_data.extend(result["text"])
                construction_items.extend(result["construction_items"])

            doc.close()
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "status": "success",
            "filename": file.filename,
            "pages_processed": len(extracted_data), # Approximation or need precise count
            "total_lines": len(extracted_data),
            "construction_items": construction_items,
            "sample_data": extracted_data[:10],
            "processing_time_seconds": processing_time,
            "cached": False
        }

    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/excel")
async def extract_excel_data(file: UploadFile = File(...)):
    """Extract construction data from Excel files with caching and async processing"""
    start_time = datetime.now()
    
    try:
        content = await file.read()
        
        # Check cache first
        cache_key = get_cache_key(content, "excel_extraction")
        cached_result = await get_cached_result(cache_key, "excel_extraction")
        if cached_result:
            logger.info(f"Returning cached result for {file.filename}")
            excel_processing_counter.labels(status='success', sheets='unknown').inc()
            return cached_result

        # Load Excel file
        try:
            excel_file = pd.ExcelFile(io.BytesIO(content))
        except Exception as e:
            logger.error(f"Invalid Excel file: {e}")
            raise HTTPException(status_code=400, detail="Invalid Excel file")

        sheets_data = {}
        construction_items = []
        sheet_count = len(excel_file.sheet_names)

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            result = process_excel_sheet(df, sheet_name)
            
            if "error" in result:
                sheets_data[sheet_name] = {"error": result["error"]}
            else:
                sheets_data[sheet_name] = result["sheet_data"]
                construction_items.extend(result["construction_items"])

        # Deduplicate CAD items
        construction_items = deduplicate_cad_items(construction_items)

        # Persist extracted materials to the materials database
        if construction_items and API_VERSIONING_AVAILABLE:
            saved_count = 0
            for item in construction_items:
                mat_router.material_counter += 1
                now = datetime.now()
                new_material = {
                    "id": mat_router.material_counter,
                    "name": item.get('material', 'Unknown'),
                    "quantity": float(item.get('quantity', 0)),
                    "unit": item.get('unit', 'unit'),
                    "price": float(item.get('price', 0)),
                    "supplier": None,
                    "project_id": None,
                    "category": item.get('category', 'extracted'),
                    "source_file": file.filename,
                    "created_at": now,
                    "updated_at": now
                }
                mat_router.materials_db[mat_router.material_counter] = new_material
                saved_count += 1
            logger.info(f"Saved {saved_count} materials to database from {file.filename}")

        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Record metrics
        document_processing_time.labels(
            document_type='excel',
            operation='extraction'
        ).observe(processing_time)
        
        excel_processing_counter.labels(
            status='success',
            sheets=str(sheet_count)
        ).inc()
        
        result = {
            "status": "success",
            "filename": file.filename,
            "sheets": list(excel_file.sheet_names),
            "sheets_data": sheets_data,
            "construction_items": construction_items,
            "materials_saved": len(construction_items) if construction_items else 0,
            "processing_time_seconds": processing_time,
            "cached": False
        }
        
        # Cache the result
        await set_cached_result(cache_key, result, ttl=7200)

        return result

    except Exception as e:
        logger.error(f"Excel extraction error: {e}")
        excel_processing_counter.labels(status='error', sheets='0').inc()
        raise HTTPException(status_code=500, detail=str(e))
