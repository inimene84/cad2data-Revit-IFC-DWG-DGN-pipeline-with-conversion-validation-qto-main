# Test Construction Platform Services
# Usage: .\TEST_SERVICES.ps1

Write-Host "`n=== Testing Construction Platform Services ===" -ForegroundColor Cyan
Write-Host ""

# Test API
Write-Host "1. Testing API (http://localhost:8000/v1/health)..." -ForegroundColor Yellow
try {
    $api = Invoke-WebRequest -Uri "http://localhost:8000/v1/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "   ✅ API: Running (Status: $($api.StatusCode))" -ForegroundColor Green
    $api.Content | ConvertFrom-Json | Format-List
} catch {
    Write-Host "   ❌ API: Not running or not built yet" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""

# Test UI
Write-Host "2. Testing UI (http://localhost:3000)..." -ForegroundColor Yellow
try {
    $ui = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "   ✅ UI: Running (Status: $($ui.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ❌ UI: Not running or not built yet" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""

# Test N8N
Write-Host "3. Testing N8N (http://localhost:5678)..." -ForegroundColor Yellow
try {
    $n8n = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "   ✅ N8N: Running (Status: $($n8n.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ❌ N8N: Not running" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""

# Test Qdrant
Write-Host "4. Testing Qdrant (http://localhost:6333/health)..." -ForegroundColor Yellow
try {
    $qdrant = Invoke-WebRequest -Uri "http://localhost:6333/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "   ✅ Qdrant: Running (Status: $($qdrant.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Qdrant: Not running" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""

# Show Docker container status
Write-Host "=== Docker Container Status ===" -ForegroundColor Cyan
docker ps --filter "name=construction" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""

