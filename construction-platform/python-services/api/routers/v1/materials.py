# Materials Router - Version 1
# construction-platform/python-services/api/routers/v1/materials.py

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime
import logging
import math

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/materials", tags=["materials"])

# In-memory storage
materials_db: dict = {}
material_counter = 0


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


# Pre-populate with Estonian construction materials
ESTONIAN_MATERIALS = [
    {"name": "Concrete C25/30", "unit": "m³", "price": 85.00, "supplier": "Betoonimeister"},
    {"name": "Steel Rebar B500B", "unit": "kg", "price": 0.85, "supplier": "BLRT Refonda"},
    {"name": "Brick 250x120x65", "unit": "pcs", "price": 0.35, "supplier": "Wienerberger"},
    {"name": "Cement CEM I 42.5", "unit": "kg", "price": 0.12, "supplier": "Kunda Nordic"},
    {"name": "Sand 0-4mm", "unit": "m³", "price": 25.00, "supplier": "Paekivitoodete Tehas"},
    {"name": "Crushed Stone 16-32mm", "unit": "m³", "price": 32.00, "supplier": "Harku Karjäär"},
    {"name": "Timber C24", "unit": "m³", "price": 450.00, "supplier": "Toftan"},
    {"name": "OSB Board 18mm", "unit": "m²", "price": 12.50, "supplier": "Estonian Cell"},
    {"name": "Mineral Wool 100mm", "unit": "m²", "price": 8.50, "supplier": "Paroc"},
    {"name": "XPS Insulation 100mm", "unit": "m²", "price": 15.00, "supplier": "Styrofoam"},
]


def init_materials():
    """Initialize materials database with Estonian construction materials."""
    global material_counter
    for mat in ESTONIAN_MATERIALS:
        material_counter += 1
        now = datetime.now()
        materials_db[material_counter] = {
            "id": material_counter,
            "name": mat["name"],
            "quantity": 0.0,
            "unit": mat["unit"],
            "price": mat["price"],
            "supplier": mat["supplier"],
            "project_id": None,
            "category": "construction",
            "created_at": now,
            "updated_at": now
        }


# Initialize on module load
init_materials()


class MaterialCreate(BaseModel):
    name: str
    quantity: float = 0
    unit: str = "unit"
    price: float = 0
    supplier: Optional[str] = None
    project_id: Optional[int] = None
    category: str = "construction"


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    project_id: Optional[int] = None
    category: Optional[str] = None


@router.get("")
async def list_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    project_id: Optional[int] = None
):
    """List all materials with filtering, search, and pagination."""
    materials = list(materials_db.values())
    
    if search:
        search_lower = search.lower()
        materials = [m for m in materials if search_lower in m["name"].lower()]
    
    if category:
        materials = [m for m in materials if m["category"] == category]
    
    if project_id:
        materials = [m for m in materials if m["project_id"] == project_id]
    
    materials = materials[skip:skip + limit]
    
    return [sanitize_value(m) for m in materials]


@router.get("/search")
async def search_materials(q: str = Query(..., min_length=1)):
    """Search materials by name."""
    search_lower = q.lower()
    results = [
        sanitize_value(m) for m in materials_db.values() 
        if search_lower in m["name"].lower()
    ]
    return {"query": q, "count": len(results), "results": results}


@router.get("/{material_id}")
async def get_material(material_id: int):
    """Get a single material by ID."""
    if material_id not in materials_db:
        raise HTTPException(status_code=404, detail="Material not found")
    return sanitize_value(materials_db[material_id])


@router.post("", status_code=201)
async def create_material(material: MaterialCreate):
    """Create a new material."""
    global material_counter
    material_counter += 1
    
    now = datetime.now()
    new_material = {
        "id": material_counter,
        "name": material.name,
        "quantity": float(material.quantity) if material.quantity else 0.0,
        "unit": material.unit,
        "price": float(material.price) if material.price else 0.0,
        "supplier": material.supplier,
        "project_id": material.project_id,
        "category": material.category,
        "created_at": now,
        "updated_at": now
    }
    
    materials_db[material_counter] = new_material
    logger.info(f"Created material: {material.name} (ID: {material_counter})")
    
    return sanitize_value(new_material)


@router.put("/{material_id}")
async def update_material(material_id: int, material: MaterialUpdate):
    """Update an existing material."""
    if material_id not in materials_db:
        raise HTTPException(status_code=404, detail="Material not found")
    
    existing = materials_db[material_id]
    
    update_data = material.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            existing[key] = value
    
    existing["updated_at"] = datetime.now()
    materials_db[material_id] = existing
    
    logger.info(f"Updated material ID: {material_id}")
    return sanitize_value(existing)


@router.delete("/{material_id}", status_code=204)
async def delete_material(material_id: int):
    """Delete a material."""
    if material_id not in materials_db:
        raise HTTPException(status_code=404, detail="Material not found")
    
    del materials_db[material_id]
    logger.info(f"Deleted material ID: {material_id}")
    return None


@router.get("/stats/summary")
async def get_materials_summary():
    """Get summary statistics for all materials."""
    materials = list(materials_db.values())
    
    total_value = 0.0
    for m in materials:
        price = m.get("price", 0) or 0
        quantity = m.get("quantity", 0) or 0
        if isinstance(price, (int, float)) and isinstance(quantity, (int, float)):
            total_value += price * quantity
    
    categories = {}
    for m in materials:
        cat = m.get("category", "unknown")
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    return {
        "total_materials": len(materials),
        "total_value": round(total_value, 2),
        "by_category": categories,
        "currency": "EUR"
    }
