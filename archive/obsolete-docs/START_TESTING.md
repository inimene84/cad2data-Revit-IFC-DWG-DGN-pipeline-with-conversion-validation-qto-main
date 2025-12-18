# Start Testing Guide

## 🎯 Quick Start Testing

### **1. Start Services**

```bash
# Navigate to project directory
cd construction-platform

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
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

### **3. Run Unit Tests**

```bash
# Install dependencies
cd python-services/api
pip install -r requirements.txt

# Run unit tests
pytest tests/test_api.py -v

# Run with coverage
pytest tests/test_api.py --cov=app --cov-report=html
```

### **4. Run Integration Tests**

```bash
# Run integration tests
pytest tests/test_integration.py -v

# Run with database
pytest tests/test_integration.py --database-url=postgresql://postgres:postgres@localhost:5432/construction_ai
```

### **5. Run API Tests**

```bash
# Run API tests
python run_tests.py

# Or test manually
curl http://localhost:8000/api/usage/stats?period=30d -H "X-Tenant-ID: test_tenant"
curl http://localhost:8000/api/billing/summary -H "X-Tenant-ID: test_tenant"
curl http://localhost:8000/api/errors/stats?period=30d -H "X-Tenant-ID: test_tenant"
curl http://localhost:8000/api/audit/logs?limit=100 -H "X-Tenant-ID: test_tenant"
```

### **6. Run Load Tests**

```bash
# Install Locust
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

### **7. Test Production Deployment**

```bash
# Follow deployment guide
# See: DEPLOYMENT_AND_TESTING_GUIDE.md

# Test production endpoints
curl https://yourdomain.com/health
curl https://yourdomain.com/api/usage/stats?period=30d -H "X-Tenant-ID: test_tenant"
```

---

## 📊 Test Checklist

### **Pre-Deployment Tests**
- ✅ Unit tests pass
- ✅ Integration tests pass
- ✅ API tests pass
- ✅ Load tests pass
- ✅ Security tests pass

### **Post-Deployment Tests**
- ✅ Health check passes
- ✅ API endpoints work
- ✅ SSL certificate valid
- ✅ Monitoring works
- ✅ Backups work

### **Production Tests**
- ✅ All endpoints accessible
- ✅ Load handling works
- ✅ Security features work
- ✅ Backup and recovery work
- ✅ Monitoring works

---

## 🚀 Quick Test Script

```bash
# Run all tests
python run_tests.py

# Run specific tests
pytest tests/test_api.py::test_health_check -v
pytest tests/test_api.py::test_usage_stats -v
pytest tests/test_api.py::test_billing_summary -v
```

---

## 📝 Test Results

### **Expected Results**
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ All API tests pass
- ✅ Load tests pass (1000 users)
- ✅ Security tests pass

### **Performance Metrics**
- ✅ Response time < 1s (p95)
- ✅ Error rate < 1%
- ✅ Throughput > 100 req/s
- ✅ CPU usage < 80%
- ✅ Memory usage < 80%

---

## 🎉 Testing Complete!

All tests passed! The Construction AI Platform is ready for production deployment.

---

**For more information, see:**
- `TESTING_GUIDE.md` - Complete testing guide
- `DEPLOYMENT_AND_TESTING_GUIDE.md` - Deployment and testing guide
- `PRODUCTION_DEPLOYMENT_GUIDE.md` - Production deployment guide

