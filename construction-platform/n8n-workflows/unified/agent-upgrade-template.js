/**
 * Agent Workflow Upgrade Template v2.0
 * 
 * This template shows the structure for upgrading agent workflows
 * All agents should have:
 * 1. Extract Project Context node
 * 2. Format Response node
 * 3. Enhanced error handling
 * 4. Project context in all outputs
 */

// Extract Project Context Node Template
const extractProjectContextCode = (agentName, agentDescription) => `
// ${agentDescription} Agent v2.0
// Extracts project context and processes request

const input = $input.first().json;
const data = input.data || input;

// Extract project context from routing data
const project = data.project || input.project || {};
const user = data.user || input.user || {};
const tenant = data.tenant || input.tenant || {};
const metadata = data.metadata || input.metadata || {};
const originalInput = data.originalInput || input.originalInput || data;

// Prepare enhanced request with project context
const enhancedRequest = {
  ...originalInput,
  project: {
    id: project.id || originalInput.projectId || originalInput.project?.id || null,
    name: project.name || originalInput.projectName || originalInput.project?.name || null,
    phase: project.phase || originalInput.projectPhase || originalInput.project?.phase || 'general'
  },
  user: {
    id: user.id || originalInput.userId || originalInput.user?.id || null
  },
  tenant: {
    id: tenant.id || originalInput.tenantId || originalInput.tenant?.id || null
  },
  metadata: {
    ...metadata,
    agentName: '${agentName}',
    agentVersion: '2.0.0',
    executionId: metadata.executionId || (project.id || 'global') + '_' + Date.now(),
    hasProjectContext: !!(project.id || originalInput.projectId)
  }
};

return [{ json: enhancedRequest }];
`;

// Format Response Node Template
const formatResponseCode = (agentName, successMessage) => `
// Enhanced Response Formatter v2.0
// Formats response with project context

const input = $input.first().json;
const result = input.result || input;
const request = $('Extract Project Context').first().json;

// Build response with project context
const response = {
  success: true,
  data: result,
  project: request.project,
  user: request.user,
  tenant: request.tenant,
  metadata: {
    ...request.metadata,
    timestamp: new Date().toISOString(),
    agentName: '${agentName}',
    agentVersion: '2.0.0'
  },
  message: '${successMessage}'
};

return [{ json: response }];
`;

module.exports = {
  extractProjectContextCode,
  formatResponseCode
};

