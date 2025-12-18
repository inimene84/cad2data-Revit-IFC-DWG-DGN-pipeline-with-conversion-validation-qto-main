# 🏗️ Construction AI Agent Setup Guide

## Overview
Complete construction site management system with Google Drive integration, DWG processing, OCR, and AI-powered Q&A.

## Database Comparison

### **Chroma (Recommended for Start)**
- **Storage:** Local files in `./data/chroma/`
- **Pros:** Zero setup, embedded, good for development
- **Cons:** No concurrent access, limited scaling
- **Best for:** Single-user, development, simple RAG

### **Postgres + pgvector (Production)**
- **Storage:** Full SQL database with vector extensions
- **Pros:** Concurrent access, complex queries, ACID compliance
- **Cons:** Requires database setup, more complex
- **Best for:** Production, multi-user, complex analytics

### **Baserow (Your existing)**
- **Storage:** PostgreSQL-based with web UI
- **Pros:** You already have it, web interface
- **Cons:** Not optimized for vector search
- **Best for:** Structured data, not ideal for embeddings

## Services Created

### 1. DWG Conversion Service (Port 5055)
```bash
python services/dwg_service.py
```
- **Health:** http://localhost:5055/health
- **Convert:** POST http://localhost:5055/convert-dwg
- **Body:** `{"input_path": "C:/path/file.dwg", "output_dir": "C:/output"}`

### 2. OCR Service (Port 5056)
```bash
python services/ocr_service.py
```
- **Health:** http://localhost:5056/health
- **OCR:** POST http://localhost:5056/ocr
- **Body:** `{"file_path": "C:/path/file.pdf"}`
- **Features:** Tesseract v5.5.0, construction-optimized settings

### 3. Drive Provisioner Service (Port 5057)
```bash
python services/drive_provisioner.py
```
- **Health:** http://localhost:5057/health
- **Create Project:** POST http://localhost:5057/create-project
- **Body:** `{"project_name": "MyProject", "drive_root": "Drive/Projects"}`

## n8n Workflows (Import Ready)

### 00_Drive_Project_Setup.json
- Creates standardized project folder structure
- 10 folders: Drawings, RFIs, Site Photos, Reports, etc.
- Integrates with Google Drive API

### 01_Intake_Drive_Gmail.json
- Watches Google Drive for new files
- Monitors Gmail for RFI/Site labels
- Normalizes and routes to project folders

### 02_Parse_Index_DWG_OCR_Embeddings.json
- DWG → XLSX conversion via service
- PDF OCR with Tesseract
- Construction-specific text processing
- Vector embeddings for search

### 03_Agent_QA_RAG.json
- RAG-based Q&A system
- Searches vector database
- Provides citations and context
- Construction domain knowledge

### 04_Reports_Out.json
- Generates HTML/XLSX reports
- Uploads to Google Drive
- Sends email notifications
- Project summaries and analytics

## Quick Start

### 1. Start All Services
```bash
# Windows Batch
start_services.bat

# PowerShell
.\start_services.ps1
```

### 2. Import n8n Workflows
1. Open n8n
2. File → Import
3. Import each JSON file from `workflows/` folder
4. Set Google Drive/Gmail credentials

### 3. Test DWG Conversion
```bash
curl -X POST http://localhost:5055/convert-dwg \
  -H "Content-Type: application/json" \
  -d '{"input_path": "C:/path/to/file.dwg", "output_dir": "C:/output"}'
```

### 4. Test OCR
```bash
curl -X POST http://localhost:5056/ocr \
  -H "Content-Type: application/json" \
  -d '{"file_path": "C:/path/to/file.pdf"}'
```

## Google Drive Folder Structure

Each project gets:
```
Drive/Projects/{ProjectName}/
├── 01_Drawings/          # Architectural, structural, MEP drawings
├── 02_RFIs/             # Request for Information documents
├── 03_Site_Photos/      # Progress photos, drone footage
├── 04_Reports/          # Daily, weekly, monthly reports
├── 05_Intake/           # Incoming documents
├── 06_Processed/        # Processed and analyzed documents
├── 07_Compliance/       # Safety, permits, inspections
├── 08_Contracts/        # Contracts, agreements, legal
├── 09_Change_Orders/    # Change orders and modifications
└── 10_Closeout/         # Final documentation
```

## OCR Features

### Construction-Optimized Settings
- **PSM 6:** Uniform block of text
- **OEM 1:** LSTM OCR Engine
- **DPI 300:** High resolution for drawings
- **Language:** English

### Extracted Data
- **Text:** Full document text
- **Dimensions:** "120.5m", "45'6\"", "3.2m x 4.5m"
- **Materials:** concrete, steel, wood, brick, insulation
- **Layers:** ROOF, WALL, FOUNDATION, STRUCTURE

## Integration with Your Baserow

Since you have Baserow at `C:\Users\valgu\self-hosted-ai-starter-kit`:

### Option 1: Keep Separate
- Use Chroma for vector search (AI Q&A)
- Use Baserow for structured data (quantities, costs)
- Sync between them via n8n workflows

### Option 2: Integrate
- Add vector columns to Baserow tables
- Use Baserow API for all data storage
- Custom vector search implementation

## Next Steps

### Immediate
1. Start services: `start_services.bat`
2. Import n8n workflows
3. Test with sample DWG/PDF files
4. Set up Google Drive credentials

### Short Term
1. Add real Chroma server (or switch to Postgres+pgvector)
2. Connect to your Baserow instance
3. Add more construction-specific OCR patterns
4. Implement automated folder creation

### Long Term
1. Add video/audio processing for site documentation
2. Integrate with IoT sensors
3. Add predictive analytics
4. Scale to multiple projects

## Troubleshooting

### Services Won't Start
- Check Python installation: `python --version`
- Install Flask: `pip install flask`
- Check port availability: `netstat -an | findstr :5055`

### Tesseract Issues
- Verify installation: `& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version`
- Check file paths in OCR service
- Test with simple image first

### n8n Connection Issues
- Verify service URLs in workflows
- Check HTTP request timeouts
- Test services individually with curl

## File Structure
```
cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main/
├── services/
│   ├── dwg_service.py          # DWG conversion microservice
│   ├── ocr_service.py          # OCR with Tesseract
│   └── drive_provisioner.py    # Google Drive folder management
├── workflows/
│   ├── 00_Drive_Project_Setup.json
│   ├── 01_Intake_Drive_Gmail.json
│   ├── 02_Parse_Index_DWG_OCR_Embeddings.json
│   ├── 03_Agent_QA_RAG.json
│   └── 04_Reports_Out.json
├── start_services.bat          # Windows batch startup
├── start_services.ps1          # PowerShell startup
└── CONSTRUCTION_AI_AGENT_SETUP.md
```

## Support

- **GitHub:** [cad2data-Revit-IFC-DWG-DGN-pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- **Services:** Check logs in service windows
- **n8n:** Use execution logs for debugging

---

**🎯 You now have a complete construction AI agent system ready to deploy!**
