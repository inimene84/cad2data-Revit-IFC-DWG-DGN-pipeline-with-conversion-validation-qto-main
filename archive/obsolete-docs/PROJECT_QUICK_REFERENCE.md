# 🚀 Construction AI Platform - Quick Reference

## 📋 Project Summary

**Unified Construction AI Platform** combining CAD/BIM data processing, AI-powered analysis, and real-time workflow automation.

---

## 🎯 Key Features

✅ **File Processing:** PDF, Excel, DWG, IFC, Revit, DGN  
✅ **AI Analysis:** Cost estimation, classification, carbon footprint  
✅ **Real-Time Updates:** WebSocket-powered status panel  
✅ **Analytics:** Cost trends, material breakdown, processing metrics  
✅ **Rate Limiting:** 100 req/min per user  
✅ **Caching:** Multi-layer Redis caching  
✅ **Error Handling:** User-friendly messages, retry logic  
✅ **Input Validation:** Pydantic models  
✅ **Circuit Breaker:** Protection against failures  

---

## 📁 Key Files

### **Frontend:**
- `web-react/src/pages/FileUpload.tsx` - File upload with drag-and-drop
- `web-react/src/pages/Analytics.tsx` - Analytics dashboard
- `web-react/src/components/StatusPanel.tsx` - Real-time status panel
- `web-react/src/services/websocket.ts` - WebSocket service

### **Backend:**
- `python-services/api/app.py` - Main FastAPI application
- `python-services/api/rate_limiting.py` - Rate limiting
- `python-services/api/cache.py` - Caching service
- `python-services/api/error_handler.py` - Error handling
- `python-services/api/validation.py` - Input validation
- `python-services/api/circuit_breaker.py` - Circuit breaker

### **Workflows:**
- `n8n-workflows/unified/00_Unified_Master_Agent.json` - Master workflow
- `n8n-workflows/simplified/00_Simplified_Master_Agent.json` - Simplified master

---

## 🔧 Quick Commands

### **Start Services:**
```bash
# All services
docker-compose -f docker-compose.prod.yml up

# Individual
python python-services/api/app.py
cd web-react && npm start
```

### **Test Endpoints:**
```bash
# Health
curl http://localhost:8000/health

# Analytics
curl http://localhost:8000/api/analytics/cost-trends?period=30d

# WebSocket
wscat -c ws://localhost:8000/ws
```

---

## 📊 Ports

- **React UI:** 3000
- **FastAPI:** 8000
- **N8N:** 5678
- **PostgreSQL:** 5432
- **Redis:** 6379
- **Qdrant:** 6333

---

## 🎯 Current Status

✅ **Phase 1:** Complete (File Management, Real-Time Status, Analytics)  
✅ **Phase 2:** Complete (Rate Limiting, Caching, Error Handling, Validation, Circuit Breaker)  
🔄 **Phase 3:** Pending (Advanced Features)  

---

## 📚 Documentation

- `PROJECT_MEMORY.md` - Complete project memory
- `HOW_THE_PROJECT_WORKS.md` - Full project overview
- `PHASE1_IMPROVEMENTS_SUMMARY.md` - Phase 1 details
- `PHASE2_IMPROVEMENTS_SUMMARY.md` - Phase 2 details
- `STEP_BY_STEP_UPLOAD_GUIDE.md` - Upload guide

---

**Last Updated:** 2025-01-15

