# Vector/Cost Estimation Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/vector.py
# Integrates with OpenConstructionEstimate-DDC-CWICR database (55K+ work items)

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter(prefix="/vector", tags=["vector", "cost-estimation"])

# QDRANT Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Available DDC CWICR collections
AVAILABLE_COLLECTIONS = {
    "en": "ddc_cwicr_en",
    "de": "ddc_cwicr_de",
    # Add more as needed: fr, es, ru, pt, zh, ar, hi
}


class CostSearchRequest(BaseModel):
    query: str
    language: str = "en"
    limit: int = 10
    filter_department: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None


class WorkItem(BaseModel):
    score: float
    rate_code: str
    name: str
    unit: str
    price_median: Optional[float] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    labor_hours: Optional[float] = None
    department: Optional[str] = None
    category: Optional[str] = None


class CostSearchResponse(BaseModel):
    query: str
    language: str
    total_results: int
    results: List[WorkItem]


@router.get("/health")
async def vector_health():
    """Check if QDRANT is accessible"""
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=5)
        collections = client.get_collections()
        return {
            "status": "healthy",
            "qdrant_host": QDRANT_HOST,
            "qdrant_port": QDRANT_PORT,
            "collections": [c.name for c in collections.collections]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "qdrant_host": QDRANT_HOST,
            "qdrant_port": QDRANT_PORT
        }


@router.get("/collections")
async def list_collections():
    """List available DDC CWICR collections"""
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=10)
        collections = client.get_collections()
        
        ddc_collections = []
        for c in collections.collections:
            if c.name.startswith("ddc_cwicr_"):
                info = client.get_collection(c.name)
                ddc_collections.append({
                    "name": c.name,
                    "language": c.name.replace("ddc_cwicr_", "").upper(),
                    "vectors_count": info.vectors_count,
                    "indexed": info.indexed_vectors_count
                })
        
        return {
            "available_collections": ddc_collections,
            "supported_languages": list(AVAILABLE_COLLECTIONS.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")


@router.post("/search", response_model=CostSearchResponse)
async def search_work_items(request: CostSearchRequest):
    """
    Semantic search for construction work items in DDC CWICR database.
    
    Uses OpenAI text-embedding-3-large for query embedding and searches
    the QDRANT vector database with 55,719 construction work items.
    """
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
        from openai import OpenAI
        
        # Validate language
        if request.language.lower() not in AVAILABLE_COLLECTIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Language '{request.language}' not available. Options: {list(AVAILABLE_COLLECTIONS.keys())}"
            )
        
        collection_name = AVAILABLE_COLLECTIONS[request.language.lower()]
        
        # Initialize clients
        qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
        
        openai = OpenAI(api_key=OPENAI_API_KEY)
        
        # Generate embedding for query using text-embedding-3-large (3072 dimensions)
        embedding_response = openai.embeddings.create(
            input=request.query,
            model="text-embedding-3-large"
        )
        query_vector = embedding_response.data[0].embedding
        
        # Build filters
        must_conditions = []
        
        if request.filter_department:
            must_conditions.append(
                FieldCondition(key="department_name", match=MatchValue(value=request.filter_department))
            )
        
        if request.price_min is not None or request.price_max is not None:
            range_params = {}
            if request.price_min is not None:
                range_params["gte"] = request.price_min
            if request.price_max is not None:
                range_params["lte"] = request.price_max
            must_conditions.append(
                FieldCondition(key="price_est_median", range=Range(**range_params))
            )
        
        query_filter = Filter(must=must_conditions) if must_conditions else None
        
        # Search QDRANT
        results = qdrant.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=request.limit,
            query_filter=query_filter
        )
        
        # Transform results
        work_items = []
        for r in results:
            payload = r.payload or {}
            work_items.append(WorkItem(
                score=round(r.score, 4),
                rate_code=payload.get("rate_code", ""),
                name=payload.get("rate_original_name", ""),
                unit=payload.get("rate_unit", ""),
                price_median=payload.get("price_est_median"),
                price_min=payload.get("price_est_min"),
                price_max=payload.get("price_est_max"),
                labor_hours=payload.get("labor_hours_workers"),
                department=payload.get("department_name"),
                category=payload.get("category_type")
            ))
        
        return CostSearchResponse(
            query=request.query,
            language=request.language.upper(),
            total_results=len(work_items),
            results=work_items
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/simple")
async def simple_search(
    q: str = Query(..., description="Search query (e.g., 'concrete foundation')"),
    lang: str = Query("en", description="Language: en, de"),
    limit: int = Query(5, ge=1, le=50, description="Number of results")
):
    """
    Simple GET endpoint for quick searches.
    
    Example: /v1/vector/search/simple?q=concrete+foundation&lang=en&limit=5
    """
    request = CostSearchRequest(query=q, language=lang, limit=limit)
    return await search_work_items(request)


@router.get("/item/{rate_code}")
async def get_work_item(rate_code: str, lang: str = Query("en")):
    """Get detailed information about a specific work item by code"""
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        if lang.lower() not in AVAILABLE_COLLECTIONS:
            raise HTTPException(status_code=400, detail=f"Language '{lang}' not available")
        
        collection_name = AVAILABLE_COLLECTIONS[lang.lower()]
        qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        # Scroll to find by rate_code
        results = qdrant.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(must=[
                FieldCondition(key="rate_code", match=MatchValue(value=rate_code))
            ]),
            limit=1,
            with_payload=True
        )
        
        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Work item '{rate_code}' not found")
        
        return results[0][0].payload
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get item: {str(e)}")
