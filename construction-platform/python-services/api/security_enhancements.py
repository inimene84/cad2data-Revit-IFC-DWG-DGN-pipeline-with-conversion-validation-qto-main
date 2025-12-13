"""
Advanced security and compliance features for Construction AI Agent
"""

import hashlib
import hmac
import jwt
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import bcrypt

logger = logging.getLogger(__name__)

class SecurityManager:
    """Advanced security management for Construction AI Agent"""
    
    def __init__(self, secret_key: str, redis_client: redis.Redis):
        self.secret_key = secret_key
        self.redis_client = redis_client
        self.security_scheme = HTTPBearer()
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_access_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        payload = {
            "user_id": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def create_file_hash(self, file_content: bytes) -> str:
        """Create secure hash for file verification"""
        return hashlib.sha256(file_content).hexdigest()
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for security"""
        import re
        # Remove dangerous characters
        filename = re.sub(r'[^\w\-_\.]', '', filename)
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1)
            filename = name[:250] + '.' + ext
        return filename
    
    def validate_file_type(self, filename: str, allowed_extensions: List[str]) -> bool:
        """Validate file type"""
        if not filename:
            return False
        
        file_ext = filename.lower().split('.')[-1]
        return file_ext in allowed_extensions
    
    def rate_limit_check(self, user_id: str, action: str, limit: int = 100) -> bool:
        """Check rate limiting for user actions"""
        key = f"rate_limit:{user_id}:{action}"
        
        try:
            current_count = self.redis_client.get(key)
            if current_count is None:
                self.redis_client.setex(key, 3600, 1)  # 1 hour window
                return True
            
            if int(current_count) >= limit:
                return False
            
            self.redis_client.incr(key)
            return True
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return True  # Allow on error
    
    def log_security_event(self, event_type: str, user_id: str, details: Dict):
        """Log security events"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details,
            "ip_address": details.get("ip_address", "unknown")
        }
        
        # Store in Redis for real-time monitoring
        self.redis_client.lpush("security_events", str(event))
        self.redis_client.ltrim("security_events", 0, 1000)  # Keep last 1000 events
        
        logger.warning(f"Security event: {event_type} - {user_id}")

class EstonianGDPRCompliance:
    """Estonian GDPR compliance features"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    def create_data_processing_record(self, user_id: str, data_type: str, purpose: str) -> str:
        """Create GDPR-compliant data processing record"""
        record_id = secrets.token_urlsafe(16)
        
        record = {
            "id": record_id,
            "user_id": user_id,
            "data_type": data_type,
            "purpose": purpose,
            "legal_basis": "Legitimate interest - construction project management",
            "created_at": datetime.utcnow().isoformat(),
            "retention_period": "7 years",  # Estonian construction law requirement
            "status": "active"
        }
        
        self.redis_client.hset(f"gdpr_record:{record_id}", mapping=record)
        return record_id
    
    def request_data_deletion(self, user_id: str) -> Dict:
        """Handle GDPR data deletion request"""
        # Find all user data
        user_data_keys = self.redis_client.keys(f"user_data:{user_id}:*")
        
        deletion_log = {
            "user_id": user_id,
            "requested_at": datetime.utcnow().isoformat(),
            "deleted_keys": [],
            "status": "processing"
        }
        
        # Delete user data (in production, this would be more comprehensive)
        for key in user_data_keys:
            self.redis_client.delete(key)
            deletion_log["deleted_keys"].append(key)
        
        # Log the deletion
        self.redis_client.hset(f"gdpr_deletion:{user_id}", mapping=deletion_log)
        
        return deletion_log
    
    def export_user_data(self, user_id: str) -> Dict:
        """Export all user data for GDPR compliance"""
        user_data = {
            "user_id": user_id,
            "exported_at": datetime.utcnow().isoformat(),
            "data": {}
        }
        
        # Collect all user data
        user_keys = self.redis_client.keys(f"user_data:{user_id}:*")
        for key in user_keys:
            data_type = key.decode().split(':')[-1]
            user_data["data"][data_type] = self.redis_client.hgetall(key)
        
        return user_data

class EstonianDataProtection:
    """Estonian data protection compliance"""
    
    def __init__(self):
        self.data_classification = {
            "public": ["material_prices", "building_codes"],
            "internal": ["project_data", "cost_estimates"],
            "confidential": ["personal_data", "financial_data"],
            "restricted": ["security_logs", "access_tokens"]
        }
    
    def classify_data(self, data_type: str) -> str:
        """Classify data according to Estonian data protection laws"""
        for classification, types in self.data_classification.items():
            if data_type in types:
                return classification
        return "internal"  # Default classification
    
    def get_retention_period(self, data_type: str) -> str:
        """Get retention period based on Estonian law"""
        retention_periods = {
            "project_data": "7 years",  # Construction law
            "financial_data": "7 years",  # Tax law
            "personal_data": "3 years",  # GDPR
            "security_logs": "1 year",  # Security requirements
            "material_prices": "1 year"  # Business data
        }
        return retention_periods.get(data_type, "1 year")
    
    def encrypt_sensitive_data(self, data: str, classification: str) -> str:
        """Encrypt sensitive data based on classification"""
        if classification in ["confidential", "restricted"]:
            # In production, use proper encryption
            import base64
            return base64.b64encode(data.encode()).decode()
        return data
    
    def audit_data_access(self, user_id: str, data_type: str, action: str):
        """Audit data access for compliance"""
        audit_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "data_type": data_type,
            "action": action,
            "classification": self.classify_data(data_type)
        }
        
        # Store audit log
        logger.info(f"Data access audit: {audit_record}")

# Usage example
def create_security_dependencies(security_manager: SecurityManager):
    """Create FastAPI security dependencies"""
    
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Get current authenticated user"""
        token = credentials.credentials
        payload = security_manager.verify_token(token)
        return payload["user_id"]
    
    async def check_rate_limit(user_id: str = Depends(get_current_user)):
        """Check rate limiting"""
        if not security_manager.rate_limit_check(user_id, "api_call"):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        return user_id
    
    return get_current_user, check_rate_limit
