# Multi-Tenancy Support
# construction-platform/python-services/api/multi_tenancy.py

from fastapi import Request, HTTPException, Depends
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class TenantManager:
    """Multi-tenant manager with tenant isolation"""
    def __init__(self):
        self.tenants: Dict[str, Dict[str, Any]] = {}
        self.tenant_databases: Dict[str, str] = {}
    
    def get_tenant_id(self, request: Request) -> Optional[str]:
        """Get tenant ID from request"""
        # Try to get tenant ID from header
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            return tenant_id
        
        # Try to get tenant ID from token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            # Extract tenant ID from token (simplified)
            # In production, decode JWT token and extract tenant_id
            return self._extract_tenant_from_token(auth_header)
        
        # Default tenant for backward compatibility
        return "default"
    
    def _extract_tenant_from_token(self, token: str) -> str:
        """Extract tenant ID from token (simplified)"""
        # In production, decode JWT token and extract tenant_id
        # For now, return default tenant
        return "default"
    
    def get_tenant_database(self, tenant_id: str) -> str:
        """Get database name for tenant"""
        if tenant_id not in self.tenant_databases:
            # Generate database name for tenant
            db_name = f"construction_ai_{tenant_id}"
            self.tenant_databases[tenant_id] = db_name
        return self.tenant_databases[tenant_id]
    
    def create_tenant(self, tenant_id: str, tenant_data: Dict[str, Any]) -> bool:
        """Create new tenant"""
        try:
            self.tenants[tenant_id] = {
                "id": tenant_id,
                "created_at": datetime.now().isoformat(),
                "status": "active",
                **tenant_data
            }
            logger.info(f"Tenant created: {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create tenant: {e}")
            return False
    
    def get_tenant(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get tenant information"""
        return self.tenants.get(tenant_id)
    
    def is_tenant_active(self, tenant_id: str) -> bool:
        """Check if tenant is active"""
        tenant = self.tenants.get(tenant_id)
        if tenant:
            return tenant.get("status") == "active"
        return False

# Global tenant manager instance
tenant_manager = TenantManager()

def get_tenant_id(request: Request) -> str:
    """Dependency to get tenant ID from request"""
    return tenant_manager.get_tenant_id(request)

def require_tenant(request: Request) -> str:
    """Require tenant ID in request"""
    tenant_id = tenant_manager.get_tenant_id(request)
    if not tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Tenant ID required. Please provide X-Tenant-ID header or valid token."
        )
    
    if not tenant_manager.is_tenant_active(tenant_id):
        raise HTTPException(
            status_code=403,
            detail="Tenant is not active. Please contact support."
        )
    
    return tenant_id
