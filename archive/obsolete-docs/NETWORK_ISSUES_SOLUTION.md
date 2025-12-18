# Network Issues - Solutions

## ⚠️ **Problem:**
Network/DNS resolution failures:
- `npm registry.npmjs.org` - DNS lookup failure (EAI_AGAIN)
- `auth.docker.io` - DNS lookup failure
- Services can't start because builds failed

## 🔍 **Diagnosis:**

This is a **DNS/network connectivity issue**, not a Docker configuration problem.

---

## ✅ **Solutions:**

### **Solution 1: Check Internet Connection**

```powershell
# Test connectivity
Test-NetConnection -ComputerName google.com -Port 80
Test-NetConnection -ComputerName registry.npmjs.org -Port 443
Test-NetConnection -ComputerName auth.docker.io -Port 443

# Check DNS
nslookup registry.npmjs.org
nslookup auth.docker.io
```

### **Solution 2: Fix DNS Settings**

#### **Windows DNS:**
1. Open **Network Settings**
2. Change DNS to:
   - **Primary:** `8.8.8.8` (Google)
   - **Secondary:** `1.1.1.1` (Cloudflare)

#### **Docker Desktop DNS:**
1. Open **Docker Desktop**
2. Go to **Settings** → **Resources** → **Network**
3. Set DNS to: `8.8.8.8,1.1.1.1`

### **Solution 3: Use Pre-built Images (If Available)**

If you have pre-built images or can use public images:

```powershell
# Pull pre-built images instead of building
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull qdrant/qdrant:latest
docker pull n8nio/n8n:latest

# Then use them directly in docker-compose
```

### **Solution 4: Build Later When Network is Stable**

Network issues are often temporary. You can:

1. **Wait and retry** (network issues often resolve themselves)
2. **Try at different times** (off-peak hours)
3. **Use mobile hotspot** (if available) to test if it's your network

### **Solution 5: Build Services That Don't Need Network**

Some services use pre-built images and don't need network during build:

```powershell
# These use pre-built images (no build needed)
docker-compose -f docker-compose.minimal.yml up -d postgres redis qdrant

# Check if they start
docker-compose -f docker-compose.minimal.yml ps
```

---

## 🚀 **Immediate Workaround:**

### **Step 1: Start Services That Use Pre-built Images**

```powershell
# These don't need building - they use pre-built images
docker-compose -f docker-compose.minimal.yml up -d postgres redis qdrant

# Check status
docker-compose -f docker-compose.minimal.yml ps
```

### **Step 2: Check What's Already Built**

```powershell
# Check built images
docker images | Select-String "construction-platform"

# If n8n is built, start it
docker-compose -f docker-compose.minimal.yml up -d n8n
```

### **Step 3: Build API/UI When Network is Stable**

Once network is working:

```powershell
# Build API (needs network for Python packages)
docker-compose -f docker-compose.minimal.yml build api

# Build UI (needs network for npm packages)
docker-compose -f docker-compose.minimal.yml build ui

# Start them
docker-compose -f docker-compose.minimal.yml up -d api ui
```

---

## 🔧 **Network Troubleshooting Commands:**

```powershell
# 1. Flush DNS cache
ipconfig /flushdns

# 2. Restart Docker Desktop
# (Close and reopen Docker Desktop)

# 3. Check Docker network
docker network ls
docker network inspect construction-platform_construction-network

# 4. Test from inside a container
docker run --rm alpine ping -c 3 8.8.8.8
docker run --rm alpine nslookup registry.npmjs.org
```

---

## 📋 **Quick Checklist:**

- [ ] Check internet connection
- [ ] Test DNS resolution
- [ ] Change DNS to 8.8.8.8 / 1.1.1.1
- [ ] Restart Docker Desktop
- [ ] Start services that use pre-built images (postgres, redis, qdrant)
- [ ] Build API/UI when network is stable

---

## 🎯 **Recommended Approach:**

1. **Fix DNS first** (most common issue)
2. **Start database services** (they use pre-built images)
3. **Wait for network stability** before building API/UI
4. **Build services one at a time** to avoid timeouts

---

**Network issues are usually temporary. Fix DNS settings and try again! 🚀**

