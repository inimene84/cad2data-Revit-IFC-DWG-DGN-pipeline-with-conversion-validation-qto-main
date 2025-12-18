#!/usr/bin/env python3
"""
Excel Cleanup Script for DataDrivenConstruction Output
Removes ads and unwanted content from converted Excel files
"""

import pandas as pd
import os
import re
from pathlib import Path
import shutil
from datetime import datetime

class ExcelCleanupTool:
    def __init__(self, input_folder, output_folder):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Common ad patterns to remove
        self.ad_patterns = [
            r'DataDrivenConstruction',
            r'Advertisement',
            r'Ad-Free',
            r'Free version',
            r'Visit.*datadrivenconstruction',
            r'www\.datadrivenconstruction',
            r'info@datadrivenconstruction',
            r'DDC.*Community',
            r'DDC.*Converter',
            r'Download.*full.*version',
            r'Upgrade.*to.*pro',
            r'Get.*ad-free',
            r'Remove.*ads',
            r'Commercial.*license',
            r'Purchase.*license'
        ]
        
        # Unwanted column patterns
        self.unwanted_columns = [
            'Advertisement',
            'Ad_Content',
            'DDC_Info',
            'Free_Version_Notice',
            'Upgrade_Notice'
        ]
    
    def clean_dataframe(self, df):
        """Clean a single DataFrame by removing ads and unwanted content"""
        print(f"  📊 Original shape: {df.shape}")
        
        # Remove rows containing ad content
        original_rows = len(df)
        for pattern in self.ad_patterns:
            # Check all columns for ad content
            mask = df.astype(str).apply(
                lambda x: x.str.contains(pattern, case=False, na=False, regex=True)
            ).any(axis=1)
            df = df[~mask]
        
        rows_removed = original_rows - len(df)
        if rows_removed > 0:
            print(f"  🗑️  Removed {rows_removed} rows with ad content")
        
        # Remove unwanted columns
        original_cols = len(df.columns)
        for col_pattern in self.unwanted_columns:
            df = df.loc[:, ~df.columns.str.contains(col_pattern, case=False, na=False)]
        
        cols_removed = original_cols - len(df.columns)
        if cols_removed > 0:
            print(f"  🗑️  Removed {cols_removed} columns with ad content")
        
        # Clean cell content
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                df[col] = df[col].astype(str).apply(self.clean_cell_content)
        
        print(f"  ✅ Cleaned shape: {df.shape}")
        return df
    
    def clean_cell_content(self, cell_content):
        """Clean individual cell content"""
        if pd.isna(cell_content) or cell_content == 'nan':
            return cell_content
        
        content = str(cell_content)
        
        # Remove ad patterns from cell content
        for pattern in self.ad_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        return content if content else None
    
    def process_excel_file(self, file_path):
        """Process a single Excel file"""
        print(f"\n🔧 Processing: {file_path.name}")
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Clean the data
            cleaned_df = self.clean_dataframe(df)
            
            # Create output filename
            output_file = self.output_folder / f"cleaned_{file_path.name}"
            
            # Save cleaned file
            cleaned_df.to_excel(output_file, index=False)
            
            # Create summary
            summary = {
                'original_file': str(file_path),
                'cleaned_file': str(output_file),
                'original_rows': len(df),
                'cleaned_rows': len(cleaned_df),
                'original_cols': len(df.columns),
                'cleaned_cols': len(cleaned_df.columns),
                'rows_removed': len(df) - len(cleaned_df),
                'cols_removed': len(df.columns) - len(cleaned_df.columns),
                'processing_date': datetime.now().isoformat()
            }
            
            print(f"  ✅ Saved: {output_file.name}")
            return summary
            
        except Exception as e:
            print(f"  ❌ Error processing {file_path.name}: {str(e)}")
            return None
    
    def process_all_excel_files(self):
        """Process all Excel files in the input folder"""
        print("🧹 Starting Excel Cleanup Process")
        print("=" * 50)
        
        # Find all Excel files
        excel_files = list(self.input_folder.rglob("*.xlsx"))
        excel_files = [f for f in excel_files if not f.name.startswith('cleaned_')]
        
        print(f"📁 Found {len(excel_files)} Excel files to clean")
        
        if not excel_files:
            print("❌ No Excel files found to process")
            return
        
        # Process each file
        summaries = []
        for file_path in excel_files:
            summary = self.process_excel_file(file_path)
            if summary:
                summaries.append(summary)
        
        # Create summary report
        self.create_summary_report(summaries)
        
        print(f"\n✅ Cleanup completed! Processed {len(summaries)} files")
        print(f"📁 Cleaned files saved to: {self.output_folder}")
    
    def create_summary_report(self, summaries):
        """Create a summary report of the cleanup process"""
        if not summaries:
            return
        
        # Create summary DataFrame
        summary_df = pd.DataFrame(summaries)
        
        # Save summary report
        summary_file = self.output_folder / "cleanup_summary.xlsx"
        
        with pd.ExcelWriter(summary_file, engine='openpyxl') as writer:
            # Summary sheet
            summary_df.to_excel(writer, sheet_name='Cleanup_Summary', index=False)
            
            # Statistics sheet
            stats = {
                'Metric': [
                    'Total Files Processed',
                    'Total Rows Removed',
                    'Total Columns Removed',
                    'Average Rows per File',
                    'Average Columns per File',
                    'Processing Date'
                ],
                'Value': [
                    len(summaries),
                    summary_df['rows_removed'].sum(),
                    summary_df['cols_removed'].sum(),
                    summary_df['cleaned_rows'].mean(),
                    summary_df['cleaned_cols'].mean(),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            
            stats_df = pd.DataFrame(stats)
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        print(f"📊 Summary report created: {summary_file}")

def main():
    """Main execution function"""
    # Define paths
    input_folder = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project"
    output_folder = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Cleaned_Excel_Files"
    
    # Create cleanup tool
    cleanup_tool = ExcelCleanupTool(input_folder, output_folder)
    
    # Process all Excel files
    cleanup_tool.process_all_excel_files()

if __name__ == "__main__":
    main()
