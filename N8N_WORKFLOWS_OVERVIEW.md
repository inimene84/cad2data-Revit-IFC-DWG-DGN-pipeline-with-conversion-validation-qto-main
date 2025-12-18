# 🔄 N8N Workflows Overview

**Last Updated:** 2025-01-15  
**Total Workflows:** 45+ workflows across 4 categories  
**Platform:** Construction AI Platform - Unified CAD/BIM & Construction Management

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Workflow Architecture](#workflow-architecture)
3. [CAD-BIM Workflows](#cad-bim-workflows)
4. [Construction Workflows](#construction-workflows)
5. [Unified Master Agent System](#unified-master-agent-system)
6. [Simplified Workflows](#simplified-workflows)
7. [Workflow Registry](#workflow-registry)
8. [Error Handling](#error-handling)
9. [Integration Points](#integration-points)
10. [Usage Guide](#usage-guide)

---

## 🎯 Overview

The Construction AI Platform uses n8n workflows to orchestrate complex AI-powered operations for:
- **CAD/BIM Processing:** Conversion, validation, classification, cost estimation, carbon footprint analysis, quantity takeoff
- **Construction Management:** Data extraction, materials accounting, document generation, file management, vendor management, compliance, visualization, BIM processing, scheduling, 3D vision
- **Unified Orchestration:** Master agent system that routes requests to appropriate specialized workflows

---

## 🏗️ Workflow Architecture

### **Directory Structure:**
```
n8n-workflows/
├── cad-bim/              # CAD/BIM specific workflows (12 workflows)
├── construction/         # Construction management workflows (13 workflows)
├── unified/              # Unified master agent system (16 workflows)
└── simplified/           # Simplified workflows with error handling (3 workflows)
```

### **Workflow Categories:**

1. **CAD-BIM Workflows** (`cad-bim/`)
   - File conversion (Revit, IFC, DWG, DGN)
   - Validation and quality assurance
   - AI-powered classification
   - Cost estimation
   - Carbon footprint analysis
   - Quantity takeoff
   - Batch processing
   - Real-time data updates

2. **Construction Workflows** (`construction/`)
   - Manager agent (orchestrator)
   - Data extraction (OCR + AI)
   - Materials accounting (BOQ)
   - Web search (market intelligence)
   - Document generation
   - File management
   - Vendor management
   - Compliance checking
   - Visualization
   - BIM processing
   - Scheduling
   - CAD data processing
   - 3D vision

3. **Unified Master Agent** (`unified/`)
   - Master agent (request router)
   - Specialized agent workflows
   - Error handler
   - Workflow registry

4. **Simplified Workflows** (`simplified/`)
   - Simplified master agent
   - Error handler workflow
   - Simplification guide

---

## 🔧 CAD-BIM Workflows

### **1. File Conversion Workflows**

#### **n8n_1_Revit_IFC_DWG_Conversation_simple.json**
- **Purpose:** Simple CAD/BIM file conversion
- **Supported Formats:** Revit (.rvt), IFC, DWG, DGN
- **Features:**
  - Basic conversion pipeline
  - Format detection
  - Output format selection

#### **n8n_2_All_Settings_Revit_IFC_DWG_Conversation_simple.json**
- **Purpose:** Advanced conversion with all settings
- **Features:**
  - Comprehensive conversion options
  - Customizable output parameters
  - Quality settings
  - Batch processing support

#### **n8n_8_Revit_IFC_DWG_Conversation_EXTRACT_Phase_with_Parse_XLSX.json**
- **Purpose:** Conversion with data extraction and Excel parsing
- **Features:**
  - Extract phase conversion
  - XLSX parsing
  - Data extraction
  - Structured output

#### **n8n_3_CAD-BIM-Batch-Converter-Pipeline.json**
- **Purpose:** Batch conversion of multiple files
- **Features:**
  - Multiple file processing
  - Parallel processing
  - Progress tracking
  - Error handling per file

### **2. Validation Workflow**

#### **n8n_4_Validation_CAD_BIM_Revit_IFC_DWG.json**
- **Purpose:** Validate CAD/BIM files for quality and compliance
- **Features:**
  - File structure validation
  - Data integrity checks
  - Compliance verification
  - Quality scoring
  - Validation reports

### **3. Classification Workflow**

#### **n8n_5_CAD_BIM_Automatic_Classification_with_LLM_and_RAG.json**
- **Purpose:** AI-powered automatic classification of BIM elements
- **Features:**
  - LLM-based classification
  - RAG (Retrieval-Augmented Generation)
  - Element categorization
  - Material identification
  - Property extraction

### **4. Cost Estimation Workflows**

#### **n8n_6_Construction_Price_Estimation_with_LLM_for_Revt_and_IFC.json**
- **Purpose:** AI-powered construction cost estimation
- **Features:**
  - LLM-based cost analysis
  - Material cost calculation
  - Labor cost estimation
  - Regional pricing (Estonian market)
  - Detailed cost breakdown

#### **n8n_6_Fixed_Construction_Price_Estimation_OpenAI_Only.json**
- **Purpose:** Cost estimation using OpenAI only
- **Features:**
  - OpenAI GPT integration
  - Simplified cost estimation
  - Faster processing
  - Cost breakdown reports

### **5. Carbon Footprint Workflow**

#### **n8n_7_Carbon_Footprint_CO2_Estimator_for_Revit and_IFC.json**
- **Purpose:** Calculate carbon footprint and CO2 emissions
- **Features:**
  - Material-based CO2 calculation
  - Lifecycle assessment
  - Environmental impact analysis
  - Carbon footprint reports
  - Sustainability scoring

### **6. Quantity Takeoff Workflow**

#### **n8n_9_CAD_BIM_Quantity_TakeOff_HTML_Report_Generator.json**
- **Purpose:** Generate quantity takeoff reports
- **Features:**
  - Automated quantity calculation
  - Material quantification
  - HTML report generation
  - Visual breakdowns
  - Export to various formats

### **7. Specialized Workflows**

#### **n8n_Project_Excel_Pipeline.json**
- **Purpose:** Data-driven construction project pipeline
- **Features:**
  - Excel-based project management
  - Data extraction from Excel
  - Project tracking
  - Progress monitoring

#### **n8n_Real_Time_Data_Update_Workflow.json**
- **Purpose:** Real-time data updates and synchronization
- **Features:**
  - Live data updates
  - WebSocket integration
  - Real-time notifications
  - Status tracking

---

## 🏗️ Construction Workflows

### **1. Manager Agent**

#### **01_Construction_Manager_Agent.json**
- **Purpose:** Master orchestrator for all construction workflows
- **Nodes:** 25 nodes
- **Connections:** 22 connections
- **Sub-Agents:** 10 specialized agents
- **Features:**
  - Request routing
  - Workflow orchestration
  - Error handling
  - Activity logging
  - Analytics tracking

### **2. Data Extraction Agent**

#### **02_Data_Extraction_Agent.json**
- **Purpose:** Advanced OCR and AI construction document analysis
- **Nodes:** 4 nodes
- **Features:**
  - OCR processing (OCR.space)
  - AI analysis (Gemini 1.5 Pro)
  - Estonian standards integration
  - Document parsing
  - Data extraction
  - Structured output

### **3. Materials Accounting Agent**

#### **03_Materials_Accounting_Agent.json**
- **Purpose:** BOQ (Bill of Quantities) and cost estimation system
- **Nodes:** 4 nodes
- **Features:**
  - Professional BOQ generation
  - 2025 Estonian market pricing
  - Material cost calculation
  - Quantity takeoff
  - Cost breakdown reports

### **4. Web Search Agent**

#### **04_Web_Search_Agent.json**
- **Purpose:** Construction market intelligence via web search
- **Nodes:** 2 nodes
- **Features:**
  - Real-time market research
  - Perplexity AI integration
  - Supplier information
  - Price comparisons
  - Market trends

### **5. Document Generation Agent**

#### **05_Document_Generation_Agent.json**
- **Purpose:** Professional construction document creation
- **Nodes:** 2 nodes
- **Features:**
  - Google Docs integration
  - Professional report generation
  - Template-based documents
  - Automated formatting
  - Multi-format export

### **6. File Manager Agent**

#### **06_File_Manager_Agent.json**
- **Purpose:** Intelligent construction file organization
- **Nodes:** 2 nodes
- **Features:**
  - Google Drive integration
  - File organization
  - Automatic categorization
  - Version control
  - Access management

### **7. Vendor Agent**

#### **07_Vendor_Agent.json**
- **Purpose:** Estonian supplier network intelligence
- **Nodes:** 2 nodes
- **Features:**
  - Supplier database
  - Estonian market suppliers (K-Rauta, Bauhof, Stokker, etc.)
  - Price comparisons
  - Vendor recommendations
  - Procurement support

### **8. Compliance Agent**

#### **08_Compliance_Agent.json**
- **Purpose:** Estonian building code compliance verification
- **Nodes:** 2 nodes
- **Features:**
  - Estonian building codes
  - Regulatory verification
  - Fire safety compliance
  - EVS-EN standards
  - Compliance reports

### **9. Visualization Agent**

#### **09_Visualization_Agent.json**
- **Purpose:** Construction data visualization
- **Nodes:** 2 nodes
- **Features:**
  - Professional charts
  - Data visualization
  - Construction-themed graphics
  - Report generation
  - Export capabilities

### **10. BIM Agent**

#### **10_BIM_Agent.json**
- **Purpose:** Advanced BIM processing with DDC integration
- **Nodes:** 2 nodes
- **Features:**
  - BIM file processing
  - DataDrivenConstruction.io integration
  - Geometry analysis
  - Property extraction
  - BIM validation

### **11. Schedule Agent**

#### **11_Schedule_Agent.json**
- **Purpose:** Project timeline management
- **Nodes:** 2 nodes
- **Features:**
  - Project scheduling
  - Milestone tracking
  - Timeline generation
  - Progress monitoring
  - Deadline management

### **12. CAD Data Processor**

#### **12_CAD_Data_Processor.json**
- **Purpose:** BIM geometry analysis
- **Nodes:** Variable
- **Features:**
  - CAD data processing
  - Geometry extraction
  - Spatial analysis
  - Property mapping

### **13. 3D Vision Agent**

#### **13_3D_Vision_Agent.json**
- **Purpose:** Advanced construction visualization
- **Nodes:** Variable
- **Features:**
  - 3D visualization
  - Advanced rendering
  - Spatial analysis
  - Visual reports

---

## 🎯 Unified Master Agent System

### **Master Agent Workflow**

#### **00_Unified_Master_Agent.json**
- **Purpose:** Central request router for all workflows
- **Triggers:**
  - Manual trigger
  - Webhook trigger (`POST /construction-ai`)
- **Features:**
  - Intelligent request analysis
  - Automatic routing to specialized agents
  - Priority-based routing
  - Multi-agent support
  - Error handling

### **Routing Logic:**

The master agent analyzes incoming requests and routes them to appropriate agents based on:

1. **Request Type:** `convert`, `validate`, `classify`, `estimate_cost`, `carbon_footprint`, `quantity_takeoff`, etc.
2. **File Category:** `cad_bim`, `document`, `data`
3. **File Extension:** `.rvt`, `.ifc`, `.dwg`, `.dgn`, `.pdf`, `.jpg`, `.png`, `.docx`, `.xlsx`, `.csv`
4. **Action:** Specific action requested

### **Specialized Agent Workflows:**

1. **Agent_cad_bim_conversion.json** - CAD/BIM conversion
2. **Agent_cad_bim_validation.json** - CAD/BIM validation
3. **Agent_cad_bim_classification.json** - AI classification
4. **Agent_cad_bim_cost_estimation.json** - Cost estimation
5. **Agent_cad_bim_carbon_footprint.json** - Carbon footprint
6. **Agent_cad_bim_quantity_takeoff.json** - Quantity takeoff
7. **Agent_construction_bim.json** - BIM processing
8. **Agent_construction_compliance.json** - Compliance
9. **Agent_construction_documents.json** - Document generation
10. **Agent_construction_file_management.json** - File management
11. **Agent_construction_scheduling.json** - Scheduling
12. **Agent_construction_vendor.json** - Vendor management
13. **Agent_construction_visualization.json** - Visualization
14. **Agent_other.json** - Other operations

### **Workflow Registry**

#### **workflow_registry.json**
- **Purpose:** Central registry of all available workflows
- **Features:**
  - Workflow metadata
  - Agent mappings
  - File paths
  - Workflow types
  - Version information

---

## 🔄 Simplified Workflows

### **Simplified Master Agent**

#### **00_Simplified_Master_Agent.json**
- **Purpose:** Simplified version with better error handling
- **Features:**
  - Simplified routing logic
  - Input validation
  - Centralized error handling
  - Reduced complexity (8 nodes vs 10+)
  - Error recovery suggestions

### **Error Handler Workflow**

#### **Error_Handler_Workflow.json**
- **Purpose:** Centralized error handling
- **Features:**
  - Standardized error responses
  - Error type classification
  - Recovery suggestions
  - Retry logic
  - Error logging

### **Simplification Guide**

#### **SIMPLIFICATION_GUIDE.json**
- **Purpose:** Documentation of simplifications
- **Benefits:**
  - Better error handling
  - Simplified workflow structure
  - Easier maintenance
  - Better error messages
  - Automatic error recovery
  - Reduced complexity

---

## 🛠️ Error Handling

### **Error Handler Utility** (`error_handler.js`)

Centralized error handling class with:

- **Error Classification:**
  - Network errors
  - Timeout errors
  - Client errors (4xx)
  - Server errors (5xx)
  - Not found errors
  - Authentication errors
  - Validation errors
  - Unknown errors

- **Recovery Features:**
  - Recovery suggestions per error type
  - Retry logic for retryable errors
  - Retry delay calculation
  - Input validation
  - Standardized success responses

- **Error Response Format:**
```json
{
  "success": false,
  "error": {
    "message": "Error message",
    "type": "error_type",
    "code": "ERROR_CODE",
    "timestamp": "2025-01-15T00:00:00.000Z",
    "executionId": "execution_id",
    "workflowName": "workflow_name",
    "context": {}
  },
  "recovery": {
    "suggestions": ["suggestion1", "suggestion2"],
    "canRetry": true,
    "retryAfter": 5
  }
}
```

---

## 🔌 Integration Points

### **External Services:**

1. **AI Services:**
   - OpenAI (GPT-4o Mini)
   - Google Gemini 1.5 Pro
   - Perplexity AI

2. **Google Services:**
   - Google Drive
   - Google Sheets
   - Google Docs
   - Vertex AI

3. **Other Services:**
   - Telegram Bot
   - OCR.space
   - DataDrivenConstruction.io

### **Internal Services:**

1. **FastAPI Backend:**
   - REST API endpoints
   - WebSocket connections
   - File processing
   - Database operations

2. **Storage:**
   - PostgreSQL (database)
   - Redis (cache)
   - Qdrant (vector DB)
   - Google Drive (file storage)

---

## 📖 Usage Guide

### **1. Starting a Workflow**

#### **Via Webhook:**
```bash
curl -X POST http://localhost:5678/webhook/construction-ai \
  -H "Content-Type: application/json" \
  -d '{
    "requestType": "convert",
    "fileExtension": ".rvt",
    "file": {
      "url": "https://example.com/file.rvt"
    }
  }'
```

#### **Via Manual Trigger:**
1. Open n8n interface
2. Navigate to the workflow
3. Click "Execute Workflow"
4. Provide input data

### **2. Request Format**

```json
{
  "requestType": "convert|validate|classify|estimate_cost|carbon_footprint|quantity_takeoff|extract_data|materials|generate_document|file_management|vendor|compliance|visualization|bim|scheduling|3d_vision",
  "fileExtension": ".rvt|.ifc|.dwg|.dgn|.pdf|.jpg|.png|.docx|.xlsx|.csv",
  "file": {
    "url": "file_url",
    "name": "file_name",
    "type": "file_type"
  },
  "options": {
    "outputFormat": "format",
    "quality": "high|medium|low"
  }
}
```

### **3. Response Format**

#### **Success Response:**
```json
{
  "success": true,
  "data": {
    "result": "processing_result",
    "file": "output_file_url",
    "metadata": {}
  },
  "message": "Operation completed successfully",
  "timestamp": "2025-01-15T00:00:00.000Z",
  "executionId": "execution_id"
}
```

#### **Error Response:**
```json
{
  "success": false,
  "error": {
    "message": "Error message",
    "type": "error_type",
    "code": "ERROR_CODE",
    "timestamp": "2025-01-15T00:00:00.000Z",
    "executionId": "execution_id",
    "workflowName": "workflow_name"
  },
  "recovery": {
    "suggestions": ["suggestion1", "suggestion2"],
    "canRetry": true,
    "retryAfter": 5
  }
}
```

---

## 📊 Workflow Statistics

### **Total Workflows:** 45+
- **CAD-BIM:** 12 workflows
- **Construction:** 13 workflows
- **Unified:** 16 workflows
- **Simplified:** 3 workflows

### **Total Nodes:** 200+ nodes across all workflows

### **Integration Points:** 8+ external services

### **Supported File Formats:**
- CAD/BIM: `.rvt`, `.ifc`, `.dwg`, `.dgn`
- Documents: `.pdf`, `.docx`
- Images: `.jpg`, `.png`
- Data: `.xlsx`, `.csv`

---

## 🎯 Key Features

### **1. Intelligent Routing**
- Automatic request analysis
- Priority-based routing
- Multi-agent support
- Fallback mechanisms

### **2. Error Handling**
- Centralized error handling
- Error type classification
- Recovery suggestions
- Retry logic

### **3. Scalability**
- Parallel processing
- Batch operations
- Real-time updates
- WebSocket support

### **4. Integration**
- Multiple AI providers
- Google services integration
- External API support
- Internal service integration

### **5. Monitoring**
- Activity logging
- Analytics tracking
- Error logging
- Performance metrics

---

## 🔧 Configuration

### **Required Credentials:**

1. **Google APIs:**
   - Google Drive API
   - Google Sheets API
   - Google Docs API
   - Vertex AI API

2. **AI Services:**
   - OpenAI API key
   - Perplexity AI API key
   - Google Gemini API key

3. **Other Services:**
   - Telegram Bot token
   - OCR.space API key
   - DataDrivenConstruction.io credentials

### **Environment Variables:**

```bash
# N8N Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password

# API Endpoints
FASTAPI_URL=http://localhost:8000
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
```

---

## 📝 Notes

- All workflows are designed for the Estonian construction market
- Currency: EUR
- Units: Metric (m, m², m³, kg, tons)
- Standards: EVS-EN European standards
- Suppliers: K-Rauta, Bauhof, Stokker, Ehituse ABC, Betoonimeister

---

## 🚀 Next Steps

1. **Import Workflows:**
   - Import workflows into n8n
   - Configure credentials
   - Test individual workflows

2. **Setup Master Agent:**
   - Import unified master agent
   - Configure routing logic
   - Test webhook endpoint

3. **Configure Integrations:**
   - Setup Google APIs
   - Configure AI services
   - Test external services

4. **Monitor & Optimize:**
   - Monitor workflow execution
   - Optimize performance
   - Update workflows as needed

---

**📅 Last Updated:** 2025-01-15  
**🔄 Status:** All workflows documented and ready for use  
**📊 Coverage:** Complete overview of all 45+ workflows

