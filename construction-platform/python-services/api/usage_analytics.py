# Usage Analytics
# construction-platform/python-services/api/usage_analytics.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

class UsageTracker:
    """Track usage analytics for tenants and users"""
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.usage_prefix = "usage_analytics"
    
    def track_file_upload(self, tenant_id: str, user_id: str, file_size: int, file_type: str):
        """Track file upload"""
        try:
            key = f"{self.usage_prefix}:{tenant_id}:files:{datetime.now().strftime('%Y-%m-%d')}"
            if self.redis:
                self.redis.incr(key)
                self.redis.expire(key, 86400 * 30)  # 30 days
            
            # Track file size
            size_key = f"{self.usage_prefix}:{tenant_id}:storage:{datetime.now().strftime('%Y-%m-%d')}"
            if self.redis:
                self.redis.incrby(size_key, file_size)
                self.redis.expire(size_key, 86400 * 30)
            
            logger.info(f"File upload tracked: {tenant_id}, {file_type}, {file_size} bytes")
        except Exception as e:
            logger.error(f"Failed to track file upload: {e}")
    
    def track_api_call(self, tenant_id: str, user_id: str, endpoint: str, method: str):
        """Track API call"""
        try:
            key = f"{self.usage_prefix}:{tenant_id}:api:{datetime.now().strftime('%Y-%m-%d')}"
            if self.redis:
                self.redis.incr(key)
                self.redis.expire(key, 86400 * 30)
            
            # Track endpoint
            endpoint_key = f"{self.usage_prefix}:{tenant_id}:endpoints:{endpoint}:{datetime.now().strftime('%Y-%m-%d')}"
            if self.redis:
                self.redis.incr(endpoint_key)
                self.redis.expire(endpoint_key, 86400 * 30)
            
            logger.debug(f"API call tracked: {tenant_id}, {method} {endpoint}")
        except Exception as e:
            logger.error(f"Failed to track API call: {e}")
    
    def track_storage_usage(self, tenant_id: str, storage_bytes: int):
        """Track storage usage"""
        try:
            key = f"{self.usage_prefix}:{tenant_id}:storage"
            if self.redis:
                self.redis.set(key, storage_bytes)
                self.redis.expire(key, 86400 * 30)
            
            logger.debug(f"Storage usage tracked: {tenant_id}, {storage_bytes} bytes")
        except Exception as e:
            logger.error(f"Failed to track storage usage: {e}")
    
    def get_usage_stats(self, tenant_id: str, period: str = "30d") -> Dict[str, Any]:
        """Get usage statistics for tenant"""
        try:
            days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
            start_date = datetime.now() - timedelta(days=days)
            
            stats = {
                "tenant_id": tenant_id,
                "period": period,
                "files_uploaded": 0,
                "api_calls": 0,
                "storage_used": 0,
                "endpoints_used": {}
            }
            
            if self.redis:
                # Get file uploads
                for i in range(days):
                    date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                    key = f"{self.usage_prefix}:{tenant_id}:files:{date}"
                    count = self.redis.get(key)
                    if count:
                        stats["files_uploaded"] += int(count)
                
                # Get API calls
                for i in range(days):
                    date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                    key = f"{self.usage_prefix}:{tenant_id}:api:{date}"
                    count = self.redis.get(key)
                    if count:
                        stats["api_calls"] += int(count)
                
                # Get storage usage
                storage_key = f"{self.usage_prefix}:{tenant_id}:storage"
                storage = self.redis.get(storage_key)
                if storage:
                    stats["storage_used"] = int(storage)
            
            return stats
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {}
    
    def get_usage_breakdown(self, tenant_id: str, period: str = "30d") -> Dict[str, Any]:
        """Get usage breakdown by endpoint"""
        try:
            days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
            start_date = datetime.now() - timedelta(days=days)
            
            breakdown = {
                "tenant_id": tenant_id,
                "period": period,
                "endpoints": {}
            }
            
            if self.redis:
                # Get endpoint usage
                pattern = f"{self.usage_prefix}:{tenant_id}:endpoints:*"
                keys = self.redis.keys(pattern)
                for key in keys:
                    endpoint = key.split(":")[-2]
                    count = self.redis.get(key)
                    if count:
                        if endpoint not in breakdown["endpoints"]:
                            breakdown["endpoints"][endpoint] = 0
                        breakdown["endpoints"][endpoint] += int(count)
            
            return breakdown
        except Exception as e:
            logger.error(f"Failed to get usage breakdown: {e}")
            return {}

# Global usage tracker instance
usage_tracker = None

def initialize_usage_tracker(redis_client):
    """Initialize usage tracker"""
    global usage_tracker
    usage_tracker = UsageTracker(redis_client)
    return usage_tracker
