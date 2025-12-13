# Audit Logging
# construction-platform/python-services/api/audit_logging.py

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import json
from enum import Enum

logger = logging.getLogger(__name__)

class AuditEventType(Enum):
    """Audit event types"""
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
    """Audit logger for comprehensive event tracking"""
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
        """Log audit event"""
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
        """Get audit logs"""
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
        """Get audit summary"""
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
    """Initialize audit logger"""
    global audit_logger
    audit_logger = AuditLogger(redis_client, db_client)
    return audit_logger
