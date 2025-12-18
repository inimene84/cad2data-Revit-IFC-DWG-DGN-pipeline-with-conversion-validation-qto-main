Write-Host "Starting Construction AI Services..." -ForegroundColor Green
Write-Host ""

# Start DWG Service
Write-Host "Starting DWG Conversion Service..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "services/dwg_service.py" -WindowStyle Normal

# Start OCR Service  
Write-Host "Starting OCR Service (Tesseract)..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "services/ocr_service.py" -WindowStyle Normal

# Start Drive Provisioner
Write-Host "Starting Drive Provisioner Service..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "services/drive_provisioner.py" -WindowStyle Normal

Write-Host ""
Write-Host "Services starting on:" -ForegroundColor Cyan
Write-Host "- DWG Service: http://localhost:5055" -ForegroundColor White
Write-Host "- OCR Service: http://localhost:5056" -ForegroundColor White  
Write-Host "- Drive Provisioner: http://localhost:5057" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
