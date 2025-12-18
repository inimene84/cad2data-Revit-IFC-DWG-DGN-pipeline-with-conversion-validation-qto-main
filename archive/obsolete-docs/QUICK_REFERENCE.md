# Quick Reference Guide

## 🚀 Quick Start

### **1. Start Services**
```bash
cd construction-platform
docker-compose -f docker-compose.prod.yml up -d
```

### **2. Health Check**
```bash
curl http://localhost:8000/health
```

### **3. Run Tests**
```bash
python run_tests.py
```

### **4. Run Load Tests**
```bash
locust -f tests/locustfile.py --host=http://localhost:8000
```

---

## 📋 Common Commands

### **Docker Compose:**
```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d

# Stop services
docker-compose -f docker-compose.prod.yml down

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f api

# Restart service
docker-compose -f docker-compose.prod.yml restart api
```

### **Testing:**
```bash
# Unit tests
pytest tests/test_api.py -v

# Integration tests
pytest tests/test_integration.py -v

# Load tests
locust -f tests/locustfile.py --host=http://localhost:8000

# All tests
python run_tests.py
```

### **API Testing:**
```bash
# Health check
curl http://localhost:8000/health

# Usage stats
curl http://localhost:8000/api/usage/stats?period=30d -H "X-Tenant-ID: test_tenant"

# Billing summary
curl http://localhost:8000/api/billing/summary -H "X-Tenant-ID: test_tenant"

# Error stats
curl http://localhost:8000/api/errors/stats?period=30d -H "X-Tenant-ID: test_tenant"
```

---

## 🔧 Configuration

### **Environment Variables:**
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/construction_ai
REDIS_HOST=redis
QDRANT_URL=http://localhost:6333
API_KEYS=key1,key2,key3
```

---

## 📊 Monitoring

### **Access Points:**
- **Grafana:** http://localhost:3001 (admin/admin)
- **Prometheus:** http://localhost:9090
- **Jaeger:** http://localhost:16686
- **Kibana:** http://localhost:5601

---

## 🎯 Key Endpoints

- `/health` - Health check
- `/metrics` - Prometheus metrics
- `/api/usage/stats` - Usage statistics
- `/api/billing/summary` - Billing summary
- `/api/errors/stats` - Error statistics
- `/api/automation/rules` - Automation rules
- `/api/backup/list` - List backups
- `/ws` - WebSocket endpoint

---

## 📝 Documentation

- `COMPLETE_PROJECT_OVERVIEW.md` - Full overview
- `PRODUCTION_DEPLOYMENT_GUIDE.md` - Deployment guide
- `TESTING_GUIDE.md` - Testing guide
- `QUICK_START_TESTING.md` - Quick testing guide

---

**For detailed information, see `COMPLETE_PROJECT_OVERVIEW.md`**

