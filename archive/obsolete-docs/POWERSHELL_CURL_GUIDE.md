# PowerShell curl Command Guide

## ⚠️ **Issue:**
In PowerShell, `curl` is an alias for `Invoke-WebRequest`, which has different syntax than Linux `curl`.

## ✅ **Solutions:**

### **Option 1: Use Invoke-WebRequest (PowerShell Native)**

```powershell
# Test API
Invoke-WebRequest -Uri "http://localhost:8000/v1/health" -UseBasicParsing

# Test UI
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing

# Test N8N
Invoke-WebRequest -Uri "http://localhost:5678" -UseBasicParsing
```

### **Option 2: Use curl.exe (Windows curl)**

```powershell
# Use curl.exe explicitly
curl.exe http://localhost:8000/v1/health
curl.exe http://localhost:3000
curl.exe http://localhost:5678
```

### **Option 3: Use Test Script**

I've created `TEST_SERVICES.ps1` - run it:

```powershell
cd construction-platform
.\TEST_SERVICES.ps1
```

### **Option 4: Separate Commands**

PowerShell requires commands on separate lines:

```powershell
# Correct way:
Invoke-WebRequest -Uri "http://localhost:8000/v1/health" -UseBasicParsing
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing

# Or use semicolon:
Invoke-WebRequest -Uri "http://localhost:8000/v1/health" -UseBasicParsing; Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
```

---

## 📋 **Quick Test Commands:**

```powershell
# Test API
$response = Invoke-WebRequest -Uri "http://localhost:8000/v1/health" -UseBasicParsing
$response.Content

# Test UI
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing

# Test N8N
Invoke-WebRequest -Uri "http://localhost:5678" -UseBasicParsing

# Test Qdrant
Invoke-WebRequest -Uri "http://localhost:6333/health" -UseBasicParsing
```

---

## 🎯 **Check Service Status:**

```powershell
# Check Docker containers
cd construction-platform
docker-compose -f docker-compose.minimal.yml ps

# Or use docker directly
docker ps --filter "name=construction"
```

---

**Use `Invoke-WebRequest` or `curl.exe` for testing in PowerShell! 🚀**

