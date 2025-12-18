# 🚀 Quick Upload Reference Guide

## 📋 Quick Start

### **Method 1: React Web UI (Easiest)**

1. **Open browser** → `http://localhost:3000/upload`
2. **Click "Choose File"** → Select your file
3. **Click "Upload"** → Wait for processing
4. **Download results** → Click "Download" button

### **Method 2: REST API (Programmatic)**

```bash
# Upload file
curl -X POST "http://localhost:8000/extract-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf"

# Check status
curl -X GET "http://localhost:8000/api/files/{file_id}"

# Download results
curl -X GET "http://localhost:8000/api/files/{file_id}/download" \
  -o output.xlsx
```

### **Method 3: Telegram Bot (Mobile)**

1. **Open Telegram** → Search for Construction AI Bot
2. **Send file** → Attach file to message
3. **Select action** → Convert, Validate, etc.
4. **Download results** → Click file to download

### **Method 4: N8N Workflow (Automated)**

1. **Create workflow** → Add webhook trigger
2. **Configure workflow** → Add file upload node
3. **Activate workflow** → Webhook is available
4. **Trigger workflow** → Send file to webhook
5. **Get results** → Results are returned

---

## 📊 Supported File Formats

| Format | Extension | Supported | Output |
|--------|-----------|-----------|--------|
| **Revit** | `.rvt` | ✅ | Excel, DAE, PDF |
| **IFC** | `.ifc` | ✅ | Excel, DAE |
| **AutoCAD** | `.dwg` | ✅ | Excel, PDF |
| **MicroStation** | `.dgn` | ✅ | Excel |
| **PDF** | `.pdf` | ✅ | Excel, Text |
| **Excel** | `.xlsx`, `.xls` | ✅ | Excel, JSON |
| **Images** | `.jpg`, `.png` | ✅ | Excel, Text |
| **Word** | `.docx` | ✅ | Excel, Text |

---

## 🔄 Upload Flow (Quick Reference)

```
User Uploads File
  ↓
FastAPI Receives File
  ↓
File Stored in uploads/
  ↓
N8N Workflow Triggered
  ↓
File Processed
  ↓
Results Stored in output/
  ↓
User Downloads Results
```

---

## 📝 API Endpoints

### **Upload Endpoint**

```http
POST /extract-pdf
Content-Type: multipart/form-data

file: (binary)
project_name: (string, optional)
workflow_type: (string, optional)
```

### **Status Endpoint**

```http
GET /api/files/{file_id}
Authorization: Bearer {token}
```

### **Download Endpoint**

```http
GET /api/files/{file_id}/download
Authorization: Bearer {token}
```

---

## 🎯 Common Use Cases

### **Use Case 1: Convert Revit File**

```bash
# Upload Revit file
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@building.rvt" \
  -F "requestType=convert" \
  -F "fileExtension=.rvt"

# Response
{
  "status": "success",
  "file_id": "file-123456",
  "filename": "building.rvt",
  "upload_status": "complete",
  "processing_status": "processing"
}
```

### **Use Case 2: Extract Data from PDF**

```bash
# Upload PDF file
curl -X POST "http://localhost:8000/extract-pdf" \
  -F "file=@construction-document.pdf"

# Response
{
  "status": "success",
  "filename": "construction-document.pdf",
  "pages_processed": 10,
  "construction_items": [...],
  "processing_time_seconds": 2.5
}
```

### **Use Case 3: Process Excel File**

```bash
# Upload Excel file
curl -X POST "http://localhost:8000/extract-excel" \
  -F "file=@materials.xlsx"

# Response
{
  "status": "success",
  "filename": "materials.xlsx",
  "sheets": ["Sheet1", "Sheet2"],
  "construction_items": [...],
  "processing_time_seconds": 1.2
}
```

---

## 🔍 Troubleshooting

### **Issue: Upload Fails**

**Solutions:**
1. Check file size (max 100 MB)
2. Check file format (supported formats only)
3. Check network connection
4. Check API credentials

### **Issue: Processing Fails**

**Solutions:**
1. Check file format (valid CAD/BIM file)
2. Check converter service (running)
3. Check database connection (PostgreSQL)
4. Check logs for errors

### **Issue: Results Not Available**

**Solutions:**
1. Check processing status (complete)
2. Check file storage (output/ directory)
3. Check database (results stored)
4. Check file permissions (readable)

---

## 📚 More Information

- **Complete Guide:** See `STEP_BY_STEP_UPLOAD_GUIDE.md`
- **API Documentation:** See `http://localhost:8000/docs`
- **Workflow Documentation:** See `UNIFIED_WORKFLOW_SYSTEM.md`
- **Project Overview:** See `HOW_THE_PROJECT_WORKS.md`

---

## 🎉 Quick Tips

1. **Use React UI** for easiest upload experience
2. **Use REST API** for programmatic access
3. **Use Telegram Bot** for mobile uploads
4. **Use N8N Workflow** for automated workflows
5. **Check file format** before uploading
6. **Monitor upload status** regularly
7. **Download results** promptly
8. **Backup results** for safety

---

**🎉 Ready to upload files! Follow the quick start guide above.**

