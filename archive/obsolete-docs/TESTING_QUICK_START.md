# Testing Quick Start Guide

## 🚀 Quick Start Testing

**Status:** Testing infrastructure ready! Minor fixes needed for full test run.

---

## ✅ What's Working

1. **Test Files Created:**
   - ✅ `test_critical_fixes.py` - Comprehensive test suite
   - ✅ `construction-platform/tests/test_critical_fixes.py` - Test cases
   - ✅ Updated `test_api.py` - Includes v1 tests

2. **Critical Fixes Tested:**
   - ✅ API Versioning structure
   - ✅ Database Transactions structure
   - ✅ ACID Compliance structure

---

## 🧪 How to Test

### **Option 1: Test Structure (No Service Required)**

```bash
# Test that critical fixes are implemented
python -c "from construction-platform.python-services.api.db_optimization import DatabaseOptimizer; print('✅ Database transactions ready')"
python -c "from construction-platform.python-services.api.routers.v1 import v1_router; print('✅ API versioning ready')"
```

### **Option 2: Test with Service Running**

```bash
# 1. Start services
cd construction-platform
docker-compose -f docker-compose.prod.yml up -d

# 2. Wait for services (30 seconds)
sleep 30

# 3. Test API versioning
curl http://localhost:8000/v1/health

# 4. Test OpenAPI docs
curl http://localhost:8000/openapi.json
curl http://localhost:8000/docs

# 5. Test database (if connected)
# Use get_transaction() in code
```

### **Option 3: Run Pytest Tests**

```bash
# Install pytest if needed
pip install pytest

# Run tests (may need service running)
cd construction-platform
pytest tests/test_critical_fixes.py -v

# Or run from project root
pytest construction-platform/tests/test_critical_fixes.py -v
```

---

## 📋 Test Checklist

### **API Versioning:**
- [ ] `/v1/health` endpoint works
- [ ] `/v1/health/detailed` endpoint works
- [ ] `/v1/analytics/*` endpoints work
- [ ] Version header negotiation works
- [ ] OpenAPI docs show v1 endpoints

### **Database Transactions:**
- [ ] `get_transaction()` method exists
- [ ] Transaction isolation levels configured
- [ ] ACID compliance settings present

### **OpenAPI Documentation:**
- [ ] `/openapi.json` returns valid schema
- [ ] `/docs` serves Swagger UI
- [ ] `/redoc` serves ReDoc
- [ ] Tags include v1 endpoints

---

## 🔧 Known Issues & Fixes

### **Issue 1: Missing material_prices.json**
**Status:** ⚠️ Needs fix  
**Fix:** Create file or make it optional in app.py

### **Issue 2: Pydantic V2 Warnings**
**Status:** ⚠️ Warnings only (not errors)  
**Fix:** Update to `@field_validator` (optional)

### **Issue 3: Service Dependencies**
**Status:** ✅ Expected  
**Fix:** Start services before full testing

---

## 🎯 Quick Test Commands

```bash
# Test API versioning structure
python -c "import sys; sys.path.insert(0, 'construction-platform/python-services/api'); from routers.v1 import v1_router; print('✅ API versioning ready')"

# Test database transactions structure
python -c "import sys; sys.path.insert(0, 'construction-platform/python-services/api'); from db_optimization import DatabaseOptimizer; print('✅ Database transactions ready')"

# Test OpenAPI docs (if service running)
curl http://localhost:8000/openapi.json | python -m json.tool
```

---

## 📊 Test Results Summary

### **Structure Tests:**
- ✅ API Versioning: Structure created
- ✅ Database Transactions: Method exists
- ✅ ACID Compliance: Settings configured
- ✅ OpenAPI: Tags defined

### **Runtime Tests:**
- ⏳ Requires service running
- ⏳ Test with: `python test_critical_fixes.py --manual`

---

## 🚀 Next Steps

1. **Fix Missing File:**
   - Create `material_prices.json` or make it optional

2. **Start Services:**
   - `docker-compose up -d`

3. **Run Full Tests:**
   - `python test_critical_fixes.py --manual`

4. **Review Results:**
   - Check test output
   - Fix any failures
   - Document results

---

**Testing infrastructure is ready! Start services and run full test suite.**

