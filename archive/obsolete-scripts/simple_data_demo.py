#!/usr/bin/env python3
"""
Simple Demo: How to Add Real Project Data to Vector Database
"""

import pandas as pd
import json
import sqlite3
from datetime import datetime
from vector_database_cost_estimation import PropertyCostVectorDB

def add_real_project_data():
    """Demonstrate how to add real project data"""
    print("🔄 Adding Real Project Data to Vector Database")
    print("=" * 50)
    
    # Initialize the vector database
    db = PropertyCostVectorDB("property_cost_vectors.db")
    
    # Sample real project data (from completed projects)
    real_projects = [
        {
            'property_type': 'villa',
            'size_sqm': 450,
            'bedrooms': 6,
            'bathrooms': 5,
            'floors': 3,
            'construction_year': 2023,
            'location': 'Munich',
            'quality_level': 'premium'
        },
        {
            'property_type': 'family_house',
            'size_sqm': 180,
            'bedrooms': 4,
            'bathrooms': 2,
            'floors': 2,
            'construction_year': 2022,
            'location': 'Berlin',
            'quality_level': 'standard'
        },
        {
            'property_type': 'apartment',
            'size_sqm': 95,
            'bedrooms': 2,
            'bathrooms': 1,
            'floors': 1,
            'construction_year': 2023,
            'location': 'Cologne',
            'quality_level': 'standard'
        }
    ]
    
    print("📊 Adding real project data...")
    for i, project in enumerate(real_projects, 1):
        project_id = db.add_property(project)
        print(f"   {i}. Added {project['property_type']} in {project['location']} (ID: {project_id})")
    
    # Add sample cost breakdowns for these projects
    cost_breakdowns = [
        # Villa Munich
        [
            {'category': 'foundation', 'material_name': 'Concrete Foundation', 'quantity': 45, 'unit': 'm3', 'unit_cost': 120, 'total_cost': 5400, 'percentage_of_total': 15},
            {'category': 'structure', 'material_name': 'Brick Walls', 'quantity': 350, 'unit': 'm2', 'unit_cost': 45, 'total_cost': 15750, 'percentage_of_total': 45},
            {'category': 'roofing', 'material_name': 'Roof Tiles', 'quantity': 200, 'unit': 'm2', 'unit_cost': 35, 'total_cost': 7000, 'percentage_of_total': 20},
            {'category': 'finishing', 'material_name': 'Luxury Finishes', 'quantity': 450, 'unit': 'm2', 'unit_cost': 80, 'total_cost': 36000, 'percentage_of_total': 20}
        ],
        # Family House Berlin
        [
            {'category': 'foundation', 'material_name': 'Concrete Foundation', 'quantity': 18, 'unit': 'm3', 'unit_cost': 120, 'total_cost': 2160, 'percentage_of_total': 15},
            {'category': 'structure', 'material_name': 'Brick Walls', 'quantity': 180, 'unit': 'm2', 'unit_cost': 45, 'total_cost': 8100, 'percentage_of_total': 45},
            {'category': 'roofing', 'material_name': 'Roof Tiles', 'quantity': 100, 'unit': 'm2', 'unit_cost': 35, 'total_cost': 3500, 'percentage_of_total': 20},
            {'category': 'finishing', 'material_name': 'Standard Finishes', 'quantity': 180, 'unit': 'm2', 'unit_cost': 50, 'total_cost': 9000, 'percentage_of_total': 20}
        ],
        # Apartment Cologne
        [
            {'category': 'foundation', 'material_name': 'Concrete Foundation', 'quantity': 9, 'unit': 'm3', 'unit_cost': 120, 'total_cost': 1080, 'percentage_of_total': 15},
            {'category': 'structure', 'material_name': 'Brick Walls', 'quantity': 95, 'unit': 'm2', 'unit_cost': 45, 'total_cost': 4275, 'percentage_of_total': 45},
            {'category': 'roofing', 'material_name': 'Roof Tiles', 'quantity': 50, 'unit': 'm2', 'unit_cost': 35, 'total_cost': 1750, 'percentage_of_total': 20},
            {'category': 'finishing', 'material_name': 'Standard Finishes', 'quantity': 95, 'unit': 'm2', 'unit_cost': 50, 'total_cost': 4750, 'percentage_of_total': 20}
        ]
    ]
    
    print("\n💰 Adding cost breakdowns...")
    property_ids = []
    conn = sqlite3.connect("property_cost_vectors.db")
    cursor = conn.cursor()
    cursor.execute("SELECT property_id FROM property_features ORDER BY created_at DESC LIMIT 3")
    property_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    for i, (property_id, breakdown) in enumerate(zip(property_ids, cost_breakdowns)):
        db.add_cost_breakdown(property_id, breakdown)
        total_cost = sum(item['total_cost'] for item in breakdown)
        print(f"   {i+1}. Added cost breakdown for property {property_id}: €{total_cost:,.2f}")
    
    print(f"\n✅ Successfully added {len(real_projects)} real projects with cost data!")
    return db

def test_cost_estimation_with_real_data():
    """Test cost estimation using the real data"""
    print("\n🔍 Testing Cost Estimation with Real Data")
    print("=" * 50)
    
    db = PropertyCostVectorDB("property_cost_vectors.db")
    
    # Test property (similar to real data)
    test_property = {
        'property_type': 'family_house',
        'size_sqm': 200,
        'bedrooms': 4,
        'bathrooms': 3,
        'floors': 2,
        'construction_year': 2024,
        'location': 'Munich',
        'quality_level': 'standard'
    }
    
    print(f"🏠 Estimating cost for test property:")
    print(f"   Type: {test_property['property_type']}")
    print(f"   Size: {test_property['size_sqm']} sqm")
    print(f"   Quality: {test_property['quality_level']}")
    print(f"   Location: {test_property['location']}")
    
    # Find similar properties
    similar = db.find_similar_properties(test_property, limit=3)
    print(f"\n📊 Found {len(similar)} similar properties:")
    for prop_id, similarity in similar:
        print(f"   Property {prop_id}: {similarity:.3f} similarity")
    
    # Estimate cost
    estimation = db.estimate_cost(test_property)
    
    print(f"\n💰 COST ESTIMATION RESULTS:")
    print(f"   Total Estimated Cost: €{estimation['estimated_total_cost']:,.2f}")
    print(f"   Cost per sqm: €{estimation['cost_per_sqm']:,.2f}")
    print(f"   Method: {estimation['method']}")
    print(f"   Confidence: {estimation['confidence']:.1%}")
    
    if 'similar_properties_count' in estimation:
        print(f"   Based on {estimation['similar_properties_count']} similar properties")

def show_data_management_methods():
    """Show different methods to add data"""
    print("\n📋 How to Add Real Project Data")
    print("=" * 50)
    
    print("1. 📝 Manual Entry (Python):")
    print("""
   # Add single project
   db = PropertyCostVectorDB()
   project_data = {
       'property_type': 'family_house',
       'size_sqm': 150,
       'bedrooms': 3,
       'bathrooms': 2,
       'construction_year': 2024,
       'location': 'Munich',
       'quality_level': 'standard'
   }
   project_id = db.add_property(project_data)
   """)
    
    print("2. 📊 Excel Import:")
    print("""
   # Import from Excel file
   manager = RealTimeDataManager()
   project_ids = manager.import_from_excel('your_projects.xlsx')
   """)
    
    print("3. 🌐 Webhook (n8n Integration):")
    print("""
   # Send data via webhook
   POST http://localhost:5000/webhook/project-data
   {
       "project_name": "My House 2024",
       "property_type": "family_house",
       "size_sqm": 200,
       "actual_total_cost": 400000,
       "location": "Munich"
   }
   """)
    
    print("4. 🔄 Automated Updates:")
    print("""
   # Schedule regular updates
   manager = RealTimeDataManager()
   manager.setup_automated_updates()
   manager.run_scheduler()  # Runs in background
   """)

def main():
    """Main demo function"""
    print("🏠 Real-Time Data Management Demo")
    print("=" * 60)
    
    # Add real project data
    db = add_real_project_data()
    
    # Test cost estimation
    test_cost_estimation_with_real_data()
    
    # Show data management methods
    show_data_management_methods()
    
    print(f"\n🎯 Key Benefits of Real-Time Data Updates:")
    print(f"   ✅ More accurate cost estimates")
    print(f"   ✅ Up-to-date market prices")
    print(f"   ✅ Better similarity matching")
    print(f"   ✅ Continuous learning from real projects")
    print(f"   ✅ Automated data quality monitoring")
    
    print(f"\n📈 Next Steps:")
    print(f"   1. Add your real project data using Excel template")
    print(f"   2. Set up webhook integration with n8n")
    print(f"   3. Schedule regular material cost updates")
    print(f"   4. Monitor data quality metrics")
    print(f"   5. Use updated database for cost estimation")

if __name__ == "__main__":
    main()
