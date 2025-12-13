# Enhanced Error Handling
# construction-platform/python-services/api/error_handler.py

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
import traceback
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Error type enumeration"""
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
    """Enhanced error handler with user-friendly messages"""
    
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
        """Classify error type"""
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
        """Create user-friendly error response"""
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
        """Global exception handler"""
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
    """Retry strategy with exponential backoff"""
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    async def retry(self, func, *args, **kwargs):
        """Retry function with exponential backoff"""
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
