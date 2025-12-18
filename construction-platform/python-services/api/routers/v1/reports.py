# Reports Router - Version 1
# construction-platform/python-services/api/routers/v1/reports.py

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime
import logging
import os
import json
import io
import base64
import math
from config import VAT_RATE, VAT_LABEL

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["reports"])

# In-memory storage
reports_db: dict = {}
report_counter = 0


def sanitize_value(value: Any) -> Any:
    """Sanitize value for JSON serialization"""
    if value is None:
        return None
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: sanitize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_value(v) for v in value]
    return value


class ReportCreate(BaseModel):
    name: str
    project_id: Optional[int] = None
    type: str = "boq"  # boq, cost_estimate, materials_list
    include_vat: bool = True
    region: str = "Tartu"
    materials: Optional[List[dict]] = None  # Materials with costs from extraction


class ReportResponse(BaseModel):
    id: int
    name: str
    project_id: Optional[int]
    type: str
    status: str
    total_cost: Optional[float]
    file_path: Optional[str]
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            float: lambda v: None if (isinstance(v, float) and (math.isnan(v) or math.isinf(v))) else v
        }


@router.get("")
async def list_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    project_id: Optional[int] = None,
    type: Optional[str] = None
):
    """List all generated reports with filtering and pagination."""
    reports = list(reports_db.values())
    
    if project_id:
        reports = [r for r in reports if r["project_id"] == project_id]
    
    if type:
        reports = [r for r in reports if r["type"] == type]
    
    # Sort by created_at descending
    reports.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Sanitize all values for JSON
    return [sanitize_value(r) for r in reports[skip:skip + limit]]


@router.get("/{report_id}")
async def get_report(report_id: int):
    """Get a single report by ID."""
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    return sanitize_value(reports_db[report_id])


@router.post("/generate", status_code=201)
async def generate_report(report_data: ReportCreate):
    """Generate a new BOQ or cost estimation report."""
    global report_counter
    report_counter += 1
    
    now = datetime.now()
    
    # Calculate VAT (Estonian VAT rate from config)
    vat_rate = VAT_RATE if report_data.include_vat else 0
    
    # Calculate cost from materials if provided
    base_cost = 0.0
    materials_list = []
    if report_data.materials:
        for m in report_data.materials:
            # Get price from material data
            price = float(m.get('estimated_price') or m.get('price') or m.get('cost') or 0)
            quantity = float(m.get('quantity') or 1)
            item_cost = price * quantity
            base_cost += item_cost
            materials_list.append({
                'name': m.get('name') or m.get('material') or 'Unknown',
                'quantity': quantity,
                'unit': m.get('unit', 'unit'),
                'unit_price': price,
                'total_price': item_cost
            })
    
    # If no materials or zero cost, use a fallback
    if base_cost == 0:
        base_cost = 0.0  # No placeholder - show actual zero
        
    vat_amount = base_cost * vat_rate
    total_cost = base_cost + vat_amount
    
    new_report = {
        "id": report_counter,
        "name": report_data.name,
        "project_id": report_data.project_id,
        "type": report_data.type,
        "status": "completed",
        "total_cost": round(total_cost, 2),
        "base_cost": round(base_cost, 2),
        "vat_amount": round(vat_amount, 2),
        "region": report_data.region,
        "include_vat": report_data.include_vat,
        "materials": materials_list,
        "materials_count": len(materials_list),
        "file_path": None,
        "created_at": now
    }
    
    reports_db[report_counter] = new_report
    logger.info(f"Generated report: {report_data.name} (ID: {report_counter})")
    
    return sanitize_value(new_report)


@router.get("/{report_id}/download")
async def download_report(report_id: int):
    """Download a report as PDF."""
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report = reports_db[report_id]
    
    # Generate PDF content
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Title
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, 750, report["name"])
        
        # Report details
        p.setFont("Helvetica", 12)
        p.drawString(100, 720, f"Report Type: {report['type'].upper()}")
        p.drawString(100, 700, f"Region: {report.get('region', 'N/A')}")
        created_at = report['created_at']
        if isinstance(created_at, datetime):
            p.drawString(100, 680, f"Generated: {created_at.strftime('%Y-%m-%d %H:%M')}")
        else:
            p.drawString(100, 680, f"Generated: {created_at}")
        
        # Cost summary
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 640, "Cost Summary")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 620, f"Base Cost: €{report.get('base_cost', 0):.2f}")
        if report.get('include_vat'):
            p.drawString(100, 600, f"{VAT_LABEL}: €{report.get('vat_amount', 0):.2f}")
        p.drawString(100, 580, f"Total Cost: €{report.get('total_cost', 0):.2f}")
        
        p.save()
        
        pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            "report_id": report_id,
            "filename": f"{report['name'].replace(' ', '_')}.pdf",
            "content_type": "application/pdf",
            "pdf_base64": pdf_base64
        }
        
    except ImportError:
        # If reportlab not available, return JSON instead
        return {
            "report_id": report_id,
            "filename": f"{report['name'].replace(' ', '_')}.json",
            "content_type": "application/json",
            "data": sanitize_value(report)
        }


@router.delete("/{report_id}", status_code=204)
async def delete_report(report_id: int):
    """Delete a report."""
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    
    del reports_db[report_id]
    logger.info(f"Deleted report ID: {report_id}")
    return None


@router.get("/stats/summary")
async def get_reports_summary():
    """Get summary statistics for all reports."""
    reports = list(reports_db.values())
    
    total_value = sum(r.get("total_cost", 0) or 0 for r in reports)
    
    by_type = {}
    for r in reports:
        t = r["type"]
        if t not in by_type:
            by_type[t] = 0
        by_type[t] += 1
    
    return {
        "total_reports": len(reports),
        "total_value": round(total_value, 2),
        "by_type": by_type,
        "currency": "EUR"
    }
