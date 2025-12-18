@echo off
echo Starting n8n with optimized configuration...

REM Set environment variables to fix deprecation warnings
set DB_SQLITE_POOL_SIZE=10
set N8N_RUNNERS_ENABLED=true
set N8N_BLOCK_ENV_ACCESS_IN_NODE=false

REM Start n8n
npx n8n@latest

pause
