# Automation Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/automation.py
# Workflow automation status and control

from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter(prefix="/automation", tags=["automation"])

N8N_URL = os.getenv("N8N_URL", "http://n8n:5678")


@router.get("/status")
async def get_automation_status():
    """Get automation system status"""
    n8n_status = "unknown"
    
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{N8N_URL}/healthz")
            n8n_status = "connected" if response.status_code == 200 else "error"
    except Exception:
        n8n_status = "disconnected"
    
    return {
        "status": "operational",
        "n8n_url": N8N_URL,
        "n8n_status": n8n_status,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/workflows")
async def list_workflows():
    """List available automation workflows"""
    # Predefined workflows
    workflows = [
        {
            "id": "construction-cost-estimation",
            "name": "Construction Cost Estimation",
            "description": "Process construction documents and estimate costs using DDC CWICR database",
            "status": "active",
            "triggers": ["file_upload", "api_call"]
        },
        {
            "id": "material-extraction",
            "name": "Material Extraction",
            "description": "Extract materials from PDF and Excel files",
            "status": "active",
            "triggers": ["file_upload"]
        },
        {
            "id": "report-generation",
            "name": "Report Generation",
            "description": "Generate cost estimate reports in PDF format",
            "status": "active",
            "triggers": ["api_call"]
        }
    ]
    
    return {
        "total_workflows": len(workflows),
        "workflows": workflows
    }
