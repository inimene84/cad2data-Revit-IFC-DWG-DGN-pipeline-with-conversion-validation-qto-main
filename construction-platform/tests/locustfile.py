# Load Testing with Locust
# construction-platform/tests/locustfile.py

from locust import HttpUser, task, between
import json
import random

class ConstructionAIUser(HttpUser):
    """Load test user for Construction AI Platform"""
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        self.tenant_id = f"test_tenant_{random.randint(1, 100)}"
        self.headers = {
            "X-Tenant-ID": self.tenant_id,
            "Content-Type": "application/json"
        }
    
    @task(3)
    def health_check(self):
        """Health check endpoint"""
        self.client.get("/health", headers=self.headers)
    
    @task(2)
    def get_usage_stats(self):
        """Get usage statistics"""
        self.client.get("/api/usage/stats?period=30d", headers=self.headers)
    
    @task(2)
    def get_billing_summary(self):
        """Get billing summary"""
        self.client.get("/api/billing/summary", headers=self.headers)
    
    @task(1)
    def get_error_stats(self):
        """Get error statistics"""
        self.client.get("/api/errors/stats?period=30d", headers=self.headers)
    
    @task(1)
    def get_audit_logs(self):
        """Get audit logs"""
        self.client.get("/api/audit/logs?limit=100", headers=self.headers)
    
    @task(1)
    def get_cost_trends(self):
        """Get cost trends"""
        self.client.get("/api/analytics/cost-trends?period=30d", headers=self.headers)
    
    @task(1)
    def get_material_breakdown(self):
        """Get material breakdown"""
        self.client.get("/api/analytics/material-breakdown?period=30d", headers=self.headers)
    
    @task(1)
    def get_processing_metrics(self):
        """Get processing metrics"""
        self.client.get("/api/analytics/processing-metrics?period=30d", headers=self.headers)

class HighLoadUser(HttpUser):
    """High load test user"""
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    def on_start(self):
        """Called when a user starts"""
        self.tenant_id = f"load_tenant_{random.randint(1, 10)}"
        self.headers = {
            "X-Tenant-ID": self.tenant_id,
            "Content-Type": "application/json"
        }
    
    @task(10)
    def health_check(self):
        """Health check endpoint"""
        self.client.get("/health", headers=self.headers)
    
    @task(5)
    def get_usage_stats(self):
        """Get usage statistics"""
        self.client.get("/api/usage/stats?period=7d", headers=self.headers)
