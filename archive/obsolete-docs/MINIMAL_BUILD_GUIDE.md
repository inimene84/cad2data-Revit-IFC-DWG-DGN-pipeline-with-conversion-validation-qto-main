# Minimal Build Guide for 7.3 GB Docker Space

## ⚠️ **Problem:**
Your Docker has only **7.3 GB** of free space, but the full build is estimated at **7-12 GB**.

## ✅ **Solution: Minimal Build Configuration**

I've created `docker-compose.minimal.yml` that includes only essential services:

### **Included Services (~4-5 GB):**
- ✅ PostgreSQL (Alpine) - ~200 MB
- ✅ Redis (Alpine) - ~50 MB
- ✅ Qdrant - ~150 MB
- ✅ N8N - ~500-800 MB
- ✅ API - ~700-900 MB
- ✅ UI - ~400-600 MB
- ✅ **One Converter Service (DWG only)** - ~1-2 GB

### **Excluded Services (~3-7 GB saved):**
- ❌ ELK Stack (Elasticsearch, Logstash, Kibana) - ~1.3-2.1 GB
- ❌ Prometheus - ~100-200 MB
- ❌ Grafana - ~200-300 MB
- ❌ Jaeger - ~100-200 MB
- ❌ Locust - ~100-200 MB
- ❌ OCR Service - ~1-2 GB
- ❌ Drive Service - ~1-2 GB
- ❌ Nginx - ~25 MB

---

## 🚀 **Quick Start:**

### **1. Clean Docker First:**
```powershell
# Remove unused images, containers, and volumes
docker system prune -a --volumes

# Check available space
docker system df
```

### **2. Build Minimal Configuration:**
```powershell
cd construction-platform

# Build only essential services
docker-compose -f docker-compose.minimal.yml build

# Start services
docker-compose -f docker-compose.minimal.yml up -d
```

### **3. Check Space Usage:**
```powershell
# After build, check actual sizes
docker images | Sort-Object Size -Descending
docker system df
```

---

## 📊 **Expected Sizes (Minimal Build):**

| Service | Estimated Size |
|---------|----------------|
| PostgreSQL (Alpine) | ~200 MB |
| Redis (Alpine) | ~50 MB |
| Qdrant | ~150 MB |
| N8N | ~500-800 MB |
| API | ~700-900 MB |
| UI | ~400-600 MB |
| DWG Converter | ~1-2 GB |
| **TOTAL** | **~3-5 GB** |

---

## 🔧 **Additional Space-Saving Tips:**

### **1. Use Alpine Base Images** ✅ (Already in minimal config)
- PostgreSQL: `postgres:15-alpine` (smaller)
- Redis: `redis:7-alpine` (smaller)

### **2. Build Services Selectively:**
```powershell
# Build only what you need, one at a time
docker-compose -f docker-compose.minimal.yml build api
docker-compose -f docker-compose.minimal.yml build ui
docker-compose -f docker-compose.minimal.yml build n8n
# etc.
```

### **3. Remove Unused Images After Build:**
```powershell
# Remove dangling images
docker image prune -a

# Remove build cache (frees space but slows future builds)
docker builder prune -a
```

### **4. Use Docker BuildKit Cache:**
```powershell
# Set environment variable for better caching
$env:DOCKER_BUILDKIT=1
$env:COMPOSE_DOCKER_CLI_BUILD=1

# Then build
docker-compose -f docker-compose.minimal.yml build
```

---

## 🎯 **If You Need More Services Later:**

### **Option 1: Build Converter Services Separately**
```powershell
# Build OCR service only when needed
docker-compose -f docker-compose.prod.yml build ocr-service

# Use it temporarily, then remove
docker-compose -f docker-compose.prod.yml up ocr-service
# ... use it ...
docker-compose -f docker-compose.prod.yml down ocr-service
docker rmi construction-ocr-service
```

### **Option 2: Use External Services**
- Use cloud-based OCR services instead of local OCR service
- Use cloud storage instead of local Drive service
- Use managed databases (if available)

### **Option 3: Expand Docker Disk Space**
- **Windows:** Docker Desktop → Settings → Resources → Advanced → Increase disk image size
- **Linux:** Resize Docker's disk allocation

---

## 📝 **Monitoring Without ELK:**

Since ELK is excluded, you can:
1. Use API logs directly: `docker-compose logs -f api`
2. Use N8N built-in monitoring (if enabled)
3. Add lightweight monitoring later (e.g., Prometheus only, ~100 MB)

---

## ✅ **Checklist:**

- [ ] Clean Docker: `docker system prune -a --volumes`
- [ ] Check space: `docker system df`
- [ ] Build minimal: `docker-compose -f docker-compose.minimal.yml build`
- [ ] Verify sizes: `docker images`
- [ ] Start services: `docker-compose -f docker-compose.minimal.yml up -d`
- [ ] Test: `curl http://localhost:8000/v1/health`

---

## 🆘 **If Still Not Enough Space:**

1. **Remove old Docker images:**
   ```powershell
   docker images
   docker rmi <old-image-id>
   ```

2. **Remove unused volumes:**
   ```powershell
   docker volume ls
   docker volume rm <volume-name>
   ```

3. **Build only one service at a time:**
   ```powershell
   docker-compose -f docker-compose.minimal.yml build api
   docker-compose -f docker-compose.minimal.yml build ui
   # etc.
   ```

4. **Consider removing converter service temporarily:**
   - Comment out `dwg-service` in `docker-compose.minimal.yml`
   - Saves ~1-2 GB
   - You can add it back later when you have more space

---

**The minimal build should fit in 7.3 GB! 🚀**

