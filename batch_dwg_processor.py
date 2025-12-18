#!/usr/bin/env python3
"""
Batch DWG Processor with Progress Tracking
Continues processing all DWG files with detailed progress reporting
"""

import subprocess
import os
import time
from pathlib import Path
from datetime import datetime
import json
import pandas as pd

class BatchDWGProcessor:
    def __init__(self, project_path, output_path):
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True)
        
        # DWG Converter path
        self.dwg_converter = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_DWG\datadrivenlibs\DwgExporter.exe"
        
        # Processing log
        self.processing_log = []
        
    def find_all_dwg_files(self):
        """Find all DWG files in the project"""
        dwg_files = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.lower().endswith('.dwg') and not file.startswith('._'):
                    dwg_files.append(Path(root) / file)
        return dwg_files
    
    def process_single_dwg(self, dwg_file, output_dir):
        """Process a single DWG file"""
        start_time = time.time()
        
        try:
            print(f"🔧 Processing: {dwg_file.name}")
            print(f"   📁 Source: {dwg_file}")
            
            # Run converter
            cmd = f'"{self.dwg_converter}" "{dwg_file}" "{output_dir}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
            
            processing_time = time.time() - start_time
            
            # Check for success
            if result.returncode == 0:
                # Find generated Excel file
                excel_files = list(output_dir.glob(f"{dwg_file.stem}*.xlsx"))
                
                if excel_files:
                    excel_file = excel_files[0]
                    file_size = excel_file.stat().st_size
                    
                    # Get Excel file info
                    try:
                        df = pd.read_excel(excel_file)
                        rows, cols = df.shape
                    except:
                        rows, cols = 0, 0
                    
                    print(f"   ✅ Success: {excel_file.name}")
                    print(f"   📊 Data: {rows} rows, {cols} columns")
                    print(f"   ⏱️  Time: {processing_time:.1f}s")
                    
                    return {
                        'file_name': dwg_file.name,
                        'file_path': str(dwg_file),
                        'status': 'Success',
                        'excel_file': str(excel_file),
                        'file_size_mb': round(file_size / (1024*1024), 2),
                        'rows': rows,
                        'columns': cols,
                        'processing_time': round(processing_time, 2),
                        'error_message': None
                    }
                else:
                    print(f"   ⚠️  Warning: No Excel file generated")
                    return {
                        'file_name': dwg_file.name,
                        'file_path': str(dwg_file),
                        'status': 'Warning',
                        'excel_file': None,
                        'file_size_mb': 0,
                        'rows': 0,
                        'columns': 0,
                        'processing_time': round(processing_time, 2),
                        'error_message': 'No Excel file generated'
                    }
            else:
                print(f"   ❌ Failed: {result.stderr}")
                return {
                    'file_name': dwg_file.name,
                    'file_path': str(dwg_file),
                    'status': 'Failed',
                    'excel_file': None,
                    'file_size_mb': 0,
                    'rows': 0,
                    'columns': 0,
                    'processing_time': round(processing_time, 2),
                    'error_message': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout: Processing took too long")
            return {
                'file_name': dwg_file.name,
                'file_path': str(dwg_file),
                'status': 'Timeout',
                'excel_file': None,
                'file_size_mb': 0,
                'rows': 0,
                'columns': 0,
                'processing_time': 600,
                'error_message': 'Processing timeout (10 minutes)'
            }
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {
                'file_name': dwg_file.name,
                'file_path': str(dwg_file),
                'status': 'Error',
                'excel_file': None,
                'file_size_mb': 0,
                'rows': 0,
                'columns': 0,
                'processing_time': round(time.time() - start_time, 2),
                'error_message': str(e)
            }
    
    def process_all_dwg_files(self):
        """Process all DWG files in the project"""
        print("🚀 Starting Batch DWG Processing")
        print("=" * 60)
        
        # Find all DWG files
        dwg_files = self.find_all_dwg_files()
        print(f"📁 Found {len(dwg_files)} DWG files to process")
        
        if not dwg_files:
            print("❌ No DWG files found to process")
            return
        
        # Create output directory
        output_dir = self.output_path / "Converted_Data"
        output_dir.mkdir(exist_ok=True)
        
        # Process each file
        total_files = len(dwg_files)
        success_count = 0
        warning_count = 0
        failed_count = 0
        
        start_time = time.time()
        
        for i, dwg_file in enumerate(dwg_files, 1):
            print(f"\n📋 Progress: {i}/{total_files} ({(i/total_files)*100:.1f}%)")
            
            result = self.process_single_dwg(dwg_file, output_dir)
            self.processing_log.append(result)
            
            # Update counters
            if result['status'] == 'Success':
                success_count += 1
            elif result['status'] == 'Warning':
                warning_count += 1
            else:
                failed_count += 1
            
            # Show running totals
            print(f"   📊 Running totals: ✅ {success_count} | ⚠️  {warning_count} | ❌ {failed_count}")
        
        # Calculate final statistics
        total_time = time.time() - start_time
        
        print(f"\n" + "=" * 60)
        print("🎉 BATCH PROCESSING COMPLETED!")
        print(f"📊 Final Results:")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ⚠️  Warnings: {warning_count}")
        print(f"   ❌ Failed: {failed_count}")
        print(f"   ⏱️  Total Time: {total_time/60:.1f} minutes")
        print(f"   📁 Output: {output_dir}")
        
        # Create detailed report
        self.create_processing_report()
        
        return {
            'total_files': total_files,
            'successful': success_count,
            'warnings': warning_count,
            'failed': failed_count,
            'total_time': total_time,
            'output_directory': str(output_dir)
        }
    
    def create_processing_report(self):
        """Create a detailed processing report"""
        if not self.processing_log:
            return
        
        # Create DataFrame from log
        df = pd.DataFrame(self.processing_log)
        
        # Save detailed report
        report_file = self.output_path / "DWG_Processing_Report.xlsx"
        
        with pd.ExcelWriter(report_file, engine='openpyxl') as writer:
            # All results
            df.to_excel(writer, sheet_name='All_Results', index=False)
            
            # Summary by status
            status_summary = df.groupby('status').agg({
                'file_name': 'count',
                'file_size_mb': 'sum',
                'rows': 'sum',
                'columns': 'mean',
                'processing_time': 'sum'
            }).round(2)
            status_summary.to_excel(writer, sheet_name='Status_Summary')
            
            # Failed files details
            failed_files = df[df['status'].isin(['Failed', 'Error', 'Timeout'])]
            if not failed_files.empty:
                failed_files.to_excel(writer, sheet_name='Failed_Files', index=False)
            
            # Performance metrics
            metrics = {
                'Metric': [
                    'Total Files Processed',
                    'Success Rate (%)',
                    'Average Processing Time (seconds)',
                    'Total Data Rows',
                    'Total File Size (MB)',
                    'Processing Date'
                ],
                'Value': [
                    len(df),
                    round((df['status'] == 'Success').sum() / len(df) * 100, 1),
                    round(df['processing_time'].mean(), 2),
                    df['rows'].sum(),
                    round(df['file_size_mb'].sum(), 2),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            metrics_df = pd.DataFrame(metrics)
            metrics_df.to_excel(writer, sheet_name='Performance_Metrics', index=False)
        
        print(f"📊 Detailed report created: {report_file}")

def main():
    """Main execution function"""
    project_path = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project"
    output_path = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Batch_Processing_Output"
    
    # Create processor
    processor = BatchDWGProcessor(project_path, output_path)
    
    # Process all DWG files
    results = processor.process_all_dwg_files()
    
    return results

if __name__ == "__main__":
    main()
