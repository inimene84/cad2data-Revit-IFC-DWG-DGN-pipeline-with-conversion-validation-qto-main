# Cleanup & Minimal Build Guide

## 🎯 **Current Docker Status:**

Your Docker shows:
- **Images:** 6.615 GB (5.438 GB reclaimable - 82%)
- **Volumes:** 33.25 GB (33.25 GB reclaimable - 99%) ⚠️ **HUGE!**
- **Build Cache:** 17.45 GB (17.44 GB reclaimable)

**Total Reclaimable: ~56 GB!** You can free up a lot of space!

---

## 🧹 **Step 1: Clean Up Docker**

### **Safe Cleanup (Recommended):**
```powershell
# Remove unused images, containers, networks, and build cache
docker system prune -a

# Remove unused volumes (CAREFUL - this removes data!)
docker volume prune

# Or remove all unused volumes (more aggressive)
docker volume prune -a
```

### **Aggressive Cleanup (Frees Maximum Space):**
```powershell
# Remove everything unused (images, containers, volumes, networks, build cache)
docker system prune -a --volumes

# This will free ~56 GB but removes:
# - All unused images
# - All stopped containers
# - All unused volumes
# - All unused networks
# - All build cache
```

### **Check Space After Cleanup:**
```powershell
docker system df
```

---

## 🚀 **Step 2: Use Minimal Build Configuration**

I've created `docker-compose.minimal.yml` that includes only essential services (~3-5 GB):

### **Included:**
- ✅ PostgreSQL (Alpine) - ~200 MB
- ✅ Redis (Alpine) - ~50 MB  
- ✅ Qdrant - ~150 MB
- ✅ N8N - ~500-800 MB
- ✅ API - ~700-900 MB
- ✅ UI - ~400-600 MB
- ✅ **One Converter (DWG only)** - ~1-2 GB

### **Excluded (saves ~3-7 GB):**
- ❌ ELK Stack (Elasticsearch, Logstash, Kibana)
- ❌ Prometheus, Grafana, Jaeger
- ❌ Locust
- ❌ OCR & Drive services (2 more converters)

---

## 📋 **Step-by-Step Instructions:**

### **1. Clean Docker:**
```powershell
# Check current space
docker system df

# Clean up (choose one):
# Safe: Remove unused images and build cache
docker system prune -a

# Aggressive: Remove everything unused including volumes
docker system prune -a --volumes

# Check space after cleanup
docker system df
```

### **2. Build Minimal Configuration:**
```powershell
cd construction-platform

# Build minimal services
docker-compose -f docker-compose.minimal.yml build

# Start services
docker-compose -f docker-compose.minimal.yml up -d
```

### **3. Verify:**
```powershell
# Check image sizes
docker images | Sort-Object Size -Descending

# Check total space used
docker system df

# Test services
curl http://localhost:8000/v1/health
curl http://localhost:5678
```

---

## 📊 **Expected Results:**

### **After Cleanup:**
- **Freed:** ~56 GB
- **Remaining:** Your original 7.3 GB + 56 GB = **~63 GB available**

### **After Minimal Build:**
- **Used:** ~3-5 GB
- **Available:** ~58-60 GB remaining

---

## ⚠️ **Important Notes:**

### **Volume Cleanup Warning:**
The `docker volume prune` command removes **unused volumes**. This includes:
- Database data (if containers are stopped)
- Application data
- Any persistent storage

**Before running `docker volume prune`:**
1. Make sure all important containers are running
2. Or backup important data first
3. Or use `docker volume ls` to see what will be removed

### **If You Need More Services Later:**
1. **Build them separately:**
   ```powershell
   # Build OCR service when needed
   docker-compose -f docker-compose.prod.yml build ocr-service
   ```

2. **Use external services:**
   - Cloud OCR APIs
   - Cloud storage
   - Managed databases

3. **Expand Docker disk:**
   - Windows: Docker Desktop → Settings → Resources → Advanced
   - Increase disk image size

---

## ✅ **Quick Commands:**

```powershell
# 1. Clean everything
docker system prune -a --volumes

# 2. Check space
docker system df

# 3. Build minimal
cd construction-platform
docker-compose -f docker-compose.minimal.yml build

# 4. Start services
docker-compose -f docker-compose.minimal.yml up -d

# 5. Check sizes
docker images | Sort-Object Size -Descending
```

---

## 🎯 **Summary:**

1. **Clean Docker first** - You have ~56 GB of reclaimable space!
2. **Use minimal build** - Only essential services (~3-5 GB)
3. **Add services later** - Build them separately when needed

**You should have plenty of space after cleanup! 🚀**

