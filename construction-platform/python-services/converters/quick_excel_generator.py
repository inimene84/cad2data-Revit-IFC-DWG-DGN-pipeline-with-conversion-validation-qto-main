#!/usr/bin/env python3
"""
Quick Excel Generator for Data-Driven Construction
Simple script to create Excel files from your project data
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
        file_inventory.append({
            'file_name': dwg_file.name,
            'file_path': str(dwg_file),
            'file_type': 'DWG',
            'folder': dwg_file.parent.name,
            'size_mb': round(dwg_file.stat().st_size / (1024*1024), 2),
            'modified_date': datetime.fromtimestamp(dwg_file.stat().st_mtime).strftime('%Y-%m-%d'),
            'status': 'Ready for conversion',
            'priority': 'High' if 'Archive' in str(dwg_file) else 'Medium'
        })
    
    # Process PDF files
    for pdf_file in pdf_files:
        file_inventory.append({
            'file_name': pdf_file.name,
            'file_path': str(pdf_file),
            'file_type': 'PDF',
            'folder': pdf_file.parent.name,
            'size_mb': round(pdf_file.stat().st_size / (1024*1024), 2),
            'modified_date': datetime.fromtimestamp(pdf_file.stat().st_mtime).strftime('%Y-%m-%d'),
            'status': 'Ready for OCR',
            'priority': 'Medium'
        })
    
    # Create Excel file with multiple sheets
    excel_file = output_path / "Data_Driven_Construction_Database.xlsx"
    
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
    print(f"📊 Total files catalogued: {len(file_inventory)}")
    print(f"📁 Output location: {output_path}")
    
    # Create processing script
    create_processing_script(output_path, file_inventory)
    
    return excel_file

def create_processing_script(output_path, file_inventory):
    """Create a script to process all files"""
    
    script_content = f'''#!/usr/bin/env python3
"""
Auto-generated processing script for your construction project
Run this to convert all DWG files to Excel data
"""

import subprocess
import os
from pathlib import Path

# DWG Converter path
dwg_converter = r"C:\\Users\\valgu\\Documents\\GitHub\\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\\DDC_Converter_DWG\\datadrivenlibs\\DwgExporter.exe"

# Files to process
files_to_process = {json.dumps([item for item in file_inventory if item['file_type'] == 'DWG'], indent=2)}

def process_dwg_file(dwg_path, output_dir):
    """Process a single DWG file"""
    try:
        print(f"Processing: {{dwg_path}}")
        cmd = f'"{dwg_converter}" "{{dwg_path}}" "{{output_dir}}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Success: {{dwg_path}}")
            return True
        else:
            print(f"❌ Failed: {{dwg_path}} - {{result.stderr}}")
            return False
    except Exception as e:
        print(f"❌ Error: {{dwg_path}} - {{str(e)}}")
        return False

def main():
    """Process all DWG files"""
    output_dir = r"{output_path}\\Converted_Data"
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    total_count = len(files_to_process)
    
    print(f"Starting conversion of {{total_count}} DWG files...")
    
    for file_info in files_to_process:
        if process_dwg_file(file_info['file_path'], output_dir):
            success_count += 1
    
    print(f"\\nConversion complete: {{success_count}}/{{total_count}} files processed successfully")

if __name__ == "__main__":
    main()
'''
    
    script_path = output_path / "process_all_files.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"🔧 Processing script created: {script_path}")

if __name__ == "__main__":
    create_project_excel()
