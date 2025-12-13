# Enhanced Multi-Layer Caching
# construction-platform/python-services/api/cache.py

import redis
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Multi-layer caching service with Redis"""
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
        self.cache_prefix = "construction_ai"
        
    def _generate_key(self, key: str, namespace: str = "default") -> str:
        """Generate cache key with namespace"""
        return f"{self.cache_prefix}:{namespace}:{key}"
    
    def get(self, key: str, namespace: str = "default") -> Optional[Dict]:
        """Get value from cache (synchronous for Redis compatibility)"""
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
    
    def set(self, key: str, value: Dict, ttl: int = None, namespace: str = "default"):
        """Set value in cache (synchronous for Redis compatibility)"""
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
    
    def delete(self, key: str, namespace: str = "default"):
        """Delete value from cache (synchronous for Redis compatibility)"""
        try:
            cache_key = self._generate_key(key, namespace)
            self.redis.delete(cache_key)
            logger.info(f"Cache delete: {cache_key}")
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear_namespace(self, namespace: str):
        """Clear all keys in a namespace (synchronous for Redis compatibility)"""
        try:
            pattern = self._generate_key("*", namespace)
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
                logger.info(f"Cache cleared namespace: {namespace}")
        except Exception as e:
            logger.error(f"Cache clear namespace error: {e}")
    
    def generate_cache_key(self, content: bytes, operation: str) -> str:
        """Generate cache key from content hash"""
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

# Allow None for redis_client (for graceful degradation)
def create_cache_service(redis_client):
    """Create cache service with graceful degradation"""
    if redis_client is None:
        return None
    try:
        return CacheService(redis_client)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to create cache service: {e}")
        return None
