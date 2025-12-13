# Analytics Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/analytics.py

from fastapi import APIRouter
from typing import Optional
import math

router = APIRouter(prefix="/analytics", tags=["analytics"])


def sanitize_float(value):
    """Sanitize float values to prevent JSON serialization errors"""
    if value is None:
        return None
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    return value


def sanitize_dict(data):
    """Recursively sanitize a dictionary for JSON serialization"""
    if isinstance(data, dict):
        return {k: sanitize_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_dict(item) for item in data]
    elif isinstance(data, float):
        return sanitize_float(data)
    return data


@router.get("/cost-trends")
async def get_cost_trends(period: str = "30d"):
    """Get cost trends - Version 1"""
    from datetime import datetime, timedelta
    days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
    start_date = datetime.now() - timedelta(days=days)
    
    # Placeholder data - replace with actual database query
    trends = [
        {"date": "2025-01-01", "total_cost": 50000, "material_cost": 30000, "labor_cost": 20000},
        {"date": "2025-01-02", "total_cost": 55000, "material_cost": 32000, "labor_cost": 23000},
    ]
    
    return sanitize_dict({"version": "v1", "period": period, "data": trends})


@router.get("/material-breakdown")
async def get_material_breakdown(period: str = "30d"):
    """Get material breakdown - Version 1"""
    breakdown = [
        {"name": "Concrete", "value": 15000},
        {"name": "Steel", "value": 12000},
    ]
    return sanitize_dict({"version": "v1", "period": period, "data": breakdown})


@router.get("/processing-metrics")
async def get_processing_metrics(period: str = "30d"):
    """Get processing metrics - Version 1"""
    metrics = {
        "files_processed": 150,
        "avg_processing_time": 12.5,
        "success_rate": 95.5,
        "total_elements": 276931
    }
    return sanitize_dict({"version": "v1", "period": period, "data": metrics})
