# Docker Build Size Analysis

## 📊 Estimated Image Sizes

### **Core Application Services:**

#### **1. API Service** (`Dockerfile.api`)
- **Base Image:** `python:3.11-slim` (~150-200 MB)
- **Build Tools:** build-essential, gcc, libffi-dev (~200 MB)
- **Python Packages:** 37 packages from requirements.txt
  - FastAPI, uvicorn, pandas, numpy (~100 MB)
  - AI/ML: sentence-transformers, google-generativeai (~200-300 MB)
  - OCR: pytesseract, Pillow, pdf2image (~100 MB)
  - Database: psycopg2, sqlalchemy, redis (~50 MB)
  - OpenTelemetry, Qdrant client (~50 MB)
- **Runtime:** Tesseract OCR (~50-100 MB)
- **Application Code:** ~5-10 MB
- **Total Estimated: ~700-900 MB**

#### **2. UI Service** (`web-react/Dockerfile`)
- **Build Stage:**
  - Base: `node:18-alpine` (~150 MB)
  - npm packages: ~30+ dependencies (~200-400 MB)
    - React, Material-UI, Three.js, Redux, etc.
- **Production Stage:**
  - Base: `nginx:alpine` (~25 MB)
  - Built React app: ~10-50 MB (compressed)
- **Total Estimated: ~400-600 MB** (only production stage in final image)

#### **3. N8N Service** (`Dockerfile.n8n`)
- **Base Image:** `n8nio/n8n:latest` (~500-800 MB)
- **Additional:** curl (~5 MB)
- **Total Estimated: ~500-800 MB**

#### **4. Converter Services** (`Dockerfile.converter`) ⚠️ **LARGEST**
- **Base Image:** `ubuntu:22.04` (~70-100 MB)
- **Wine + Dependencies:** ~500-800 MB (Wine is very large!)
  - wine, winetricks, wine64, wine32, xvfb
  - vcrun2019 runtime libraries
- **Python Packages:** ~50-100 MB
- **CAD Converters:** Could be 200-500 MB
  - DDC_Converter_DWG, DDC_Converter_Revit, etc.
  - DLLs, libraries, Qt libraries
- **Total Estimated: ~1-2 GB per converter service**
- **Note:** 3 converter services (dwg, ocr, drive) = **~3-6 GB total**

---

### **Database & Infrastructure Services:**

#### **5. PostgreSQL**
- **Image:** `postgres:15` (~200-300 MB)

#### **6. Redis**
- **Image:** `redis:7-alpine` (~50-100 MB)

#### **7. Qdrant**
- **Image:** `qdrant/qdrant:latest` (~100-200 MB)

#### **8. Elasticsearch** ⚠️ **LARGE**
- **Image:** `elasticsearch:8.11.0` (~500-800 MB)
- **Data Volume:** Can grow significantly

#### **9. Logstash**
- **Image:** `logstash:8.11.0` (~300-500 MB)

#### **10. Kibana**
- **Image:** `kibana:8.11.0` (~500-800 MB)

#### **11. Prometheus**
- **Image:** `prom/prometheus:latest` (~100-200 MB)

#### **12. Grafana**
- **Image:** `grafana/grafana:latest` (~200-300 MB)

#### **13. Jaeger**
- **Image:** `jaegertracing/all-in-one:latest` (~100-200 MB)

#### **14. Nginx**
- **Image:** `nginx:alpine` (~25 MB)

#### **15. Locust** (Load Testing)
- **Image:** `locustio/locust:latest` (~100-200 MB)

---

## 📦 **Total Estimated Size**

### **By Category:**

| Category | Services | Estimated Size |
|----------|----------|----------------|
| **Application** | API, UI, N8N | ~1.6-2.3 GB |
| **Converters** | DWG, OCR, Drive | ~3-6 GB |
| **Databases** | PostgreSQL, Redis, Qdrant | ~350-600 MB |
| **Monitoring** | Prometheus, Grafana, Jaeger | ~400-700 MB |
| **ELK Stack** | Elasticsearch, Logstash, Kibana | ~1.3-2.1 GB |
| **Infrastructure** | Nginx, Locust | ~125-225 MB |
| **TOTAL** | **All Services** | **~7-12 GB** |

---

## ⚠️ **Largest Contributors:**

1. **Converter Services (Wine):** ~3-6 GB (50-60% of total)
2. **ELK Stack:** ~1.3-2.1 GB (15-20% of total)
3. **Application Services:** ~1.6-2.3 GB (15-20% of total)
4. **Other Services:** ~1-2 GB (10-15% of total)

---

## 💡 **Size Optimization Tips:**

### **1. Multi-Stage Builds** ✅ (Already implemented)
- API and UI use multi-stage builds
- Only production dependencies in final images

### **2. Alpine Base Images** ✅ (Partially implemented)
- UI uses `nginx:alpine` (25 MB vs 100+ MB)
- Redis uses `redis:7-alpine`
- Consider: `python:3.11-alpine` for API (smaller but may have compatibility issues)

### **3. Converter Services** ⚠️ (Hard to optimize)
- Wine is inherently large (~500-800 MB)
- Could use separate VMs/containers for converters
- Or use cloud-based converter services

### **4. ELK Stack** (Optional)
- Can be disabled for smaller deployments
- Use lighter alternatives (e.g., Loki instead of ELK)

### **5. Remove Unused Services**
- Locust (load testing) - only needed for testing
- Jaeger (tracing) - can be disabled
- Some monitoring services can be optional

---

## 🎯 **Minimum Deployment Size:**

If you disable optional services:
- **Core Services:** API, UI, N8N, PostgreSQL, Redis, Qdrant
- **Converters:** 3 services with Wine
- **Basic Monitoring:** Prometheus, Grafana
- **Estimated: ~5-7 GB**

---

## 📝 **Notes:**

1. **First Build:** Downloads all base images (~2-3 GB)
2. **Subsequent Builds:** Much faster (uses cache)
3. **Runtime:** Images are compressed and shared layers
4. **Disk Space:** Actual disk usage may be less due to layer sharing
5. **Wine:** The biggest contributor - consider alternatives if possible

---

## 🔍 **Check Actual Sizes After Build:**

```powershell
# After build completes, check sizes:
docker images | Sort-Object Size -Descending

# Or get detailed sizes:
docker system df -v
```

---

**Estimated Total Build Size: ~7-12 GB** (depending on optional services)

