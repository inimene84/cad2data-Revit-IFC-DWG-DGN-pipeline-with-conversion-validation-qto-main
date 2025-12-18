#!/usr/bin/env python3
"""
Simple Excel Generator for Data-Driven Construction
Uses only built-in Python libraries - no external dependencies
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime

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
    
    # Create CSV files (Excel-compatible)
    csv_output_path = output_path / "CSV_Data"
    csv_output_path.mkdir(exist_ok=True)
    
    # 1. File Inventory CSV
    inventory_file = csv_output_path / "File_Inventory.csv"
    with open(inventory_file, 'w', newline='', encoding='utf-8') as f:
        if file_inventory:
            writer = csv.DictWriter(f, fieldnames=file_inventory[0].keys())
            writer.writeheader()
            writer.writerows(file_inventory)
    
    # 2. Project Summary CSV
    summary_data = [
        {'Metric': 'Total Files', 'Value': len(file_inventory)},
        {'Metric': 'DWG Files', 'Value': len(dwg_files)},
        {'Metric': 'PDF Files', 'Value': len(pdf_files)},
        {'Metric': 'Total Size (MB)', 'Value': sum(item['size_mb'] for item in file_inventory)},
        {'Metric': 'Processing Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {'Metric': 'Status', 'Value': 'Ready for Processing'}
    ]
    
    summary_file = csv_output_path / "Project_Summary.csv"
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Metric', 'Value'])
        writer.writeheader()
        writer.writerows(summary_data)
    
    # 3. Processing Plan CSV
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
    
    plan_file = csv_output_path / "Processing_Plan.csv"
    with open(plan_file, 'w', newline='', encoding='utf-8') as f:
        if processing_plan:
            writer = csv.DictWriter(f, fieldnames=processing_plan[0].keys())
            writer.writeheader()
            writer.writerows(processing_plan)
    
    # 4. Construction Categories CSV
    categories = [
        {'category': 'Structural', 'description': 'Foundations, beams, columns, slabs', 'priority': 'Critical'},
        {'category': 'Architectural', 'description': 'Walls, doors, windows, finishes', 'priority': 'High'},
        {'category': 'MEP', 'description': 'Mechanical, electrical, plumbing', 'priority': 'High'},
        {'category': 'Site', 'description': 'Landscaping, utilities, paving', 'priority': 'Medium'},
        {'category': 'Interior', 'description': 'Furniture, fixtures, equipment', 'priority': 'Medium'},
        {'category': 'Safety', 'description': 'Fire safety, security, emergency', 'priority': 'Critical'}
    ]
    
    categories_file = csv_output_path / "Construction_Categories.csv"
    with open(categories_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['category', 'description', 'priority'])
        writer.writeheader()
        writer.writerows(categories)
    
    # 5. Data Requirements CSV
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
    
    requirements_file = csv_output_path / "Data_Requirements.csv"
    with open(requirements_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['requirement', 'description', 'required'])
        writer.writeheader()
        writer.writerows(requirements)
    
    # Create processing script
    create_processing_script(output_path, file_inventory)
    
    # Create JSON summary
    json_summary = {
        'project_info': {
            'total_files': len(file_inventory),
            'dwg_files': len(dwg_files),
            'pdf_files': len(pdf_files),
            'total_size_mb': sum(item['size_mb'] for item in file_inventory),
            'processing_date': datetime.now().isoformat()
        },
        'file_breakdown': {
            'by_type': {},
            'by_folder': {},
            'by_priority': {}
        },
        'output_files': {
            'csv_data_folder': str(csv_output_path),
            'files_created': [
                'File_Inventory.csv',
                'Project_Summary.csv', 
                'Processing_Plan.csv',
                'Construction_Categories.csv',
                'Data_Requirements.csv'
            ]
        }
    }
    
    # Analyze file breakdown
    for item in file_inventory:
        # By type
        file_type = item['file_type']
        json_summary['file_breakdown']['by_type'][file_type] = json_summary['file_breakdown']['by_type'].get(file_type, 0) + 1
        
        # By folder
        folder = item['folder']
        json_summary['file_breakdown']['by_folder'][folder] = json_summary['file_breakdown']['by_folder'].get(folder, 0) + 1
        
        # By priority
        priority = item['priority']
        json_summary['file_breakdown']['by_priority'][priority] = json_summary['file_breakdown']['by_priority'].get(priority, 0) + 1
    
    # Save JSON summary
    json_file = output_path / "project_summary.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ CSV database created in: {csv_output_path}")
    print(f"📊 Total files catalogued: {len(file_inventory)}")
    print(f"📁 Output location: {output_path}")
    print(f"\n📋 Files created:")
    print(f"   - File_Inventory.csv ({len(file_inventory)} files)")
    print(f"   - Project_Summary.csv")
    print(f"   - Processing_Plan.csv ({len(processing_plan)} items)")
    print(f"   - Construction_Categories.csv")
    print(f"   - Data_Requirements.csv")
    print(f"   - project_summary.json")
    
    return csv_output_path

def create_processing_script(output_path, file_inventory):
    """Create a script to process all files"""
    
    # Filter DWG files
    dwg_files = [item for item in file_inventory if item['file_type'] == 'DWG']
    
    # Create batch script
    batch_script = f'''@echo off
echo Starting DWG conversion process...
echo.

mkdir "Converted_Data" 2>nul

'''
    
    for file_info in dwg_files:
        batch_script += f'''echo Processing: {file_info['file_name']}
"C:\\Users\\valgu\\Documents\\GitHub\\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\\DDC_Converter_DWG\\datadrivenlibs\\DwgExporter.exe" "{file_info['file_path']}" "Converted_Data"
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
& "C:\\Users\\valgu\\Documents\\GitHub\\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\\DDC_Converter_DWG\\datadrivenlibs\\DwgExporter.exe" "{file_info['file_path']}" "Converted_Data"
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
