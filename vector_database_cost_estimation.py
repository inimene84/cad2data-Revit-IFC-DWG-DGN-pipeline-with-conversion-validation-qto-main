#!/usr/bin/env python3
"""
Vector Database Solution for Private Property Cost Estimation
Supports: Houses, Family Mansions, Residential Buildings
"""

import pandas as pd
import numpy as np
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import hashlib

class PropertyCostVectorDB:
    """
    Vector Database for Private Property Cost Estimation
    Stores property features, materials, and costs as vectors for similarity search
    """
    
    def __init__(self, db_path: str = "property_cost_vectors.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with vector tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Property features table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS property_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT UNIQUE,
            property_type TEXT,  -- house, mansion, apartment, etc.
            size_sqm REAL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            floors INTEGER,
            construction_year INTEGER,
            location TEXT,
            quality_level TEXT,  -- basic, standard, luxury, premium
            features_vector TEXT,  -- JSON array of normalized features
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Material costs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS material_costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_name TEXT,
            material_category TEXT,  -- structural, finishing, MEP, etc.
            unit TEXT,  -- m2, m3, piece, etc.
            cost_per_unit REAL,
            region TEXT,
            quality_level TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT  -- manual, market_data, ai_estimated
        )
        ''')
        
        # Property cost breakdowns table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cost_breakdowns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT,
            category TEXT,  -- foundation, structure, roofing, etc.
            material_name TEXT,
            quantity REAL,
            unit TEXT,
            unit_cost REAL,
            total_cost REAL,
            percentage_of_total REAL,
            FOREIGN KEY (property_id) REFERENCES property_features(property_id)
        )
        ''')
        
        # Similarity search results cache
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS similarity_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_hash TEXT,
            similar_properties TEXT,  -- JSON array of similar property IDs
            similarity_scores TEXT,  -- JSON array of scores
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_property(self, property_data: Dict) -> str:
        """Add a new property to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate property ID
        property_id = hashlib.md5(
            f"{property_data['property_type']}_{property_data['size_sqm']}_{property_data['location']}".encode()
        ).hexdigest()[:12]
        
        # Create features vector
        features_vector = self._create_features_vector(property_data)
        
        cursor.execute('''
        INSERT OR REPLACE INTO property_features 
        (property_id, property_type, size_sqm, bedrooms, bathrooms, floors, 
         construction_year, location, quality_level, features_vector)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            property_data['property_type'],
            property_data['size_sqm'],
            property_data.get('bedrooms', 0),
            property_data.get('bathrooms', 0),
            property_data.get('floors', 1),
            property_data.get('construction_year', 2024),
            property_data.get('location', 'Unknown'),
            property_data.get('quality_level', 'standard'),
            json.dumps(features_vector)
        ))
        
        conn.commit()
        conn.close()
        return property_id
        
    def add_material_cost(self, material_data: Dict):
        """Add material cost information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO material_costs 
        (material_name, material_category, unit, cost_per_unit, region, quality_level, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            material_data['material_name'],
            material_data['material_category'],
            material_data['unit'],
            material_data['cost_per_unit'],
            material_data.get('region', 'Global'),
            material_data.get('quality_level', 'standard'),
            material_data.get('source', 'manual')
        ))
        
        conn.commit()
        conn.close()
        
    def add_cost_breakdown(self, property_id: str, breakdown_data: List[Dict]):
        """Add detailed cost breakdown for a property"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing breakdown
        cursor.execute('DELETE FROM cost_breakdowns WHERE property_id = ?', (property_id,))
        
        # Add new breakdown
        for item in breakdown_data:
            cursor.execute('''
            INSERT INTO cost_breakdowns 
            (property_id, category, material_name, quantity, unit, unit_cost, total_cost, percentage_of_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                property_id,
                item['category'],
                item['material_name'],
                item['quantity'],
                item['unit'],
                item['unit_cost'],
                item['total_cost'],
                item['percentage_of_total']
            ))
        
        conn.commit()
        conn.close()
        
    def _create_features_vector(self, property_data: Dict) -> List[float]:
        """Create normalized feature vector for similarity search"""
        # Normalize features to 0-1 range
        features = [
            property_data['size_sqm'] / 1000,  # Normalize size (max 1000 sqm)
            property_data.get('bedrooms', 0) / 10,  # Normalize bedrooms (max 10)
            property_data.get('bathrooms', 0) / 5,  # Normalize bathrooms (max 5)
            property_data.get('floors', 1) / 5,  # Normalize floors (max 5)
            (property_data.get('construction_year', 2024) - 1900) / 124,  # Normalize year
            self._quality_to_number(property_data.get('quality_level', 'standard')) / 4,  # Normalize quality
        ]
        return features
        
    def _quality_to_number(self, quality: str) -> int:
        """Convert quality level to number"""
        quality_map = {'basic': 1, 'standard': 2, 'luxury': 3, 'premium': 4}
        return quality_map.get(quality.lower(), 2)
        
    def find_similar_properties(self, query_property: Dict, limit: int = 5) -> List[Tuple[str, float]]:
        """Find similar properties using vector similarity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create query vector
        query_vector = np.array(self._create_features_vector(query_property))
        
        # Get all properties
        cursor.execute('SELECT property_id, features_vector FROM property_features')
        properties = cursor.fetchall()
        
        similarities = []
        for property_id, features_json in properties:
            features_vector = np.array(json.loads(features_json))
            
            # Calculate cosine similarity
            similarity = np.dot(query_vector, features_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(features_vector)
            )
            similarities.append((property_id, float(similarity)))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        conn.close()
        
        return similarities[:limit]
        
    def estimate_cost(self, property_data: Dict) -> Dict:
        """Estimate cost for a property using similar properties and material costs"""
        # Find similar properties
        similar_properties = self.find_similar_properties(property_data, limit=3)
        
        if not similar_properties:
            return self._estimate_from_materials(property_data)
        
        # Get cost data from similar properties
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        similar_costs = []
        for property_id, similarity in similar_properties:
            cursor.execute('''
            SELECT SUM(total_cost) as total_cost 
            FROM cost_breakdowns 
            WHERE property_id = ?
            ''', (property_id,))
            result = cursor.fetchone()
            if result and result[0]:
                similar_costs.append((result[0], similarity))
        
        conn.close()
        
        if similar_costs:
            # Weighted average based on similarity
            total_weighted_cost = sum(cost * similarity for cost, similarity in similar_costs)
            total_weight = sum(similarity for _, similarity in similar_costs)
            estimated_cost = total_weighted_cost / total_weight
            
            # Adjust for size difference
            similar_property_size = self._get_average_similar_size(similar_properties)
            size_factor = property_data['size_sqm'] / similar_property_size
            adjusted_cost = estimated_cost * size_factor
            
            return {
                'estimated_total_cost': adjusted_cost,
                'cost_per_sqm': adjusted_cost / property_data['size_sqm'],
                'method': 'similar_properties',
                'similar_properties_count': len(similar_costs),
                'confidence': min(0.95, sum(similarity for _, similarity in similar_costs) / len(similar_costs))
            }
        else:
            return self._estimate_from_materials(property_data)
            
    def _get_average_similar_size(self, similar_properties: List[Tuple[str, float]]) -> float:
        """Get average size of similar properties"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        property_ids = [pid for pid, _ in similar_properties]
        placeholders = ','.join('?' * len(property_ids))
        cursor.execute(f'''
        SELECT AVG(size_sqm) FROM property_features 
        WHERE property_id IN ({placeholders})
        ''', property_ids)
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 200  # Default 200 sqm
        
    def _estimate_from_materials(self, property_data: Dict) -> Dict:
        """Fallback estimation using material costs"""
        # This would use the material costs table for detailed estimation
        # For now, return a simple estimation
        base_cost_per_sqm = {
            'basic': 1200,
            'standard': 1800,
            'luxury': 2800,
            'premium': 4000
        }
        
        quality = property_data.get('quality_level', 'standard')
        cost_per_sqm = base_cost_per_sqm.get(quality, 1800)
        total_cost = property_data['size_sqm'] * cost_per_sqm
        
        return {
            'estimated_total_cost': total_cost,
            'cost_per_sqm': cost_per_sqm,
            'method': 'material_based',
            'confidence': 0.7
        }
        
    def populate_sample_data(self):
        """Populate database with sample residential property data"""
        print("🏠 Populating vector database with sample residential properties...")
        
        # Sample properties
        sample_properties = [
            {
                'property_type': 'family_house',
                'size_sqm': 150,
                'bedrooms': 3,
                'bathrooms': 2,
                'floors': 2,
                'construction_year': 2020,
                'location': 'Munich',
                'quality_level': 'standard'
            },
            {
                'property_type': 'family_house',
                'size_sqm': 200,
                'bedrooms': 4,
                'bathrooms': 3,
                'floors': 2,
                'construction_year': 2018,
                'location': 'Berlin',
                'quality_level': 'luxury'
            },
            {
                'property_type': 'mansion',
                'size_sqm': 500,
                'bedrooms': 6,
                'bathrooms': 5,
                'floors': 3,
                'construction_year': 2022,
                'location': 'Hamburg',
                'quality_level': 'premium'
            },
            {
                'property_type': 'apartment',
                'size_sqm': 80,
                'bedrooms': 2,
                'bathrooms': 1,
                'floors': 1,
                'construction_year': 2021,
                'location': 'Cologne',
                'quality_level': 'standard'
            },
            {
                'property_type': 'villa',
                'size_sqm': 350,
                'bedrooms': 5,
                'bathrooms': 4,
                'floors': 2,
                'construction_year': 2019,
                'location': 'Frankfurt',
                'quality_level': 'luxury'
            }
        ]
        
        # Add properties
        property_ids = []
        for prop in sample_properties:
            prop_id = self.add_property(prop)
            property_ids.append(prop_id)
            
        # Add sample material costs
        materials = [
            {'material_name': 'Concrete Foundation', 'material_category': 'structural', 'unit': 'm3', 'cost_per_unit': 120, 'region': 'Germany'},
            {'material_name': 'Brick Wall', 'material_category': 'structural', 'unit': 'm2', 'cost_per_unit': 45, 'region': 'Germany'},
            {'material_name': 'Roof Tiles', 'material_category': 'roofing', 'unit': 'm2', 'cost_per_unit': 35, 'region': 'Germany'},
            {'material_name': 'Hardwood Flooring', 'material_category': 'finishing', 'unit': 'm2', 'cost_per_unit': 80, 'region': 'Germany'},
            {'material_name': 'Marble Countertop', 'material_category': 'finishing', 'unit': 'm2', 'cost_per_unit': 200, 'region': 'Germany'},
            {'material_name': 'Premium Kitchen', 'material_category': 'furnishing', 'unit': 'piece', 'cost_per_unit': 15000, 'region': 'Germany'},
            {'material_name': 'Luxury Bathroom', 'material_category': 'furnishing', 'unit': 'piece', 'cost_per_unit': 8000, 'region': 'Germany'},
        ]
        
        for material in materials:
            self.add_material_cost(material)
            
        # Add sample cost breakdowns
        for i, prop_id in enumerate(property_ids):
            prop = sample_properties[i]
            breakdown = self._generate_sample_breakdown(prop)
            self.add_cost_breakdown(prop_id, breakdown)
            
        print(f"✅ Added {len(sample_properties)} sample properties to vector database")
        
    def _generate_sample_breakdown(self, property_data: Dict) -> List[Dict]:
        """Generate sample cost breakdown for a property"""
        size = property_data['size_sqm']
        quality = property_data['quality_level']
        
        # Base costs per sqm by quality
        base_costs = {
            'basic': {'foundation': 50, 'structure': 200, 'roofing': 80, 'finishing': 300, 'mep': 150},
            'standard': {'foundation': 80, 'structure': 350, 'roofing': 120, 'finishing': 500, 'mep': 250},
            'luxury': {'foundation': 120, 'structure': 500, 'roofing': 180, 'finishing': 800, 'mep': 400},
            'premium': {'foundation': 150, 'structure': 700, 'roofing': 250, 'finishing': 1200, 'mep': 600}
        }
        
        costs = base_costs.get(quality, base_costs['standard'])
        breakdown = []
        
        for category, cost_per_sqm in costs.items():
            total_cost = size * cost_per_sqm
            breakdown.append({
                'category': category,
                'material_name': f'{category.title()} Materials',
                'quantity': size,
                'unit': 'm2',
                'unit_cost': cost_per_sqm,
                'total_cost': total_cost,
                'percentage_of_total': 0  # Will be calculated later
            })
        
        # Calculate percentages
        total_cost = sum(item['total_cost'] for item in breakdown)
        for item in breakdown:
            item['percentage_of_total'] = (item['total_cost'] / total_cost) * 100
            
        return breakdown

def main():
    """Demo the vector database for property cost estimation"""
    print("🏠 Vector Database for Private Property Cost Estimation")
    print("=" * 60)
    
    # Initialize database
    db = PropertyCostVectorDB()
    
    # Populate with sample data
    db.populate_sample_data()
    
    # Test estimation for a new property
    test_property = {
        'property_type': 'family_house',
        'size_sqm': 180,
        'bedrooms': 3,
        'bathrooms': 2,
        'floors': 2,
        'construction_year': 2023,
        'location': 'Munich',
        'quality_level': 'standard'
    }
    
    print(f"\n🔍 Estimating cost for test property:")
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

if __name__ == "__main__":
    main()
