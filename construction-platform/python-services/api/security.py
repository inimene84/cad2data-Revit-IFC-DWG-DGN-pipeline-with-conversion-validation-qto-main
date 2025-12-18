# Security Hardening
# construction-platform/python-services/api/security.py

from fastapi import Request, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Dict
import logging
import time
import hmac
import hashlib
import secrets

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old entries
        if client_ip in self.clients:
            self.clients[client_ip] = [
                t for t in self.clients[client_ip]
                if current_time - t < self.period
            ]
        else:
            self.clients[client_ip] = []
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            return Response(
                status_code=429,
                content="Rate limit exceeded",
                headers={"Retry-After": str(self.period)}
            )
        
        # Add current request
        self.clients[client_ip].append(current_time)
        
        response = await call_next(request)
        return response

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware"""
    def __init__(self, app, api_keys: List[str] = None):
        super().__init__(app)
        self.api_keys = api_keys or []
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public endpoints
        public_paths = [
            "/health", "/v1/health", "/v1/health/detailed",
            "/docs", "/openapi.json", "/redoc", "/metrics",
            "/extract-pdf", "/extract-excel", "/process-cad",
            "/calculate-materials", "/generate-report",
            # Add new v1 endpoints to public paths
            "/v1/projects", "/v1/materials", "/v1/reports", "/v1/chat",
            "/v1/materials/search", "/v1/materials/stats/summary",
            "/v1/reports/stats/summary"
        ]
        # Also allow analytics and settings endpoints and any subpaths of the main resources
        if (request.url.path in public_paths or 
            request.url.path.startswith("/docs") or 
            request.url.path.startswith("/static") or
            request.url.path.startswith("/v1/analytics") or
            request.url.path.startswith("/api/analytics") or
            request.url.path.startswith("/v1/settings") or
            request.url.path.startswith("/api/settings") or
            # Allow all sub-resources for CRUD
            request.url.path.startswith("/v1/projects") or
            request.url.path.startswith("/v1/materials") or
            request.url.path.startswith("/v1/reports") or
            request.url.path.startswith("/v1/chat")):
            return await call_next(request)
        
        # Check API key
        api_key = request.headers.get("X-API-Key")
        if api_key and api_key in self.api_keys:
            return await call_next(request)
        
        # Check authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            # Verify token (simplified)
            if self.verify_token(token):
                return await call_next(request)
        
        # Return 401 Unauthorized
        return Response(
            status_code=401,
            content="Unauthorized"
        )
    
    def verify_token(self, token: str) -> bool:
        """Verify authentication token"""
        # In production, verify JWT token
        # For now, return True for demonstration
        return True

class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """CSRF protection middleware"""
    async def dispatch(self, request: Request, call_next):
        # Skip CSRF protection for GET and OPTIONS requests (OPTIONS for CORS preflight)
        if request.method in ("GET", "OPTIONS"):
            return await call_next(request)
        
        # Skip CSRF protection for file upload endpoints (handled by API)
        upload_paths = ["/extract-pdf", "/extract-excel", "/process-cad"]
        if request.url.path in upload_paths or request.url.path.endswith("/extract-excel") or request.url.path.endswith("/extract-pdf"):
            return await call_next(request)
        
        # Skip CSRF protection for settings and analytics endpoints
        if (request.url.path.startswith("/v1/settings") or 
            request.url.path.startswith("/api/settings") or
            request.url.path.startswith("/v1/analytics") or
            request.url.path.startswith("/api/analytics") or
            request.url.path.startswith("/v1/vector") or
            request.url.path.startswith("/calculate-materials") or
            request.url.path.startswith("/generate-report") or
            # Allow new v1 endpoints
            request.url.path.startswith("/v1/projects") or
            request.url.path.startswith("/v1/materials") or
            request.url.path.startswith("/v1/reports") or
            request.url.path.startswith("/v1/chat")):
            return await call_next(request)
        
        # Check CSRF token
        csrf_token = request.headers.get("X-CSRF-Token")
        if not csrf_token:
            return Response(
                status_code=403,
                content="CSRF token missing"
            )
        
        # Verify CSRF token (simplified)
        if not self.verify_csrf_token(csrf_token, request):
            return Response(
                status_code=403,
                content="Invalid CSRF token"
            )
        
        return await call_next(request)
    
    def verify_csrf_token(self, token: str, request: Request) -> bool:
        """Verify CSRF token"""
        # In production, verify CSRF token
        # For now, return True for demonstration
        return True

def generate_api_key() -> str:
    """Generate API key"""
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password"""
    return hash_password(password) == password_hash
