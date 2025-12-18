import redis
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Redis for caching
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'redis'), 
        port=6379, 
        db=0, 
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Redis connected successfully")
    redis_available = True
except Exception as e:
    redis_client = None
    redis_available = False
    logger.warning(f"Redis not available: {e}, caching disabled")
