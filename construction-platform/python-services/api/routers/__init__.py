# API Routers
# construction-platform/python-services/api/routers/__init__.py

from fastapi import APIRouter

# Version 1 router
from .v1 import v1_router

__all__ = ["v1_router"]
