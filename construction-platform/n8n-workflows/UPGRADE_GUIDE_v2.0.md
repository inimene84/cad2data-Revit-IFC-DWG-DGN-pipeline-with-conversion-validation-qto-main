# 🔄 N8N Workflows Upgrade Guide v2.0

**Upgrade Date:** 2025-01-15  
**Version:** 2.0.0  
**Status:** ✅ Complete

---

## 📋 Overview

This guide documents the upgrades made to the n8n workflows for the Construction AI Platform, specifically enhanced for working with new construction projects. All workflows have been upgraded with project context support, enhanced error handling, and improved monitoring capabilities.

---

## 🆕 New Features

### **1. Project Context Support**

All workflows now support project context, allowing you to:
- Track which project a request belongs to
- Filter and organize data by project
- Apply project-specific settings and configurations
- Generate project-specific reports and analytics

**How to Use:**
```json
{
  "requestType": "convert",
  "fileExtension": ".rvt",
  "projectId": "proj_123",
  "projectName": "New Office Building",
  "projectPhase": "design",
  "userId": "user_456",
  "tenantId": "tenant_789"
}
```

Or via HTTP Headers:
```http
POST /webhook/construction-ai
X-Project-ID: proj_123
X-Project-Name: New Office Building
X-User-ID: user_456
X-Tenant-ID: tenant_789
```

### **2. Enhanced Error Handling**

Error handler now includes:
- Project context in error logs
- User and tenant tracking
- Workflow version tracking
- Enhanced recovery suggestions
- Better error categorization

### **3. Multi-Tenant Support**

Workflows now support:
- Tenant isolation
- Tenant-specific configurations
- Tenant-level analytics
- Tenant-aware error handling

### **4. Execution Tracking**

Each execution now includes:
- Unique execution ID (includes project ID if available)
- Workflow version tracking
- Project context flag
- Timestamp and metadata

---

## 🔧 Upgraded Workflows

### **1. Unified Master Agent (`00_Unified_Master_Agent.json`)**

**Upgrade:** v1.0.0 → v2.0.0

**Changes:**
- ✅ Added project context extraction from body, query, and headers
- ✅ Enhanced routing with project context
- ✅ Added execution ID generation with project ID
- ✅ Added workflow version tracking
- ✅ Improved metadata output

**Usage Example:**
```json
{
  "requestType": "convert",
  "fileExtension": ".rvt",
  "file": {
    "url": "https://example.com/file.rvt"
  },
  "projectId": "proj_123",
  "projectName": "New Office Building",
  "projectPhase": "design"
}
```

### **2. Error Handler (`error_handler.js`)**

**Upgrade:** v1.0.0 → v2.0.0

**Changes:**
- ✅ Added project context support
- ✅ Enhanced error logging with project/user/tenant info
- ✅ Added workflow version tracking
- ✅ Improved error categorization

**Usage:**
```javascript
const handler = new ErrorHandler({
  projectId: 'proj_123',
  projectName: 'New Office Building',
  userId: 'user_456',
  tenantId: 'tenant_789',
  workflowName: 'Conversion Workflow'
});

const errorResponse = handler.handleError(error, { additionalContext: 'value' });
```

### **3. Workflow Registry (`workflow_registry.json`)**

**Upgrade:** v1.0.0 → v2.0.0

**Changes:**
- ✅ Added upgrade metadata
- ✅ Version tracking
- ✅ Feature list documentation

---

## 📁 New Files

### **1. Project Configuration (`project-config.json`)**

**Purpose:** Centralized project configuration template

**Features:**
- Default project settings
- Project template for new projects
- Workflow priorities per project
- Integration configurations
- Error handling settings

**Usage:**
1. Copy the template section
2. Replace `{{PLACEHOLDER}}` values with actual project data
3. Save as `project-{PROJECT_ID}-config.json`
4. Reference in workflow execution

---

## 🚀 Migration Guide

### **Step 1: Update Workflow Imports**

1. Import the upgraded `00_Unified_Master_Agent.json` into n8n
2. Update any existing workflows that reference the old master agent
3. Configure credentials if needed

### **Step 2: Update API Calls**

Update your API calls to include project context:

**Before:**
```json
{
  "requestType": "convert",
  "fileExtension": ".rvt"
}
```

**After:**
```json
{
  "requestType": "convert",
  "fileExtension": ".rvt",
  "projectId": "proj_123",
  "projectName": "New Office Building",
  "projectPhase": "design",
  "userId": "user_456"
}
```

### **Step 3: Configure Project Settings**

1. Review `project-config.json`
2. Create project-specific configuration files
3. Update workflow priorities if needed
4. Configure integrations per project

### **Step 4: Update Error Handling**

If using custom error handling, update to use the new ErrorHandler:

```javascript
// Before
const handler = new ErrorHandler({
  executionId: 'exec_123',
  workflowName: 'My Workflow'
});

// After
const handler = new ErrorHandler({
  executionId: 'exec_123',
  workflowName: 'My Workflow',
  projectId: 'proj_123',
  projectName: 'New Office Building',
  userId: 'user_456',
  tenantId: 'tenant_789'
});
```

---

## 📊 Request/Response Format

### **Request Format (Enhanced)**

```json
{
  "requestType": "convert|validate|classify|estimate_cost|carbon_footprint|quantity_takeoff|extract_data|materials|generate_document|file_management|vendor|compliance|visualization|bim|scheduling|3d_vision",
  "fileExtension": ".rvt|.ifc|.dwg|.dgn|.pdf|.jpg|.png|.docx|.xlsx|.csv",
  "file": {
    "url": "file_url",
    "name": "file_name",
    "type": "file_type"
  },
  "project": {
    "id": "project_id",
    "name": "project_name",
    "phase": "project_phase"
  },
  "user": {
    "id": "user_id"
  },
  "tenant": {
    "id": "tenant_id"
  },
  "options": {
    "outputFormat": "format",
    "quality": "high|medium|low"
  }
}
```

### **Response Format (Enhanced)**

```json
{
  "success": true,
  "data": {
    "result": "processing_result",
    "file": "output_file_url",
    "metadata": {}
  },
  "project": {
    "id": "project_id",
    "name": "project_name",
    "phase": "project_phase"
  },
  "metadata": {
    "executionId": "project_id_1234567890",
    "workflowVersion": "2.0.0",
    "hasProjectContext": true,
    "timestamp": "2025-01-15T00:00:00.000Z"
  },
  "message": "Operation completed successfully"
}
```

---

## 🔍 Testing

### **Test with Project Context:**

```bash
curl -X POST http://localhost:5678/webhook/construction-ai \
  -H "Content-Type: application/json" \
  -H "X-Project-ID: proj_test_123" \
  -H "X-Project-Name: Test Project" \
  -d '{
    "requestType": "convert",
    "fileExtension": ".rvt",
    "file": {
      "url": "https://example.com/test.rvt"
    }
  }'
```

### **Test without Project Context (Backward Compatible):**

```bash
curl -X POST http://localhost:5678/webhook/construction-ai \
  -H "Content-Type: application/json" \
  -d '{
    "requestType": "convert",
    "fileExtension": ".rvt",
    "file": {
      "url": "https://example.com/test.rvt"
    }
  }'
```

---

## ⚠️ Breaking Changes

### **None!**

This upgrade is **fully backward compatible**. Existing workflows and API calls will continue to work without project context. The project context features are optional and enhance functionality when provided.

---

## 📝 Configuration

### **Project Configuration**

Create a project-specific configuration file:

```json
{
  "id": "proj_123",
  "name": "New Office Building",
  "phase": "design",
  "settings": {
    "timezone": "Europe/Tallinn",
    "currency": "EUR",
    "units": "metric",
    "locale": "et-EE",
    "standards": ["EVS-EN"],
    "suppliers": ["K-Rauta", "Bauhof", "Stokker"]
  }
}
```

### **Environment Variables**

No new environment variables required. Existing configuration continues to work.

---

## 🎯 Best Practices

1. **Always Include Project Context:**
   - Provides better tracking and analytics
   - Enables project-specific configurations
   - Improves error handling and debugging

2. **Use Consistent Project IDs:**
   - Use a naming convention (e.g., `proj_123`, `project_abc`)
   - Keep project IDs unique across tenants

3. **Set Project Phase:**
   - Helps with workflow routing and priority
   - Enables phase-specific processing

4. **Include User Context:**
   - Enables user-level analytics
   - Improves audit logging
   - Helps with permission checking

5. **Log Project Context:**
   - All errors now include project context
   - Use this for debugging and monitoring
   - Filter logs by project ID

---

## 📚 Additional Resources

- **N8N Workflows Overview:** See `N8N_WORKFLOWS_OVERVIEW.md`
- **Project Configuration:** See `project-config.json`
- **Error Handling:** See `unified/error_handler.js`
- **Workflow Registry:** See `unified/workflow_registry.json`

---

## ✅ Upgrade Checklist

- [x] Unified Master Agent upgraded to v2.0.0
- [x] Error Handler enhanced with project context
- [x] Workflow Registry updated with upgrade metadata
- [x] Project Configuration template created
- [x] Upgrade guide documentation created
- [x] Backward compatibility maintained
- [x] Testing examples provided

---

**📅 Last Updated:** 2025-01-15  
**🔄 Version:** 2.0.0  
**✅ Status:** Complete and Ready for Use

