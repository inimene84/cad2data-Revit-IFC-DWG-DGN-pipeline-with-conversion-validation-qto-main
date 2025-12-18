#!/usr/bin/env python3
"""
Working Excel Generator for Data-Driven Construction
Creates both Excel and CSV files from your project data
"""

import os
import pandas as pd
import subprocess
from pathlib import Path
from datetime import datetime
import json

def create_project_excel():
    """Create a comprehensive Excel file for data-driven construction"""
    
    # Project paths
    project_path = Path(r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project")
    output_path = project_path / "Excel_Output"
    output_path.mkdir(exist_ok=True)
    
    print("🏗️ Creating Data-Driven Construction Excel Database")
    print("=" * 60)
    
    # Find all files
    dwg_files = []
    pdf_files = []
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.lower().endswith('.dwg'):
                dwg_files.append(Path(root) / file)
            elif file.lower().endswith('.pdf'):
                pdf_files.append(Path(root) / file)
    
    print(f"📁 Found {len(dwg_files)} DWG files")
    print(f"📄 Found {len(pdf_files)} PDF files")
    
    # Create file inventory
    file_inventory = []
    
    # Process DWG files
    for dwg_file in dwg_files:
        try:
            stat = dwg_file.stat()
            file_inventory.append({
                'file_name': dwg_file.name,
                'file_path': str(dwg_file),
                'file_type': 'DWG',
                'folder': dwg_file.parent.name,
                'size_mb': round(stat.st_size / (1024*1024), 2),
                'modified_date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
                'status': 'Ready for conversion',
                'priority': 'High' if 'Archive' in str(dwg_file) else 'Medium'
            })
        except Exception as e:
            print(f"❌ Error processing {dwg_file.name}: {e}")
    
    # Process PDF files
    for pdf_file in pdf_files:
        try:
            stat = pdf_file.stat()
            file_inventory.append({
                'file_name': pdf_file.name,
                'file_path': str(pdf_file),
                'file_type': 'PDF',
                'folder': pdf_file.parent.name,
                'size_mb': round(stat.st_size / (1024*1024), 2),
                'modified_date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
                'status': 'Ready for OCR',
                'priority': 'Medium'
            })
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
    
    # Create Excel file with multiple sheets
    excel_file = output_path / "Data_Driven_Construction_Database.xlsx"
    
    try:
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            
            # Sheet 1: File Inventory
            df_inventory = pd.DataFrame(file_inventory)
            df_inventory.to_excel(writer, sheet_name='File_Inventory', index=False)
            
            # Sheet 2: Project Summary
            summary_data = {
                'Metric': [
                    'Total Files',
                    'DWG Files',
                    'PDF Files',
                    'Total Size (MB)',
                    'Project Date',
                    'Status'
                ],
                'Value': [
                    len(file_inventory),
                    len(dwg_files),
                    len(pdf_files),
                    sum(item['size_mb'] for item in file_inventory),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Ready for Processing'
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Project_Summary', index=False)
            
            # Sheet 3: Processing Plan
            processing_plan = []
            for item in file_inventory:
                if item['file_type'] == 'DWG':
                    processing_plan.append({
                        'file_name': item['file_name'],
                        'action': 'Convert to Excel',
                        'tool': 'DwgExporter.exe',
                        'expected_output': 'Element data + quantities',
                        'estimated_time': '2-5 minutes',
                        'priority': item['priority']
                    })
                elif item['file_type'] == 'PDF':
                    processing_plan.append({
                        'file_name': item['file_name'],
                        'action': 'OCR + Text extraction',
                        'tool': 'Tesseract OCR',
                        'expected_output': 'Text + dimensions',
                        'estimated_time': '1-3 minutes',
                        'priority': item['priority']
                    })
            
            df_plan = pd.DataFrame(processing_plan)
            df_plan.to_excel(writer, sheet_name='Processing_Plan', index=False)
            
            # Sheet 4: Construction Categories
            categories = [
                {'category': 'Structural', 'description': 'Foundations, beams, columns, slabs', 'priority': 'Critical'},
                {'category': 'Architectural', 'description': 'Walls, doors, windows, finishes', 'priority': 'High'},
                {'category': 'MEP', 'description': 'Mechanical, electrical, plumbing', 'priority': 'High'},
                {'category': 'Site', 'description': 'Landscaping, utilities, paving', 'priority': 'Medium'},
                {'category': 'Interior', 'description': 'Furniture, fixtures, equipment', 'priority': 'Medium'},
                {'category': 'Safety', 'description': 'Fire safety, security, emergency', 'priority': 'Critical'}
            ]
            df_categories = pd.DataFrame(categories)
            df_categories.to_excel(writer, sheet_name='Construction_Categories', index=False)
            
            # Sheet 5: Data Requirements
            requirements = [
                {'requirement': 'Element ID', 'description': 'Unique identifier for each element', 'required': 'Yes'},
                {'requirement': 'Element Type', 'description': 'Category/type of construction element', 'required': 'Yes'},
                {'requirement': 'Dimensions', 'description': 'Length, width, height, thickness', 'required': 'Yes'},
                {'requirement': 'Quantities', 'description': 'Volume, area, length, count', 'required': 'Yes'},
                {'requirement': 'Materials', 'description': 'Material specifications and properties', 'required': 'Yes'},
                {'requirement': 'Location', 'description': 'Floor, room, coordinates', 'required': 'Yes'},
                {'requirement': 'Cost Data', 'description': 'Unit costs, labor rates, equipment', 'required': 'No'},
                {'requirement': 'Schedule', 'description': 'Construction sequence, dependencies', 'required': 'No'}
            ]
            df_requirements = pd.DataFrame(requirements)
            df_requirements.to_excel(writer, sheet_name='Data_Requirements', index=False)
        
        print(f"\n✅ Excel database created: {excel_file}")
        
    except Exception as e:
        print(f"❌ Error creating Excel file: {e}")
        print("📄 Creating CSV files instead...")
        create_csv_files(output_path, file_inventory, dwg_files, pdf_files)
        return None
    
    print(f"📊 Total files catalogued: {len(file_inventory)}")
    print(f"📁 Output location: {output_path}")
    
    # Create processing scripts
    create_processing_scripts(output_path, file_inventory)
    
    return excel_file

def create_csv_files(output_path, file_inventory, dwg_files, pdf_files):
    """Create CSV files as fallback"""
    csv_path = output_path / "CSV_Data"
    csv_path.mkdir(exist_ok=True)
    
    # File Inventory CSV
    df_inventory = pd.DataFrame(file_inventory)
    df_inventory.to_csv(csv_path / "File_Inventory.csv", index=False)
    
    # Project Summary CSV
    summary_data = {
        'Metric': ['Total Files', 'DWG Files', 'PDF Files', 'Total Size (MB)', 'Project Date', 'Status'],
        'Value': [
            len(file_inventory),
            len(dwg_files), 
            len(pdf_files),
            sum(item['size_mb'] for item in file_inventory),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Ready for Processing'
        ]
    }
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv(csv_path / "Project_Summary.csv", index=False)
    
    print(f"✅ CSV files created in: {csv_path}")

def create_processing_scripts(output_path, file_inventory):
    """Create processing scripts for DWG files"""
    
    # DWG Converter path
    dwg_converter = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe"
    
    # Filter DWG files
    dwg_files = [item for item in file_inventory if item['file_type'] == 'DWG']
    
    # Create batch script
    batch_script = '''@echo off
echo Starting DWG conversion process...
echo.

mkdir "Converted_Data" 2>nul

'''
    
    for file_info in dwg_files:
        batch_script += f'''echo Processing: {file_info['file_name']}
"{dwg_converter}" "{file_info['file_path']}" "Converted_Data"
if %errorlevel% equ 0 (
    echo ✅ Success: {file_info['file_name']}
) else (
    echo ❌ Failed: {file_info['file_name']}
)
echo.

'''
    
    batch_script += '''echo Conversion process completed!
pause
'''
    
    # Save batch script
    batch_file = output_path / "process_dwg_files.bat"
    with open(batch_file, 'w', encoding='utf-8') as f:
        f.write(batch_script)
    
    # Create PowerShell script
    ps_script = f'''# PowerShell script for DWG conversion
Write-Host "Starting DWG conversion process..." -ForegroundColor Green
Write-Host ""

# Create output directory
New-Item -ItemType Directory -Force -Path "Converted_Data" | Out-Null

'''
    
    for file_info in dwg_files:
        ps_script += f'''Write-Host "Processing: {file_info['file_name']}" -ForegroundColor Yellow
& "{dwg_converter}" "{file_info['file_path']}" "Converted_Data"
if ($LASTEXITCODE -eq 0) {{
    Write-Host "✅ Success: {file_info['file_name']}" -ForegroundColor Green
}} else {{
    Write-Host "❌ Failed: {file_info['file_name']}" -ForegroundColor Red
}}
Write-Host ""

'''
    
    ps_script += '''Write-Host "Conversion process completed!" -ForegroundColor Green
Read-Host "Press Enter to continue"
'''
    
    # Save PowerShell script
    ps_file = output_path / "process_dwg_files.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    print(f"🔧 Processing scripts created:")
    print(f"   - process_dwg_files.bat")
    print(f"   - process_dwg_files.ps1")

if __name__ == "__main__":
    create_project_excel()
