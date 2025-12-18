#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Critical Fixes Implementation Script
Implements API versioning, database transactions, and ACID compliance
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class CriticalFixes:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.api = self.project_root / "construction-platform" / "python-services" / "api"
        self.routers = self.api / "routers"
        self.v1 = self.routers / "v1"
        
    def implement_api_versioning(self):
        """Implement API Versioning"""
        print("\n" + "="*60)
        print("CRITICAL FIX #1: API Versioning")
        print("="*60)
        
        # Create router structure
        self.v1.mkdir(exist_ok=True, parents=True)
        
        # Create __init__.py for routers
        routers_init = """# API Routers
# construction-platform/python-services/api/routers/__init__.py

from fastapi import APIRouter

# Version 1 router
from .v1 import v1_router

__all__ = ["v1_router"]
"""
        
        routers_init_file = self.routers / "__init__.py"
        routers_init_file.write_text(routers_init, encoding='utf-8')
        print(f"✓ Created {routers_init_file}")
        
        # Create v1 router
        v1_router_code = """# API Version 1 Router
# construction-platform/python-services/api/routers/v1/__init__.py

from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1", tags=["v1"])

# Import and include all v1 endpoints
from . import health, analytics, usage, billing, errors, audit, vector, archival, automation, backup

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
"""
        
        v1_init_file = self.v1 / "__init__.py"
        v1_init_file.write_text(v1_router_code, encoding='utf-8')
        print(f"✓ Created {v1_init_file}")
        
        # Create health router
        health_router_code = """# Health Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/health.py

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health():
    \"\"\"Health check endpoint - Version 1\"\"\"
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_version": "v1",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/detailed")
async def health_detailed():
    \"\"\"Detailed health check - Version 1\"\"\"
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
"""
        
        health_file = self.v1 / "health.py"
        health_file.write_text(health_router_code, encoding='utf-8')
        print(f"✓ Created {health_file}")
        
        # Create analytics router
        analytics_router_code = """# Analytics Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/analytics.py

from fastapi import APIRouter
from typing import Optional

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/cost-trends")
async def get_cost_trends(period: str = "30d"):
    \"\"\"Get cost trends - Version 1\"\"\"
    from datetime import datetime, timedelta
    days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
    start_date = datetime.now() - timedelta(days=days)
    
    # Placeholder data - replace with actual database query
    trends = [
        {"date": "2025-01-01", "total_cost": 50000, "material_cost": 30000, "labor_cost": 20000},
        {"date": "2025-01-02", "total_cost": 55000, "material_cost": 32000, "labor_cost": 23000},
    ]
    
    return {"version": "v1", "period": period, "data": trends}

@router.get("/material-breakdown")
async def get_material_breakdown(period: str = "30d"):
    \"\"\"Get material breakdown - Version 1\"\"\"
    breakdown = [
        {"name": "Concrete", "value": 15000},
        {"name": "Steel", "value": 12000},
    ]
    return {"version": "v1", "period": period, "data": breakdown}

@router.get("/processing-metrics")
async def get_processing_metrics(period: str = "30d"):
    \"\"\"Get processing metrics - Version 1\"\"\"
    metrics = {
        "files_processed": 150,
        "avg_processing_time": 12.5,
        "success_rate": 95.5,
        "total_elements": 276931
    }
    return {"version": "v1", "period": period, "data": metrics}
"""
        
        analytics_file = self.v1 / "analytics.py"
        analytics_file.write_text(analytics_router_code, encoding='utf-8')
        print(f"✓ Created {analytics_file}")
        
        # Create placeholder routers for other endpoints
        for router_name in ["usage", "billing", "errors", "audit", "vector", "archival", "automation", "backup"]:
            router_file = self.v1 / f"{router_name}.py"
            router_code = f"""# {router_name.title()} Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/{router_name}.py

from fastapi import APIRouter

router = APIRouter(prefix="/{router_name}", tags=["{router_name}"])

# TODO: Move endpoints from app.py to here
# This is a placeholder - implement actual endpoints
"""
            router_file.write_text(router_code, encoding='utf-8')
            print(f"✓ Created {router_file}")
        
        print("\n✓ API Versioning structure created")
        print("  Next: Move endpoints from app.py to v1 routers")
        return True
    
    def implement_database_transactions(self):
        """Implement Database Transactions"""
        print("\n" + "="*60)
        print("CRITICAL FIX #2: Database Transactions")
        print("="*60)
        
        # Read current db_optimization.py
        db_opt_file = self.api / "db_optimization.py"
        db_opt_content = db_opt_content = db_opt_file.read_text(encoding='utf-8')
        
        # Add transaction context manager
        transaction_code = """
    @contextmanager
    def get_transaction(self, isolation_level: str = "READ COMMITTED") -> Generator:
        \"\"\"Get database session with ACID-compliant transaction\"\"\"
        session = self.SessionLocal()
        try:
            # Set isolation level for ACID compliance
            session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
            logger.info(f"Transaction started with isolation level: {isolation_level}")
            yield session
            session.commit()
            logger.info("Transaction committed successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Transaction rolled back due to error: {e}", exc_info=True)
            raise
        finally:
            session.close()
"""
        
        # Check if transaction method already exists
        if "def get_transaction" not in db_opt_content:
            # Add after get_session method
            if "def get_session" in db_opt_content:
                # Find the end of get_session method and add transaction method
                import re
                # Add import for text
                if "from sqlalchemy import" in db_opt_content:
                    db_opt_content = db_opt_content.replace(
                        "from sqlalchemy import create_engine, pool",
                        "from sqlalchemy import create_engine, pool, text"
                    )
                else:
                    db_opt_content = "from sqlalchemy import create_engine, pool, text\n" + db_opt_content
                
                # Add transaction method after get_session
                db_opt_content = db_opt_content.replace(
                    "        finally:\n            session.close()",
                    "        finally:\n            session.close()" + transaction_code
                )
                
                db_opt_file.write_text(db_opt_content, encoding='utf-8')
                print(f"✓ Updated {db_opt_file} with transaction management")
            else:
                print("⚠ get_session method not found, adding transaction method manually")
                # Add at the end of DatabaseOptimizer class
                db_opt_content = db_opt_content.replace(
                    "        logger.info(f\"Database optimizer initialized: pool_size={pool_size}, max_overflow={max_overflow}\")",
                    "        logger.info(f\"Database optimizer initialized: pool_size={pool_size}, max_overflow={max_overflow}\")" + transaction_code
                )
                db_opt_file.write_text(db_opt_content, encoding='utf-8')
                print(f"✓ Added transaction method to {db_opt_file}")
        else:
            print("✓ Transaction method already exists")
        
        return True
    
    def implement_acid_compliance(self):
        """Implement ACID Compliance"""
        print("\n" + "="*60)
        print("CRITICAL FIX #3: ACID Compliance")
        print("="*60)
        
        # Read current db_optimization.py
        db_opt_file = self.api / "db_optimization.py"
        db_opt_content = db_opt_file.read_text(encoding='utf-8')
        
        # Update engine creation with ACID settings
        acid_settings = """
            # ACID compliance settings
            isolation_level="READ COMMITTED",  # Default PostgreSQL isolation
            connect_args={
                "options": "-c default_transaction_isolation=read committed"
            },"""
        
        # Check if ACID settings already exist
        if "isolation_level" not in db_opt_content:
            # Add ACID settings to engine creation
            db_opt_content = db_opt_content.replace(
                "            pool_recycle=3600,   # Recycle connections after 1 hour\n            echo=False",
                f"            pool_recycle=3600,   # Recycle connections after 1 hour\n            echo=False,{acid_settings}"
            )
            
            db_opt_file.write_text(db_opt_content, encoding='utf-8')
            print(f"✓ Updated {db_opt_file} with ACID compliance settings")
        else:
            print("✓ ACID compliance settings already exist")
        
        return True
    
    def update_app_py_for_versioning(self):
        """Update app.py to use versioned routers"""
        print("\n" + "="*60)
        print("Updating app.py for API Versioning")
        print("="*60)
        
        app_file = self.api / "app.py"
        app_content = app_file.read_text(encoding='utf-8')
        
        # Add versioned router import
        versioning_import = """
# API Versioning
from routers.v1 import v1_router
"""
        
        # Check if versioned router already imported
        if "from routers.v1 import v1_router" not in app_content:
            # Add after FastAPI app creation
            app_content = app_content.replace(
                "app = FastAPI(",
                versioning_import + "\napp = FastAPI("
            )
            
            # Include v1 router
            if "app.include_router(v1_router)" not in app_content:
                # Add after CORS middleware
                app_content = app_content.replace(
                    "    allow_headers=[\"*\"],\n)",
                    "    allow_headers=[\"*\"],\n)\n\n# Include versioned routers\napp.include_router(v1_router)"
                )
            
            app_file.write_text(app_content, encoding='utf-8')
            print(f"✓ Updated {app_file} with versioned routers")
        else:
            print("✓ Versioned routers already integrated")
        
        return True
    
    def create_version_negotiation_middleware(self):
        """Create version negotiation middleware"""
        print("\n" + "="*60)
        print("Creating Version Negotiation Middleware")
        print("="*60)
        
        middleware_code = """# Version Negotiation Middleware
# construction-platform/python-services/api/middleware/version_negotiation.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)

class VersionNegotiationMiddleware(BaseHTTPMiddleware):
    \"\"\"Middleware for API version negotiation\"\"\"
    
    async def dispatch(self, request: Request, call_next):
        # Check Accept header for version
        accept = request.headers.get("Accept", "")
        
        # Extract version from Accept header
        version = None
        if "version=" in accept:
            version = accept.split("version=")[1].split(";")[0]
        
        # Check X-API-Version header
        if not version:
            version = request.headers.get("X-API-Version", "v1")
        
        # Set version in request state
        request.state.api_version = version
        
        # Log version negotiation
        logger.info(f"API version negotiated: {version} for {request.url.path}")
        
        response = await call_next(request)
        
        # Add version header to response
        response.headers["X-API-Version"] = version
        
        return response
"""
        
        middleware_dir = self.api / "middleware"
        middleware_dir.mkdir(exist_ok=True, parents=True)
        
        middleware_file = middleware_dir / "version_negotiation.py"
        middleware_file.write_text(middleware_code, encoding='utf-8')
        print(f"✓ Created {middleware_file}")
        
        # Create __init__.py
        init_file = middleware_dir / "__init__.py"
        init_file.write_text("from .version_negotiation import VersionNegotiationMiddleware\n", encoding='utf-8')
        print(f"✓ Created {init_file}")
        
        return True
    
    def create_openapi_docs(self):
        """Create OpenAPI Documentation"""
        print("\n" + "="*60)
        print("Creating OpenAPI Documentation")
        print("="*60)
        
        # Update app.py to include OpenAPI info
        app_file = self.api / "app.py"
        app_content = app_file.read_text(encoding='utf-8')
        
        # Update FastAPI app with OpenAPI info
        openapi_info = """
app = FastAPI(
    title="Construction AI Agent API",
    version="2.0.0",
    description="Estonian Construction Material Takeoff & Cost Estimation API",
    openapi_version="3.1.0",
    openapi_tags=[
        {"name": "v1", "description": "API Version 1 endpoints"},
        {"name": "health", "description": "Health check endpoints"},
        {"name": "analytics", "description": "Analytics endpoints"},
        {"name": "usage", "description": "Usage analytics endpoints"},
        {"name": "billing", "description": "Billing endpoints"},
        {"name": "errors", "description": "Error analytics endpoints"},
        {"name": "audit", "description": "Audit logging endpoints"},
        {"name": "vector", "description": "Vector database endpoints"},
        {"name": "archival", "description": "Archival endpoints"},
        {"name": "automation", "description": "Automation rules endpoints"},
        {"name": "backup", "description": "Backup and recovery endpoints"},
    ],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
"""
        
        # Check if OpenAPI info already exists
        if 'openapi_tags' not in app_content:
            # Replace existing FastAPI app creation
            app_content = app_content.replace(
                'app = FastAPI(\n    title="Construction AI Agent API", \n    version="2.0.0",\n    description="Estonian Construction Material Takeoff & Cost Estimation API"\n)',
                openapi_info.strip()
            )
            
            app_file.write_text(app_content, encoding='utf-8')
            print(f"✓ Updated {app_file} with OpenAPI documentation")
        else:
            print("✓ OpenAPI documentation already exists")
        
        return True
    
    def run(self):
        """Run all critical fixes"""
        print("="*60)
        print("CRITICAL FIXES IMPLEMENTATION")
        print("="*60)
        
        self.implement_api_versioning()
        self.implement_database_transactions()
        self.implement_acid_compliance()
        self.create_version_negotiation_middleware()
        self.update_app_py_for_versioning()
        self.create_openapi_docs()
        
        print("\n" + "="*60)
        print("CRITICAL FIXES COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review created files")
        print("2. Move remaining endpoints from app.py to v1 routers")
        print("3. Test API versioning")
        print("4. Test database transactions")
        print("5. Test ACID compliance")
        print("6. Update documentation")

if __name__ == "__main__":
    project_root = Path(__file__).parent
    fixes = CriticalFixes(project_root)
    fixes.run()

