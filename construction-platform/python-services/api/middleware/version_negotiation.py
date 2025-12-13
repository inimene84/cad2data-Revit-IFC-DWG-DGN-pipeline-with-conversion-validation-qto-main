# Version Negotiation Middleware
# construction-platform/python-services/api/middleware/version_negotiation.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)

class VersionNegotiationMiddleware(BaseHTTPMiddleware):
    """Middleware for API version negotiation"""
    
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
