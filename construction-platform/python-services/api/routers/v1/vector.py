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
                    "vectors_count": info.points_count,
                    "status": info.status.value if hasattr(info.status, 'value') else str(info.status)
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
        
        # Search QDRANT using query_points (new API)
        search_result = qdrant.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=request.limit,
            query_filter=query_filter
        )
        results = search_result.points
        
        # Transform results
        work_items = []
        for r in results:
            payload = r.payload or {}
            # Data is nested in payload_full
            pf = payload.get("payload_full", {})
            cost = pf.get("cost_summary", {})
            hierarchy = pf.get("hierarchy", {})
            
            work_items.append(WorkItem(
                score=round(r.score, 4),
                rate_code=pf.get("rate_code", ""),
                name=pf.get("rate_name", ""),
                unit=pf.get("rate_unit", ""),
                price_median=cost.get("total_cost_position"),
                price_min=cost.get("total_resource_cost_position"),
                price_max=cost.get("total_cost_position"),
                labor_hours=cost.get("worker_labor_hours"),
                department=hierarchy.get("department_name"),
                category=hierarchy.get("category_type")
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


# ===== BULK COST ESTIMATION ENDPOINT =====

class MaterialItem(BaseModel):
    """Input material/work item for cost estimation"""
    name: str
    quantity: float = 1.0
    unit: str = "unit"
    category: Optional[str] = None


class EstimatedItem(BaseModel):
    """Estimated cost for a single item"""
    input_name: str
    input_quantity: float
    input_unit: str
    category: str
    ddc_rate_code: str
    ddc_name: str
    ddc_unit: str
    unit_price: float
    labor_hours: float
    total_net: float
    vat_rate: float
    vat_amount: float
    total_gross: float
    confidence_percent: int


class BulkEstimationRequest(BaseModel):
    """Request for bulk cost estimation"""
    materials: List[MaterialItem]
    language: str = "en"
    country: str = "EE"  # ISO 2-letter code


class BulkEstimationResponse(BaseModel):
    """Full cost estimation response"""
    project_name: Optional[str] = None
    country: str
    currency: str
    vat_rate: float
    total_net: float
    total_vat: float
    total_gross: float
    total_labor_hours: float
    items_count: int
    avg_confidence: int
    items: List[EstimatedItem]
    cost_by_category: dict
    generated_at: str


# VAT rates by country
VAT_RATES = {
    "EE": 0.24,  # Estonia
    "FI": 0.255, # Finland
    "DE": 0.19,  # Germany
    "LV": 0.21,  # Latvia
    "LT": 0.21,  # Lithuania
    "PL": 0.23,  # Poland
    "SE": 0.25,  # Sweden
    "NO": 0.25,  # Norway
    "DK": 0.25,  # Denmark
}


@router.post("/estimate", response_model=BulkEstimationResponse)
async def bulk_cost_estimation(request: BulkEstimationRequest):
    """
    Bulk cost estimation for multiple materials/work items.
    
    Takes a list of materials with quantities and returns complete cost
    breakdown using DDC CWICR database pricing with VAT calculation.
    """
    from datetime import datetime
    
    try:
        from qdrant_client import QdrantClient
        from openai import OpenAI
        
        # Get VAT rate for country
        vat_rate = VAT_RATES.get(request.country.upper(), 0.24)
        
        # Validate language
        if request.language.lower() not in AVAILABLE_COLLECTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' not available"
            )
        
        collection_name = AVAILABLE_COLLECTIONS[request.language.lower()]
        
        # Initialize clients
        qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
        
        openai = OpenAI(api_key=OPENAI_API_KEY)
        
        # Process each material
        estimated_items = []
        total_net = 0.0
        total_vat = 0.0
        total_gross = 0.0
        total_labor_hours = 0.0
        total_confidence = 0
        cost_by_category = {}
        
        for material in request.materials:
            # Generate embedding
            embedding_response = openai.embeddings.create(
                input=material.name,
                model="text-embedding-3-large"
            )
            query_vector = embedding_response.data[0].embedding
            
            # Search QDRANT
            search_result = qdrant.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=1
            )
            
            # Get best match
            if search_result.points:
                best = search_result.points[0]
                payload = best.payload or {}
                pf = payload.get("payload_full", {})
                cost = pf.get("cost_summary", {})
                hierarchy = pf.get("hierarchy", {})
                
                unit_price = cost.get("total_cost_position", 0) or 0
                labor_hours = (cost.get("worker_labor_hours", 0) or 0)
                confidence = int(best.score * 100)
                ddc_name = pf.get("rate_name", "")
                ddc_rate_code = pf.get("rate_code", "")
                ddc_unit = pf.get("rate_unit", "")
                category = material.category or hierarchy.get("department_name", "Other")
            else:
                unit_price = 0
                labor_hours = 0
                confidence = 0
                ddc_name = "Not found"
                ddc_rate_code = ""
                ddc_unit = ""
                category = material.category or "Other"
            
            # Calculate costs
            item_net = unit_price * material.quantity
            item_vat = item_net * vat_rate
            item_gross = item_net + item_vat
            item_labor = labor_hours * material.quantity
            
            # Add to totals
            total_net += item_net
            total_vat += item_vat
            total_gross += item_gross
            total_labor_hours += item_labor
            total_confidence += confidence
            
            # Track by category
            if category not in cost_by_category:
                cost_by_category[category] = {"count": 0, "cost": 0}
            cost_by_category[category]["count"] += 1
            cost_by_category[category]["cost"] += item_gross
            
            estimated_items.append(EstimatedItem(
                input_name=material.name,
                input_quantity=material.quantity,
                input_unit=material.unit,
                category=category,
                ddc_rate_code=ddc_rate_code,
                ddc_name=ddc_name,
                ddc_unit=ddc_unit,
                unit_price=round(unit_price, 2),
                labor_hours=round(labor_hours, 2),
                total_net=round(item_net, 2),
                vat_rate=vat_rate,
                vat_amount=round(item_vat, 2),
                total_gross=round(item_gross, 2),
                confidence_percent=confidence
            ))
        
        avg_confidence = int(total_confidence / len(request.materials)) if request.materials else 0
        
        return BulkEstimationResponse(
            country=request.country.upper(),
            currency="EUR",
            vat_rate=vat_rate,
            total_net=round(total_net, 2),
            total_vat=round(total_vat, 2),
            total_gross=round(total_gross, 2),
            total_labor_hours=round(total_labor_hours, 2),
            items_count=len(estimated_items),
            avg_confidence=avg_confidence,
            items=estimated_items,
            cost_by_category=cost_by_category,
            generated_at=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Estimation failed: {str(e)}")
