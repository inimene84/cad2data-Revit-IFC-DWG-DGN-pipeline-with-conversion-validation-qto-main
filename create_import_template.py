#!/usr/bin/env python3
"""
Create Excel template for importing real project data
"""

import pandas as pd
from datetime import datetime

# Sample data for the template
sample_data = [
    {
        'Project Name': 'Villa Munich 2023',
        'Property Type': 'villa',
        'Size (sqm)': 350,
        'Bedrooms': 5,
        'Bathrooms': 4,
        'Floors': 2,
        'Construction Year': 2023,
        'Location': 'Munich',
        'Quality Level': 'luxury',
        'Actual Total Cost': 850000,
        'Construction Start Date': '2023-01-15',
        'Construction End Date': '2023-12-20',
        'Contractor Name': 'Bauhaus München',
        'Project Status': 'completed',
        'Data Source': 'contractor_quote'
    },
    {
        'Project Name': 'Family House Berlin 2022',
        'Property Type': 'family_house',
        'Size (sqm)': 180,
        'Bedrooms': 4,
        'Bathrooms': 2,
        'Floors': 2,
        'Construction Year': 2022,
        'Location': 'Berlin',
        'Quality Level': 'standard',
        'Actual Total Cost': 320000,
        'Construction Start Date': '2022-03-01',
        'Construction End Date': '2022-11-30',
        'Contractor Name': 'Berlin Bau GmbH',
        'Project Status': 'completed',
        'Data Source': 'manual'
    },
    {
        'Project Name': 'Modern Apartment Cologne 2023',
        'Property Type': 'apartment',
        'Size (sqm)': 95,
        'Bedrooms': 2,
        'Bathrooms': 1,
        'Floors': 1,
        'Construction Year': 2023,
        'Location': 'Cologne',
        'Quality Level': 'standard',
        'Actual Total Cost': 180000,
        'Construction Start Date': '2023-06-01',
        'Construction End Date': '2023-12-15',
        'Contractor Name': 'Köln Bau GmbH',
        'Project Status': 'completed',
        'Data Source': 'manual'
    },
    {
        'Project Name': 'Luxury Villa Hamburg 2024',
        'Property Type': 'villa',
        'Size (sqm)': 450,
        'Bedrooms': 6,
        'Bathrooms': 5,
        'Floors': 3,
        'Construction Year': 2024,
        'Location': 'Hamburg',
        'Quality Level': 'premium',
        'Actual Total Cost': 1200000,
        'Construction Start Date': '2024-01-15',
        'Construction End Date': '2024-12-20',
        'Contractor Name': 'Hamburg Bau AG',
        'Project Status': 'in_progress',
        'Data Source': 'contractor_quote'
    },
    {
        'Project Name': 'Family House Frankfurt 2024',
        'Property Type': 'family_house',
        'Size (sqm)': 220,
        'Bedrooms': 4,
        'Bathrooms': 3,
        'Floors': 2,
        'Construction Year': 2024,
        'Location': 'Frankfurt',
        'Quality Level': 'luxury',
        'Actual Total Cost': 650000,
        'Construction Start Date': '2024-03-01',
        'Construction End Date': '2024-11-30',
        'Contractor Name': 'Frankfurt Construction Ltd',
        'Project Status': 'completed',
        'Data Source': 'contractor_quote'
    }
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Create Excel file with multiple sheets
with pd.ExcelWriter('Project_Data_Import_Template.xlsx', engine='openpyxl') as writer:
    # Sheet 1: Sample Data
    df.to_excel(writer, sheet_name='Sample_Data', index=False)
    
    # Sheet 2: Template (empty with headers)
    template_df = pd.DataFrame(columns=df.columns)
    template_df.to_excel(writer, sheet_name='Template', index=False)
    
    # Sheet 3: Field Descriptions
    field_descriptions = pd.DataFrame([
        {'Field Name': 'Project Name', 'Description': 'Unique name for the project', 'Required': 'Yes', 'Example': 'Villa Munich 2023'},
        {'Field Name': 'Property Type', 'Description': 'Type of property (villa, family_house, apartment, mansion)', 'Required': 'Yes', 'Example': 'villa'},
        {'Field Name': 'Size (sqm)', 'Description': 'Total floor area in square meters', 'Required': 'Yes', 'Example': '350'},
        {'Field Name': 'Bedrooms', 'Description': 'Number of bedrooms', 'Required': 'No', 'Example': '5'},
        {'Field Name': 'Bathrooms', 'Description': 'Number of bathrooms', 'Required': 'No', 'Example': '4'},
        {'Field Name': 'Floors', 'Description': 'Number of floors', 'Required': 'No', 'Example': '2'},
        {'Field Name': 'Construction Year', 'Description': 'Year construction was completed or started', 'Required': 'Yes', 'Example': '2023'},
        {'Field Name': 'Location', 'Description': 'City or region where property is located', 'Required': 'Yes', 'Example': 'Munich'},
        {'Field Name': 'Quality Level', 'Description': 'Quality level (basic, standard, luxury, premium)', 'Required': 'No', 'Example': 'luxury'},
        {'Field Name': 'Actual Total Cost', 'Description': 'Total construction cost in EUR', 'Required': 'Yes', 'Example': '850000'},
        {'Field Name': 'Construction Start Date', 'Description': 'Start date of construction (YYYY-MM-DD)', 'Required': 'No', 'Example': '2023-01-15'},
        {'Field Name': 'Construction End Date', 'Description': 'End date of construction (YYYY-MM-DD)', 'Required': 'No', 'Example': '2023-12-20'},
        {'Field Name': 'Contractor Name', 'Description': 'Name of the main contractor', 'Required': 'No', 'Example': 'Bauhaus München'},
        {'Field Name': 'Project Status', 'Description': 'Current status (planned, in_progress, completed, cancelled)', 'Required': 'No', 'Example': 'completed'},
        {'Field Name': 'Data Source', 'Description': 'Source of the data (manual, contractor_quote, api, file_import)', 'Required': 'No', 'Example': 'contractor_quote'}
    ])
    field_descriptions.to_excel(writer, sheet_name='Field_Descriptions', index=False)
    
    # Sheet 4: Validation Rules
    validation_rules = pd.DataFrame([
        {'Field': 'Project Name', 'Rule': 'Must be unique and descriptive', 'Format': 'Text'},
        {'Field': 'Property Type', 'Rule': 'Must be one of: villa, family_house, apartment, mansion', 'Format': 'Text'},
        {'Field': 'Size (sqm)', 'Rule': 'Must be positive number', 'Format': 'Number'},
        {'Field': 'Bedrooms', 'Rule': 'Must be non-negative integer', 'Format': 'Integer'},
        {'Field': 'Bathrooms', 'Rule': 'Must be non-negative integer', 'Format': 'Integer'},
        {'Field': 'Floors', 'Rule': 'Must be positive integer', 'Format': 'Integer'},
        {'Field': 'Construction Year', 'Rule': 'Must be between 1900 and current year', 'Format': 'Integer'},
        {'Field': 'Location', 'Rule': 'Must be valid city/region name', 'Format': 'Text'},
        {'Field': 'Quality Level', 'Rule': 'Must be one of: basic, standard, luxury, premium', 'Format': 'Text'},
        {'Field': 'Actual Total Cost', 'Rule': 'Must be positive number', 'Format': 'Number'},
        {'Field': 'Construction Start Date', 'Rule': 'Must be valid date (YYYY-MM-DD)', 'Format': 'Date'},
        {'Field': 'Construction End Date', 'Rule': 'Must be valid date (YYYY-MM-DD)', 'Format': 'Date'},
        {'Field': 'Contractor Name', 'Rule': 'Must be valid company name', 'Format': 'Text'},
        {'Field': 'Project Status', 'Rule': 'Must be one of: planned, in_progress, completed, cancelled', 'Format': 'Text'},
        {'Field': 'Data Source', 'Rule': 'Must be one of: manual, contractor_quote, api, file_import', 'Format': 'Text'}
    ])
    validation_rules.to_excel(writer, sheet_name='Validation_Rules', index=False)

print("✅ Excel template created: Project_Data_Import_Template.xlsx")
print("📊 Contains 4 sheets:")
print("   - Sample_Data: Example data to get you started")
print("   - Template: Empty template for your data")
print("   - Field_Descriptions: Detailed field descriptions")
print("   - Validation_Rules: Data validation rules")
