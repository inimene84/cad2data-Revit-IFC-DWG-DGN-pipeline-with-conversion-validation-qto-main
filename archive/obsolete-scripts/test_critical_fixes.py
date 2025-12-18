#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Critical Fixes Test Runner
Tests the 3 critical fixes: API Versioning, Database Transactions, ACID Compliance
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def run_critical_fixes_tests():
    """Run tests for critical fixes"""
    print("\n" + "="*60)
    print("CRITICAL FIXES TESTING")
    print("="*60)
    
    project_root = Path(__file__).parent
    tests_dir = project_root / "construction-platform" / "tests"
    test_file = tests_dir / "test_critical_fixes.py"
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"\n📋 Running tests from: {test_file}")
    print("\n" + "-"*60)
    
    try:
        # Change to tests directory
        os.chdir(tests_dir.parent)
        
        # Run pytest
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                str(test_file),
                "-v",
                "--tb=short",
                "--color=yes"
            ],
            capture_output=False,
            text=True
        )
        
        print("\n" + "-"*60)
        
        if result.returncode == 0:
            print("\n✅ All critical fixes tests passed!")
            return True
        else:
            print(f"\n❌ Some tests failed (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_versioning_manual():
    """Manual test for API versioning"""
    print("\n" + "="*60)
    print("MANUAL API VERSIONING TEST")
    print("="*60)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/v1/health",
        "/v1/health/detailed",
        "/v1/analytics/cost-trends?period=30d",
        "/v1/analytics/material-breakdown?period=30d",
        "/v1/analytics/processing-metrics?period=30d",
    ]
    
    print("\nTesting v1 endpoints...")
    all_passed = True
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - {response.status_code}")
            else:
                print(f"❌ {endpoint} - {response.status_code}")
                all_passed = False
        except requests.exceptions.ConnectionError:
            print(f"⚠️  {endpoint} - Service not running (start with: docker-compose up)")
            all_passed = False
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_openapi_docs():
    """Test OpenAPI documentation"""
    print("\n" + "="*60)
    print("OPENAPI DOCUMENTATION TEST")
    print("="*60)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/openapi.json",
        "/docs",
        "/redoc",
    ]
    
    print("\nTesting OpenAPI endpoints...")
    all_passed = True
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - {response.status_code}")
            else:
                print(f"❌ {endpoint} - {response.status_code}")
                all_passed = False
        except requests.exceptions.ConnectionError:
            print(f"⚠️  {endpoint} - Service not running")
            all_passed = False
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("="*60)
    print("CRITICAL FIXES TEST SUITE")
    print("="*60)
    
    # Run pytest tests
    pytest_passed = run_critical_fixes_tests()
    
    # Run manual tests (if service is running)
    print("\n" + "="*60)
    print("MANUAL TESTS (requires running service)")
    print("="*60)
    print("\nTo run manual tests, start the service first:")
    print("  cd construction-platform")
    print("  docker-compose -f docker-compose.prod.yml up -d")
    print("\nThen run:")
    print("  python test_critical_fixes.py --manual")
    
    if "--manual" in sys.argv:
        api_passed = test_api_versioning_manual()
        openapi_passed = test_openapi_docs()
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Pytest Tests: {'✅ PASSED' if pytest_passed else '❌ FAILED'}")
        print(f"API Versioning: {'✅ PASSED' if api_passed else '❌ FAILED'}")
        print(f"OpenAPI Docs: {'✅ PASSED' if openapi_passed else '❌ FAILED'}")
        
        if pytest_passed and api_passed and openapi_passed:
            print("\n🎉 All critical fixes tests passed!")
            sys.exit(0)
        else:
            print("\n⚠️  Some tests failed. Review the output above.")
            sys.exit(1)
    else:
        if pytest_passed:
            print("\n✅ Critical fixes tests passed!")
            print("\n💡 Tip: Start the service and run with --manual flag for full testing")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Review the output above.")
            sys.exit(1)

