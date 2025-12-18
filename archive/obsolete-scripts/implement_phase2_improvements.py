#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 Improvements Implementation Script
Implements core improvements for Construction AI Platform
"""

import os
import sys
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class Phase2Improvements:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.api = self.project_root / "construction-platform" / "python-services" / "api"
        
    def implement_rate_limiting(self):
        """Implement API Rate Limiting with Token Bucket Algorithm"""
        print("\n" + "="*60)
        print("Phase 2.1: API Rate Limiting")
        print("="*60)
        
        rate_limiting_code = """# Rate Limiting with Token Bucket Algorithm
# construction-platform/python-services/api/rate_limiting.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Tuple
import time
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

class TokenBucket:
    \"\"\"Token Bucket Rate Limiting Algorithm\"\"\"
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity  # Maximum tokens
        self.refill_rate = refill_rate  # Tokens per second
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self, tokens: int = 1) -> bool:
        \"\"\"Try to acquire tokens from the bucket\"\"\"
        async with self.lock:
            # Refill tokens based on time passed
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            
            # Check if enough tokens available
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    async def get_retry_after(self) -> float:
        \"\"\"Calculate time until next token is available\"\"\"
        async with self.lock:
            if self.tokens >= 1:
                return 0
            return (1 - self.tokens) / self.refill_rate

class RateLimiter:
    \"\"\"Rate Limiter with per-user token buckets\"\"\"
    def __init__(self):
        # Default: 100 requests per minute per user
        self.default_capacity = 100
        self.default_refill_rate = 100 / 60  # tokens per second
        self.buckets: Dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(self.default_capacity, self.default_refill_rate)
        )
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    def get_client_id(self, request: Request) -> str:
        \"\"\"Get client identifier from request\"\"\"
        # Try to get user ID from token/header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            # Extract user ID from token (simplified)
            return f"user_{hash(auth_header) % 10000}"
        
        # Fallback to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip_{client_ip}"
    
    async def check_rate_limit(self, request: Request, tokens: int = 1) -> Tuple[bool, Dict]:
        \"\"\"Check if request is within rate limit\"\"\"
        client_id = self.get_client_id(request)
        bucket = self.buckets[client_id]
        
        # Cleanup old buckets periodically
        if time.time() - self.last_cleanup > self.cleanup_interval:
            await self._cleanup_buckets()
            self.last_cleanup = time.time()
        
        # Try to acquire tokens
        if await bucket.acquire(tokens):
            return True, {
                "X-RateLimit-Limit": str(self.default_capacity),
                "X-RateLimit-Remaining": str(int(bucket.tokens)),
                "X-RateLimit-Reset": str(int(time.time() + 60))
            }
        else:
            retry_after = await bucket.get_retry_after()
            return False, {
                "X-RateLimit-Limit": str(self.default_capacity),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time() + retry_after)),
                "Retry-After": str(int(retry_after))
            }
    
    async def _cleanup_buckets(self):
        \"\"\"Remove inactive buckets to free memory\"\"\"
        # In production, implement proper cleanup logic
        pass

# Global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    \"\"\"Rate limiting middleware\"\"\"
    # Skip rate limiting for health checks and metrics
    if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    # Check rate limit
    allowed, headers = await rate_limiter.check_rate_limit(request)
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                "retry_after": headers.get("Retry-After", "60")
            },
            headers=headers
        )
    
    # Add rate limit headers to response
    response = await call_next(request)
    for key, value in headers.items():
        response.headers[key] = value
    
    return response
"""
        
        rate_limiting_file = self.api / "rate_limiting.py"
        rate_limiting_file.write_text(rate_limiting_code, encoding='utf-8')
        print(f"✓ Created {rate_limiting_file}")
        return True
    
    def implement_caching(self):
        """Enhance Multi-Layer Caching"""
        print("\n" + "="*60)
        print("Phase 2.2: Multi-Layer Caching")
        print("="*60)
        
        caching_code = """# Enhanced Multi-Layer Caching
# construction-platform/python-services/api/cache.py

import redis
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CacheService:
    \"\"\"Multi-layer caching service with Redis\"\"\"
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
        self.cache_prefix = "construction_ai"
        
    def _generate_key(self, key: str, namespace: str = "default") -> str:
        \"\"\"Generate cache key with namespace\"\"\"
        return f"{self.cache_prefix}:{namespace}:{key}"
    
    async def get(self, key: str, namespace: str = "default") -> Optional[Dict]:
        \"\"\"Get value from cache\"\"\"
        try:
            cache_key = self._generate_key(key, namespace)
            cached = self.redis.get(cache_key)
            if cached:
                logger.info(f"Cache hit: {cache_key}")
                return json.loads(cached)
            logger.info(f"Cache miss: {cache_key}")
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Dict, ttl: int = None, namespace: str = "default"):
        \"\"\"Set value in cache\"\"\"
        try:
            cache_key = self._generate_key(key, namespace)
            ttl = ttl or self.default_ttl
            self.redis.setex(
                cache_key,
                ttl,
                json.dumps(value, default=str)
            )
            logger.info(f"Cache set: {cache_key} (TTL: {ttl}s)")
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    async def delete(self, key: str, namespace: str = "default"):
        \"\"\"Delete value from cache\"\"\"
        try:
            cache_key = self._generate_key(key, namespace)
            self.redis.delete(cache_key)
            logger.info(f"Cache delete: {cache_key}")
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    async def clear_namespace(self, namespace: str):
        \"\"\"Clear all keys in a namespace\"\"\"
        try:
            pattern = self._generate_key("*", namespace)
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
                logger.info(f"Cache cleared namespace: {namespace}")
        except Exception as e:
            logger.error(f"Cache clear namespace error: {e}")
    
    def generate_cache_key(self, content: bytes, operation: str) -> str:
        \"\"\"Generate cache key from content hash\"\"\"
        content_hash = hashlib.md5(content).hexdigest()
        return f"{operation}:{content_hash}"

# Cache namespaces
CACHE_NAMESPACES = {
    "analysis": "analysis_results",
    "metadata": "file_metadata",
    "projects": "project_data",
    "analytics": "analytics_data",
    "pdf_extraction": "pdf_extraction",
    "excel_extraction": "excel_extraction"
}
"""
        
        caching_file = self.api / "cache.py"
        caching_file.write_text(caching_code, encoding='utf-8')
        print(f"✓ Created {caching_file}")
        return True
    
    def implement_error_handling(self):
        """Implement Enhanced Error Handling"""
        print("\n" + "="*60)
        print("Phase 2.3: Enhanced Error Handling")
        print("="*60)
        
        error_handling_code = """# Enhanced Error Handling
# construction-platform/python-services/api/error_handler.py

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
import traceback
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    \"\"\"Error type enumeration\"\"\"
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    NOT_FOUND_ERROR = "not_found_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    SERVER_ERROR = "server_error"
    NETWORK_ERROR = "network_error"
    TIMEOUT_ERROR = "timeout_error"
    UNKNOWN_ERROR = "unknown_error"

class ErrorHandler:
    \"\"\"Enhanced error handler with user-friendly messages\"\"\"
    
    ERROR_MESSAGES = {
        ErrorType.VALIDATION_ERROR: "Invalid input data. Please check your request.",
        ErrorType.AUTHENTICATION_ERROR: "Authentication failed. Please check your credentials.",
        ErrorType.AUTHORIZATION_ERROR: "You don't have permission to access this resource.",
        ErrorType.NOT_FOUND_ERROR: "The requested resource was not found.",
        ErrorType.RATE_LIMIT_ERROR: "Too many requests. Please try again later.",
        ErrorType.SERVER_ERROR: "An internal server error occurred. Please try again later.",
        ErrorType.NETWORK_ERROR: "Network error occurred. Please check your connection.",
        ErrorType.TIMEOUT_ERROR: "Request timed out. Please try again.",
        ErrorType.UNKNOWN_ERROR: "An unexpected error occurred. Please contact support."
    }
    
    @staticmethod
    def classify_error(error: Exception) -> ErrorType:
        \"\"\"Classify error type\"\"\"
        error_str = str(error).lower()
        
        if "validation" in error_str or "invalid" in error_str:
            return ErrorType.VALIDATION_ERROR
        elif "authentication" in error_str or "unauthorized" in error_str:
            return ErrorType.AUTHENTICATION_ERROR
        elif "forbidden" in error_str or "permission" in error_str:
            return ErrorType.AUTHORIZATION_ERROR
        elif "not found" in error_str or "404" in error_str:
            return ErrorType.NOT_FOUND_ERROR
        elif "rate limit" in error_str or "429" in error_str:
            return ErrorType.RATE_LIMIT_ERROR
        elif "timeout" in error_str or "timed out" in error_str:
            return ErrorType.TIMEOUT_ERROR
        elif "network" in error_str or "connection" in error_str:
            return ErrorType.NETWORK_ERROR
        else:
            return ErrorType.SERVER_ERROR
    
    @staticmethod
    def create_error_response(
        error: Exception,
        error_type: Optional[ErrorType] = None,
        status_code: int = 500,
        include_details: bool = False
    ) -> JSONResponse:
        \"\"\"Create user-friendly error response\"\"\"
        if error_type is None:
            error_type = ErrorHandler.classify_error(error)
        
        error_message = ErrorHandler.ERROR_MESSAGES.get(
            error_type,
            ErrorHandler.ERROR_MESSAGES[ErrorType.UNKNOWN_ERROR]
        )
        
        response_data = {
            "error": error_type.value,
            "message": error_message,
            "status_code": status_code
        }
        
        # Include details in development mode
        if include_details:
            response_data["details"] = str(error)
            response_data["traceback"] = traceback.format_exc()
        
        # Log error
        logger.error(f"Error: {error_type.value} - {error_message}", exc_info=error)
        
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
    
    @staticmethod
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        \"\"\"Global exception handler\"\"\"
        # Check if it's an HTTPException
        if isinstance(exc, HTTPException):
            error_type = ErrorHandler.classify_error(exc)
            return ErrorHandler.create_error_response(
                exc,
                error_type,
                exc.status_code,
                include_details=False
            )
        
        # Handle other exceptions
        error_type = ErrorHandler.classify_error(exc)
        status_code = 500 if error_type == ErrorType.SERVER_ERROR else 400
        
        return ErrorHandler.create_error_response(
            exc,
            error_type,
            status_code,
            include_details=False
        )

class RetryStrategy:
    \"\"\"Retry strategy with exponential backoff\"\"\"
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    async def retry(self, func, *args, **kwargs):
        \"\"\"Retry function with exponential backoff\"\"\"
        import asyncio
        import random
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                
                # Calculate delay with exponential backoff and jitter
                delay = min(
                    self.base_delay * (2 ** attempt),
                    self.max_delay
                )
                jitter = random.uniform(0, delay * 0.1)
                delay += jitter
                
                logger.warning(f"Retry attempt {attempt + 1}/{self.max_retries} after {delay:.2f}s")
                await asyncio.sleep(delay)
        
        raise Exception("Max retries exceeded")
"""
        
        error_handler_file = self.api / "error_handler.py"
        error_handler_file.write_text(error_handling_code, encoding='utf-8')
        print(f"✓ Created {error_handler_file}")
        return True
    
    def implement_input_validation(self):
        """Implement Input Validation Layer"""
        print("\n" + "="*60)
        print("Phase 2.4: Input Validation Layer")
        print("="*60)
        
        validation_code = """# Input Validation Layer with Pydantic
# construction-platform/python-services/api/validation.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from enum import Enum
import re

class FileType(str, Enum):
    \"\"\"Supported file types\"\"\"
    PDF = "pdf"
    EXCEL = "excel"
    DWG = "dwg"
    IFC = "ifc"
    RVT = "rvt"
    DGN = "dgn"
    IMAGE = "image"

class UploadFileRequest(BaseModel):
    \"\"\"Request model for file upload\"\"\"
    file_name: str = Field(..., min_length=1, max_length=255)
    file_type: FileType
    file_size: int = Field(..., gt=0, le=100_000_000)  # Max 100MB
    project_name: Optional[str] = Field(None, min_length=1, max_length=100)
    workflow_type: Optional[str] = Field("auto", min_length=1, max_length=50)
    
    @validator("file_name")
    def validate_file_name(cls, v):
        \"\"\"Validate file name\"\"\"
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            raise ValueError("Invalid file name format")
        return v
    
    @validator("file_type")
    def validate_file_type(cls, v):
        \"\"\"Validate file type\"\"\"
        if v not in FileType:
            raise ValueError(f"Unsupported file type: {v}")
        return v

class AnalyticsRequest(BaseModel):
    \"\"\"Request model for analytics\"\"\"
    period: str = Field("30d", regex="^(7d|30d|90d|1y)$")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    @validator("period")
    def validate_period(cls, v):
        \"\"\"Validate period\"\"\"
        valid_periods = ["7d", "30d", "90d", "1y"]
        if v not in valid_periods:
            raise ValueError(f"Invalid period: {v}. Must be one of {valid_periods}")
        return v

class MaterialCalculationRequest(BaseModel):
    \"\"\"Request model for material calculation\"\"\"
    materials: List[Dict[str, Any]] = Field(..., min_items=1)
    region: str = Field("Tartu", min_length=1, max_length=50)
    include_vat: bool = Field(True)
    
    @validator("materials")
    def validate_materials(cls, v):
        \"\"\"Validate materials list\"\"\"
        required_fields = ["material", "quantity", "unit"]
        for material in v:
            for field in required_fields:
                if field not in material:
                    raise ValueError(f"Missing required field: {field}")
        return v

class ReportGenerationRequest(BaseModel):
    \"\"\"Request model for report generation\"\"\"
    project_name: str = Field(..., min_length=1, max_length=100)
    summary: Dict[str, Any] = Field(..., min_items=1)
    include_vat: bool = Field(True)
    include_suppliers: bool = Field(False)
    
    @validator("summary")
    def validate_summary(cls, v):
        \"\"\"Validate summary\"\"\"
        if not isinstance(v, dict):
            raise ValueError("Summary must be a dictionary")
        return v
"""
        
        validation_file = self.api / "validation.py"
        validation_file.write_text(validation_code, encoding='utf-8')
        print(f"✓ Created {validation_file}")
        return True
    
    def implement_circuit_breaker(self):
        """Implement Circuit Breaker Pattern"""
        print("\n" + "="*60)
        print("Phase 2.5: Circuit Breaker Pattern")
        print("="*60)
        
        circuit_breaker_code = """# Circuit Breaker Pattern
# construction-platform/python-services/api/circuit_breaker.py

from enum import Enum
from typing import Callable, Any
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    \"\"\"Circuit breaker states\"\"\"
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    \"\"\"Circuit breaker to protect against cascading failures\"\"\"
    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 60.0,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        \"\"\"Execute function with circuit breaker protection\"\"\"
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker: Attempting to reset (HALF_OPEN)")
            else:
                raise Exception("Circuit breaker is OPEN. Service unavailable.")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    async def call_async(self, func: Callable, *args, **kwargs) -> Any:
        \"\"\"Execute async function with circuit breaker protection\"\"\"
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker: Attempting to reset (HALF_OPEN)")
            else:
                raise Exception("Circuit breaker is OPEN. Service unavailable.")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        \"\"\"Handle successful call\"\"\"
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker: Service recovered (CLOSED)")
    
    def _on_failure(self):
        \"\"\"Handle failed call\"\"\"
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker: Service failing (OPEN) - {self.failure_count} failures")
    
    def _should_attempt_reset(self) -> bool:
        \"\"\"Check if should attempt to reset circuit breaker\"\"\"
        if self.last_failure_time is None:
            return True
        
        return time.time() - self.last_failure_time >= self.timeout

def circuit_breaker(
    failure_threshold: int = 5,
    success_threshold: int = 2,
    timeout: float = 60.0,
    expected_exception: type = Exception
):
    \"\"\"Decorator for circuit breaker\"\"\"
    breaker = CircuitBreaker(failure_threshold, success_threshold, timeout, expected_exception)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await breaker.call_async(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
"""
        
        circuit_breaker_file = self.api / "circuit_breaker.py"
        circuit_breaker_file.write_text(circuit_breaker_code, encoding='utf-8')
        print(f"✓ Created {circuit_breaker_file}")
        return True
    
    def update_app_py(self):
        """Update app.py with Phase 2 improvements"""
        print("\n" + "="*60)
        print("Phase 2.6: Updating app.py")
        print("="*60)
        
        # Read current app.py
        app_file = self.api / "app.py"
        app_content = app_file.read_text(encoding='utf-8')
        
        # Add imports
        imports_to_add = """
from rate_limiting import rate_limit_middleware
from cache import CacheService, CACHE_NAMESPACES
from error_handler import ErrorHandler, ErrorType
from validation import UploadFileRequest, AnalyticsRequest, MaterialCalculationRequest
from circuit_breaker import CircuitBreaker, circuit_breaker
"""
        
        # Check if imports already exist
        if "from rate_limiting import" not in app_content:
            # Add imports after existing imports
            import_end = app_content.find("from config import")
            if import_end == -1:
                import_end = app_content.find("import uvicorn")
            if import_end != -1:
                app_content = app_content[:import_end] + imports_to_add + "\n" + app_content[import_end:]
        
        # Add middleware
        middleware_code = """
# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Initialize cache service
cache_service = CacheService(redis_client) if redis_client else None

# Add global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return await ErrorHandler.exception_handler(request, exc)
"""
        
        # Check if middleware already added
        if "rate_limit_middleware" not in app_content:
            # Add after CORS middleware
            cors_end = app_content.find("app.add_middleware(\n    CORSMiddleware")
            if cors_end != -1:
                # Find the end of CORS middleware block
                cors_block_end = app_content.find(")", cors_end) + 1
                app_content = app_content[:cors_block_end] + "\n" + middleware_code + "\n" + app_content[cors_block_end:]
        
        # Write updated app.py
        app_file.write_text(app_content, encoding='utf-8')
        print(f"✓ Updated {app_file}")
        return True
    
    def run(self):
        """Run Phase 2 improvements implementation"""
        print("="*60)
        print("Phase 2 Improvements Implementation")
        print("="*60)
        
        # Implement improvements
        self.implement_rate_limiting()
        self.implement_caching()
        self.implement_error_handling()
        self.implement_input_validation()
        self.implement_circuit_breaker()
        self.update_app_py()
        
        print("\n" + "="*60)
        print("Phase 2 Improvements Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review created files")
        print("2. Test rate limiting")
        print("3. Test caching")
        print("4. Test error handling")
        print("5. Test input validation")
        print("6. Test circuit breaker")

if __name__ == "__main__":
    project_root = Path(__file__).parent
    improvements = Phase2Improvements(project_root)
    improvements.run()

