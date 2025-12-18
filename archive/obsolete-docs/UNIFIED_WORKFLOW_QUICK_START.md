# 🚀 Unified Workflow System - Quick Start Guide

## 📋 Quick Overview

The unified workflow system combines all 22 n8n workflows into one master agent system without duplication.

---

## 🎯 What You Have

### **1. Master Workflow**
- `00_Unified_Master_Agent.json` - Entry point for all requests

### **2. Agent Workflows (14 agents)**
- `Agent_cad_bim_*.json` - CAD-BIM agents (6 agents)
- `Agent_construction_*.json` - Construction agents (8 agents)

### **3. Workflow Registry**
- `workflow_registry.json` - Maps agents to workflows

---

## 🚀 Quick Start (5 Steps)

### **Step 1: Import to n8n**
```bash
# Import master workflow
Import: 00_Unified_Master_Agent.json

# Import agent workflows
Import: Agent_*.json (14 files)

# Import actual workflows
Import: cad-bim/*.json (12 files)
Import: construction/*.json (13 files)
```

### **Step 2: Get Workflow IDs**
1. Open each workflow in n8n
2. Copy the workflow ID from the URL
3. Update `workflow_registry.json` with actual IDs

### **Step 3: Update Master Workflow**
1. Open `00_Unified_Master_Agent.json` in n8n
2. Add `Execute Workflow` nodes for each agent
3. Set workflow IDs from registry
4. Configure input/output parameters

### **Step 4: Configure Credentials**
1. Set OpenAI API key
2. Set Google Vertex AI credentials
3. Set Telegram Bot credentials
4. Set Google Drive credentials

### **Step 5: Test**
1. Test master workflow with manual trigger
2. Test each agent individually
3. Test end-to-end workflows

---

## 📊 Usage Examples

### **Example 1: CAD-BIM Conversion**
```json
{
  "requestType": "convert",
  "fileType": "rvt",
  "fileExtension": ".rvt",
  "fileId": "GOOGLE_DRIVE_FILE_ID"
}
```

### **Example 2: Cost Estimation**
```json
{
  "requestType": "estimate_cost",
  "projectName": "My Project",
  "fileName": "project.xlsx"
}
```

### **Example 3: Data Extraction**
```json
{
  "requestType": "extract_data",
  "fileType": "pdf",
  "fileExtension": ".pdf",
  "fileId": "GOOGLE_DRIVE_FILE_ID"
}
```

---

## 🔧 API Endpoints

### **Webhook Endpoint**
```
POST /construction-ai
```

### **Request Body**
```json
{
  "requestType": "convert",
  "fileType": "rvt",
  "fileExtension": ".rvt",
  "fileId": "GOOGLE_DRIVE_FILE_ID"
}
```

### **Response**
```json
{
  "success": true,
  "route": "cad_bim_conversion",
  "agents": ["cad_bim_conversion"],
  "result": {
    "status": "completed",
    "output": "..."
  }
}
```

---

## 📝 Next Steps

1. **Complete Integration:** Follow the implementation checklist in `UNIFIED_WORKFLOW_COMPLETE.md`
2. **Test System:** Test all workflows end-to-end
3. **Deploy:** Deploy to production environment
4. **Monitor:** Set up monitoring and logging

---

**🎉 Ready to use! Follow the steps above to complete the integration.**

