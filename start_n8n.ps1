# PowerShell script to start n8n with proper configuration
Write-Host "Starting n8n with optimized configuration..." -ForegroundColor Green

# Set environment variables
$env:DB_SQLITE_POOL_SIZE = "10"
$env:N8N_RUNNERS_ENABLED = "true"
$env:N8N_BLOCK_ENV_ACCESS_IN_NODE = "false"

# Additional environment variables that might help with the Luxon issue
$env:NODE_OPTIONS = "--max-old-space-size=4096"

Write-Host "Environment variables set:" -ForegroundColor Yellow
Write-Host "DB_SQLITE_POOL_SIZE: $env:DB_SQLITE_POOL_SIZE"
Write-Host "N8N_RUNNERS_ENABLED: $env:N8N_RUNNERS_ENABLED"
Write-Host "N8N_BLOCK_ENV_ACCESS_IN_NODE: $env:N8N_BLOCK_ENV_ACCESS_IN_NODE"
Write-Host "NODE_OPTIONS: $env:NODE_OPTIONS"

Write-Host "Starting n8n..." -ForegroundColor Green
npx n8n@latest
