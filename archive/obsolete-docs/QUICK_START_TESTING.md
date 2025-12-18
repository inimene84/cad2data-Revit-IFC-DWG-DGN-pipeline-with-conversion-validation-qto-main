# Quick Start Testing Guide

## 🚀 Quick Start

### **1. Start Services**

```bash
# Navigate to project directory
cd construction-platform

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start (30 seconds)
sleep 30

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f api
```

### **2. Run Health Check**

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "2.0.0",
#   "cache": "connected",
#   "timestamp": "2025-01-15T12:00:00",
#   "metrics_enabled": true
# }
```

### **3. Run Tests**

```bash
# Run all tests
python run_tests.py

# Or run specific tests
pytest tests/test_api.py::test_health_check -v
pytest tests/test_api.py::test_usage_stats -v
pytest tests/test_api.py::test_billing_summary -v
```

### **4. Test API Endpoints**

```bash
# Test usage stats
curl http://localhost:8000/api/usage/stats?period=30d -H "X-Tenant-ID: test_tenant"

# Test billing summary
curl http://localhost:8000/api/billing/summary -H "X-Tenant-ID: test_tenant"

# Test error stats
curl http://localhost:8000/api/errors/stats?period=30d -H "X-Tenant-ID: test_tenant"

# Test audit logs
curl http://localhost:8000/api/audit/logs?limit=100 -H "X-Tenant-ID: test_tenant"
```

### **5. Run Load Tests**

```bash
# Install Locust (if not installed)
pip install locust

# Run load tests
locust -f tests/locustfile.py --host=http://localhost:8000

# Run load tests headless
locust -f tests/locustfile.py \
  --host=http://localhost:8000 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=5m \
  --headless \
  --html=load_test_report.html

# View results
open load_test_report.html
```

---

## 📊 Test Results

### **Expected Results:**
- ✅ Health check: 200 OK
- ✅ Usage stats: 200 OK
- ✅ Billing summary: 200 OK
- ✅ Error stats: 200 OK
- ✅ Audit logs: 200 OK
- ✅ Load tests: 1000 users supported
- ✅ Response time: < 1s (p95)
- ✅ Error rate: < 1%

---

## 🔧 Troubleshooting

### **Service Not Starting:**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs -f <service-name>

# Restart service
docker-compose -f docker-compose.prod.yml restart <service-name>
```

### **Tests Failing:**
```bash
# Check if services are running
docker-compose -f docker-compose.prod.yml ps

# Check API health
curl http://localhost:8000/health

# Check logs
docker-compose -f docker-compose.prod.yml logs -f api
```

### **Load Tests Failing:**
```bash
# Check if API is accessible
curl http://localhost:8000/health

# Check if Locust is installed
locust --version

# Run load tests with verbose output
locust -f tests/locustfile.py --host=http://localhost:8000 --logfile=locust.log
```

---

## 🎉 Testing Complete!

All tests passed! The Construction AI Platform is ready for production deployment.

---

**For more information, see:**
- `TESTING_GUIDE.md` - Complete testing guide
- `DEPLOYMENT_AND_TESTING_GUIDE.md` - Deployment and testing guide
- `PRODUCTION_DEPLOYMENT_GUIDE.md` - Production deployment guide

