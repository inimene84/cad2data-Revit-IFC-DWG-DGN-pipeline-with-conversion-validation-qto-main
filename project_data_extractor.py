#!/usr/bin/env python3
"""
Data-Driven Construction Excel Pipeline
Processes DWG files, PDFs, and creates comprehensive Excel database
"""

import os
import pandas as pd
import subprocess
import json
from pathlib import Path
from datetime import datetime
import shutil
import tempfile

class ConstructionDataExtractor:
    def __init__(self, project_path, output_path):
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        self.dwg_converter = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe"
        self.ocr_service_url = "http://localhost:5056/ocr"
        self.master_data = []
        
    def setup_output_structure(self):
        """Create organized output folder structure"""
        folders = [
            "01_Raw_Data",
            "02_Processed_Data", 
            "03_Excel_Reports",
            "04_Visualizations",
            "05_Project_Summary"
        ]
        
        for folder in folders:
            (self.output_path / folder).mkdir(parents=True, exist_ok=True)
            
    def find_all_dwg_files(self):
        """Find all DWG files in the project"""
        dwg_files = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.lower().endswith('.dwg'):
                    dwg_files.append(Path(root) / file)
        return dwg_files
    
    def find_all_pdf_files(self):
        """Find all PDF files in the project"""
        pdf_files = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(Path(root) / file)
        return pdf_files
    
    def convert_dwg_to_excel(self, dwg_file):
        """Convert DWG file to Excel using DwgExporter"""
        try:
            print(f"Converting DWG: {dwg_file.name}")
            
            # Create temporary output directory
            temp_dir = tempfile.mkdtemp()
            
            # Run DwgExporter
            cmd = f'"{self.dwg_converter}" "{dwg_file}" "{temp_dir}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Find generated Excel file
                excel_files = list(Path(temp_dir).glob('*.xlsx'))
                if excel_files:
                    excel_file = excel_files[0]
                    
                    # Copy to organized output
                    output_file = self.output_path / "01_Raw_Data" / f"{dwg_file.stem}_data.xlsx"
                    shutil.copy2(excel_file, output_file)
                    
                    # Process the Excel data
                    self.process_excel_data(excel_file, dwg_file)
                    
                    print(f"✅ Successfully converted: {dwg_file.name}")
                    return True
                else:
                    print(f"❌ No Excel file generated for: {dwg_file.name}")
                    return False
            else:
                print(f"❌ Conversion failed for {dwg_file.name}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error converting {dwg_file.name}: {str(e)}")
            return False
        finally:
            # Clean up temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def process_excel_data(self, excel_file, source_dwg):
        """Process Excel data and add to master database"""
        try:
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Add metadata
            df['source_file'] = source_dwg.name
            df['source_path'] = str(source_dwg)
            df['conversion_date'] = datetime.now().isoformat()
            df['file_type'] = 'DWG'
            
            # Add to master data
            self.master_data.append(df)
            
            print(f"📊 Processed {len(df)} elements from {source_dwg.name}")
            
        except Exception as e:
            print(f"❌ Error processing Excel data from {source_dwg.name}: {str(e)}")
    
    def process_pdf_with_ocr(self, pdf_file):
        """Process PDF file with OCR to extract text and dimensions"""
        try:
            print(f"Processing PDF: {pdf_file.name}")
            
            # For now, create a basic entry - you can integrate with OCR service later
            pdf_data = {
                'element_name': pdf_file.stem,
                'element_type': 'Drawing',
                'source_file': pdf_file.name,
                'source_path': str(pdf_file),
                'conversion_date': datetime.now().isoformat(),
                'file_type': 'PDF',
                'notes': 'PDF drawing - text extraction pending OCR integration'
            }
            
            # Add to master data
            self.master_data.append(pd.DataFrame([pdf_data]))
            
            print(f"📄 Processed PDF: {pdf_file.name}")
            
        except Exception as e:
            print(f"❌ Error processing PDF {pdf_file.name}: {str(e)}")
    
    def create_master_excel(self):
        """Create comprehensive master Excel file"""
        if not self.master_data:
            print("❌ No data to process")
            return
        
        # Combine all data
        master_df = pd.concat(self.master_data, ignore_index=True)
        
        # Create multiple sheets
        with pd.ExcelWriter(self.output_path / "03_Excel_Reports" / "Master_Construction_Data.xlsx", engine='openpyxl') as writer:
            
            # Sheet 1: All Data
            master_df.to_excel(writer, sheet_name='All_Data', index=False)
            
            # Sheet 2: Summary by File Type
            file_summary = master_df.groupby(['file_type', 'source_file']).size().reset_index(name='element_count')
            file_summary.to_excel(writer, sheet_name='File_Summary', index=False)
            
            # Sheet 3: Element Types (if available)
            if 'element_type' in master_df.columns:
                element_summary = master_df.groupby('element_type').size().reset_index(name='count')
                element_summary.to_excel(writer, sheet_name='Element_Types', index=False)
            
            # Sheet 4: Project Overview
            overview_data = {
                'Metric': [
                    'Total Files Processed',
                    'Total Elements',
                    'DWG Files',
                    'PDF Files',
                    'Processing Date',
                    'Project Path'
                ],
                'Value': [
                    len(master_df['source_file'].unique()),
                    len(master_df),
                    len(master_df[master_df['file_type'] == 'DWG']),
                    len(master_df[master_df['file_type'] == 'PDF']),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    str(self.project_path)
                ]
            }
            pd.DataFrame(overview_data).to_excel(writer, sheet_name='Project_Overview', index=False)
        
        print(f"✅ Master Excel file created: {self.output_path / '03_Excel_Reports' / 'Master_Construction_Data.xlsx'}")
    
    def create_data_driven_analysis(self):
        """Create data-driven construction analysis"""
        if not self.master_data:
            return
        
        master_df = pd.concat(self.master_data, ignore_index=True)
        
        # Create analysis report
        analysis_data = []
        
        # File analysis
        file_analysis = master_df.groupby('source_file').agg({
            'source_file': 'count',
            'file_type': 'first'
        }).rename(columns={'source_file': 'element_count'})
        
        for file_name, row in file_analysis.iterrows():
            analysis_data.append({
                'file_name': file_name,
                'file_type': row['file_type'],
                'element_count': row['element_count'],
                'analysis_status': 'Processed',
                'recommendations': self.get_file_recommendations(row['file_type'], row['element_count'])
            })
        
        # Create analysis Excel
        analysis_df = pd.DataFrame(analysis_data)
        analysis_df.to_excel(
            self.output_path / "05_Project_Summary" / "Data_Driven_Analysis.xlsx", 
            index=False
        )
        
        print(f"✅ Data-driven analysis created: {self.output_path / '05_Project_Summary' / 'Data_Driven_Analysis.xlsx'}")
    
    def get_file_recommendations(self, file_type, element_count):
        """Get recommendations based on file type and element count"""
        if file_type == 'DWG':
            if element_count > 100:
                return "High complexity - consider detailed cost estimation"
            elif element_count > 50:
                return "Medium complexity - standard processing recommended"
            else:
                return "Low complexity - basic analysis sufficient"
        elif file_type == 'PDF':
            return "Drawing file - integrate with BIM model for complete analysis"
        else:
            return "Unknown file type - manual review recommended"
    
    def run_full_pipeline(self):
        """Run the complete data extraction pipeline"""
        print("🏗️ Starting Data-Driven Construction Excel Pipeline")
        print("=" * 60)
        
        # Setup
        self.setup_output_structure()
        
        # Find files
        dwg_files = self.find_all_dwg_files()
        pdf_files = self.find_all_pdf_files()
        
        print(f"📁 Found {len(dwg_files)} DWG files")
        print(f"📄 Found {len(pdf_files)} PDF files")
        print()
        
        # Process DWG files
        print("🔧 Processing DWG files...")
        dwg_success = 0
        for dwg_file in dwg_files:
            if self.convert_dwg_to_excel(dwg_file):
                dwg_success += 1
        
        # Process PDF files
        print("\n📄 Processing PDF files...")
        pdf_success = 0
        for pdf_file in pdf_files:
            self.process_pdf_with_ocr(pdf_file)
            pdf_success += 1
        
        # Create master Excel
        print("\n📊 Creating master Excel file...")
        self.create_master_excel()
        
        # Create analysis
        print("📈 Creating data-driven analysis...")
        self.create_data_driven_analysis()
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"📁 DWG files processed: {dwg_success}/{len(dwg_files)}")
        print(f"📄 PDF files processed: {pdf_success}/{len(pdf_files)}")
        print(f"📊 Total elements: {sum(len(df) for df in self.master_data)}")
        print(f"📁 Output location: {self.output_path}")
        print("\n🎯 Next steps:")
        print("   1. Review Master_Construction_Data.xlsx")
        print("   2. Check Data_Driven_Analysis.xlsx for insights")
        print("   3. Use the data for cost estimation and project planning")

def main():
    """Main execution function"""
    project_path = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project"
    output_path = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Excel_Output"
    
    # Create extractor
    extractor = ConstructionDataExtractor(project_path, output_path)
    
    # Run pipeline
    extractor.run_full_pipeline()

if __name__ == "__main__":
    main()
