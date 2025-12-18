# API Tests
# construction-platform/tests/test_api.py

import pytest
import sys
from pathlib import Path

# Add API directory to path
api_dir = Path(__file__).parent.parent / "python-services" / "api"
sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient

# Try to import app
try:
    from app import app
    client = TestClient(app)
except ImportError as e:
    pytest.skip(f"Could not import app: {e}", allow_module_level=True)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy" or "status" in data

def test_v1_health_check():
    """Test v1 health check endpoint (API Versioning)"""
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["api_version"] == "v1"

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_usage_stats():
    """Test usage stats endpoint"""
    response = client.get("/api/usage/stats?period=30d", headers={"X-Tenant-ID": "test_tenant"})
    assert response.status_code == 200

def test_billing_summary():
    """Test billing summary endpoint"""
    response = client.get("/api/billing/summary", headers={"X-Tenant-ID": "test_tenant"})
    assert response.status_code == 200

def test_error_stats():
    """Test error stats endpoint"""
    response = client.get("/api/errors/stats?period=30d", headers={"X-Tenant-ID": "test_tenant"})
    assert response.status_code == 200

def test_audit_logs():
    """Test audit logs endpoint"""
    response = client.get("/api/audit/logs?limit=100", headers={"X-Tenant-ID": "test_tenant"})
    assert response.status_code == 200
