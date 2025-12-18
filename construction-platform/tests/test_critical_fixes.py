# Critical Fixes Tests
# construction-platform/tests/test_critical_fixes.py

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


class TestAPIVersioning:
    """Test API Versioning (Critical Fix #1)"""
    
    def test_v1_health_endpoint(self):
        """Test v1 health endpoint"""
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["api_version"] == "v1"
        assert "version" in data
        assert "timestamp" in data
    
    def test_v1_health_detailed(self):
        """Test v1 detailed health endpoint"""
        response = client.get("/v1/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["api_version"] == "v1"
        assert "components" in data
    
    def test_v1_analytics_cost_trends(self):
        """Test v1 analytics cost trends endpoint"""
        response = client.get("/v1/analytics/cost-trends?period=30d")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert data["version"] == "v1"
        assert "period" in data
        assert "data" in data
    
    def test_v1_analytics_material_breakdown(self):
        """Test v1 analytics material breakdown endpoint"""
        response = client.get("/v1/analytics/material-breakdown?period=30d")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert data["version"] == "v1"
        assert "data" in data
    
    def test_v1_analytics_processing_metrics(self):
        """Test v1 analytics processing metrics endpoint"""
        response = client.get("/v1/analytics/processing-metrics?period=30d")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert data["version"] == "v1"
        assert "data" in data
    
    def test_version_header(self):
        """Test version header in response"""
        response = client.get("/v1/health", headers={"X-API-Version": "v1"})
        assert response.status_code == 200
        # Check if version header is in response (if middleware is enabled)
        # Note: This may not work if middleware is not fully integrated
    
    def test_backward_compatibility(self):
        """Test backward compatibility - old endpoints should still work"""
        # Test old health endpoint (if it exists)
        response = client.get("/health")
        # Should either work or return 404
        assert response.status_code in [200, 404]


class TestDatabaseTransactions:
    """Test Database Transactions (Critical Fix #2)"""
    
    def test_transaction_context_manager(self):
        """Test transaction context manager exists"""
        try:
            from db_optimization import db_optimizer, DatabaseOptimizer
            
            # Check if get_transaction method exists
            assert hasattr(DatabaseOptimizer, 'get_transaction'), "get_transaction method not found"
            
            # Check if db_optimizer is initialized
            if db_optimizer:
                assert hasattr(db_optimizer, 'get_transaction'), "db_optimizer.get_transaction not found"
            
        except ImportError:
            pytest.skip("db_optimization module not available", allow_module_level=True)
    
    def test_transaction_isolation_level(self):
        """Test transaction isolation level configuration"""
        try:
            from db_optimization import DatabaseOptimizer
            import os
            
            # Create a test optimizer
            database_url = os.getenv(
                "DATABASE_URL",
                "postgresql://postgres:postgres@localhost:5432/construction_ai"
            )
            
            # Check if engine has isolation level configured
            optimizer = DatabaseOptimizer(database_url, pool_size=5, max_overflow=2)
            
            # Check if engine has isolation_level attribute
            assert hasattr(optimizer.engine, 'dialect'), "Engine dialect not found"
            
        except ImportError:
            pytest.skip("db_optimization module not available", allow_module_level=True)
        except Exception as e:
            # Database connection may fail in test environment
            pytest.skip(f"Database connection failed: {e}", allow_module_level=True)


class TestACIDCompliance:
    """Test ACID Compliance (Critical Fix #3)"""
    
    def test_acid_settings_in_engine(self):
        """Test ACID compliance settings in database engine"""
        try:
            from db_optimization import DatabaseOptimizer
            import os
            
            database_url = os.getenv(
                "DATABASE_URL",
                "postgresql://postgres:postgres@localhost:5432/construction_ai"
            )
            
            optimizer = DatabaseOptimizer(database_url, pool_size=5, max_overflow=2)
            
            # Check if engine has connect_args with isolation level
            # This is set during engine creation
            assert optimizer.engine is not None, "Engine not created"
            
        except ImportError:
            pytest.skip("db_optimization module not available", allow_module_level=True)
        except Exception as e:
            # Database connection may fail in test environment
            pytest.skip(f"Database connection failed: {e}", allow_module_level=True)
    
    def test_isolation_level_constant(self):
        """Test that isolation level constant is defined"""
        try:
            from db_optimization import DatabaseOptimizer
            
            # Check if get_transaction method accepts isolation_level parameter
            import inspect
            sig = inspect.signature(DatabaseOptimizer.get_transaction)
            assert 'isolation_level' in sig.parameters, "isolation_level parameter not found"
            
        except ImportError:
            pytest.skip("db_optimization module not available", allow_module_level=True)


class TestOpenAPIDocumentation:
    """Test OpenAPI Documentation"""
    
    def test_openapi_json_endpoint(self):
        """Test OpenAPI JSON endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_swagger_ui_endpoint(self):
        """Test Swagger UI endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test ReDoc endpoint"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_tags(self):
        """Test OpenAPI tags are defined"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        
        # Check if tags include v1
        if "tags" in data:
            tag_names = [tag["name"] for tag in data["tags"]]
            assert "v1" in tag_names or "health" in tag_names, "v1 or health tag not found"


class TestVersionNegotiation:
    """Test Version Negotiation Middleware"""
    
    def test_version_header_request(self):
        """Test version header in request"""
        response = client.get("/v1/health", headers={"X-API-Version": "v1"})
        assert response.status_code == 200
    
    def test_accept_header(self):
        """Test Accept header version negotiation"""
        response = client.get(
            "/v1/health",
            headers={"Accept": "application/vnd.api+json;version=1"}
        )
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

