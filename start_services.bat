@echo off
echo Starting Construction AI Services...
echo.

echo Starting DWG Conversion Service...
start "DWG Service" cmd /k "cd /d %~dp0 && python services/dwg_service.py"

echo Starting OCR Service (Tesseract)...
start "OCR Service" cmd /k "cd /d %~dp0 && python services/ocr_service.py"

echo Starting Drive Provisioner Service...
start "Drive Provisioner" cmd /k "cd /d %~dp0 && python services/drive_provisioner.py"

echo.
echo Services starting on:
echo - DWG Service: http://localhost:5055
echo - OCR Service: http://localhost:5056  
echo - Drive Provisioner: http://localhost:5057
echo.
echo Press any key to continue...
pause
