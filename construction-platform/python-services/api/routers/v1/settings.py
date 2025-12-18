# Settings Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/settings.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os

router = APIRouter(prefix="/settings", tags=["settings"])

class SettingsRequest(BaseModel):
    """Request model for settings"""
    language: Optional[str] = "en"
    region: Optional[str] = "tartu"
    enableNotifications: Optional[bool] = True
    darkMode: Optional[bool] = False
    n8nWebhookUrl: Optional[str] = None
    apiKey: Optional[str] = None
    defaultWorkflow: Optional[str] = "auto"
    includeVat: Optional[bool] = True

@router.get("")
async def get_settings():
    """Get user settings - Version 1"""
    # In a real implementation, this would fetch from database
    # For now, return default settings
    return {
        "version": "v1",
        "settings": {
            "language": "en",
            "region": "tartu",
            "enableNotifications": True,
            "darkMode": False,
            "n8nWebhookUrl": "https://n8n.srv1071801.hstgr.cloud/webhook",
            "defaultWorkflow": "auto",
            "includeVat": True
        }
    }

@router.post("")
async def save_settings(settings: SettingsRequest):
    """Save user settings - Version 1"""
    try:
        # In a real implementation, this would save to database
        # For now, we'll just return success
        # TODO: Implement database storage for user settings
        
        # Convert to dict for response
        settings_dict = settings.dict(exclude_none=True)
        
        return {
            "version": "v1",
            "status": "success",
            "message": "Settings saved successfully",
            "settings": settings_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving settings: {str(e)}")

@router.put("")
async def update_settings(settings: SettingsRequest):
    """Update user settings - Version 1"""
    # Same as POST for now
    return await save_settings(settings)


@router.get("/vat")
async def get_vat_settings():
    """Get VAT configuration for Estonia - Version 1"""
    from config import VAT_RATE, VAT_COUNTRY, VAT_LABEL
    
    return {
        "vat_rate": VAT_RATE,
        "vat_percentage": int(VAT_RATE * 100),
        "vat_country": VAT_COUNTRY,
        "vat_label": VAT_LABEL,
        "currency": "EUR"
    }

