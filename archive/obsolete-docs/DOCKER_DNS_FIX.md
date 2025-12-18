# Docker DNS Fix Guide

## 🔍 **Issue:**
- ✅ Host can connect to npm/Docker registries
- ❌ Docker builds failing with DNS errors
- **Cause:** Docker Desktop has separate DNS settings

## ✅ **Solution: Fix Docker Desktop DNS**

### **Step 1: Update Docker Desktop DNS Settings**

1. **Open Docker Desktop**
2. Go to **Settings** (gear icon)
3. Navigate to **Resources** → **Network**
4. Set **DNS servers** to:
   ```
   8.8.8.8
   1.1.1.1
   ```
5. Click **Apply & Restart**

### **Step 2: Restart Docker Desktop**

1. Right-click Docker Desktop icon in system tray
2. Select **Quit Docker Desktop**
3. Wait 10 seconds
4. Restart Docker Desktop

### **Step 3: Flush DNS Cache**

```powershell
# Flush Windows DNS cache
ipconfig /flushdns

# Restart Docker Desktop network
# (Docker Desktop restart does this automatically)
```

---

## 🚀 **Alternative: Use Docker Daemon DNS Config**

If Docker Desktop settings don't work, edit Docker daemon config:

### **Windows (Docker Desktop):**
1. Open Docker Desktop
2. Settings → **Docker Engine**
3. Add DNS configuration:
   ```json
   {
     "dns": ["8.8.8.8", "1.1.1.1"]
   }
   ```
4. Click **Apply & Restart**

---

## 📋 **Quick Fix Commands:**

```powershell
# 1. Check current Docker DNS
docker run --rm alpine cat /etc/resolv.conf

# 2. Test DNS from inside container
docker run --rm alpine nslookup registry.npmjs.org

# 3. If DNS fails, restart Docker Desktop
# (Close and reopen Docker Desktop)

# 4. After restart, test again
docker run --rm alpine nslookup registry.npmjs.org
```

---

## 🎯 **Current Status:**

### **What's Working:**
- ✅ N8N image built (construction-platform-n8n)
- ✅ Host network connectivity
- ✅ Pre-built images available (postgres, redis, qdrant)

### **What Needs Network:**
- ⚠️ API build (needs Python packages from PyPI)
- ⚠️ UI build (needs npm packages)

---

## 🚀 **Immediate Actions:**

### **1. Start Available Services:**
```powershell
# Start services that don't need building
docker-compose -f docker-compose.minimal.yml up -d postgres redis qdrant n8n

# Check status
docker-compose -f docker-compose.minimal.yml ps
```

### **2. Fix Docker DNS:**
- Update Docker Desktop DNS settings (8.8.8.8, 1.1.1.1)
- Restart Docker Desktop

### **3. Retry Builds:**
```powershell
# After DNS fix, retry builds
docker-compose -f docker-compose.minimal.yml build api
docker-compose -f docker-compose.minimal.yml build ui
```

---

## 🔧 **If DNS Fix Doesn't Work:**

### **Option 1: Use VPN/Proxy**
If you're behind a corporate firewall:
- Configure Docker Desktop to use proxy
- Or use VPN

### **Option 2: Build Offline**
- Download packages manually
- Use local package cache
- Build from local sources

### **Option 3: Use Pre-built Images**
- Use public images from Docker Hub
- Build custom images on a machine with better network
- Transfer images to this machine

---

## ✅ **Checklist:**

- [ ] Update Docker Desktop DNS (8.8.8.8, 1.1.1.1)
- [ ] Restart Docker Desktop
- [ ] Flush DNS cache (`ipconfig /flushdns`)
- [ ] Test DNS from container (`docker run --rm alpine nslookup registry.npmjs.org`)
- [ ] Start available services (postgres, redis, qdrant, n8n)
- [ ] Retry API/UI builds after DNS fix

---

**Fix Docker Desktop DNS settings and restart - this should resolve the issue! 🚀**

