# Health Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/health.py

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health():
    """Health check endpoint - Version 1"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_version": "v1",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/detailed")
async def health_detailed():
    """Detailed health check - Version 1"""
    # Add detailed health checks here
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_version": "v1",
        "components": {
            "database": "connected",
            "redis": "connected",
            "qdrant": "connected"
        },
        "timestamp": datetime.now().isoformat()
    }
