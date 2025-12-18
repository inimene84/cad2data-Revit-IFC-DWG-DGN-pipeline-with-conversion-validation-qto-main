#!/bin/bash
# Load Test Script
# construction-platform/tests/run_load_tests.sh

set -e

echo "Starting load tests..."

# Start Locust
locust -f tests/locustfile.py     --host=http://localhost:8000     --users=1000     --spawn-rate=10     --run-time=10m     --headless     --html=load_test_report.html     --csv=load_test_results

echo "Load tests completed!"
echo "Results saved to load_test_report.html and load_test_results.csv"
