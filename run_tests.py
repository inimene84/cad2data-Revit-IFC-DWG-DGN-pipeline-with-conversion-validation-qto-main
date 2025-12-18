#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Runner Script
Runs all tests for the Construction AI Platform
"""

import os
import sys
import subprocess
import pytest
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class TestRunner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.api = self.project_root / "construction-platform" / "python-services" / "api"
        self.tests = self.project_root / "construction-platform" / "tests"
        
    def run_unit_tests(self):
        """Run unit tests"""
        print("\n" + "="*60)
        print("Running Unit Tests")
        print("="*60)
        
        try:
            # Change to API directory
            os.chdir(self.api)
            
            # Run pytest
            result = subprocess.run(
                ["pytest", "../tests/test_api.py", "-v", "--tb=short"],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error running unit tests: {e}")
            return False
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("\n" + "="*60)
        print("Running Integration Tests")
        print("="*60)
        
        try:
            # Change to API directory
            os.chdir(self.api)
            
            # Run pytest
            result = subprocess.run(
                ["pytest", "../tests/test_integration.py", "-v", "--tb=short"],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error running integration tests: {e}")
            return False
    
    def run_load_tests(self):
        """Run load tests"""
        print("\n" + "="*60)
        print("Running Load Tests")
        print("="*60)
        
        try:
            # Change to tests directory
            os.chdir(self.tests)
            
            # Run Locust
            result = subprocess.run(
                ["locust", "-f", "locustfile.py", "--host=http://localhost:8000", "--users=100", "--spawn-rate=10", "--run-time=5m", "--headless", "--html=load_test_report.html"],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error running load tests: {e}")
            return False
    
    def run_health_check(self):
        """Run health check"""
        print("\n" + "="*60)
        print("Running Health Check")
        print("="*60)
        
        try:
            import requests
            
            # Check health endpoint
            response = requests.get("http://localhost:8000/health", timeout=5)
            
            if response.status_code == 200:
                print("✓ Health check passed")
                print(f"Status: {response.json()}")
                return True
            else:
                print(f"✗ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Health check failed: {e}")
            return False
    
    def run_api_tests(self):
        """Run API tests"""
        print("\n" + "="*60)
        print("Running API Tests")
        print("="*60)
        
        try:
            import requests
            
            # Test endpoints
            endpoints = [
                ("/health", "GET"),
                ("/api/usage/stats?period=30d", "GET"),
                ("/api/billing/summary", "GET"),
                ("/api/errors/stats?period=30d", "GET"),
                ("/api/audit/logs?limit=100", "GET"),
            ]
            
            headers = {"X-Tenant-ID": "test_tenant"}
            base_url = "http://localhost:8000"
            
            passed = 0
            failed = 0
            
            for endpoint, method in endpoints:
                try:
                    url = f"{base_url}{endpoint}"
                    if method == "GET":
                        response = requests.get(url, headers=headers, timeout=5)
                    else:
                        response = requests.post(url, headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        print(f"✓ {method} {endpoint} - OK")
                        passed += 1
                    else:
                        print(f"✗ {method} {endpoint} - Failed: {response.status_code}")
                        failed += 1
                except Exception as e:
                    print(f"✗ {method} {endpoint} - Error: {e}")
                    failed += 1
            
            print(f"\nResults: {passed} passed, {failed} failed")
            return failed == 0
        except Exception as e:
            print(f"Error running API tests: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*60)
        print("Running All Tests")
        print("="*60)
        
        results = {
            "unit_tests": False,
            "integration_tests": False,
            "load_tests": False,
            "health_check": False,
            "api_tests": False
        }
        
        # Run health check first
        results["health_check"] = self.run_health_check()
        
        if not results["health_check"]:
            print("\n⚠ Health check failed. Skipping other tests.")
            return results
        
        # Run unit tests
        results["unit_tests"] = self.run_unit_tests()
        
        # Run integration tests
        results["integration_tests"] = self.run_integration_tests()
        
        # Run API tests
        results["api_tests"] = self.run_api_tests()
        
        # Run load tests (optional)
        # results["load_tests"] = self.run_load_tests()
        
        # Print summary
        print("\n" + "="*60)
        print("Test Results Summary")
        print("="*60)
        
        for test_name, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name}: {status}")
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r)
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal: {total_tests} tests")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        
        return all(results.values())

if __name__ == "__main__":
    project_root = Path(__file__).parent
    runner = TestRunner(project_root)
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)

