# Error Analytics
# construction-platform/python-services/api/error_analytics.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

class ErrorAnalytics:
    """Error analytics for tracking and analyzing error patterns"""
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.error_prefix = "error_analytics"
        self.error_patterns: Dict[str, int] = defaultdict(int)
    
    def track_error(self, error_type: str, error_message: str, tenant_id: str = "default", context: Dict[str, Any] = None):
        """Track error occurrence"""
        try:
            timestamp = datetime.now()
            date_key = timestamp.strftime('%Y-%m-%d')
            hour_key = timestamp.strftime('%Y-%m-%d-%H')
            
            # Track error by type
            type_key = f"{self.error_prefix}:{tenant_id}:types:{error_type}:{date_key}"
            if self.redis:
                self.redis.incr(type_key)
                self.redis.expire(type_key, 86400 * 30)  # 30 days
            
            # Track error by hour
            hour_key_full = f"{self.error_prefix}:{tenant_id}:hours:{hour_key}"
            if self.redis:
                self.redis.incr(hour_key_full)
                self.redis.expire(hour_key_full, 86400 * 7)  # 7 days
            
            # Track error message pattern
            message_hash = hash(error_message) % 10000
            pattern_key = f"{self.error_prefix}:{tenant_id}:patterns:{message_hash}:{date_key}"
            if self.redis:
                self.redis.incr(pattern_key)
                self.redis.expire(pattern_key, 86400 * 30)
            
            # Store error details
            error_details = {
                "error_type": error_type,
                "error_message": error_message,
                "tenant_id": tenant_id,
                "timestamp": timestamp.isoformat(),
                "context": context or {}
            }
            
            error_key = f"{self.error_prefix}:{tenant_id}:errors:{timestamp.isoformat()}"
            if self.redis:
                self.redis.setex(error_key, 86400 * 30, json.dumps(error_details))
            
            # Update in-memory patterns
            self.error_patterns[error_type] += 1
            
            logger.warning(f"Error tracked: {error_type}, {tenant_id}")
        except Exception as e:
            logger.error(f"Failed to track error: {e}")
    
    def get_error_stats(self, tenant_id: str, period: str = "30d") -> Dict[str, Any]:
        """Get error statistics"""
        try:
            days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
            start_date = datetime.now() - timedelta(days=days)
            
            stats = {
                "tenant_id": tenant_id,
                "period": period,
                "total_errors": 0,
                "errors_by_type": {},
                "errors_by_hour": {},
                "top_errors": []
            }
            
            if self.redis:
                # Get errors by type
                for i in range(days):
                    date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                    pattern = f"{self.error_prefix}:{tenant_id}:types:*:{date}"
                    keys = self.redis.keys(pattern)
                    for key in keys:
                        error_type = key.split(":")[-2]
                        count = self.redis.get(key)
                        if count:
                            if error_type not in stats["errors_by_type"]:
                                stats["errors_by_type"][error_type] = 0
                            stats["errors_by_type"][error_type] += int(count)
                            stats["total_errors"] += int(count)
                
                # Get top errors
                for error_type, count in stats["errors_by_type"].items():
                    stats["top_errors"].append({
                        "error_type": error_type,
                        "count": count,
                        "percentage": (count / stats["total_errors"] * 100) if stats["total_errors"] > 0 else 0
                    })
                
                # Sort by count
                stats["top_errors"].sort(key=lambda x: x["count"], reverse=True)
                stats["top_errors"] = stats["top_errors"][:10]  # Top 10
            
            return stats
        except Exception as e:
            logger.error(f"Failed to get error stats: {e}")
            return {}
    
    def get_error_trends(self, tenant_id: str, period: str = "30d") -> List[Dict[str, Any]]:
        """Get error trends over time"""
        try:
            days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
            start_date = datetime.now() - timedelta(days=days)
            
            trends = []
            
            if self.redis:
                for i in range(days):
                    date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                    pattern = f"{self.error_prefix}:{tenant_id}:types:*:{date}"
                    keys = self.redis.keys(pattern)
                    
                    daily_errors = {}
                    for key in keys:
                        error_type = key.split(":")[-2]
                        count = self.redis.get(key)
                        if count:
                            daily_errors[error_type] = int(count)
                    
                    trends.append({
                        "date": date,
                        "errors": daily_errors,
                        "total": sum(daily_errors.values())
                    })
            
            return trends
        except Exception as e:
            logger.error(f"Failed to get error trends: {e}")
            return []
    
    def analyze_error_patterns(self, tenant_id: str, period: str = "30d") -> Dict[str, Any]:
        """Analyze error patterns"""
        try:
            stats = self.get_error_stats(tenant_id, period)
            trends = self.get_error_trends(tenant_id, period)
            
            analysis = {
                "tenant_id": tenant_id,
                "period": period,
                "total_errors": stats.get("total_errors", 0),
                "error_rate": stats.get("total_errors", 0) / 30 if period == "30d" else stats.get("total_errors", 0) / 365,
                "top_errors": stats.get("top_errors", []),
                "trends": trends,
                "recommendations": []
            }
            
            # Generate recommendations
            if analysis["error_rate"] > 10:
                analysis["recommendations"].append("High error rate detected. Please review error logs and fix common issues.")
            
            if stats.get("errors_by_type", {}).get("validation_error", 0) > 50:
                analysis["recommendations"].append("High validation errors. Please review input validation rules.")
            
            if stats.get("errors_by_type", {}).get("server_error", 0) > 20:
                analysis["recommendations"].append("High server errors. Please check server health and logs.")
            
            return analysis
        except Exception as e:
            logger.error(f"Failed to analyze error patterns: {e}")
            return {}

# Global error analytics instance
error_analytics = None

def initialize_error_analytics(redis_client):
    """Initialize error analytics"""
    global error_analytics
    error_analytics = ErrorAnalytics(redis_client)
    return error_analytics
