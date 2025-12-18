@echo off
echo Starting DWG conversion process...
echo.

mkdir "Converted_Data" 2>nul

echo Processing: TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg
) else (
    echo ❌ Failed: TRN_EP_AS-4-01_V04_Asendiplaan_vertikaal.dwg
)
echo.

echo Processing: TRN_PP_AR-4-02_V01_Valisvalgustid.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-4-02_V01_Valisvalgustid.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-4-02_V01_Valisvalgustid.dwg
)
echo.

echo Processing: TRN_PP_AR-5-01_V01_Korruseplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-5-01_V01_Korruseplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-5-01_V01_Korruseplaan.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-5-01_V01_Korruseplaan.dwg
)
echo.

echo Processing: TRN_PP_AR-5-02_V01_Katuse-plaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-5-02_V01_Katuse-plaan.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-5-02_V01_Katuse-plaan.dwg
)
echo.

echo Processing: TRN_PP_AR-5-03_V01_Lagede-korgused.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-5-03_V01_Lagede-korgused.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-5-03_V01_Lagede-korgused.dwg
)
echo.

echo Processing: TRN_PP_AR-6-01_V01_Loiked.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-6-01_V01_Loiked.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-6-01_V01_Loiked.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-6-01_V01_Loiked.dwg
)
echo.

echo Processing: TRN_PP_AR-6-02_V01_Vaated.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-6-02_V01_Vaated.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-6-02_V01_Vaated.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-6-02_V01_Vaated.dwg
)
echo.

echo Processing: TRN_PP_AR-6-03_V01_Vaated.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-6-03_V01_Vaated.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-6-03_V01_Vaated.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-6-03_V01_Vaated.dwg
)
echo.

echo Processing: TRN_PP_AR-7-01_V01_Soklisolm.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-01_V01_Soklisolm.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-01_V01_Soklisolm.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-01_V01_Soklisolm.dwg
)
echo.

echo Processing: TRN_PP_AR-7-02_V01_Aken-vert.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-02_V01_Aken-vert.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-02_V01_Aken-vert.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-02_V01_Aken-vert.dwg
)
echo.

echo Processing: TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg
)
echo.

echo Processing: TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg
)
echo.

echo Processing: TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg
)
echo.

echo Processing: TRN_PP_AR-7-06_V01_Parapett.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-06_V01_Parapett.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-06_V01_Parapett.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-06_V01_Parapett.dwg
)
echo.

echo Processing: TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg
)
echo.

echo Processing: TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg
)
echo.

echo Processing: TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg
)
echo.

echo Processing: TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg
)
echo.

echo Processing: TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg
)
echo.

echo Processing: TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg
)
echo.

echo Processing: TRN_PP_AR-8-01_V01_Konstr-vert.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-01_V01_Konstr-vert.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-8-01_V01_Konstr-vert.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-8-01_V01_Konstr-vert.dwg
)
echo.

echo Processing: TRN_PP_AR-8-02_V01_Konstr-hor.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-02_V01_Konstr-hor.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-8-02_V01_Konstr-hor.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-8-02_V01_Konstr-hor.dwg
)
echo.

echo Processing: TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg
)
echo.

echo Processing: TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg
)
echo.

echo Processing: TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg
)
echo.

echo Processing: TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg
) else (
    echo ❌ Failed: TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg
)
echo.

echo Processing: TRN_PP_AS-4-01_V01_Asendiplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\TRN_PP_AS-4-01_V01_Asendiplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_PP_AS-4-01_V01_Asendiplaan.dwg
) else (
    echo ❌ Failed: TRN_PP_AS-4-01_V01_Asendiplaan.dwg
)
echo.

echo Processing: ._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-4-02_V01_Valisvalgustid.dwg
)
echo.

echo Processing: ._TRN_PP_AR-5-01_V01_Korruseplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-5-01_V01_Korruseplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-5-01_V01_Korruseplaan.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-5-01_V01_Korruseplaan.dwg
)
echo.

echo Processing: ._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-5-02_V01_Katuse-plaan.dwg
)
echo.

echo Processing: ._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-5-03_V01_Lagede-korgused.dwg
)
echo.

echo Processing: ._TRN_PP_AR-6-01_V01_Loiked.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-6-01_V01_Loiked.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-6-01_V01_Loiked.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-6-01_V01_Loiked.dwg
)
echo.

echo Processing: ._TRN_PP_AR-6-02_V01_Vaated.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-6-02_V01_Vaated.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-6-02_V01_Vaated.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-6-02_V01_Vaated.dwg
)
echo.

echo Processing: ._TRN_PP_AR-6-03_V01_Vaated.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-6-03_V01_Vaated.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-6-03_V01_Vaated.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-6-03_V01_Vaated.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-01_V01_Soklisolm.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-01_V01_Soklisolm.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-01_V01_Soklisolm.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-01_V01_Soklisolm.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-02_V01_Aken-vert.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-02_V01_Aken-vert.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-02_V01_Aken-vert.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-02_V01_Aken-vert.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-03_V01_Aken-hor-laudisega-seinas.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-04_V01_Aken-hor-fassaadiplaadiga-seinas.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-05_V01_Klaasfassaadi-ja-terrassi-solm.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-06_V01_Parapett.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-06_V01_Parapett.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-06_V01_Parapett.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-06_V01_Parapett.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-07_V01_Parapett-varikatus-klaasfassaad.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-08_V01_Katuste-uhendus.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-09_V01_Peasissepaasu-trepp.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-10_V01_Magamistoa-terrass.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-11_V01_Valisseina-sisenurk.dwg
)
echo.

echo Processing: ._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-7-12_V01_Vihmaveetoru-laudise-taga.dwg
)
echo.

echo Processing: ._TRN_PP_AR-8-01_V01_Konstr-vert.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-01_V01_Konstr-vert.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-8-01_V01_Konstr-vert.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-8-01_V01_Konstr-vert.dwg
)
echo.

echo Processing: ._TRN_PP_AR-8-02_V01_Konstr-hor.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-02_V01_Konstr-hor.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-8-02_V01_Konstr-hor.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-8-02_V01_Konstr-hor.dwg
)
echo.

echo Processing: ._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-8-03_V01_Akende-spetsifikatsioon.dwg
)
echo.

echo Processing: ._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-8-04_V01_Klaasfassaad-KLF-01.dwg
)
echo.

echo Processing: ._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-8-05_V01_Klaasfassaad-KLF-02.dwg
)
echo.

echo Processing: ._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AR-8-06_V01_Valisuste-spetsifikatsioon.dwg
)
echo.

echo Processing: ._TRN_PP_AS-4-01_V01_Asendiplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_1\__MACOSX\._TRN_PP_AS-4-01_V01_Asendiplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_PP_AS-4-01_V01_Asendiplaan.dwg
) else (
    echo ❌ Failed: ._TRN_PP_AS-4-01_V01_Asendiplaan.dwg
)
echo.

echo Processing: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
) else (
    echo ❌ Failed: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
)
echo.

echo Processing: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
) else (
    echo ❌ Failed: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
)
echo.

echo Processing: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
) else (
    echo ❌ Failed: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
)
echo.

echo Processing: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
) else (
    echo ❌ Failed: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
)
echo.

echo Processing: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
)
echo.

echo Processing: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
)
echo.

echo Processing: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
)
echo.

echo Processing: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_2\__MACOSX\._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
)
echo.

echo Processing: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg
) else (
    echo ❌ Failed: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg
)
echo.

echo Processing: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
) else (
    echo ❌ Failed: TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
)
echo.

echo Processing: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg
) else (
    echo ❌ Failed: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg
)
echo.

echo Processing: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
) else (
    echo ❌ Failed: TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
)
echo.

echo Processing: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg
) else (
    echo ❌ Failed: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg
)
echo.

echo Processing: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
) else (
    echo ❌ Failed: TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
)
echo.

echo Processing: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg
) else (
    echo ❌ Failed: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg
)
echo.

echo Processing: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
) else (
    echo ❌ Failed: TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
)
echo.

echo Processing: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan (1).dwg
)
echo.

echo Processing: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-5-01_V01_Abihoone-Korruseplaan.dwg
)
echo.

echo Processing: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan (1).dwg
)
echo.

echo Processing: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-5-02_V01_Abihoone-Katuse-plaan.dwg
)
echo.

echo Processing: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige (1).dwg
)
echo.

echo Processing: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AR-6-02_V01_Abihoone-Vaated-loige.dwg
)
echo.

echo Processing: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg
) else (
    echo ❌ Failed: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan (1).dwg
)
echo.

echo Processing: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe" "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Archive_3\__MACOSX\._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
) else (
    echo ❌ Failed: ._TRN_EP_AS-4-01_V01_Abihoone-Asendiplaan.dwg
)
echo.

echo Conversion process completed!
pause
