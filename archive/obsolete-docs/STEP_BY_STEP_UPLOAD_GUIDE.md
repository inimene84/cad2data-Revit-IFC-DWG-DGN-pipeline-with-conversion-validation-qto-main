# 📤 Step-by-Step File Upload Guide

## 📋 Overview

This guide provides detailed step-by-step instructions for uploading files to the Construction AI Platform using different methods:

1. **React Web UI** - Web interface
2. **REST API** - Direct API calls
3. **Telegram Bot** - Telegram integration
4. **N8N Workflow** - Automated workflows

---

## 🎯 Method 1: Upload via React Web UI

### **Step 1: Access the React Web UI**

1. **Open your web browser**
   - Navigate to: `http://localhost:3000` (local development)
   - Or: `https://yourdomain.com` (production)

2. **Login to the system**
   - Enter your username and password
   - Click "Login" button

### **Step 2: Navigate to Upload Page**

1. **Click on "Upload" button** in the navigation menu
   - Or navigate to: `http://localhost:3000/upload`
   - Or: `https://yourdomain.com/upload`

2. **Select upload type**
   - **CAD/BIM Files** - For Revit, IFC, DWG, DGN files
   - **Documents** - For PDF, JPG, PNG files
   - **Excel Files** - For Excel, CSV files

### **Step 3: Select File to Upload**

1. **Click "Choose File" button**
   - File picker dialog opens
   - Navigate to your file location
   - Select the file you want to upload

2. **Verify file selection**
   - File name appears in the upload form
   - File size is displayed
   - File type is validated

### **Step 4: Configure Upload Options**

1. **Select request type** (optional)
   - **Convert** - Convert file to Excel
   - **Validate** - Validate file
   - **Classify** - Classify elements
   - **Estimate Cost** - Estimate costs
   - **Carbon Footprint** - Calculate carbon footprint
   - **Quantity Takeoff** - Calculate quantities

2. **Enter additional parameters** (optional)
   - **Project ID** - Associate with project
   - **Description** - File description
   - **Tags** - File tags

### **Step 5: Upload File**

1. **Click "Upload" button**
   - File upload starts
   - Progress bar shows upload progress
   - Status updates in real-time

2. **Wait for upload to complete**
   - Upload progress: 0% → 100%
   - File is validated
   - File is stored in `uploads/` directory

### **Step 6: Monitor Upload Status**

1. **Check upload status**
   - Status: "Uploading" → "Processing" → "Complete"
   - File ID is displayed
   - Processing time is shown

2. **View upload results**
   - Click "View Results" button
   - Results page opens
   - Download processed files

### **Step 7: Download Results**

1. **Navigate to Results page**
   - Click "Results" in navigation menu
   - Or: `http://localhost:3000/results`
   - Or: `https://yourdomain.com/results`

2. **Download processed files**
   - Click "Download" button for Excel file
   - Click "Download" button for DAE file (if available)
   - Click "Download" button for PDF file (if available)

---

## 🎯 Method 2: Upload via REST API

### **Step 1: Prepare API Request**

1. **Get API endpoint**
   - Local: `http://localhost:8000/api/files/upload`
   - Production: `https://yourdomain.com/api/files/upload`

2. **Get API credentials**
   - API key from `.env.production`
   - Or: JWT token from login endpoint

### **Step 2: Create HTTP Request**

1. **Using cURL:**
   ```bash
   curl -X POST "http://localhost:8000/api/files/upload" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/file.rvt" \
     -F "requestType=convert" \
     -F "fileExtension=.rvt"
   ```

2. **Using Python:**
   ```python
   import requests

   url = "http://localhost:8000/api/files/upload"
   headers = {
       "Authorization": "Bearer YOUR_API_KEY"
   }
   files = {
       "file": open("/path/to/your/file.rvt", "rb")
   }
   data = {
       "requestType": "convert",
       "fileExtension": ".rvt"
   }
   
   response = requests.post(url, headers=headers, files=files, data=data)
   print(response.json())
   ```

3. **Using JavaScript (fetch):**
   ```javascript
   const formData = new FormData();
   formData.append('file', fileInput.files[0]);
   formData.append('requestType', 'convert');
   formData.append('fileExtension', '.rvt');

   fetch('http://localhost:8000/api/files/upload', {
     method: 'POST',
     headers: {
       'Authorization': 'Bearer YOUR_API_KEY'
     },
     body: formData
   })
   .then(response => response.json())
   .then(data => console.log(data));
   ```

### **Step 3: Send Request**

1. **Execute HTTP request**
   - Request is sent to FastAPI backend
   - File is uploaded to server
   - Request is validated

2. **Wait for response**
   - Response contains file ID
   - Response contains upload status
   - Response contains processing status

### **Step 4: Check Upload Status**

1. **Get file status:**
   ```bash
   curl -X GET "http://localhost:8000/api/files/{file_id}" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

2. **Response contains:**
   - File ID
   - File name
   - File size
   - Upload status
   - Processing status
   - Results (if available)

### **Step 5: Download Results**

1. **Get processed files:**
   ```bash
   curl -X GET "http://localhost:8000/api/files/{file_id}/download" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -o output.xlsx
   ```

2. **Download specific file type:**
   ```bash
   curl -X GET "http://localhost:8000/api/files/{file_id}/download?type=excel" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -o output.xlsx
   ```

---

## 🎯 Method 3: Upload via Telegram Bot

### **Step 1: Start Telegram Bot**

1. **Open Telegram app**
   - Search for your Construction AI Bot
   - Or: Click bot link from your admin

2. **Start conversation**
   - Click "Start" button
   - Bot sends welcome message
   - Bot displays available commands

### **Step 2: Send File to Bot**

1. **Attach file to message**
   - Click "Attach" button (paperclip icon)
   - Select "File" option
   - Choose file from your device

2. **Send file to bot**
   - File is uploaded to Telegram
   - Bot receives file
   - Bot processes file

### **Step 3: Configure Processing Options**

1. **Bot asks for processing type**
   - Bot sends message: "What would you like to do with this file?"
   - Options: Convert, Validate, Classify, Estimate Cost, etc.

2. **Select processing type**
   - Click on desired option
   - Or: Type command (e.g., `/convert`)
   - Bot processes your selection

### **Step 4: Monitor Processing**

1. **Bot sends status updates**
   - Status: "Uploading" → "Processing" → "Complete"
   - Progress updates in real-time
   - Estimated completion time

2. **Bot sends results**
   - Results are sent as files
   - Results are sent as messages
   - Results include download links

### **Step 5: Download Results**

1. **Download from Telegram**
   - Click on file to download
   - File is downloaded to your device
   - File is saved in Downloads folder

2. **Download from web interface**
   - Bot sends download link
   - Click on link to open web interface
   - Download file from web interface

---

## 🎯 Method 4: Upload via N8N Workflow

### **Step 1: Access N8N Interface**

1. **Open N8N interface**
   - Navigate to: `http://localhost:5678` (local development)
   - Or: `https://yourdomain.com/n8n` (production)

2. **Login to N8N**
   - Enter your N8N credentials
   - Click "Login" button

### **Step 2: Create or Edit Workflow**

1. **Create new workflow**
   - Click "New Workflow" button
   - Or: Edit existing workflow

2. **Add webhook trigger**
   - Add "Webhook" node
   - Configure webhook settings
   - Set webhook path (e.g., `/upload-file`)

### **Step 3: Configure Workflow**

1. **Add file upload node**
   - Add "HTTP Request" node
   - Configure to receive file
   - Set file upload settings

2. **Add processing nodes**
   - Add "Convert File" node
   - Add "Process Results" node
   - Add "Store Results" node

### **Step 4: Activate Workflow**

1. **Save workflow**
   - Click "Save" button
   - Workflow is saved
   - Workflow is ready to use

2. **Activate workflow**
   - Click "Activate" button
   - Workflow is activated
   - Webhook is available

### **Step 5: Trigger Workflow**

1. **Send file to webhook**
   ```bash
   curl -X POST "http://localhost:5678/webhook/upload-file" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/file.rvt" \
     -F "requestType=convert"
   ```

2. **Monitor workflow execution**
   - Check workflow execution log
   - View processing status
   - Check for errors

### **Step 6: Get Results**

1. **Check workflow results**
   - View workflow execution results
   - Download processed files
   - View processing logs

2. **Download results**
   - Results are stored in `output/` directory
   - Results are available via webhook
   - Results are sent to configured endpoint

---

## 🔄 Complete Upload Flow

### **Step-by-Step Flow Diagram**

```
Step 1: User selects file
  │
  ├─→ React UI: Click "Choose File"
  ├─→ API: POST /api/files/upload
  ├─→ Telegram: Send file to bot
  └─→ N8N: Trigger webhook
        │
        ▼
Step 2: File is uploaded
  │
  ├─→ FastAPI receives file
  ├─→ File is validated
  ├─→ File is stored in uploads/
  └─→ Metadata is stored in PostgreSQL
        │
        ▼
Step 3: N8N workflow is triggered
  │
  ├─→ Master Workflow receives webhook
  ├─→ Input Validator validates input
  ├─→ Simplified Router determines route
  └─→ Agent Workflow is executed
        │
        ▼
Step 4: File is processed
  │
  ├─→ Agent downloads file from uploads/
  ├─→ Converter service processes file
  ├─→ CAD converter generates Excel
  └─→ Results are stored in output/
        │
        ▼
Step 5: Results are stored
  │
  ├─→ Results are stored in PostgreSQL
  ├─→ Results are stored in Redis (cache)
  ├─→ Results are stored in Qdrant (vector DB)
  └─→ Results are stored in file system
        │
        ▼
Step 6: User receives results
  │
  ├─→ React UI: Display results
  ├─→ API: Return results in response
  ├─→ Telegram: Send results to bot
  └─→ N8N: Return results to webhook
        │
        ▼
Step 7: User downloads results
  │
  ├─→ React UI: Download from web interface
  ├─→ API: Download via API endpoint
  ├─→ Telegram: Download from bot
  └─→ N8N: Download from workflow results
```

---

## 📊 File Upload Examples

### **Example 1: Upload Revit File via React UI**

```
Step 1: Open React UI
  → Navigate to http://localhost:3000
  → Click "Upload" button

Step 2: Select file
  → Click "Choose File"
  → Select file.rvt
  → File name: file.rvt
  → File size: 50 MB
  → File type: .rvt

Step 3: Configure options
  → Request Type: Convert
  → File Extension: .rvt
  → Project ID: project-123
  → Description: Main building model

Step 4: Upload file
  → Click "Upload" button
  → Upload progress: 0% → 100%
  → Status: "Uploading" → "Processing" → "Complete"

Step 5: View results
  → Click "View Results"
  → Results page opens
  → Excel file: file.xlsx
  → DAE file: file.dae
  → PDF file: file.pdf

Step 6: Download results
  → Click "Download" button for Excel file
  → File is downloaded to Downloads folder
  → File is ready to use
```

### **Example 2: Upload PDF via REST API**

```bash
# Step 1: Prepare request
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/construction-document.pdf" \
  -F "requestType=extract_data" \
  -F "fileExtension=.pdf"

# Step 2: Response
{
  "status": "success",
  "file_id": "file-123456",
  "filename": "construction-document.pdf",
  "file_size": 1024000,
  "upload_status": "complete",
  "processing_status": "processing",
  "message": "File uploaded successfully"
}

# Step 3: Check status
curl -X GET "http://localhost:8000/api/files/file-123456" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 4: Response
{
  "status": "success",
  "file_id": "file-123456",
  "filename": "construction-document.pdf",
  "upload_status": "complete",
  "processing_status": "complete",
  "results": {
    "excel_file": "file-123456.xlsx",
    "extracted_data": {
      "materials": [...],
      "quantities": [...],
      "measurements": [...]
    }
  }
}

# Step 5: Download results
curl -X GET "http://localhost:8000/api/files/file-123456/download" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -o construction-document.xlsx
```

### **Example 3: Upload DWG via Telegram Bot**

```
Step 1: Start bot
  → Open Telegram
  → Search for Construction AI Bot
  → Click "Start"

Step 2: Send file
  → Click "Attach" button
  → Select "File"
  → Choose file.dwg
  → Send file to bot

Step 3: Bot processes file
  → Bot: "File received. What would you like to do?"
  → Options: Convert, Validate, Classify
  → User: Click "Convert"

Step 4: Bot processes file
  → Bot: "Processing file..."
  → Bot: "Status: Uploading → Processing → Complete"
  → Bot: "File processed successfully"

Step 5: Bot sends results
  → Bot: "Results ready!"
  → Bot: [Excel file]
  → Bot: [Download link]
  → User: Click file to download
```

### **Example 4: Upload IFC via N8N Workflow**

```bash
# Step 1: Create workflow
# - Add Webhook node
# - Add HTTP Request node
# - Add Convert File node
# - Add Store Results node

# Step 2: Activate workflow
# - Click "Activate" button
# - Webhook URL: http://localhost:5678/webhook/upload-ifc

# Step 3: Trigger workflow
curl -X POST "http://localhost:5678/webhook/upload-ifc" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/building.ifc" \
  -F "requestType=convert" \
  -F "fileExtension=.ifc"

# Step 4: Monitor workflow
# - Check workflow execution log
# - View processing status
# - Check for errors

# Step 5: Get results
# - Results are stored in output/
# - Results are available via webhook
# - Results are sent to configured endpoint
```

---

## 🔍 Troubleshooting

### **Common Issues and Solutions**

#### **Issue 1: File Upload Fails**

**Problem:** File upload fails with error message

**Solutions:**
1. **Check file size**
   - Maximum file size: 100 MB (default)
   - If file is larger, compress it or increase limit

2. **Check file format**
   - Supported formats: .rvt, .ifc, .dwg, .dgn, .pdf, .jpg, .png
   - If file format is not supported, convert it first

3. **Check network connection**
   - Ensure stable internet connection
   - Check firewall settings
   - Check proxy settings

4. **Check API credentials**
   - Verify API key is correct
   - Verify API key has necessary permissions
   - Verify API key is not expired

#### **Issue 2: File Processing Fails**

**Problem:** File is uploaded but processing fails

**Solutions:**
1. **Check file format**
   - Ensure file is valid CAD/BIM file
   - Ensure file is not corrupted
   - Ensure file is not password protected

2. **Check converter service**
   - Verify converter service is running
   - Check converter service logs
   - Verify converter has necessary permissions

3. **Check database connection**
   - Verify PostgreSQL is running
   - Check database connection settings
   - Verify database has necessary permissions

#### **Issue 3: Results Not Available**

**Problem:** File is processed but results are not available

**Solutions:**
1. **Check processing status**
   - Verify processing is complete
   - Check processing logs
   - Verify no errors occurred

2. **Check file storage**
   - Verify results are stored in output/
   - Check file permissions
   - Verify file system has space

3. **Check database**
   - Verify results are stored in database
   - Check database query
   - Verify database connection

#### **Issue 4: Download Fails**

**Problem:** Unable to download processed files

**Solutions:**
1. **Check file existence**
   - Verify file exists in output/
   - Check file permissions
   - Verify file is not corrupted

2. **Check download endpoint**
   - Verify download endpoint is correct
   - Check API credentials
   - Verify API has necessary permissions

3. **Check network connection**
   - Ensure stable internet connection
   - Check firewall settings
   - Check proxy settings

---

## 📚 API Reference

### **Upload Endpoint**

**POST /api/files/upload**

**Request:**
```json
{
  "file": "file.rvt",
  "requestType": "convert",
  "fileExtension": ".rvt",
  "projectId": "project-123",
  "description": "Main building model"
}
```

**Response:**
```json
{
  "status": "success",
  "file_id": "file-123456",
  "filename": "file.rvt",
  "file_size": 52428800,
  "upload_status": "complete",
  "processing_status": "processing",
  "message": "File uploaded successfully"
}
```

### **Get File Status Endpoint**

**GET /api/files/{file_id}**

**Response:**
```json
{
  "status": "success",
  "file_id": "file-123456",
  "filename": "file.rvt",
  "upload_status": "complete",
  "processing_status": "complete",
  "results": {
    "excel_file": "file-123456.xlsx",
    "dae_file": "file-123456.dae",
    "pdf_file": "file-123456.pdf"
  }
}
```

### **Download File Endpoint**

**GET /api/files/{file_id}/download**

**Query Parameters:**
- `type` - File type (excel, dae, pdf)
- `format` - File format (xlsx, csv, json)

**Response:**
- File content (binary)
- Content-Type: application/octet-stream
- Content-Disposition: attachment; filename="file.xlsx"

---

## 🎯 Best Practices

### **1. File Preparation**

- **Compress large files** - Reduce file size before uploading
- **Validate file format** - Ensure file is in supported format
- **Check file integrity** - Verify file is not corrupted
- **Remove password protection** - Ensure file is not password protected

### **2. Upload Process**

- **Use stable connection** - Ensure stable internet connection
- **Monitor upload progress** - Check upload progress regularly
- **Verify upload completion** - Confirm upload is complete
- **Check upload status** - Verify file is stored correctly

### **3. Processing**

- **Monitor processing status** - Check processing status regularly
- **Check processing logs** - Review processing logs for errors
- **Verify processing completion** - Confirm processing is complete
- **Check results quality** - Verify results are accurate

### **4. Results**

- **Download results promptly** - Download results as soon as available
- **Verify results accuracy** - Check results for accuracy
- **Store results securely** - Store results in secure location
- **Backup results** - Keep backup copies of results

---

## 🎉 Summary

### **Upload Methods:**

1. **React Web UI** - Easy to use, visual interface
2. **REST API** - Programmatic access, automation
3. **Telegram Bot** - Mobile-friendly, convenient
4. **N8N Workflow** - Automated workflows, integration

### **Upload Flow:**

1. **Select file** - Choose file to upload
2. **Upload file** - Upload file to server
3. **Process file** - Process file with converter
4. **Store results** - Store results in database
5. **Download results** - Download processed files

### **Key Points:**

- ✅ Supported formats: .rvt, .ifc, .dwg, .dgn, .pdf, .jpg, .png
- ✅ Maximum file size: 100 MB (default)
- ✅ Processing time: Varies by file size and type
- ✅ Results storage: Database, file system, cache
- ✅ Download options: Excel, DAE, PDF, JSON

**🎉 Ready to upload files! Follow the step-by-step guide above.**

