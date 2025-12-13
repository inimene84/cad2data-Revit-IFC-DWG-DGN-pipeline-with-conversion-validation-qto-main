# API Version 1 Router
# construction-platform/python-services/api/routers/v1/__init__.py

from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1", tags=["v1"])

# Import and include all v1 endpoints
from . import health, analytics, usage, billing, errors, audit, vector, archival, automation, backup, settings
# New functional routers
from . import projects, materials, reports, chat

v1_router.include_router(health.router)
v1_router.include_router(analytics.router)
v1_router.include_router(usage.router)
v1_router.include_router(billing.router)
v1_router.include_router(errors.router)
v1_router.include_router(audit.router)
v1_router.include_router(vector.router)
v1_router.include_router(archival.router)
v1_router.include_router(automation.router)
v1_router.include_router(backup.router)
v1_router.include_router(settings.router)
# New functional routers
v1_router.include_router(projects.router)
v1_router.include_router(materials.router)
v1_router.include_router(reports.router)
v1_router.include_router(chat.router)

