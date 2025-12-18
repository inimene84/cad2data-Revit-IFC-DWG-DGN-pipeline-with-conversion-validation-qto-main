# PowerShell script for DWG conversion
Write-Host "Starting DWG conversion process..." -ForegroundColor Green
Write-Host ""

# Create output directory
New-Item -ItemType Directory -Force -Path "Converted_Data" | Out-Null

Write-Host "Processing: TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-5-01_V01_Korruseplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-5-01_V01_Korruseplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-5-01_V01_Korruseplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-5-01_V01_Korruseplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-6-01_V01_Loiked.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-6-01_V01_Loiked.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-6-01_V01_Loiked.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-6-01_V01_Loiked.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-6-02_V01_Vaated.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-6-02_V01_Vaated.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-6-02_V01_Vaated.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-6-02_V01_Vaated.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-6-03_V01_Vaated.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-6-03_V01_Vaated.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-6-03_V01_Vaated.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-6-03_V01_Vaated.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-01_V01_Soklisolm.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-01_V01_Soklisolm.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-01_V01_Soklisolm.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-01_V01_Soklisolm.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-02_V01_Aken-vert.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-02_V01_Aken-vert.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-02_V01_Aken-vert.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-02_V01_Aken-vert.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-06_V01_Parapett.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-06_V01_Parapett.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-06_V01_Parapett.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-06_V01_Parapett.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-8-01_V01_Konstr-vert.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-01_V01_Konstr-vert.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-8-01_V01_Konstr-vert.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-8-01_V01_Konstr-vert.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-8-02_V01_Konstr-hor.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-02_V01_Konstr-hor.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-8-02_V01_Konstr-hor.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-8-02_V01_Konstr-hor.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_PP_AS-4-01_V01_Asendiplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AS-4-01_V01_Asendiplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_PP_AS-4-01_V01_Asendiplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_PP_AS-4-01_V01_Asendiplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-5-01_V01_Korruseplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-5-01_V01_Korruseplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-5-01_V01_Korruseplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-5-01_V01_Korruseplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-6-01_V01_Loiked.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-6-01_V01_Loiked.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-6-01_V01_Loiked.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-6-01_V01_Loiked.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-6-02_V01_Vaated.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-6-02_V01_Vaated.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-6-02_V01_Vaated.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-6-02_V01_Vaated.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-6-03_V01_Vaated.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-6-03_V01_Vaated.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-6-03_V01_Vaated.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-6-03_V01_Vaated.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-01_V01_Soklisolm.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-01_V01_Soklisolm.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-01_V01_Soklisolm.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-01_V01_Soklisolm.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-02_V01_Aken-vert.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-02_V01_Aken-vert.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-02_V01_Aken-vert.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-02_V01_Aken-vert.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-06_V01_Parapett.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-06_V01_Parapett.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-06_V01_Parapett.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-06_V01_Parapett.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-8-01_V01_Konstr-vert.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-01_V01_Konstr-vert.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-8-01_V01_Konstr-vert.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-8-01_V01_Konstr-vert.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-8-02_V01_Konstr-hor.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-02_V01_Konstr-hor.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-8-02_V01_Konstr-hor.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-8-02_V01_Konstr-hor.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_PP_AS-4-01_V01_Asendiplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AS-4-01_V01_Asendiplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_PP_AS-4-01_V01_Asendiplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_PP_AS-4-01_V01_Asendiplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Processing: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Yellow
& "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Green
} else {
    Write-Host "❌ Failed: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" -ForegroundColor Red
}
Write-Host ""

Write-Host "Conversion process completed!" -ForegroundColor Green
Read-Host "Press Enter to continue"
