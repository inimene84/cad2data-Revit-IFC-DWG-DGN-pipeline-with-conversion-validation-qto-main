# Network Build Issues - Fix Guide

## ⚠️ **Problem:**
Network resolution failures during Docker build:
- Ubuntu package repositories timing out
- Large build context (1.26 GB) taking too long
- Converter service failing to install Wine

## ✅ **Fixes Applied:**

### **1. Added Retry Logic to Converter Dockerfile**
Updated `Dockerfile.converter` to retry up to 5 times with 10-second delays.

### **2. Build Options:**

---

## 🚀 **Option 1: Skip Converter Service (Recommended for Now)**

The converter service is the largest (~1-2 GB) and most problematic. You can skip it and add it later:

```powershell
# Build without converter service
docker-compose -f docker-compose.minimal.yml build postgres redis qdrant n8n api ui

# Start services (without converter)
docker-compose -f docker-compose.minimal.yml up -d postgres redis qdrant n8n api ui
```

**Then add converter later when network is stable:**
```powershell
docker-compose -f docker-compose.minimal.yml build dwg-service
docker-compose -f docker-compose.minimal.yml up -d dwg-service
```

---

## 🚀 **Option 2: Build Services One at a Time**

Build services individually to avoid network issues affecting all builds:

```powershell
# 1. Build databases first (small, fast)
docker-compose -f docker-compose.minimal.yml build postgres redis qdrant

# 2. Build application services
docker-compose -f docker-compose.minimal.yml build n8n
docker-compose -f docker-compose.minimal.yml build api
docker-compose -f docker-compose.minimal.yml build ui

# 3. Build converter last (when network is stable)
docker-compose -f docker-compose.minimal.yml build dwg-service
```

---

## 🚀 **Option 3: Retry Converter Build**

The converter Dockerfile now has retry logic. Try building it again:

```powershell
# Build converter with retry logic
docker-compose -f docker-compose.minimal.yml build dwg-service
```

If it still fails, wait a few minutes and try again (network issues are often temporary).

---

## 🚀 **Option 4: Use Pre-built Base Image**

If network issues persist, you can manually pull the base image first:

```powershell
# Pull base image first
docker pull ubuntu:22.04

# Then build converter
docker-compose -f docker-compose.minimal.yml build dwg-service
```

---

## 📋 **Recommended Approach:**

### **Step 1: Build Core Services First**
```powershell
# Build everything except converter
docker-compose -f docker-compose.minimal.yml build postgres redis qdrant n8n api ui

# Start core services
docker-compose -f docker-compose.minimal.yml up -d postgres redis qdrant n8n api ui

# Test core services
curl http://localhost:8000/v1/health
curl http://localhost:5678
```

### **Step 2: Add Converter Later**
```powershell
# When network is stable, build converter
docker-compose -f docker-compose.minimal.yml build dwg-service

# Start converter
docker-compose -f docker-compose.minimal.yml up -d dwg-service
```

---

## 🔧 **Network Troubleshooting:**

### **If Network Issues Persist:**

1. **Check Internet Connection:**
   ```powershell
   ping archive.ubuntu.com
   ```

2. **Try Different DNS:**
   - Windows: Change DNS to 8.8.8.8 or 1.1.1.1
   - Docker Desktop: Settings → Resources → Network → DNS

3. **Use Docker BuildKit:**
   ```powershell
   $env:DOCKER_BUILDKIT=1
   $env:COMPOSE_DOCKER_CLI_BUILD=1
   docker-compose -f docker-compose.minimal.yml build
   ```

4. **Build During Off-Peak Hours:**
   - Network issues are often worse during peak times
   - Try building early morning or late evening

---

## ✅ **Current Status:**

- ✅ **N8N:** Built successfully
- ✅ **API:** Ready to build (cached)
- ✅ **UI:** Ready to build (cached)
- ⚠️ **Converter:** Network issues (retry logic added)

---

## 🎯 **Quick Commands:**

```powershell
# Build core services (skip converter)
docker-compose -f docker-compose.minimal.yml build postgres redis qdrant n8n api ui

# Start core services
docker-compose -f docker-compose.minimal.yml up -d postgres redis qdrant n8n api ui

# Test
curl http://localhost:8000/v1/health

# Build converter later (when network is stable)
docker-compose -f docker-compose.minimal.yml build dwg-service
```

---

**The converter service is optional for initial testing. Build core services first! 🚀**

