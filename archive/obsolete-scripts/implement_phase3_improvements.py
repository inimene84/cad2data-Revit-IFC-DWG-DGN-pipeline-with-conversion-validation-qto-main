#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3 Improvements Implementation Script
Implements advanced features for Construction AI Platform
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

class Phase3Improvements:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.api = self.project_root / "construction-platform" / "python-services" / "api"
        self.monitoring = self.project_root / "construction-platform" / "monitoring"
        self.sql = self.project_root / "construction-platform" / "sql"
        
    def implement_multi_tenancy(self):
        """Implement Multi-Tenancy Support"""
        print("\n" + "="*60)
        print("Phase 3.1: Multi-Tenancy Support")
        print("="*60)
        
        multi_tenancy_code = """# Multi-Tenancy Support
# construction-platform/python-services/api/multi_tenancy.py

from fastapi import Request, HTTPException, Depends
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class TenantManager:
    \"\"\"Multi-tenant manager with tenant isolation\"\"\"
    def __init__(self):
        self.tenants: Dict[str, Dict[str, Any]] = {}
        self.tenant_databases: Dict[str, str] = {}
    
    def get_tenant_id(self, request: Request) -> Optional[str]:
        \"\"\"Get tenant ID from request\"\"\"
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
        \"\"\"Extract tenant ID from token (simplified)\"\"\"
        # In production, decode JWT token and extract tenant_id
        # For now, return default tenant
        return "default"
    
    def get_tenant_database(self, tenant_id: str) -> str:
        \"\"\"Get database name for tenant\"\"\"
        if tenant_id not in self.tenant_databases:
            # Generate database name for tenant
            db_name = f"construction_ai_{tenant_id}"
            self.tenant_databases[tenant_id] = db_name
        return self.tenant_databases[tenant_id]
    
    def create_tenant(self, tenant_id: str, tenant_data: Dict[str, Any]) -> bool:
        \"\"\"Create new tenant\"\"\"
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
        \"\"\"Get tenant information\"\"\"
        return self.tenants.get(tenant_id)
    
    def is_tenant_active(self, tenant_id: str) -> bool:
        \"\"\"Check if tenant is active\"\"\"
        tenant = self.tenants.get(tenant_id)
        if tenant:
            return tenant.get("status") == "active"
        return False

# Global tenant manager instance
tenant_manager = TenantManager()

def get_tenant_id(request: Request) -> str:
    \"\"\"Dependency to get tenant ID from request\"\"\"
    return tenant_manager.get_tenant_id(request)

def require_tenant(request: Request) -> str:
    \"\"\"Require tenant ID in request\"\"\"
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
"""
        
        multi_tenancy_file = self.api / "multi_tenancy.py"
        multi_tenancy_file.write_text(multi_tenancy_code, encoding='utf-8')
        print(f"✓ Created {multi_tenancy_file}")
        return True
    
    def implement_usage_analytics(self):
        """Implement Usage Analytics"""
        print("\n" + "="*60)
        print("Phase 3.2: Usage Analytics")
        print("="*60)
        
        usage_analytics_code = """# Usage Analytics
# construction-platform/python-services/api/usage_analytics.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

class UsageTracker:
    \"\"\"Track usage analytics for tenants and users\"\"\"
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.usage_prefix = "usage_analytics"
    
    def track_file_upload(self, tenant_id: str, user_id: str, file_size: int, file_type: str):
        \"\"\"Track file upload\"\"\"
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
        \"\"\"Track API call\"\"\"
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
        \"\"\"Track storage usage\"\"\"
        try:
            key = f"{self.usage_prefix}:{tenant_id}:storage"
            if self.redis:
                self.redis.set(key, storage_bytes)
                self.redis.expire(key, 86400 * 30)
            
            logger.debug(f"Storage usage tracked: {tenant_id}, {storage_bytes} bytes")
        except Exception as e:
            logger.error(f"Failed to track storage usage: {e}")
    
    def get_usage_stats(self, tenant_id: str, period: str = "30d") -> Dict[str, Any]:
        \"\"\"Get usage statistics for tenant\"\"\"
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
        \"\"\"Get usage breakdown by endpoint\"\"\"
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
    \"\"\"Initialize usage tracker\"\"\"
    global usage_tracker
    usage_tracker = UsageTracker(redis_client)
    return usage_tracker
"""
        
        usage_analytics_file = self.api / "usage_analytics.py"
        usage_analytics_file.write_text(usage_analytics_code, encoding='utf-8')
        print(f"✓ Created {usage_analytics_file}")
        return True
    
    def implement_billing(self):
        """Implement Billing Integration"""
        print("\n" + "="*60)
        print("Phase 3.3: Billing Integration")
        print("="*60)
        
        billing_code = """# Billing Integration
# construction-platform/python-services/api/billing.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class BillingManager:
    \"\"\"Billing manager for usage-based billing\"\"\"
    def __init__(self):
        self.pricing_plans: Dict[str, Dict[str, Any]] = {
            "free": {
                "name": "Free",
                "price": 0.0,
                "file_upload_limit": 100,
                "storage_limit_gb": 1,
                "api_calls_limit": 1000,
                "features": ["basic_processing", "basic_analytics"]
            },
            "starter": {
                "name": "Starter",
                "price": 29.0,
                "file_upload_limit": 1000,
                "storage_limit_gb": 10,
                "api_calls_limit": 10000,
                "features": ["basic_processing", "basic_analytics", "priority_support"]
            },
            "professional": {
                "name": "Professional",
                "price": 99.0,
                "file_upload_limit": 10000,
                "storage_limit_gb": 100,
                "api_calls_limit": 100000,
                "features": ["advanced_processing", "advanced_analytics", "priority_support", "custom_workflows"]
            },
            "enterprise": {
                "name": "Enterprise",
                "price": 299.0,
                "file_upload_limit": -1,  # Unlimited
                "storage_limit_gb": -1,  # Unlimited
                "api_calls_limit": -1,  # Unlimited
                "features": ["all_features", "custom_integrations", "dedicated_support", "sla"]
            }
        }
        
        self.usage_pricing: Dict[str, Decimal] = {
            "file_upload": Decimal("0.10"),  # $0.10 per file
            "storage_gb": Decimal("0.05"),  # $0.05 per GB per month
            "api_call": Decimal("0.001"),  # $0.001 per API call
            "processing_minute": Decimal("0.50"),  # $0.50 per processing minute
        }
    
    def get_pricing_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        \"\"\"Get pricing plan by ID\"\"\"
        return self.pricing_plans.get(plan_id)
    
    def calculate_usage_cost(self, tenant_id: str, usage_stats: Dict[str, Any]) -> Decimal:
        \"\"\"Calculate usage-based cost\"\"\"
        try:
            total_cost = Decimal("0.0")
            
            # File upload cost
            files_uploaded = usage_stats.get("files_uploaded", 0)
            total_cost += Decimal(str(files_uploaded)) * self.usage_pricing["file_upload"]
            
            # Storage cost
            storage_gb = usage_stats.get("storage_used", 0) / (1024 ** 3)  # Convert to GB
            total_cost += Decimal(str(storage_gb)) * self.usage_pricing["storage_gb"]
            
            # API call cost
            api_calls = usage_stats.get("api_calls", 0)
            total_cost += Decimal(str(api_calls)) * self.usage_pricing["api_call"]
            
            # Processing cost (estimated)
            processing_minutes = usage_stats.get("processing_minutes", 0)
            total_cost += Decimal(str(processing_minutes)) * self.usage_pricing["processing_minute"]
            
            return total_cost
        except Exception as e:
            logger.error(f"Failed to calculate usage cost: {e}")
            return Decimal("0.0")
    
    def generate_invoice(self, tenant_id: str, period: str = "monthly") -> Dict[str, Any]:
        \"\"\"Generate invoice for tenant\"\"\"
        try:
            # Get tenant plan
            tenant_plan = self.get_pricing_plan("professional")  # Default plan
            base_cost = Decimal(str(tenant_plan["price"]))
            
            # Get usage stats
            from usage_analytics import usage_tracker
            if usage_tracker:
                usage_stats = usage_tracker.get_usage_stats(tenant_id, period="30d")
                usage_cost = self.calculate_usage_cost(tenant_id, usage_stats)
            else:
                usage_cost = Decimal("0.0")
                usage_stats = {}
            
            # Calculate total
            total_cost = base_cost + usage_cost
            
            invoice = {
                "tenant_id": tenant_id,
                "period": period,
                "invoice_date": datetime.now().isoformat(),
                "base_cost": float(base_cost),
                "usage_cost": float(usage_cost),
                "total_cost": float(total_cost),
                "usage_stats": usage_stats,
                "plan": tenant_plan["name"],
                "status": "pending"
            }
            
            logger.info(f"Invoice generated: {tenant_id}, ${total_cost}")
            return invoice
        except Exception as e:
            logger.error(f"Failed to generate invoice: {e}")
            return {}
    
    def get_billing_summary(self, tenant_id: str) -> Dict[str, Any]:
        \"\"\"Get billing summary for tenant\"\"\"
        try:
            tenant_plan = self.get_pricing_plan("professional")  # Default plan
            
            from usage_analytics import usage_tracker
            if usage_tracker:
                usage_stats = usage_tracker.get_usage_stats(tenant_id, period="30d")
                usage_cost = self.calculate_usage_cost(tenant_id, usage_stats)
            else:
                usage_cost = Decimal("0.0")
                usage_stats = {}
            
            summary = {
                "tenant_id": tenant_id,
                "plan": tenant_plan["name"],
                "base_cost": float(Decimal(str(tenant_plan["price"]))),
                "usage_cost": float(usage_cost),
                "total_cost": float(Decimal(str(tenant_plan["price"])) + usage_cost),
                "usage_stats": usage_stats,
                "limits": {
                    "file_upload_limit": tenant_plan["file_upload_limit"],
                    "storage_limit_gb": tenant_plan["storage_limit_gb"],
                    "api_calls_limit": tenant_plan["api_calls_limit"]
                }
            }
            
            return summary
        except Exception as e:
            logger.error(f"Failed to get billing summary: {e}")
            return {}

# Global billing manager instance
billing_manager = BillingManager()
"""
        
        billing_file = self.api / "billing.py"
        billing_file.write_text(billing_code, encoding='utf-8')
        print(f"✓ Created {billing_file}")
        return True
    
    def implement_error_analytics(self):
        """Implement Error Analytics"""
        print("\n" + "="*60)
        print("Phase 3.4: Error Analytics")
        print("="*60)
        
        error_analytics_code = """# Error Analytics
# construction-platform/python-services/api/error_analytics.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

class ErrorAnalytics:
    \"\"\"Error analytics for tracking and analyzing error patterns\"\"\"
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.error_prefix = "error_analytics"
        self.error_patterns: Dict[str, int] = defaultdict(int)
    
    def track_error(self, error_type: str, error_message: str, tenant_id: str = "default", context: Dict[str, Any] = None):
        \"\"\"Track error occurrence\"\"\"
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
        \"\"\"Get error statistics\"\"\"
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
        \"\"\"Get error trends over time\"\"\"
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
        \"\"\"Analyze error patterns\"\"\"
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
    \"\"\"Initialize error analytics\"\"\"
    global error_analytics
    error_analytics = ErrorAnalytics(redis_client)
    return error_analytics
"""
        
        error_analytics_file = self.api / "error_analytics.py"
        error_analytics_file.write_text(error_analytics_code, encoding='utf-8')
        print(f"✓ Created {error_analytics_file}")
        return True
    
    def implement_audit_logging(self):
        """Implement Audit Logging"""
        print("\n" + "="*60)
        print("Phase 3.5: Audit Logging")
        print("="*60)
        
        audit_logging_code = """# Audit Logging
# construction-platform/python-services/api/audit_logging.py

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import json
from enum import Enum

logger = logging.getLogger(__name__)

class AuditEventType(Enum):
    \"\"\"Audit event types\"\"\"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    FILE_UPLOAD = "file_upload"
    FILE_DELETE = "file_delete"
    FILE_DOWNLOAD = "file_download"
    DATA_ACCESS = "data_access"
    DATA_MODIFY = "data_modify"
    DATA_DELETE = "data_delete"
    CONFIG_CHANGE = "config_change"
    SECURITY_EVENT = "security_event"
    API_CALL = "api_call"
    WORKFLOW_EXECUTION = "workflow_execution"
    ERROR = "error"
    OTHER = "other"

class AuditLogger:
    \"\"\"Audit logger for comprehensive event tracking\"\"\"
    def __init__(self, redis_client=None, db_client=None):
        self.redis = redis_client
        self.db = db_client
        self.audit_prefix = "audit_log"
        self.logger = logging.getLogger("audit")
    
    def log_event(
        self,
        event_type: AuditEventType,
        user_id: str,
        tenant_id: str = "default",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        \"\"\"Log audit event\"\"\"
        try:
            timestamp = datetime.now()
            event = {
                "event_type": event_type.value,
                "user_id": user_id,
                "tenant_id": tenant_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "action": action,
                "timestamp": timestamp.isoformat(),
                "details": details or {},
                "ip_address": ip_address,
                "user_agent": user_agent
            }
            
            # Log to Redis
            if self.redis:
                event_key = f"{self.audit_prefix}:{tenant_id}:{timestamp.isoformat()}"
                self.redis.setex(event_key, 86400 * 90, json.dumps(event))  # 90 days
            
            # Log to database
            if self.db:
                # In production, insert into PostgreSQL audit_logs table
                pass
            
            # Log to file
            self.logger.info(f"Audit event: {event_type.value}, {user_id}, {tenant_id}, {action}")
            
            return event
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            return None
    
    def get_audit_logs(
        self,
        tenant_id: str,
        event_type: Optional[AuditEventType] = None,
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        \"\"\"Get audit logs\"\"\"
        try:
            logs = []
            
            if self.redis:
                # Get audit logs from Redis
                pattern = f"{self.audit_prefix}:{tenant_id}:*"
                keys = self.redis.keys(pattern)
                
                for key in keys[:limit]:
                    event_data = self.redis.get(key)
                    if event_data:
                        event = json.loads(event_data)
                        
                        # Filter by event type
                        if event_type and event["event_type"] != event_type.value:
                            continue
                        
                        # Filter by user ID
                        if user_id and event["user_id"] != user_id:
                            continue
                        
                        # Filter by date range
                        event_date = datetime.fromisoformat(event["timestamp"])
                        if start_date and event_date < start_date:
                            continue
                        if end_date and event_date > end_date:
                            continue
                        
                        logs.append(event)
                
                # Sort by timestamp
                logs.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return logs
        except Exception as e:
            logger.error(f"Failed to get audit logs: {e}")
            return []
    
    def get_audit_summary(
        self,
        tenant_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        \"\"\"Get audit summary\"\"\"
        try:
            logs = self.get_audit_logs(tenant_id, start_date=start_date, end_date=end_date, limit=10000)
            
            summary = {
                "tenant_id": tenant_id,
                "total_events": len(logs),
                "events_by_type": {},
                "events_by_user": {},
                "events_by_action": {}
            }
            
            for log in logs:
                # Count by type
                event_type = log["event_type"]
                if event_type not in summary["events_by_type"]:
                    summary["events_by_type"][event_type] = 0
                summary["events_by_type"][event_type] += 1
                
                # Count by user
                user_id = log["user_id"]
                if user_id not in summary["events_by_user"]:
                    summary["events_by_user"][user_id] = 0
                summary["events_by_user"][user_id] += 1
                
                # Count by action
                action = log.get("action")
                if action:
                    if action not in summary["events_by_action"]:
                        summary["events_by_action"][action] = 0
                    summary["events_by_action"][action] += 1
            
            return summary
        except Exception as e:
            logger.error(f"Failed to get audit summary: {e}")
            return {}

# Global audit logger instance
audit_logger = None

def initialize_audit_logger(redis_client=None, db_client=None):
    \"\"\"Initialize audit logger\"\"\"
    global audit_logger
    audit_logger = AuditLogger(redis_client, db_client)
    return audit_logger
"""
        
        audit_logging_file = self.api / "audit_logging.py"
        audit_logging_file.write_text(audit_logging_code, encoding='utf-8')
        print(f"✓ Created {audit_logging_file}")
        return True
    
    def implement_vector_db_integration(self):
        """Implement Vector DB Integration"""
        print("\n" + "="*60)
        print("Phase 3.6: Vector DB Integration")
        print("="*60)
        
        vector_db_code = """# Vector DB Integration for Qdrant
# construction-platform/python-services/api/vector_db.py

from typing import Dict, Any, Optional, List
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np

logger = logging.getLogger(__name__)

class VectorDBService:
    \"\"\"Vector database service for similarity search\"\"\"
    def __init__(self, qdrant_url: str = "http://localhost:6333", collection_name: str = "cost_estimates"):
        try:
            self.client = QdrantClient(url=qdrant_url)
            self.collection_name = collection_name
            self._ensure_collection()
            logger.info(f"Vector DB connected: {qdrant_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.client = None
    
    def _ensure_collection(self):
        \"\"\"Ensure collection exists\"\"\"
        if not self.client:
            return
        
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                logger.info(f"Collection created: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to ensure collection: {e}")
    
    def add_cost_estimate(
        self,
        estimate_id: str,
        vector: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        \"\"\"Add cost estimate to vector database\"\"\"
        if not self.client:
            return False
        
        try:
            point = PointStruct(
                id=estimate_id,
                vector=vector,
                payload=metadata
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Cost estimate added: {estimate_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add cost estimate: {e}")
            return False
    
    def search_similar_estimates(
        self,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        \"\"\"Search for similar cost estimates\"\"\"
        if not self.client:
            return []
        
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )
            
            similar_estimates = []
            for result in results:
                similar_estimates.append({
                    "id": result.id,
                    "score": result.score,
                    "metadata": result.payload
                })
            
            logger.info(f"Found {len(similar_estimates)} similar estimates")
            return similar_estimates
        except Exception as e:
            logger.error(f"Failed to search similar estimates: {e}")
            return []
    
    def get_estimate_by_id(self, estimate_id: str) -> Optional[Dict[str, Any]]:
        \"\"\"Get cost estimate by ID\"\"\"
        if not self.client:
            return None
        
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[estimate_id]
            )
            
            if result:
                return {
                    "id": result[0].id,
                    "metadata": result[0].payload
                }
            
            return None
        except Exception as e:
            logger.error(f"Failed to get estimate by ID: {e}")
            return None
    
    def delete_estimate(self, estimate_id: str) -> bool:
        \"\"\"Delete cost estimate from vector database\"\"\"
        if not self.client:
            return False
        
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[estimate_id]
            )
            
            logger.info(f"Cost estimate deleted: {estimate_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete cost estimate: {e}")
            return False

# Global vector DB service instance
vector_db_service = None

def initialize_vector_db(qdrant_url: str = "http://localhost:6333", collection_name: str = "cost_estimates"):
    \"\"\"Initialize vector DB service\"\"\"
    global vector_db_service
    vector_db_service = VectorDBService(qdrant_url, collection_name)
    return vector_db_service
"""
        
        vector_db_file = self.api / "vector_db.py"
        vector_db_file.write_text(vector_db_code, encoding='utf-8')
        print(f"✓ Created {vector_db_file}")
        return True
    
    def implement_automated_archival(self):
        """Implement Automated Archival"""
        print("\n" + "="*60)
        print("Phase 3.7: Automated Archival")
        print("="*60)
        
        archival_code = """# Automated Archival
# construction-platform/python-services/api/archival.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

class ArchivalService:
    \"\"\"Automated archival service for old files\"\"\"
    def __init__(self, archive_dir: str = "archives", retention_days: int = 90, s3_client=None):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
        self.retention_days = retention_days
        self.s3_client = s3_client
        self.archived_files: Dict[str, Dict[str, Any]] = {}
    
    def archive_file(self, file_path: str, tenant_id: str = "default") -> bool:
        \"\"\"Archive file to S3 Glacier or local archive\"\"\"
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                logger.warning(f"File not found: {file_path}")
                return False
            
            # Generate archive path
            archive_path = self.archive_dir / tenant_id / file_path_obj.name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file to archive
            shutil.copy2(file_path, archive_path)
            
            # If S3 client available, upload to S3 Glacier
            if self.s3_client:
                try:
                    s3_key = f"archives/{tenant_id}/{file_path_obj.name}"
                    self.s3_client.upload_file(
                        file_path,
                        "construction-ai-archives",
                        s3_key,
                        ExtraArgs={"StorageClass": "GLACIER"}
                    )
                    logger.info(f"File archived to S3 Glacier: {s3_key}")
                except Exception as e:
                    logger.error(f"Failed to upload to S3: {e}")
            
            # Record archival
            self.archived_files[file_path] = {
                "tenant_id": tenant_id,
                "original_path": file_path,
                "archive_path": str(archive_path),
                "archived_at": datetime.now().isoformat(),
                "file_size": file_path_obj.stat().st_size
            }
            
            # Delete original file
            file_path_obj.unlink()
            
            logger.info(f"File archived: {file_path} -> {archive_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to archive file: {e}")
            return False
    
    def archive_old_files(self, tenant_id: str = "default", days_old: int = None) -> int:
        \"\"\"Archive files older than specified days\"\"\"
        try:
            days_old = days_old or self.retention_days
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            archived_count = 0
            
            # Get files from uploads directory
            uploads_dir = Path("uploads") / tenant_id
            if uploads_dir.exists():
                for file_path in uploads_dir.iterdir():
                    if file_path.is_file():
                        file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_mtime < cutoff_date:
                            if self.archive_file(str(file_path), tenant_id):
                                archived_count += 1
            
            logger.info(f"Archived {archived_count} old files for tenant {tenant_id}")
            return archived_count
        except Exception as e:
            logger.error(f"Failed to archive old files: {e}")
            return 0
    
    def restore_file(self, archive_path: str, restore_path: str) -> bool:
        \"\"\"Restore file from archive\"\"\"
        try:
            archive_path_obj = Path(archive_path)
            if not archive_path_obj.exists():
                logger.warning(f"Archive file not found: {archive_path}")
                return False
            
            restore_path_obj = Path(restore_path)
            restore_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file from archive
            shutil.copy2(archive_path, restore_path)
            
            logger.info(f"File restored: {archive_path} -> {restore_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore file: {e}")
            return False
    
    def get_archived_files(self, tenant_id: str = "default") -> List[Dict[str, Any]]:
        \"\"\"Get list of archived files\"\"\"
        try:
            archived_files = []
            
            archive_dir = self.archive_dir / tenant_id
            if archive_dir.exists():
                for file_path in archive_dir.iterdir():
                    if file_path.is_file():
                        archived_files.append({
                            "file_name": file_path.name,
                            "archive_path": str(file_path),
                            "file_size": file_path.stat().st_size,
                            "archived_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
            
            return archived_files
        except Exception as e:
            logger.error(f"Failed to get archived files: {e}")
            return []

# Global archival service instance
archival_service = None

def initialize_archival_service(archive_dir: str = "archives", retention_days: int = 90, s3_client=None):
    \"\"\"Initialize archival service\"\"\"
    global archival_service
    archival_service = ArchivalService(archive_dir, retention_days, s3_client)
    return archival_service
"""
        
        archival_file = self.api / "archival.py"
        archival_file.write_text(archival_code, encoding='utf-8')
        print(f"✓ Created {archival_file}")
        return True
    
    def create_elk_stack_config(self):
        """Create ELK Stack Configuration"""
        print("\n" + "="*60)
        print("Phase 3.8: ELK Stack Configuration")
        print("="*60)
        
        elk_compose_code = """# ELK Stack Docker Compose
# construction-platform/monitoring/elk-stack.yml

version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elk-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - monitoring

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: elk-logstash
    volumes:
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5044:5044"
      - "9600:9600"
    depends_on:
      - elasticsearch
    networks:
      - monitoring

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: elk-kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - monitoring

volumes:
  elasticsearch_data:

networks:
  monitoring:
    driver: bridge
"""
        
        elk_compose_file = self.monitoring / "elk-stack.yml"
        elk_compose_file.parent.mkdir(exist_ok=True)
        elk_compose_file.write_text(elk_compose_code, encoding='utf-8')
        print(f"✓ Created {elk_compose_file}")
        return True
    
    def create_opentelemetry_config(self):
        """Create OpenTelemetry Configuration"""
        print("\n" + "="*60)
        print("Phase 3.9: OpenTelemetry Configuration")
        print("="*60)
        
        opentelemetry_code = """# OpenTelemetry Configuration
# construction-platform/python-services/api/opentelemetry_config.py

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import logging

logger = logging.getLogger(__name__)

def setup_opentelemetry(service_name: str = "construction-ai-api", jaeger_endpoint: str = "http://localhost:14268/api/traces"):
    \"\"\"Setup OpenTelemetry with Jaeger\"\"\"
    try:
        # Create tracer provider
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)
        
        # Create Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
            endpoint=jaeger_endpoint
        )
        
        # Create span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        tracer_provider.add_span_processor(span_processor)
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument()
        
        # Instrument Redis
        RedisInstrumentor().instrument()
        
        # Instrument requests
        RequestsInstrumentor().instrument()
        
        logger.info(f"OpenTelemetry configured: {service_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")
        return False

# Auto-setup if enabled
import os
if os.getenv("ENABLE_OPENTELEMETRY", "false").lower() == "true":
    setup_opentelemetry()
"""
        
        opentelemetry_file = self.api / "opentelemetry_config.py"
        opentelemetry_file.write_text(opentelemetry_code, encoding='utf-8')
        print(f"✓ Created {opentelemetry_file}")
        return True
    
    def create_jaeger_config(self):
        """Create Jaeger Configuration"""
        print("\n" + "="*60)
        print("Phase 3.10: Jaeger Configuration")
        print("="*60)
        
        jaeger_compose_code = """# Jaeger Docker Compose
# construction-platform/monitoring/jaeger.yml

version: '3.8'

services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
    ports:
      - "5775:5775/udp"  # Agent (zipkin.thrift)
      - "6831:6831/udp"  # Agent (jaeger.thrift)
      - "6832:6832/udp"  # Agent (jaeger.thrift)
      - "5778:5778"      # Agent config
      - "16686:16686"    # UI
      - "14268:14268"    # Collector HTTP
      - "14250:14250"    # Collector gRPC
      - "9411:9411"      # Zipkin
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge
"""
        
        jaeger_compose_file = self.monitoring / "jaeger.yml"
        jaeger_compose_file.parent.mkdir(exist_ok=True)
        jaeger_compose_file.write_text(jaeger_compose_code, encoding='utf-8')
        print(f"✓ Created {jaeger_compose_file}")
        return True
    
    def update_app_py_for_phase3(self):
        """Update app.py with Phase 3 improvements"""
        print("\n" + "="*60)
        print("Phase 3.11: Updating app.py")
        print("="*60)
        
        # Read current app.py
        app_file = self.api / "app.py"
        app_content = app_file.read_text(encoding='utf-8')
        
        # Add Phase 3 imports
        phase3_imports = """
# Phase 3 Improvements
try:
    from multi_tenancy import tenant_manager, get_tenant_id, require_tenant
    from usage_analytics import usage_tracker, initialize_usage_tracker
    from billing import billing_manager
    from error_analytics import error_analytics, initialize_error_analytics
    from audit_logging import audit_logger, initialize_audit_logger, AuditEventType
    from vector_db import vector_db_service, initialize_vector_db
    from archival import archival_service, initialize_archival_service
    from opentelemetry_config import setup_opentelemetry
    PHASE3_IMPROVEMENTS_AVAILABLE = True
except ImportError as e:
    PHASE3_IMPROVEMENTS_AVAILABLE = False
    tenant_manager = None
    usage_tracker = None
    billing_manager = None
    error_analytics = None
    audit_logger = None
    vector_db_service = None
    archival_service = None
"""
        
        # Check if Phase 3 imports already exist
        if "from multi_tenancy import" not in app_content:
            # Add after Phase 2 imports
            phase2_end = app_content.find("except ImportError as e:")
            if phase2_end != -1:
                # Find the end of Phase 2 exception block
                phase2_block_end = app_content.find("from config import", phase2_end)
                if phase2_block_end != -1:
                    app_content = app_content[:phase2_block_end] + phase3_imports + "\n" + app_content[phase2_block_end:]
        
        # Add Phase 3 initialization
        phase3_init_code = """
# Phase 3: Initialize advanced features
if PHASE3_IMPROVEMENTS_AVAILABLE:
    # Initialize usage tracker
    if redis_client:
        initialize_usage_tracker(redis_client)
        logger.info("Usage tracker initialized")
    
    # Initialize error analytics
    if redis_client:
        initialize_error_analytics(redis_client)
        logger.info("Error analytics initialized")
    
    # Initialize audit logger
    if redis_client:
        initialize_audit_logger(redis_client)
        logger.info("Audit logger initialized")
    
    # Initialize vector DB
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    initialize_vector_db(qdrant_url)
    logger.info("Vector DB initialized")
    
    # Initialize archival service
    archive_dir = os.getenv("ARCHIVE_DIR", "archives")
    retention_days = int(os.getenv("RETENTION_DAYS", "90"))
    initialize_archival_service(archive_dir, retention_days)
    logger.info("Archival service initialized")
    
    # Setup OpenTelemetry if enabled
    if os.getenv("ENABLE_OPENTELEMETRY", "false").lower() == "true":
        setup_opentelemetry()
        logger.info("OpenTelemetry configured")
"""
        
        # Check if Phase 3 initialization already exists
        if "initialize_usage_tracker" not in app_content:
            # Add after Phase 2 initialization
            phase2_init_end = app_content.find("logger.info(\"Phase 2 improvements not available or disabled\")")
            if phase2_init_end != -1:
                phase2_init_block_end = app_content.find("\n# ==========================================", phase2_init_end)
                if phase2_init_block_end != -1:
                    app_content = app_content[:phase2_init_block_end] + phase3_init_code + "\n" + app_content[phase2_init_block_end:]
        
        # Add Phase 3 API endpoints
        phase3_endpoints_code = """
# Phase 3: Usage Analytics API endpoints
if PHASE3_IMPROVEMENTS_AVAILABLE:
    @app.get("/api/usage/stats")
    async def get_usage_stats(tenant_id: str = Depends(get_tenant_id), period: str = "30d"):
        \"\"\"Get usage statistics for tenant\"\"\"
        if usage_tracker:
            return usage_tracker.get_usage_stats(tenant_id, period)
        return {"error": "Usage tracker not available"}
    
    @app.get("/api/usage/breakdown")
    async def get_usage_breakdown(tenant_id: str = Depends(get_tenant_id), period: str = "30d"):
        \"\"\"Get usage breakdown by endpoint\"\"\"
        if usage_tracker:
            return usage_tracker.get_usage_breakdown(tenant_id, period)
        return {"error": "Usage tracker not available"}
    
    @app.get("/api/billing/summary")
    async def get_billing_summary(tenant_id: str = Depends(get_tenant_id)):
        \"\"\"Get billing summary for tenant\"\"\"
        if billing_manager:
            return billing_manager.get_billing_summary(tenant_id)
        return {"error": "Billing manager not available"}
    
    @app.get("/api/billing/invoice")
    async def generate_invoice(tenant_id: str = Depends(get_tenant_id), period: str = "monthly"):
        \"\"\"Generate invoice for tenant\"\"\"
        if billing_manager:
            return billing_manager.generate_invoice(tenant_id, period)
        return {"error": "Billing manager not available"}
    
    @app.get("/api/errors/stats")
    async def get_error_stats(tenant_id: str = Depends(get_tenant_id), period: str = "30d"):
        \"\"\"Get error statistics\"\"\"
        if error_analytics:
            return error_analytics.get_error_stats(tenant_id, period)
        return {"error": "Error analytics not available"}
    
    @app.get("/api/errors/analysis")
    async def analyze_errors(tenant_id: str = Depends(get_tenant_id), period: str = "30d"):
        \"\"\"Analyze error patterns\"\"\"
        if error_analytics:
            return error_analytics.analyze_error_patterns(tenant_id, period)
        return {"error": "Error analytics not available"}
    
    @app.get("/api/audit/logs")
    async def get_audit_logs(tenant_id: str = Depends(get_tenant_id), limit: int = 100):
        \"\"\"Get audit logs\"\"\"
        if audit_logger:
            return audit_logger.get_audit_logs(tenant_id, limit=limit)
        return {"error": "Audit logger not available"}
    
    @app.get("/api/vector/search")
    async def search_similar_estimates(query_vector: List[float], limit: int = 10):
        \"\"\"Search for similar cost estimates\"\"\"
        if vector_db_service:
            return vector_db_service.search_similar_estimates(query_vector, limit)
        return {"error": "Vector DB service not available"}
    
    @app.post("/api/archival/archive")
    async def archive_old_files(tenant_id: str = Depends(get_tenant_id), days_old: int = 90):
        \"\"\"Archive old files\"\"\"
        if archival_service:
            archived_count = archival_service.archive_old_files(tenant_id, days_old)
            return {"status": "success", "archived_count": archived_count}
        return {"error": "Archival service not available"}
"""
        
        # Check if Phase 3 endpoints already exist
        if "@app.get(\"/api/usage/stats\")" not in app_content:
            # Add before the global exception handler
            exception_handler_start = app_content.find("# Phase 2: Add global exception handler")
            if exception_handler_start != -1:
                app_content = app_content[:exception_handler_start] + phase3_endpoints_code + "\n" + app_content[exception_handler_start:]
        
        # Write updated app.py
        app_file.write_text(app_content, encoding='utf-8')
        print(f"✓ Updated {app_file}")
        return True
    
    def create_sql_schema(self):
        """Create SQL Schema for Multi-Tenancy"""
        print("\n" + "="*60)
        print("Phase 3.12: Creating SQL Schema")
        print("="*60)
        
        sql_schema_code = """-- SQL Schema for Multi-Tenancy and Audit Logging
-- construction-platform/sql/schema.sql

-- Tenants table
CREATE TABLE IF NOT EXISTS tenants (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    plan VARCHAR(50) NOT NULL DEFAULT 'free',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- Files table
CREATE TABLE IF NOT EXISTS files (
    id VARCHAR(255) PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    action VARCHAR(50),
    details JSONB,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Usage analytics table
CREATE TABLE IF NOT EXISTS usage_analytics (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_value BIGINT NOT NULL,
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Billing table
CREATE TABLE IF NOT EXISTS billing (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    invoice_id VARCHAR(255) UNIQUE NOT NULL,
    period VARCHAR(50) NOT NULL,
    base_cost DECIMAL(10, 2) NOT NULL,
    usage_cost DECIMAL(10, 2) NOT NULL,
    total_cost DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_files_tenant_id ON files(tenant_id);
CREATE INDEX IF NOT EXISTS idx_files_user_id ON files(user_id);
CREATE INDEX IF NOT EXISTS idx_files_created_at ON files(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_tenant_id ON audit_logs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_usage_analytics_tenant_id ON usage_analytics(tenant_id);
CREATE INDEX IF NOT EXISTS idx_usage_analytics_metric_date ON usage_analytics(metric_date);
CREATE INDEX IF NOT EXISTS idx_billing_tenant_id ON billing(tenant_id);
CREATE INDEX IF NOT EXISTS idx_billing_status ON billing(status);
"""
        
        sql_file = self.sql / "schema.sql"
        sql_file.parent.mkdir(exist_ok=True)
        sql_file.write_text(sql_schema_code, encoding='utf-8')
        print(f"✓ Created {sql_file}")
        return True
    
    def update_docker_compose(self):
        """Update Docker Compose with Phase 3 services"""
        print("\n" + "="*60)
        print("Phase 3.13: Updating Docker Compose")
        print("="*60)
        
        # Read current docker-compose.prod.yml
        docker_compose_file = self.project_root / "construction-platform" / "docker-compose.prod.yml"
        docker_compose_content = docker_compose_file.read_text(encoding='utf-8')
        
        # Add ELK Stack and Jaeger services
        elk_jaeger_services = """
  # ELK Stack
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elk-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - default
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: elk-logstash
    volumes:
      - ./monitoring/logstash/config:/usr/share/logstash/config
      - ./monitoring/logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5044:5044"
      - "9600:9600"
    depends_on:
      - elasticsearch
    networks:
      - default
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: elk-kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - default
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5601/api/status || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Jaeger
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"
      - "14268:14268"
      - "14250:14250"
      - "9411:9411"
    networks:
      - default
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:16686/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
"""
        
        # Check if ELK services already exist
        if "elasticsearch:" not in docker_compose_content:
            # Add before volumes section
            volumes_start = docker_compose_content.find("volumes:")
            if volumes_start != -1:
                docker_compose_content = docker_compose_content[:volumes_start] + elk_jaeger_services + "\n" + docker_compose_content[volumes_start:]
            
            # Add elasticsearch_data volume
            if "elasticsearch_data:" not in docker_compose_content:
                volumes_end = docker_compose_content.find("networks:")
                if volumes_end != -1:
                    elasticsearch_volume = "  elasticsearch_data:\n    driver: local\n"
                    docker_compose_content = docker_compose_content[:volumes_end] + elasticsearch_volume + "\n" + docker_compose_content[volumes_end:]
        
        # Write updated docker-compose.prod.yml
        docker_compose_file.write_text(docker_compose_content, encoding='utf-8')
        print(f"✓ Updated {docker_compose_file}")
        return True
    
    def update_requirements_txt(self):
        """Update requirements.txt with Phase 3 dependencies"""
        print("\n" + "="*60)
        print("Phase 3.14: Updating requirements.txt")
        print("="*60)
        
        requirements_file = self.api / "requirements.txt"
        
        # Read current requirements.txt
        if requirements_file.exists():
            requirements_content = requirements_file.read_text(encoding='utf-8')
        else:
            requirements_content = ""
        
        # Add Phase 3 dependencies
        phase3_dependencies = """
# Phase 3 Improvements
qdrant-client>=1.7.0
opentelemetry-api>=1.21.0
opentelemetry-sdk>=1.21.0
opentelemetry-exporter-jaeger-thrift>=1.21.0
opentelemetry-instrumentation-fastapi>=0.42b0
opentelemetry-instrumentation-redis>=0.42b0
opentelemetry-instrumentation-requests>=0.42b0
boto3>=1.34.0  # For S3 archival
psycopg2-binary>=2.9.9  # For PostgreSQL
sqlalchemy>=2.0.23  # For database ORM
"""
        
        # Check if Phase 3 dependencies already exist
        if "qdrant-client" not in requirements_content:
            requirements_content += phase3_dependencies
        
        # Write updated requirements.txt
        requirements_file.write_text(requirements_content, encoding='utf-8')
        print(f"✓ Updated {requirements_file}")
        return True
    
    def run(self):
        """Run Phase 3 improvements implementation"""
        print("="*60)
        print("Phase 3 Improvements Implementation")
        print("="*60)
        
        # Implement improvements
        self.implement_multi_tenancy()
        self.implement_usage_analytics()
        self.implement_billing()
        self.implement_error_analytics()
        self.implement_audit_logging()
        self.implement_vector_db_integration()
        self.implement_automated_archival()
        self.create_elk_stack_config()
        self.create_opentelemetry_config()
        self.create_jaeger_config()
        self.update_app_py_for_phase3()
        self.create_sql_schema()
        self.update_docker_compose()
        self.update_requirements_txt()
        
        print("\n" + "="*60)
        print("Phase 3 Improvements Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review created files")
        print("2. Install Phase 3 dependencies")
        print("3. Test multi-tenancy")
        print("4. Test usage analytics")
        print("5. Test billing")
        print("6. Test error analytics")
        print("7. Test audit logging")
        print("8. Test vector DB")
        print("9. Test archival")
        print("10. Test ELK Stack")
        print("11. Test Jaeger")

if __name__ == "__main__":
    project_root = Path(__file__).parent
    improvements = Phase3Improvements(project_root)
    improvements.run()

