/**
 * Simplified Error Handler for Construction AI Platform
 * Centralized error handling utility for all workflows
 */

/**
 * Enhanced Error Handler for Construction AI Platform v2.0
 * Supports project context and improved error tracking
 */

class ErrorHandler {
    constructor(context = {}) {
        this.context = context;
        this.executionId = context.executionId || 'unknown';
        this.workflowName = context.workflowName || 'unknown';
        this.projectId = context.projectId || context.project?.id || null;
        this.projectName = context.projectName || context.project?.name || null;
        this.userId = context.userId || context.user?.id || null;
        this.tenantId = context.tenantId || context.tenant?.id || null;
        this.timestamp = new Date().toISOString();
        this.version = '2.0.0';
    }

    /**
     * Handle errors with standardized format
     */
    handleError(error, context = {}) {
        const errorInfo = {
            success: false,
            error: {
                message: this.getErrorMessage(error),
                type: this.getErrorType(error),
                code: this.getErrorCode(error),
                timestamp: this.timestamp,
                executionId: this.executionId,
                workflowName: this.workflowName,
                workflowVersion: this.version,
                // Project context (NEW)
                project: {
                    id: this.projectId,
                    name: this.projectName
                },
                user: {
                    id: this.userId
                },
                tenant: {
                    id: this.tenantId
                },
                context: context
            },
            recovery: {
                suggestions: this.getRecoverySuggestions(error),
                canRetry: this.canRetry(error),
                retryAfter: this.getRetryAfter(error)
            }
        };

        // Enhanced logging with project context
        const logMessage = {
            error: errorInfo.error,
            project: this.projectId ? `Project: ${this.projectId} (${this.projectName})` : 'No project context',
            user: this.userId ? `User: ${this.userId}` : 'Unknown user',
            tenant: this.tenantId ? `Tenant: ${this.tenantId}` : 'Unknown tenant'
        };
        console.error('Error:', logMessage);

        return errorInfo;
    }

    /**
     * Get user-friendly error message
     */
    getErrorMessage(error) {
        if (typeof error === 'string') {
            return error;
        }
        if (error?.message) {
            return error.message;
        }
        if (error?.error?.message) {
            return error.error.message;
        }
        return 'An unexpected error occurred';
    }

    /**
     * Get error type
     */
    getErrorType(error) {
        if (error?.code === 'ENOTFOUND' || error?.code === 'ECONNREFUSED') {
            return 'network_error';
        }
        if (error?.code === 'ETIMEDOUT') {
            return 'timeout_error';
        }
        if (error?.statusCode) {
            if (error.statusCode >= 400 && error.statusCode < 500) {
                return 'client_error';
            }
            if (error.statusCode >= 500) {
                return 'server_error';
            }
        }
        if (error?.message?.includes('not found')) {
            return 'not_found';
        }
        if (error?.message?.includes('unauthorized') || error?.message?.includes('forbidden')) {
            return 'authentication_error';
        }
        if (error?.message?.includes('validation') || error?.message?.includes('invalid')) {
            return 'validation_error';
        }
        return 'unknown_error';
    }

    /**
     * Get error code
     */
    getErrorCode(error) {
        return error?.code || error?.statusCode || 'UNKNOWN_ERROR';
    }

    /**
     * Get recovery suggestions
     */
    getRecoverySuggestions(error) {
        const errorType = this.getErrorType(error);
        const suggestions = {
            network_error: [
                'Check your internet connection',
                'Verify the service is available',
                'Try again in a few moments'
            ],
            timeout_error: [
                'The request took too long',
                'Try again with a smaller file',
                'Check if the service is overloaded'
            ],
            client_error: [
                'Check your input parameters',
                'Verify file format and size',
                'Ensure all required fields are provided'
            ],
            server_error: [
                'Service temporarily unavailable',
                'Try again later',
                'Contact support if problem persists'
            ],
            not_found: [
                'Check if the file/resource exists',
                'Verify the file ID or path',
                'Ensure you have access permissions'
            ],
            authentication_error: [
                'Check your API credentials',
                'Verify authentication tokens',
                'Ensure your account has necessary permissions'
            ],
            validation_error: [
                'Check input format',
                'Verify required fields',
                'Ensure data types are correct'
            ],
            unknown_error: [
                'Try again',
                'Check logs for details',
                'Contact support if problem persists'
            ]
        };

        return suggestions[errorType] || suggestions.unknown_error;
    }

    /**
     * Check if error can be retried
     */
    canRetry(error) {
        const errorType = this.getErrorType(error);
        const retryableErrors = ['network_error', 'timeout_error', 'server_error'];
        return retryableErrors.includes(errorType);
    }

    /**
     * Get retry delay in seconds
     */
    getRetryAfter(error) {
        const errorType = this.getErrorType(error);
        const delays = {
            network_error: 5,
            timeout_error: 10,
            server_error: 30,
            default: 60
        };
        return delays[errorType] || delays.default;
    }

    /**
     * Validate input parameters
     */
    validateInput(input, requiredFields = []) {
        const errors = [];

        // Check required fields
        for (const field of requiredFields) {
            if (!input[field] && input[field] !== 0 && input[field] !== false) {
                errors.push(`Missing required field: ${field}`);
            }
        }

        // Validate file extensions
        if (input.fileExtension) {
            const validExtensions = ['.rvt', '.ifc', '.dwg', '.dgn', '.pdf', '.jpg', '.png', '.docx', '.xlsx', '.csv'];
            const ext = input.fileExtension.toLowerCase();
            if (!validExtensions.includes(ext)) {
                errors.push(`Invalid file extension: ${ext}. Valid extensions: ${validExtensions.join(', ')}`);
            }
        }

        // Validate request type
        if (input.requestType) {
            const validTypes = ['convert', 'validate', 'classify', 'estimate_cost', 'carbon_footprint', 'quantity_takeoff', 'extract_data', 'materials', 'generate_document', 'file_management', 'vendor', 'compliance', 'visualization', 'bim', 'scheduling', '3d_vision'];
            if (!validTypes.includes(input.requestType)) {
                errors.push(`Invalid request type: ${input.requestType}. Valid types: ${validTypes.join(', ')}`);
            }
        }

        if (errors.length > 0) {
            return {
                valid: false,
                errors: errors
            };
        }

        return { valid: true };
    }

    /**
     * Create standardized success response
     */
    createSuccessResponse(data, message = 'Operation completed successfully') {
        return {
            success: true,
            data: data,
            message: message,
            timestamp: this.timestamp,
            executionId: this.executionId
        };
    }

    /**
     * Wrap async function with error handling
     */
    async wrapAsync(fn, context = {}) {
        try {
            const result = await fn();
            return this.createSuccessResponse(result);
        } catch (error) {
            return this.handleError(error, context);
        }
    }
}

// Export for use in n8n workflows
module.exports = ErrorHandler;

