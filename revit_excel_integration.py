#!/usr/bin/env python3
"""
Revit Excel Integration Script
Imports Excel data into Revit parameters and families
"""

import pandas as pd
import os
from pathlib import Path

class RevitExcelIntegration:
    def __init__(self, excel_folder, revit_project_path):
        self.excel_folder = Path(excel_folder)
        self.revit_project_path = Path(revit_project_path)
        
    def create_revit_import_template(self):
        """Create Excel template for Revit parameter import"""
        
        # Sample data structure for Revit import
        revit_template = {
            'Element_ID': ['WALL_001', 'WALL_002', 'DOOR_001', 'WINDOW_001'],
            'Element_Type': ['Wall', 'Wall', 'Door', 'Window'],
            'Family_Name': ['Basic Wall', 'Basic Wall', 'Single-Flush', 'Fixed'],
            'Type_Name': ['Generic 8"', 'Generic 6"', '36" x 84"', '24" x 48"'],
            'Length': [10.0, 15.5, 3.0, 2.0],
            'Height': [10.0, 10.0, 7.0, 4.0],
            'Width': [0.67, 0.5, 0.125, 0.125],
            'Area': [67.0, 77.5, 0.375, 0.25],
            'Volume': [44.89, 38.75, 0.047, 0.031],
            'Material': ['Concrete', 'Steel', 'Wood', 'Glass'],
            'Cost_Per_Unit': [120.0, 150.0, 800.0, 600.0],
            'Total_Cost': [5386.8, 5812.5, 37.6, 18.6],
            'Level': ['Level 1', 'Level 1', 'Level 1', 'Level 1'],
            'Room': ['Room 101', 'Room 102', 'Room 101', 'Room 102'],
            'Comments': ['Load bearing', 'Partition', 'Entry door', 'View window']
        }
        
        template_df = pd.DataFrame(revit_template)
        
        # Save template
        template_file = self.excel_folder / "Revit_Import_Template.xlsx"
        template_df.to_excel(template_file, index=False)
        
        print(f"✅ Revit import template created: {template_file}")
        return template_file
    
    def process_dwg_data_for_revit(self):
        """Process DWG Excel files for Revit import"""
        
        # Find all cleaned Excel files
        excel_files = list(self.excel_folder.glob("cleaned_*.xlsx"))
        
        revit_data = []
        
        for file in excel_files:
            try:
                df = pd.read_excel(file)
                
                # Extract relevant data for Revit
                if 'ID' in df.columns and 'Name' in df.columns:
                    for _, row in df.iterrows():
                        revit_data.append({
                            'Source_File': file.name,
                            'Element_ID': row.get('ID', ''),
                            'Element_Name': row.get('Name', ''),
                            'Description': row.get('Description', ''),
                            'Layer': row.get('Layer', ''),
                            'Color': row.get('Color', ''),
                            'Handle': row.get('Handle', ''),
                            'File_Path': str(file)
                        })
                        
            except Exception as e:
                print(f"❌ Error processing {file.name}: {e}")
        
        # Create consolidated Revit data
        revit_df = pd.DataFrame(revit_data)
        
        # Save consolidated data
        consolidated_file = self.excel_folder / "Consolidated_Revit_Data.xlsx"
        revit_df.to_excel(consolidated_file, index=False)
        
        print(f"✅ Consolidated Revit data created: {consolidated_file}")
        print(f"📊 Total elements: {len(revit_df)}")
        
        return consolidated_file
    
    def create_revit_parameter_mapping(self):
        """Create mapping between Excel columns and Revit parameters"""
        
        mapping = {
            'Excel_Column': [
                'Element_ID', 'Element_Type', 'Family_Name', 'Type_Name',
                'Length', 'Height', 'Width', 'Area', 'Volume',
                'Material', 'Cost_Per_Unit', 'Total_Cost',
                'Level', 'Room', 'Comments'
            ],
            'Revit_Parameter': [
                'Element ID', 'Type', 'Family', 'Type Name',
                'Length', 'Height', 'Width', 'Area', 'Volume',
                'Material', 'Cost Per Unit', 'Total Cost',
                'Level', 'Room', 'Comments'
            ],
            'Parameter_Type': [
                'Text', 'Text', 'Text', 'Text',
                'Length', 'Length', 'Length', 'Area', 'Volume',
                'Text', 'Currency', 'Currency',
                'Text', 'Text', 'Text'
            ],
            'Parameter_Group': [
                'Identity Data', 'Identity Data', 'Identity Data', 'Identity Data',
                'Dimensions', 'Dimensions', 'Dimensions', 'Dimensions', 'Dimensions',
                'Materials and Finishes', 'Construction', 'Construction',
                'Identity Data', 'Identity Data', 'Identity Data'
            ]
        }
        
        mapping_df = pd.DataFrame(mapping)
        
        # Save mapping
        mapping_file = self.excel_folder / "Revit_Parameter_Mapping.xlsx"
        mapping_df.to_excel(mapping_file, index=False)
        
        print(f"✅ Parameter mapping created: {mapping_file}")
        return mapping_file
    
    def create_quantity_schedule_template(self):
        """Create quantity takeoff schedule template"""
        
        # Sample quantity data
        quantities = {
            'Category': ['Walls', 'Doors', 'Windows', 'Floors', 'Roofs'],
            'Element_Type': ['Basic Wall', 'Single-Flush Door', 'Fixed Window', 'Generic Floor', 'Generic Roof'],
            'Count': [45, 12, 8, 5, 2],
            'Total_Area': [1250.5, 0, 0, 800.2, 650.3],
            'Total_Volume': [850.4, 0, 0, 0, 0],
            'Total_Length': [0, 0, 0, 0, 0],
            'Material': ['Concrete', 'Wood', 'Glass', 'Concrete', 'Steel'],
            'Unit_Cost': [120.0, 800.0, 600.0, 95.0, 180.0],
            'Total_Cost': [102048.0, 9600.0, 4800.0, 76019.0, 117054.0]
        }
        
        quantities_df = pd.DataFrame(quantities)
        
        # Save quantities template
        quantities_file = self.excel_folder / "Quantity_Takeoff_Schedule.xlsx"
        quantities_df.to_excel(quantities_file, index=False)
        
        print(f"✅ Quantity schedule created: {quantities_file}")
        return quantities_file

def main():
    """Main execution function"""
    
    # Paths
    excel_folder = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project\Cleaned_Excel_Files"
    revit_project_path = r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\Project"
    
    # Create integration tool
    integration = RevitExcelIntegration(excel_folder, revit_project_path)
    
    print("🏗️ Creating Revit Integration Files")
    print("=" * 50)
    
    # Create all templates
    integration.create_revit_import_template()
    integration.process_dwg_data_for_revit()
    integration.create_revit_parameter_mapping()
    integration.create_quantity_schedule_template()
    
    print("\n✅ All Revit integration files created!")
    print("📁 Location: Project/Cleaned_Excel_Files/")

if __name__ == "__main__":
    main()
