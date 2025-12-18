from typing import Optional, Dict
import hashlib
import json
import logging
from .redis_client import redis_client
from .metrics import cache_hit_counter, cache_miss_counter, redis_connection_status

logger = logging.getLogger(__name__)

def get_cache_key(file_content: bytes, operation: str) -> str:
    """Generate cache key for file operations"""
    file_hash = hashlib.md5(file_content).hexdigest()
    return f"construction_ai:{operation}:{file_hash}"

async def get_cached_result(cache_key: str, operation: str) -> Optional[Dict]:
    """Get cached result if available"""
    if not redis_client:
        cache_miss_counter.labels(operation=operation).inc()
        return None
    try:
        cached = redis_client.get(cache_key)
        if cached:
            cache_hit_counter.labels(operation=operation).inc()
            return json.loads(cached)
        else:
            cache_miss_counter.labels(operation=operation).inc()
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
        cache_miss_counter.labels(operation=operation).inc()
    return None

async def set_cached_result(cache_key: str, result: Dict, ttl: int = 3600):
    """Cache result with TTL"""
    if not redis_client:
        return
    try:
        redis_client.setex(cache_key, ttl, json.dumps(result))
    except Exception as e:
        logger.warning(f"Cache write error: {e}")
        redis_connection_status.set(0)
