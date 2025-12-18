#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Unified Master Workflow for Construction Platform
Combines all n8n workflows into one master agent system
"""

import json
import os
import sys
import io
from pathlib import Path
from typing import Dict, List, Any

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class UnifiedWorkflowBuilder:
    def __init__(self, workflows_dir):
        self.workflows_dir = Path(workflows_dir)
        self.cad_bim_dir = self.workflows_dir / "cad-bim"
        self.construction_dir = self.workflows_dir / "construction"
        self.output_dir = self.workflows_dir / "unified"
        self.output_dir.mkdir(exist_ok=True)
        
        # Agent registry
        self.agents = {
            "cad_bim_conversion": [],
            "cad_bim_validation": [],
            "cad_bim_classification": [],
            "cad_bim_cost_estimation": [],
            "cad_bim_carbon_footprint": [],
            "cad_bim_quantity_takeoff": [],
            "construction_data_extraction": [],
            "construction_materials": [],
            "construction_documents": [],
            "construction_file_management": [],
            "construction_vendor": [],
            "construction_compliance": [],
            "construction_visualization": [],
            "construction_bim": [],
            "construction_scheduling": [],
            "construction_3d_vision": [],
        }
        
    def load_workflow(self, file_path):
        """Load a workflow JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def categorize_workflow(self, workflow_name, workflow_data):
        """Categorize workflow by functionality"""
        name_lower = workflow_name.lower()
        
        # CAD-BIM Conversion
        if "conversation" in name_lower or "conversion" in name_lower or "extract" in name_lower:
            if "simple" in name_lower:
                return "cad_bim_conversion"
            elif "batch" in name_lower:
                return "cad_bim_conversion"
            elif "extract" in name_lower:
                return "cad_bim_conversion"
        
        # CAD-BIM Validation
        if "validation" in name_lower:
            return "cad_bim_validation"
        
        # CAD-BIM Classification
        if "classification" in name_lower or "rag" in name_lower:
            return "cad_bim_classification"
        
        # CAD-BIM Cost Estimation
        if "price" in name_lower or "cost" in name_lower or "estimation" in name_lower:
            return "cad_bim_cost_estimation"
        
        # CAD-BIM Carbon Footprint
        if "carbon" in name_lower or "co2" in name_lower or "footprint" in name_lower:
            return "cad_bim_carbon_footprint"
        
        # CAD-BIM Quantity Takeoff
        if "quantity" in name_lower or "qto" in name_lower or "takeoff" in name_lower:
            return "cad_bim_quantity_takeoff"
        
        # Construction Data Extraction
        if "data extraction" in name_lower or "extraction" in name_lower:
            return "construction_data_extraction"
        
        # Construction Materials
        if "materials" in name_lower or "accounting" in name_lower:
            return "construction_materials"
        
        # Construction Documents
        if "document" in name_lower or "generation" in name_lower:
            return "construction_documents"
        
        # Construction File Management
        if "file manager" in name_lower or "file" in name_lower:
            return "construction_file_management"
        
        # Construction Vendor
        if "vendor" in name_lower:
            return "construction_vendor"
        
        # Construction Compliance
        if "compliance" in name_lower:
            return "construction_compliance"
        
        # Construction Visualization
        if "visualization" in name_lower or "visual" in name_lower:
            return "construction_visualization"
        
        # Construction BIM
        if "bim" in name_lower and "agent" in name_lower:
            return "construction_bim"
        
        # Construction Scheduling
        if "schedule" in name_lower or "timeline" in name_lower:
            return "construction_scheduling"
        
        # Construction 3D Vision
        if "3d" in name_lower or "vision" in name_lower:
            return "construction_3d_vision"
        
        # Construction Manager
        if "manager" in name_lower:
            return "construction_manager"
        
        # CAD Data Processor
        if "cad data" in name_lower or "processor" in name_lower:
            return "cad_bim_conversion"
        
        return "other"
    
    def analyze_workflows(self):
        """Analyze all workflows and categorize them"""
        print("Analyzing workflows...")
        
        # Analyze CAD-BIM workflows
        for workflow_file in self.cad_bim_dir.glob("*.json"):
            workflow_data = self.load_workflow(workflow_file)
            if workflow_data:
                workflow_name = workflow_data.get("name", workflow_file.stem)
                category = self.categorize_workflow(workflow_name, workflow_data)
                
                if category in self.agents:
                    self.agents[category].append({
                        "name": workflow_name,
                        "file": workflow_file.name,
                        "path": str(workflow_file),
                        "id": workflow_file.stem,
                        "type": "cad_bim"
                    })
                else:
                    if "other" not in self.agents:
                        self.agents["other"] = []
                    self.agents["other"].append({
                        "name": workflow_name,
                        "file": workflow_file.name,
                        "path": str(workflow_file),
                        "id": workflow_file.stem,
                        "type": "cad_bim"
                    })
        
        # Analyze Construction workflows
        for workflow_file in self.construction_dir.glob("*.json"):
            if workflow_file.name == "CONSTRUCTION_SYSTEM_SUMMARY.json":
                continue
                
            workflow_data = self.load_workflow(workflow_file)
            if workflow_data:
                workflow_name = workflow_data.get("name", workflow_file.stem)
                category = self.categorize_workflow(workflow_name, workflow_data)
                
                if category in self.agents:
                    self.agents[category].append({
                        "name": workflow_name,
                        "file": workflow_file.name,
                        "path": str(workflow_file),
                        "id": workflow_file.stem,
                        "type": "construction"
                    })
                else:
                    if "other" not in self.agents:
                        self.agents["other"] = []
                    self.agents["other"].append({
                        "name": workflow_name,
                        "file": workflow_file.name,
                        "path": str(workflow_file),
                        "id": workflow_file.stem,
                        "type": "construction"
                    })
        
        # Print summary
        print("\nWorkflow Analysis:")
        for category, workflows in self.agents.items():
            if workflows:
                print(f"  {category}: {len(workflows)} workflows")
                for wf in workflows:
                    # Remove emojis for Windows console compatibility
                    name = wf['name'].encode('ascii', 'ignore').decode('ascii')
                    print(f"    - {name}")
    
    def create_unified_master_workflow(self):
        """Create unified master workflow"""
        print("\nCreating unified master workflow...")
        
        # Master workflow structure
        master_workflow = {
            "name": "🏗️ Unified Construction AI Platform - Master Agent",
            "nodes": [],
            "connections": {},
            "pinData": {},
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True,
                "saveDataErrorExecution": "all",
                "saveDataSuccessExecution": "all",
                "saveExecutionProgress": False,
                "timezone": "Europe/Tallinn"
            },
            "staticData": {},
            "tags": [
                {"id": "unified", "name": "unified"},
                {"id": "master", "name": "master"},
                {"id": "construction", "name": "construction"},
                {"id": "cad_bim", "name": "cad_bim"}
            ],
            "triggerCount": 1,
            "updatedAt": "2025-01-15T00:00:00.000Z",
            "versionId": "1.0.0"
        }
        
        # Node positions
        x_start = 240
        y_start = 300
        x_spacing = 300
        y_spacing = 200
        
        # 1. Manual Trigger (for testing) + Webhook Trigger (for production)
        manual_trigger = {
            "parameters": {},
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [x_start, y_start],
            "id": "manual-trigger-001",
            "name": "Manual Trigger"
        }
        
        webhook_trigger = {
            "parameters": {
                "httpMethod": "POST",
                "path": "construction-ai",
                "responseMode": "responseNode",
                "options": {}
            },
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [x_start, y_start + 100],
            "id": "webhook-trigger-001",
            "name": "Webhook Trigger",
            "webhookId": "unified-construction-webhook"
        }
        
        # 2. Input Router - Route requests to appropriate agents
        input_router = {
            "parameters": {
                "mode": "combine",
                "combinationMode": "multiplex"
            },
            "type": "n8n-nodes-base.merge",
            "typeVersion": 2.1,
            "position": [x_start + x_spacing, y_start],
            "id": "input-router-001",
            "name": "Input Router"
        }
        
        # 3. Request Analyzer - Analyze input and determine which agents to call
        request_analyzer = {
            "parameters": {
                "jsCode": """
// Unified Construction AI Platform - Request Analyzer
// Analyzes input and routes to appropriate agents

const input = $input.first().json;
const body = input.body || input;
const query = input.query || {};
const headers = input.headers || {};

// Extract request type
const requestType = body.requestType || body.type || query.type || 'unknown';
const fileType = body.fileType || body.file?.type || query.fileType || '';
const action = body.action || query.action || 'process';
const fileExtension = body.fileExtension || body.file?.extension || query.fileExtension || '';

// Determine file category
let fileCategory = 'unknown';
if (fileExtension) {
    const ext = fileExtension.toLowerCase();
    if (['.rvt', '.ifc', '.dwg', '.dgn'].includes(ext)) {
        fileCategory = 'cad_bim';
    } else if (['.pdf', '.jpg', '.png', '.docx'].includes(ext)) {
        fileCategory = 'document';
    } else if (['.xlsx', '.csv'].includes(ext)) {
        fileCategory = 'data';
    }
}

// Route mapping
const routing = {
    // CAD-BIM Conversion
    cad_bim_conversion: {
        agents: ['cad_bim_conversion'],
        priority: 1,
        conditions: [
            fileCategory === 'cad_bim',
            requestType === 'convert',
            action === 'convert',
            fileExtension.match(/\\.(rvt|ifc|dwg|dgn)$/i)
        ]
    },
    
    // CAD-BIM Validation
    cad_bim_validation: {
        agents: ['cad_bim_validation'],
        priority: 2,
        conditions: [
            requestType === 'validate',
            action === 'validate',
            body.validation !== undefined
        ]
    },
    
    // CAD-BIM Classification
    cad_bim_classification: {
        agents: ['cad_bim_classification'],
        priority: 3,
        conditions: [
            requestType === 'classify',
            action === 'classify',
            body.classification !== undefined
        ]
    },
    
    // CAD-BIM Cost Estimation
    cad_bim_cost_estimation: {
        agents: ['cad_bim_cost_estimation'],
        priority: 4,
        conditions: [
            requestType === 'estimate_cost',
            action === 'estimate_cost',
            body.costEstimation !== undefined
        ]
    },
    
    // CAD-BIM Carbon Footprint
    cad_bim_carbon_footprint: {
        agents: ['cad_bim_carbon_footprint'],
        priority: 5,
        conditions: [
            requestType === 'carbon_footprint',
            action === 'carbon_footprint',
            body.carbonFootprint !== undefined
        ]
    },
    
    // CAD-BIM Quantity Takeoff
    cad_bim_quantity_takeoff: {
        agents: ['cad_bim_quantity_takeoff'],
        priority: 6,
        conditions: [
            requestType === 'quantity_takeoff',
            action === 'quantity_takeoff',
            body.quantityTakeoff !== undefined
        ]
    },
    
    // Construction Data Extraction
    construction_data_extraction: {
        agents: ['construction_data_extraction'],
        priority: 7,
        conditions: [
            requestType === 'extract_data',
            action === 'extract_data',
            fileCategory === 'document'
        ]
    },
    
    // Construction Materials
    construction_materials: {
        agents: ['construction_materials'],
        priority: 8,
        conditions: [
            requestType === 'materials',
            action === 'materials',
            body.materials !== undefined
        ]
    },
    
    // Construction Documents
    construction_documents: {
        agents: ['construction_documents'],
        priority: 9,
        conditions: [
            requestType === 'generate_document',
            action === 'generate_document',
            body.documentGeneration !== undefined
        ]
    },
    
    // Construction File Management
    construction_file_management: {
        agents: ['construction_file_management'],
        priority: 10,
        conditions: [
            requestType === 'file_management',
            action === 'file_management',
            body.fileManagement !== undefined
        ]
    },
    
    // Construction Vendor
    construction_vendor: {
        agents: ['construction_vendor'],
        priority: 11,
        conditions: [
            requestType === 'vendor',
            action === 'vendor',
            body.vendor !== undefined
        ]
    },
    
    // Construction Compliance
    construction_compliance: {
        agents: ['construction_compliance'],
        priority: 12,
        conditions: [
            requestType === 'compliance',
            action === 'compliance',
            body.compliance !== undefined
        ]
    },
    
    // Construction Visualization
    construction_visualization: {
        agents: ['construction_visualization'],
        priority: 13,
        conditions: [
            requestType === 'visualization',
            action === 'visualization',
            body.visualization !== undefined
        ]
    },
    
    // Construction BIM
    construction_bim: {
        agents: ['construction_bim'],
        priority: 14,
        conditions: [
            requestType === 'bim',
            action === 'bim',
            body.bim !== undefined
        ]
    },
    
    // Construction Scheduling
    construction_scheduling: {
        agents: ['construction_scheduling'],
        priority: 15,
        conditions: [
            requestType === 'scheduling',
            action === 'scheduling',
            body.scheduling !== undefined
        ]
    },
    
    // Construction 3D Vision
    construction_3d_vision: {
        agents: ['construction_3d_vision'],
        priority: 16,
        conditions: [
            requestType === '3d_vision',
            action === '3d_vision',
            body.vision3d !== undefined
        ]
    }
};

// Find matching route
let selectedRoute = null;
let maxPriority = 0;

for (const [routeName, routeConfig] of Object.entries(routing)) {
    const matchCount = routeConfig.conditions.filter(c => c === true).length;
    if (matchCount > 0 && routeConfig.priority > maxPriority) {
        selectedRoute = routeName;
        maxPriority = routeConfig.priority;
    }
}

// Default route if no match
if (!selectedRoute) {
    selectedRoute = 'cad_bim_conversion'; // Default to conversion
}

// Prepare output
const output = {
    route: selectedRoute,
    agents: routing[selectedRoute]?.agents || ['cad_bim_conversion'],
    requestType: requestType,
    fileType: fileType,
    fileCategory: fileCategory,
    action: action,
    originalInput: body,
    metadata: {
        timestamp: new Date().toISOString(),
        priority: maxPriority,
        confidence: maxPriority > 0 ? 'high' : 'low'
    }
};

return [{ json: output }];
"""
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [x_start + x_spacing * 2, y_start],
            "id": "request-analyzer-001",
            "name": "Request Analyzer"
        }
        
        # 4. Agent Router - Route to specific agents based on analysis
        agent_router = {
            "parameters": {
                "rules": {
                    "values": [
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict"
                                },
                                "conditions": [
                                    {
                                        "id": "route-cad-bim-conversion",
                                        "leftValue": "={{ $json.route }}",
                                        "rightValue": "cad_bim_conversion",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            },
                            "renameOutput": True,
                            "outputKey": "CAD-BIM Conversion"
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict"
                                },
                                "conditions": [
                                    {
                                        "id": "route-cad-bim-validation",
                                        "leftValue": "={{ $json.route }}",
                                        "rightValue": "cad_bim_validation",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            },
                            "renameOutput": True,
                            "outputKey": "CAD-BIM Validation"
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict"
                                },
                                "conditions": [
                                    {
                                        "id": "route-cad-bim-classification",
                                        "leftValue": "={{ $json.route }}",
                                        "rightValue": "cad_bim_classification",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            },
                            "renameOutput": True,
                            "outputKey": "CAD-BIM Classification"
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict"
                                },
                                "conditions": [
                                    {
                                        "id": "route-cad-bim-cost-estimation",
                                        "leftValue": "={{ $json.route }}",
                                        "rightValue": "cad_bim_cost_estimation",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            },
                            "renameOutput": True,
                            "outputKey": "CAD-BIM Cost Estimation"
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict"
                                },
                                "conditions": [
                                    {
                                        "id": "route-construction-data-extraction",
                                        "leftValue": "={{ $json.route }}",
                                        "rightValue": "construction_data_extraction",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            },
                            "renameOutput": True,
                            "outputKey": "Construction Data Extraction"
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict"
                                },
                                "conditions": [
                                    {
                                        "id": "route-construction-materials",
                                        "leftValue": "={{ $json.route }}",
                                        "rightValue": "construction_materials",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals"
                                        }
                                    }
                                ]
                            },
                            "renameOutput": True,
                            "outputKey": "Construction Materials"
                        }
                    ]
                },
                "options": {
                    "fallbackOutput": "default"
                }
            },
            "type": "n8n-nodes-base.switch",
            "typeVersion": 3.2,
            "position": [x_start + x_spacing * 3, y_start],
            "id": "agent-router-001",
            "name": "Agent Router"
        }
        
        # Add nodes to workflow
        master_workflow["nodes"].extend([
            manual_trigger,
            webhook_trigger,
            input_router,
            request_analyzer,
            agent_router
        ])
        
        # Add connections
        master_workflow["connections"] = {
            "Manual Trigger": {
                "main": [[{"node": "Input Router", "type": "main", "index": 0}]]
            },
            "Webhook Trigger": {
                "main": [[{"node": "Input Router", "type": "main", "index": 0}]]
            },
            "Input Router": {
                "main": [[{"node": "Request Analyzer", "type": "main", "index": 0}]]
            },
            "Request Analyzer": {
                "main": [[{"node": "Agent Router", "type": "main", "index": 0}]]
            }
        }
        
        # Save master workflow
        master_workflow_path = self.output_dir / "00_Unified_Master_Agent.json"
        with open(master_workflow_path, 'w', encoding='utf-8') as f:
            json.dump(master_workflow, f, indent=2, ensure_ascii=False)
        
        print(f"Created master workflow: {master_workflow_path}")
        return master_workflow_path
    
    def create_agent_workflows(self):
        """Create agent workflows that can be called by master workflow"""
        print("\nCreating agent workflows...")
        
        # For each category, create a unified agent workflow
        for category, workflows in self.agents.items():
            if not workflows:
                continue
            
            # Create agent workflow
            agent_workflow = {
                "name": f"Agent: {category.replace('_', ' ').title()}",
                "nodes": [],
                "connections": {},
                "settings": {
                    "executionOrder": "v1",
                    "saveManualExecutions": True
                },
                "tags": [
                    {"id": "agent", "name": "agent"},
                    {"id": category, "name": category}
                ]
            }
            
            # Add execute workflow trigger
            trigger_node = {
                "parameters": {},
                "type": "n8n-nodes-base.executeWorkflowTrigger",
                "typeVersion": 1,
                "position": [240, 300],
                "id": f"{category}-trigger-001",
                "name": "Called by Master"
            }
            
            agent_workflow["nodes"].append(trigger_node)
            
            # For now, create a placeholder that will call the actual workflows
            # In production, these would be Execute Workflow nodes
            
            # Save agent workflow
            agent_workflow_path = self.output_dir / f"Agent_{category}.json"
            with open(agent_workflow_path, 'w', encoding='utf-8') as f:
                json.dump(agent_workflow, f, indent=2, ensure_ascii=False)
            
            print(f"Created agent workflow: {agent_workflow_path}")
    
    def create_workflow_registry(self):
        """Create workflow registry with all workflows"""
        print("\nCreating workflow registry...")
        
        registry = {
            "version": "1.0.0",
            "created_at": "2025-01-15T00:00:00.000Z",
            "workflows": {},
            "agents": {}
        }
        
        # Add all workflows to registry
        for category, workflows in self.agents.items():
            if workflows:
                registry["agents"][category] = {
                    "name": category.replace('_', ' ').title(),
                    "workflows": workflows,
                    "count": len(workflows)
                }
        
        # Save registry
        registry_path = self.output_dir / "workflow_registry.json"
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        
        print(f"Created workflow registry: {registry_path}")
        return registry_path
    
    def run(self):
        """Run the unified workflow builder"""
        print("=" * 60)
        print("Unified Construction AI Platform - Workflow Builder")
        print("=" * 60)
        
        # Analyze workflows
        self.analyze_workflows()
        
        # Create unified master workflow
        self.create_unified_master_workflow()
        
        # Create agent workflows
        self.create_agent_workflows()
        
        # Create workflow registry
        self.create_workflow_registry()
        
        print("\n" + "=" * 60)
        print("Unified workflow creation complete!")
        print("=" * 60)
        print(f"\nOutput directory: {self.output_dir}")
        print("\nNext steps:")
        print("1. Import master workflow into n8n")
        print("2. Import all agent workflows into n8n")
        print("3. Update workflow IDs in master workflow")
        print("4. Configure credentials")
        print("5. Test the unified system")

if __name__ == "__main__":
    workflows_dir = Path(__file__).parent / "construction-platform" / "n8n-workflows"
    
    if not workflows_dir.exists():
        print(f"Error: {workflows_dir} does not exist!")
        print("Run combine_projects.py first to create the project.")
        exit(1)
    
    builder = UnifiedWorkflowBuilder(workflows_dir)
    builder.run()

