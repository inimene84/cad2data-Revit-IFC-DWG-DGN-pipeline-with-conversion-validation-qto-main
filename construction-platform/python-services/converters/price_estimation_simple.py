#!/usr/bin/env python3
"""
Simple Construction Price Estimation for IFC Parking Structure
Based on German/EU construction costs (2024)
"""

import pandas as pd
import numpy as np

def estimate_construction_costs():
    print("🏗️ Construction Price Estimation for Parking Structure")
    print("=" * 60)
    
    # Load the IFC data
    df = pd.read_excel('./Sample_Projects/Ifc2x3_Parking_sample_ifc.xlsx')
    
    # Define typical unit costs (EUR per m³) for different building elements
    # Based on German construction costs 2024
    unit_costs = {
        'IfcWallStandardCase': 450,    # Concrete walls: €450/m³
        'IfcColumn': 380,              # Concrete columns: €380/m³
        'IfcSlab': 420,                # Concrete slabs: €420/m³
        'IfcBeam': 400,                # Concrete beams: €400/m³
        'IfcFooting': 350,             # Foundations: €350/m³
        'IfcStair': 800,               # Stairs: €800/m³
        'IfcRamp': 500,                # Ramps: €500/m³
        'IfcRailing': 150,             # Railings: €150/m (per length)
        'IfcDoor': 800,                # Doors: €800/unit
        'IfcWindow': 600,              # Windows: €600/unit
        'Default': 300                 # Default rate: €300/m³
    }
    
    # Get volume column
    volume_col = '[BaseQuantities] GrossVolume'
    area_col = '[BaseQuantities] GrossArea'
    length_col = '[BaseQuantities] Length'
    
    # Filter elements with quantity data
    df_with_quantities = df.dropna(subset=[volume_col], how='all').copy()
    
    print(f"📊 Analyzing {len(df_with_quantities)} elements with quantity data")
    print(f"📊 Total elements in project: {len(df)}")
    print()
    
    # Calculate costs for each element
    costs = []
    total_cost = 0
    category_totals = {}
    
    for idx, row in df_with_quantities.iterrows():
        category = row['Category']
        name = row['Name']
        volume = row[volume_col] if pd.notna(row[volume_col]) else 0
        
        # Get unit cost for this category
        unit_cost = unit_costs.get(category, unit_costs['Default'])
        
        # Calculate element cost
        element_cost = volume * unit_cost
        costs.append(element_cost)
        total_cost += element_cost
        
        # Track by category
        if category not in category_totals:
            category_totals[category] = {'volume': 0, 'cost': 0, 'count': 0}
        category_totals[category]['volume'] += volume
        category_totals[category]['cost'] += element_cost
        category_totals[category]['count'] += 1
    
    # Add cost column to dataframe
    df_with_quantities['Estimated_Cost_EUR'] = costs
    df_with_quantities['Unit_Cost_EUR_m3'] = df_with_quantities['Category'].map(
        lambda x: unit_costs.get(x, unit_costs['Default'])
    )
    
    # Display results
    print("💰 COST ESTIMATION RESULTS")
    print("=" * 60)
    print(f"Total Estimated Cost: €{total_cost:,.2f}")
    print(f"Average Cost per Element: €{total_cost/len(df_with_quantities):,.2f}")
    print()
    
    print("📋 COST BREAKDOWN BY ELEMENT TYPE")
    print("-" * 60)
    for category, data in sorted(category_totals.items(), key=lambda x: x[1]['cost'], reverse=True):
        print(f"{category:25} | {data['count']:3d} elements | {data['volume']:8.1f} m³ | €{data['cost']:10,.0f}")
    
    print()
    print("🔝 TOP 10 MOST EXPENSIVE ELEMENTS")
    print("-" * 80)
    top_elements = df_with_quantities.nlargest(10, 'Estimated_Cost_EUR')
    for idx, row in top_elements.iterrows():
        print(f"€{row['Estimated_Cost_EUR']:8,.0f} | {row['Category']:20} | {row['Name'][:40]}")
    
    # Save detailed results to Excel
    output_file = './Sample_Projects/Price_Estimation_Results.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = []
        for category, data in category_totals.items():
            summary_data.append({
                'Element_Type': category,
                'Count': data['count'],
                'Total_Volume_m3': round(data['volume'], 2),
                'Unit_Cost_EUR_m3': unit_costs.get(category, unit_costs['Default']),
                'Total_Cost_EUR': round(data['cost'], 2),
                'Percentage_of_Total': round((data['cost'] / total_cost) * 100, 1)
            })
        
        summary_df = pd.DataFrame(summary_data).sort_values('Total_Cost_EUR', ascending=False)
        summary_df.to_excel(writer, sheet_name='Cost_Summary', index=False)
        
        # Detailed elements sheet
        detailed_cols = ['Name', 'Category', volume_col, 'Unit_Cost_EUR_m3', 'Estimated_Cost_EUR']
        df_with_quantities[detailed_cols].to_excel(writer, sheet_name='Detailed_Elements', index=False)
        
        # Project totals sheet
        totals_data = pd.DataFrame([
            {'Metric': 'Total Project Cost', 'Value': f"€{total_cost:,.2f}"},
            {'Metric': 'Total Elements Analyzed', 'Value': len(df_with_quantities)},
            {'Metric': 'Total Volume', 'Value': f"{df_with_quantities[volume_col].sum():.1f} m³"},
            {'Metric': 'Average Cost per m³', 'Value': f"€{total_cost/df_with_quantities[volume_col].sum():.2f}"},
            {'Metric': 'Project Type', 'Value': 'Parking Structure'},
            {'Metric': 'Cost Basis', 'Value': 'German Construction Costs 2024'},
            {'Metric': 'Analysis Date', 'Value': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
        ])
        totals_data.to_excel(writer, sheet_name='Project_Totals', index=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    print(f"📊 Excel file contains 3 sheets: Cost_Summary, Detailed_Elements, Project_Totals")
    
    return total_cost, category_totals

if __name__ == "__main__":
    try:
        total_cost, breakdown = estimate_construction_costs()
        print(f"\n✅ Price estimation completed successfully!")
        print(f"💰 Total estimated cost: €{total_cost:,.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
