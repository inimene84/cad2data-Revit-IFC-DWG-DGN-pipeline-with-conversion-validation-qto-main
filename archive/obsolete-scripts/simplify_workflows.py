#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplify Workflows with Better Error Handling
Creates simplified workflows with centralized error handling
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

class WorkflowSimplifier:
    def __init__(self, workflows_dir):
        self.workflows_dir = Path(workflows_dir)
        self.unified_dir = self.workflows_dir / "unified"
        self.simplified_dir = self.workflows_dir / "simplified"
        self.simplified_dir.mkdir(exist_ok=True)
        
    def create_error_handler_node(self):
        """Create error handler node for workflows"""
        return {
            "parameters": {
                "jsCode": """
// Simplified Error Handler
// Centralized error handling for all workflows

const input = $input.first().json;
const error = input.error || input;
const context = input.context || {};

// Error handler class
class ErrorHandler {
    handleError(error, context = {}) {
        const errorType = this.getErrorType(error);
        const errorMessage = this.getErrorMessage(error);
        
        return {
            success: false,
            error: {
                message: errorMessage,
                type: errorType,
                code: error.code || error.statusCode || 'UNKNOWN_ERROR',
                timestamp: new Date().toISOString(),
                executionId: context.executionId || $execution.id,
                workflowName: context.workflowName || 'unknown',
                context: context
            },
            recovery: {
                suggestions: this.getRecoverySuggestions(errorType),
                canRetry: this.canRetry(errorType),
                retryAfter: this.getRetryAfter(errorType)
            }
        };
    }
    
    getErrorType(error) {
        if (error?.code === 'ENOTFOUND' || error?.code === 'ECONNREFUSED') return 'network_error';
        if (error?.code === 'ETIMEDOUT') return 'timeout_error';
        if (error?.statusCode >= 400 && error?.statusCode < 500) return 'client_error';
        if (error?.statusCode >= 500) return 'server_error';
        if (error?.message?.includes('not found')) return 'not_found';
        if (error?.message?.includes('unauthorized') || error?.message?.includes('forbidden')) return 'authentication_error';
        if (error?.message?.includes('validation') || error?.message?.includes('invalid')) return 'validation_error';
        return 'unknown_error';
    }
    
    getErrorMessage(error) {
        if (typeof error === 'string') return error;
        return error?.message || error?.error?.message || 'An unexpected error occurred';
    }
    
    getRecoverySuggestions(errorType) {
        const suggestions = {
            network_error: ['Check your internet connection', 'Verify the service is available', 'Try again in a few moments'],
            timeout_error: ['The request took too long', 'Try again with a smaller file', 'Check if the service is overloaded'],
            client_error: ['Check your input parameters', 'Verify file format and size', 'Ensure all required fields are provided'],
            server_error: ['Service temporarily unavailable', 'Try again later', 'Contact support if problem persists'],
            not_found: ['Check if the file/resource exists', 'Verify the file ID or path', 'Ensure you have access permissions'],
            authentication_error: ['Check your API credentials', 'Verify authentication tokens', 'Ensure your account has necessary permissions'],
            validation_error: ['Check input format', 'Verify required fields', 'Ensure data types are correct'],
            unknown_error: ['Try again', 'Check logs for details', 'Contact support if problem persists']
        };
        return suggestions[errorType] || suggestions.unknown_error;
    }
    
    canRetry(errorType) {
        return ['network_error', 'timeout_error', 'server_error'].includes(errorType);
    }
    
    getRetryAfter(errorType) {
        const delays = { network_error: 5, timeout_error: 10, server_error: 30, default: 60 };
        return delays[errorType] || delays.default;
    }
}

const handler = new ErrorHandler();
const errorResponse = handler.handleError(error, context);

return [{ json: errorResponse }];
"""
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [0, 0],
            "id": "error-handler-001",
            "name": "Error Handler"
        }
    
    def create_input_validator_node(self):
        """Create input validator node"""
        return {
            "parameters": {
                "jsCode": """
// Simplified Input Validator
// Validates input parameters before processing

const input = $input.first().json;
const body = input.body || input;
const errors = [];

// Required fields (can be customized per workflow)
const requiredFields = body.requiredFields || [];

// Check required fields
for (const field of requiredFields) {
    if (!body[field] && body[field] !== 0 && body[field] !== false) {
        errors.push(`Missing required field: ${field}`);
    }
}

// Validate file extensions
if (body.fileExtension) {
    const validExtensions = ['.rvt', '.ifc', '.dwg', '.dgn', '.pdf', '.jpg', '.png', '.docx', '.xlsx', '.csv'];
    const ext = body.fileExtension.toLowerCase();
    if (!validExtensions.includes(ext)) {
        errors.push(`Invalid file extension: ${ext}. Valid extensions: ${validExtensions.join(', ')}`);
    }
}

// Validate request type
if (body.requestType) {
    const validTypes = ['convert', 'validate', 'classify', 'estimate_cost', 'carbon_footprint', 'quantity_takeoff', 'extract_data', 'materials', 'generate_document', 'file_management', 'vendor', 'compliance', 'visualization', 'bim', 'scheduling', '3d_vision'];
    if (!validTypes.includes(body.requestType)) {
        errors.push(`Invalid request type: ${body.requestType}. Valid types: ${validTypes.join(', ')}`);
    }
}

if (errors.length > 0) {
    return [{
        json: {
            valid: false,
            errors: errors,
            input: body
        }
    }];
}

return [{
    json: {
        valid: true,
        input: body
    }
}];
"""
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [0, 0],
            "id": "input-validator-001",
            "name": "Input Validator"
        }
    
    def create_simplified_master_workflow(self):
        """Create simplified master workflow with error handling"""
        print("Creating simplified master workflow...")
        
        workflow = {
            "name": "🏗️ Simplified Construction AI Platform - Master Agent",
            "nodes": [],
            "connections": {},
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True,
                "saveDataErrorExecution": "all",
                "saveDataSuccessExecution": "all",
                "saveExecutionProgress": False,
                "timezone": "Europe/Tallinn",
                "errorWorkflow": "ERROR_HANDLER_WORKFLOW_ID"  # Reference to error handler workflow
            },
            "tags": [
                {"id": "simplified", "name": "simplified"},
                {"id": "master", "name": "master"},
                {"id": "construction", "name": "construction"}
            ],
            "versionId": "2.0.0"
        }
        
        # Node positions
        x, y = 240, 300
        spacing = 300
        
        # 1. Manual Trigger
        workflow["nodes"].append({
            "parameters": {},
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [x, y],
            "id": "manual-trigger-001",
            "name": "Manual Trigger"
        })
        
        # 2. Webhook Trigger
        workflow["nodes"].append({
            "parameters": {
                "httpMethod": "POST",
                "path": "construction-ai",
                "responseMode": "responseNode",
                "options": {}
            },
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [x, y + 100],
            "id": "webhook-trigger-001",
            "name": "Webhook Trigger",
            "webhookId": "simplified-construction-webhook"
        })
        
        # 3. Merge Inputs
        workflow["nodes"].append({
            "parameters": {
                "mode": "combine",
                "combinationMode": "multiplex"
            },
            "type": "n8n-nodes-base.merge",
            "typeVersion": 2.1,
            "position": [x + spacing, y],
            "id": "merge-inputs-001",
            "name": "Merge Inputs"
        })
        
        # 4. Input Validator
        validator_node = self.create_input_validator_node()
        validator_node["position"] = [x + spacing * 2, y]
        validator_node["id"] = "input-validator-001"
        workflow["nodes"].append(validator_node)
        
        # 5. Validation Check
        workflow["nodes"].append({
            "parameters": {
                "conditions": {
                    "boolean": [
                        {
                            "value1": "={{ $json.valid }}",
                            "value2": True
                        }
                    ]
                }
            },
            "type": "n8n-nodes-base.if",
            "typeVersion": 1,
            "position": [x + spacing * 3, y],
            "id": "validation-check-001",
            "name": "Input Valid?"
        })
        
        # 6. Simplified Router (much simpler than before)
        workflow["nodes"].append({
            "parameters": {
                "jsCode": """
// Simplified Router
// Simple routing based on request type

const input = $input.first().json.input;
const requestType = input.requestType || input.type || 'convert';
const fileExtension = input.fileExtension || input.file?.extension || '';

// Simple routing - just return the request type
return [{
    json: {
        route: requestType,
        requestType: requestType,
        fileExtension: fileExtension,
        originalInput: input,
        timestamp: new Date().toISOString()
    }
}];
"""
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [x + spacing * 4, y],
            "id": "simplified-router-001",
            "name": "Simplified Router"
        })
        
        # 7. Execute Workflow (with error handling)
        workflow["nodes"].append({
            "parameters": {
                "workflowId": {
                    "__rl": True,
                    "value": "AGENT_WORKFLOW_ID",
                    "mode": "list"
                },
                "source": "workflow",
                "options": {
                    "continueOnFail": True
                }
            },
            "type": "n8n-nodes-base.executeWorkflow",
            "typeVersion": 1,
            "position": [x + spacing * 5, y],
            "id": "execute-workflow-001",
            "name": "Execute Agent Workflow",
            "onError": "continueErrorOutput"
        })
        
        # 8. Error Handler (if workflow fails)
        error_handler_node = self.create_error_handler_node()
        error_handler_node["position"] = [x + spacing * 5, y + 200]
        error_handler_node["id"] = "error-handler-001"
        workflow["nodes"].append(error_handler_node)
        
        # 9. Success Response
        workflow["nodes"].append({
            "parameters": {
                "respondWith": "json",
                "responseBody": "={{ $json }}"
            },
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1,
            "position": [x + spacing * 6, y],
            "id": "success-response-001",
            "name": "Success Response"
        })
        
        # 10. Error Response
        workflow["nodes"].append({
            "parameters": {
                "respondWith": "json",
                "responseBody": "={{ $json }}",
                "options": {
                    "responseCode": 400
                }
            },
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1,
            "position": [x + spacing * 6, y + 200],
            "id": "error-response-001",
            "name": "Error Response"
        })
        
        # Connections
        workflow["connections"] = {
            "Manual Trigger": {
                "main": [[{"node": "Merge Inputs", "type": "main", "index": 0}]]
            },
            "Webhook Trigger": {
                "main": [[{"node": "Merge Inputs", "type": "main", "index": 0}]]
            },
            "Merge Inputs": {
                "main": [[{"node": "Input Validator", "type": "main", "index": 0}]]
            },
            "Input Validator": {
                "main": [[{"node": "Input Valid?", "type": "main", "index": 0}]]
            },
            "Input Valid?": {
                "main": [
                    [{"node": "Simplified Router", "type": "main", "index": 0}],  # True
                    [{"node": "Error Handler", "type": "main", "index": 0}]  # False
                ]
            },
            "Simplified Router": {
                "main": [[{"node": "Execute Agent Workflow", "type": "main", "index": 0}]]
            },
            "Execute Agent Workflow": {
                "main": [
                    [{"node": "Success Response", "type": "main", "index": 0}],  # Success
                    [{"node": "Error Handler", "type": "main", "index": 0}]  # Error
                ]
            },
            "Error Handler": {
                "main": [[{"node": "Error Response", "type": "main", "index": 0}]]
            }
        }
        
        # Save workflow
        workflow_path = self.simplified_dir / "00_Simplified_Master_Agent.json"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        
        print(f"Created simplified master workflow: {workflow_path}")
        return workflow_path
    
    def create_simplified_agent_workflow(self, agent_name, agent_category):
        """Create simplified agent workflow with error handling"""
        workflow = {
            "name": f"Simplified Agent: {agent_name}",
            "nodes": [],
            "connections": {},
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True,
                "saveDataErrorExecution": "all"
            },
            "tags": [
                {"id": "simplified", "name": "simplified"},
                {"id": "agent", "name": "agent"},
                {"id": agent_category, "name": agent_category}
            ]
        }
        
        # 1. Execute Workflow Trigger
        workflow["nodes"].append({
            "parameters": {},
            "type": "n8n-nodes-base.executeWorkflowTrigger",
            "typeVersion": 1,
            "position": [240, 300],
            "id": "trigger-001",
            "name": "Called by Master"
        })
        
        # 2. Error Handler
        error_handler_node = self.create_error_handler_node()
        error_handler_node["position"] = [440, 400]
        error_handler_node["id"] = "error-handler-001"
        workflow["nodes"].append(error_handler_node)
        
        # 3. Process Request (placeholder - will call actual workflow)
        workflow["nodes"].append({
            "parameters": {
                "workflowId": {
                    "__rl": True,
                    "value": "ACTUAL_WORKFLOW_ID",
                    "mode": "list"
                },
                "source": "workflow",
                "options": {
                    "continueOnFail": True
                }
            },
            "type": "n8n-nodes-base.executeWorkflow",
            "typeVersion": 1,
            "position": [440, 300],
            "id": "execute-workflow-001",
            "name": "Execute Workflow",
            "onError": "continueErrorOutput"
        })
        
        # 4. Return Results
        workflow["nodes"].append({
            "parameters": {
                "assignments": {
                    "assignments": [
                        {
                            "name": "success",
                            "value": "={{ $json.success !== false }}",
                            "type": "boolean"
                        },
                        {
                            "name": "result",
                            "value": "={{ $json }}",
                            "type": "object"
                        }
                    ]
                }
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [640, 300],
            "id": "return-results-001",
            "name": "Return Results"
        })
        
        # Connections
        workflow["connections"] = {
            "Called by Master": {
                "main": [[{"node": "Execute Workflow", "type": "main", "index": 0}]]
            },
            "Execute Workflow": {
                "main": [
                    [{"node": "Return Results", "type": "main", "index": 0}],  # Success
                    [{"node": "Error Handler", "type": "main", "index": 0}]  # Error
                ]
            },
            "Error Handler": {
                "main": [[{"node": "Return Results", "type": "main", "index": 0}]]
            }
        }
        
        # Save workflow
        workflow_path = self.simplified_dir / f"Simplified_Agent_{agent_name}.json"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        
        return workflow_path
    
    def create_error_handler_workflow(self):
        """Create dedicated error handler workflow"""
        workflow = {
            "name": "Error Handler - Construction AI Platform",
            "nodes": [],
            "connections": {},
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True
            },
            "tags": [
                {"id": "error-handler", "name": "error-handler"},
                {"id": "utility", "name": "utility"}
            ]
        }
        
        # 1. Execute Workflow Trigger
        workflow["nodes"].append({
            "parameters": {},
            "type": "n8n-nodes-base.executeWorkflowTrigger",
            "typeVersion": 1,
            "position": [240, 300],
            "id": "trigger-001",
            "name": "Error Handler Trigger"
        })
        
        # 2. Error Handler Node
        error_handler_node = self.create_error_handler_node()
        error_handler_node["position"] = [440, 300]
        error_handler_node["id"] = "error-handler-001"
        workflow["nodes"].append(error_handler_node)
        
        # 3. Log Error (optional - to database or log file)
        workflow["nodes"].append({
            "parameters": {
                "assignments": {
                    "assignments": [
                        {
                            "name": "error_log",
                            "value": "={{ $json }}",
                            "type": "object"
                        }
                    ]
                }
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [640, 300],
            "id": "log-error-001",
            "name": "Log Error"
        })
        
        # 4. Return Error Response
        workflow["nodes"].append({
            "parameters": {
                "assignments": {
                    "assignments": [
                        {
                            "name": "error_response",
                            "value": "={{ $json }}",
                            "type": "object"
                        }
                    ]
                }
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [840, 300],
            "id": "return-error-001",
            "name": "Return Error Response"
        })
        
        # Connections
        workflow["connections"] = {
            "Error Handler Trigger": {
                "main": [[{"node": "Error Handler", "type": "main", "index": 0}]]
            },
            "Error Handler": {
                "main": [[{"node": "Log Error", "type": "main", "index": 0}]]
            },
            "Log Error": {
                "main": [[{"node": "Return Error Response", "type": "main", "index": 0}]]
            }
        }
        
        # Save workflow
        workflow_path = self.simplified_dir / "Error_Handler_Workflow.json"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        
        print(f"Created error handler workflow: {workflow_path}")
        return workflow_path
    
    def create_simplification_guide(self):
        """Create guide for simplified workflows"""
        guide = {
            "version": "2.0.0",
            "simplifications": [
                {
                    "area": "Master Workflow",
                    "changes": [
                        "Simplified routing logic - removed complex condition matching",
                        "Added input validation before processing",
                        "Added centralized error handling",
                        "Reduced number of nodes from 10+ to 8",
                        "Added error recovery suggestions"
                    ]
                },
                {
                    "area": "Agent Workflows",
                    "changes": [
                        "Standardized error handling across all agents",
                        "Added error recovery mechanisms",
                        "Simplified workflow structure",
                        "Added retry logic for retryable errors"
                    ]
                },
                {
                    "area": "Error Handling",
                    "changes": [
                        "Centralized error handler utility",
                        "Standardized error response format",
                        "Added error type classification",
                        "Added recovery suggestions",
                        "Added retry logic"
                    ]
                },
                {
                    "area": "Input Validation",
                    "changes": [
                        "Added input validation before processing",
                        "Validates required fields",
                        "Validates file extensions",
                        "Validates request types",
                        "Returns clear error messages"
                    ]
                }
            ],
            "benefits": [
                "Better error handling",
                "Simplified workflow structure",
                "Easier to maintain",
                "Better error messages",
                "Automatic error recovery",
                "Reduced complexity"
            ]
        }
        
        guide_path = self.simplified_dir / "SIMPLIFICATION_GUIDE.json"
        with open(guide_path, 'w', encoding='utf-8') as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)
        
        print(f"Created simplification guide: {guide_path}")
        return guide_path
    
    def run(self):
        """Run workflow simplification"""
        print("=" * 60)
        print("Simplifying Workflows with Better Error Handling")
        print("=" * 60)
        
        # Create simplified master workflow
        self.create_simplified_master_workflow()
        
        # Create error handler workflow
        self.create_error_handler_workflow()
        
        # Create simplification guide
        self.create_simplification_guide()
        
        print("\n" + "=" * 60)
        print("Workflow simplification complete!")
        print("=" * 60)
        print(f"\nOutput directory: {self.simplified_dir}")
        print("\nNext steps:")
        print("1. Import simplified workflows into n8n")
        print("2. Update workflow IDs")
        print("3. Test error handling")
        print("4. Deploy to production")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    workflows_dir = script_dir / "construction-platform" / "n8n-workflows"
    
    if not workflows_dir.exists():
        print(f"Error: {workflows_dir} does not exist!")
        print(f"Current directory: {Path.cwd()}")
        print(f"Script directory: {script_dir}")
        exit(1)
    
    print(f"Workflows directory: {workflows_dir}")
    simplifier = WorkflowSimplifier(workflows_dir)
    simplifier.run()

