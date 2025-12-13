# Rate Limiting with Token Bucket Algorithm
# construction-platform/python-services/api/rate_limiting.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Tuple
import time
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

class TokenBucket:
    """Token Bucket Rate Limiting Algorithm"""
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity  # Maximum tokens
        self.refill_rate = refill_rate  # Tokens per second
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self, tokens: int = 1) -> bool:
        """Try to acquire tokens from the bucket"""
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
        """Calculate time until next token is available"""
        async with self.lock:
            if self.tokens >= 1:
                return 0
            return (1 - self.tokens) / self.refill_rate

class RateLimiter:
    """Rate Limiter with per-user token buckets"""
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
        """Get client identifier from request"""
        # Try to get user ID from token/header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            # Extract user ID from token (simplified)
            return f"user_{hash(auth_header) % 10000}"
        
        # Fallback to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip_{client_ip}"
    
    async def check_rate_limit(self, request: Request, tokens: int = 1) -> Tuple[bool, Dict]:
        """Check if request is within rate limit"""
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
        """Remove inactive buckets to free memory"""
        # In production, implement proper cleanup logic
        pass

# Global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
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
