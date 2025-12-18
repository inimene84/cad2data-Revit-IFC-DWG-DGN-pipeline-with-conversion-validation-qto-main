#!/usr/bin/env python3
"""
Real-Time Data Manager for Property Cost Vector Database
Allows adding real project data and updating cost estimates in real-time
"""

import pandas as pd
import numpy as np
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import hashlib
import requests
import schedule
import time
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealTimeDataManager:
    """
    Manages real-time data updates for the property cost vector database
    """
    
    def __init__(self, db_path: str = "property_cost_vectors.db"):
        self.db_path = db_path
        self.init_database()
        self.setup_data_sources()
        
    def init_database(self):
        """Initialize database with additional tables for real-time data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Real project data table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_project_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT UNIQUE,
            project_name TEXT,
            property_type TEXT,
            size_sqm REAL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            floors INTEGER,
            construction_year INTEGER,
            location TEXT,
            quality_level TEXT,
            actual_total_cost REAL,
            cost_per_sqm REAL,
            construction_start_date DATE,
            construction_end_date DATE,
            contractor_name TEXT,
            project_status TEXT,  -- planned, in_progress, completed, cancelled
            data_source TEXT,  -- manual, api, file_import, n8n_workflow
            confidence_score REAL,  -- 0-1, how reliable is this data
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Material cost updates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS material_cost_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_name TEXT,
            material_category TEXT,
            unit TEXT,
            old_cost_per_unit REAL,
            new_cost_per_unit REAL,
            cost_change_percent REAL,
            region TEXT,
            quality_level TEXT,
            update_source TEXT,  -- market_data, contractor_quote, supplier_price
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            effective_date DATE,
            notes TEXT
        )
        ''')
        
        # Data quality metrics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_quality_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT,
            metric_value REAL,
            measurement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
        ''')
        
        # API data sources table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name TEXT,
            source_type TEXT,  -- api, file, manual, webhook
            endpoint_url TEXT,
            api_key TEXT,
            update_frequency TEXT,  -- daily, weekly, monthly
            last_successful_update TIMESTAMP,
            last_error TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def setup_data_sources(self):
        """Setup default data sources for real-time updates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add default data sources
        default_sources = [
            {
                'source_name': 'Manual Entry',
                'source_type': 'manual',
                'endpoint_url': None,
                'api_key': None,
                'update_frequency': 'on_demand',
                'is_active': True
            },
            {
                'source_name': 'File Import',
                'source_type': 'file',
                'endpoint_url': None,
                'api_key': None,
                'update_frequency': 'on_demand',
                'is_active': True
            },
            {
                'source_name': 'n8n Workflow',
                'source_type': 'webhook',
                'endpoint_url': 'http://localhost:5678/webhook/project-data',
                'api_key': None,
                'update_frequency': 'on_demand',
                'is_active': True
            }
        ]
        
        for source in default_sources:
            cursor.execute('''
            INSERT OR IGNORE INTO data_sources 
            (source_name, source_type, endpoint_url, api_key, update_frequency, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                source['source_name'],
                source['source_type'],
                source['endpoint_url'],
                source['api_key'],
                source['update_frequency'],
                source['is_active']
            ))
        
        conn.commit()
        conn.close()
        
    def add_real_project_data(self, project_data: Dict) -> str:
        """Add real project data from completed or ongoing projects"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate project ID
        project_id = hashlib.md5(
            f"{project_data['project_name']}_{project_data['location']}_{project_data['construction_year']}".encode()
        ).hexdigest()[:12]
        
        # Calculate cost per sqm
        cost_per_sqm = project_data['actual_total_cost'] / project_data['size_sqm'] if project_data['size_sqm'] > 0 else 0
        
        # Calculate confidence score based on data completeness
        confidence_score = self._calculate_confidence_score(project_data)
        
        cursor.execute('''
        INSERT OR REPLACE INTO real_project_data 
        (project_id, project_name, property_type, size_sqm, bedrooms, bathrooms, floors,
         construction_year, location, quality_level, actual_total_cost, cost_per_sqm,
         construction_start_date, construction_end_date, contractor_name, project_status,
         data_source, confidence_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            project_data['project_name'],
            project_data['property_type'],
            project_data['size_sqm'],
            project_data.get('bedrooms', 0),
            project_data.get('bathrooms', 0),
            project_data.get('floors', 1),
            project_data['construction_year'],
            project_data['location'],
            project_data.get('quality_level', 'standard'),
            project_data['actual_total_cost'],
            cost_per_sqm,
            project_data.get('construction_start_date'),
            project_data.get('construction_end_date'),
            project_data.get('contractor_name'),
            project_data.get('project_status', 'completed'),
            project_data.get('data_source', 'manual'),
            confidence_score
        ))
        
        # Update the main property_features table with this real data
        self._update_property_features_from_real_data(project_id, project_data)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Added real project data: {project_data['project_name']} (ID: {project_id})")
        return project_id
        
    def _calculate_confidence_score(self, project_data: Dict) -> float:
        """Calculate confidence score based on data completeness and quality"""
        score = 0.0
        
        # Required fields (40 points)
        if project_data.get('project_name'): score += 10
        if project_data.get('actual_total_cost'): score += 10
        if project_data.get('size_sqm'): score += 10
        if project_data.get('location'): score += 10
        
        # Optional fields (30 points)
        if project_data.get('construction_year'): score += 5
        if project_data.get('contractor_name'): score += 5
        if project_data.get('construction_start_date'): score += 5
        if project_data.get('construction_end_date'): score += 5
        if project_data.get('bedrooms'): score += 5
        if project_data.get('bathrooms'): score += 5
        
        # Data quality indicators (30 points)
        if project_data.get('actual_total_cost', 0) > 0: score += 10
        if project_data.get('size_sqm', 0) > 0: score += 10
        if project_data.get('data_source') == 'contractor_quote': score += 10
        elif project_data.get('data_source') == 'manual': score += 5
        
        return min(1.0, score / 100.0)
        
    def _update_property_features_from_real_data(self, project_id: str, project_data: Dict):
        """Update the main property_features table with real project data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create features vector from real data
        features_vector = self._create_features_vector(project_data)
        
        cursor.execute('''
        INSERT OR REPLACE INTO property_features 
        (property_id, property_type, size_sqm, bedrooms, bathrooms, floors,
         construction_year, location, quality_level, features_vector)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            project_data['property_type'],
            project_data['size_sqm'],
            project_data.get('bedrooms', 0),
            project_data.get('bathrooms', 0),
            project_data.get('floors', 1),
            project_data['construction_year'],
            project_data['location'],
            project_data.get('quality_level', 'standard'),
            json.dumps(features_vector)
        ))
        
        conn.commit()
        conn.close()
        
    def _create_features_vector(self, project_data: Dict) -> List[float]:
        """Create normalized feature vector for similarity search"""
        features = [
            project_data['size_sqm'] / 1000,  # Normalize size
            project_data.get('bedrooms', 0) / 10,  # Normalize bedrooms
            project_data.get('bathrooms', 0) / 5,  # Normalize bathrooms
            project_data.get('floors', 1) / 5,  # Normalize floors
            (project_data.get('construction_year', 2024) - 1900) / 124,  # Normalize year
            self._quality_to_number(project_data.get('quality_level', 'standard')) / 4,  # Normalize quality
        ]
        return features
        
    def _quality_to_number(self, quality: str) -> int:
        """Convert quality level to number"""
        quality_map = {'basic': 1, 'standard': 2, 'luxury': 3, 'premium': 4}
        return quality_map.get(quality.lower(), 2)
        
    def import_from_excel(self, file_path: str, sheet_name: str = 'Sheet1') -> List[str]:
        """Import real project data from Excel file"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            project_ids = []
            
            for _, row in df.iterrows():
                project_data = {
                    'project_name': str(row.get('Project Name', '')),
                    'property_type': str(row.get('Property Type', 'family_house')),
                    'size_sqm': float(row.get('Size (sqm)', 0)),
                    'bedrooms': int(row.get('Bedrooms', 0)),
                    'bathrooms': int(row.get('Bathrooms', 0)),
                    'floors': int(row.get('Floors', 1)),
                    'construction_year': int(row.get('Construction Year', 2024)),
                    'location': str(row.get('Location', 'Unknown')),
                    'quality_level': str(row.get('Quality Level', 'standard')),
                    'actual_total_cost': float(row.get('Actual Total Cost', 0)),
                    'construction_start_date': row.get('Construction Start Date'),
                    'construction_end_date': row.get('Construction End Date'),
                    'contractor_name': str(row.get('Contractor Name', '')),
                    'project_status': str(row.get('Project Status', 'completed')),
                    'data_source': 'file_import'
                }
                
                if project_data['actual_total_cost'] > 0 and project_data['size_sqm'] > 0:
                    project_id = self.add_real_project_data(project_data)
                    project_ids.append(project_id)
                    
            logger.info(f"Imported {len(project_ids)} projects from Excel file")
            return project_ids
            
        except Exception as e:
            logger.error(f"Error importing from Excel: {e}")
            return []
            
    def import_from_csv(self, file_path: str) -> List[str]:
        """Import real project data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            project_ids = []
            
            for _, row in df.iterrows():
                project_data = {
                    'project_name': str(row.get('project_name', '')),
                    'property_type': str(row.get('property_type', 'family_house')),
                    'size_sqm': float(row.get('size_sqm', 0)),
                    'bedrooms': int(row.get('bedrooms', 0)),
                    'bathrooms': int(row.get('bathrooms', 0)),
                    'floors': int(row.get('floors', 1)),
                    'construction_year': int(row.get('construction_year', 2024)),
                    'location': str(row.get('location', 'Unknown')),
                    'quality_level': str(row.get('quality_level', 'standard')),
                    'actual_total_cost': float(row.get('actual_total_cost', 0)),
                    'construction_start_date': row.get('construction_start_date'),
                    'construction_end_date': row.get('construction_end_date'),
                    'contractor_name': str(row.get('contractor_name', '')),
                    'project_status': str(row.get('project_status', 'completed')),
                    'data_source': 'file_import'
                }
                
                if project_data['actual_total_cost'] > 0 and project_data['size_sqm'] > 0:
                    project_id = self.add_real_project_data(project_data)
                    project_ids.append(project_id)
                    
            logger.info(f"Imported {len(project_ids)} projects from CSV file")
            return project_ids
            
        except Exception as e:
            logger.error(f"Error importing from CSV: {e}")
            return []
            
    def update_material_costs(self, material_updates: List[Dict]):
        """Update material costs with new market data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for update in material_updates:
            # Get old cost
            cursor.execute('''
            SELECT cost_per_unit FROM material_costs 
            WHERE material_name = ? AND region = ? AND quality_level = ?
            ORDER BY last_updated DESC LIMIT 1
            ''', (update['material_name'], update['region'], update['quality_level']))
            
            old_cost_result = cursor.fetchone()
            old_cost = old_cost_result[0] if old_cost_result else 0
            
            # Calculate change percentage
            cost_change_percent = 0
            if old_cost > 0:
                cost_change_percent = ((update['new_cost_per_unit'] - old_cost) / old_cost) * 100
            
            # Insert update record
            cursor.execute('''
            INSERT INTO material_cost_updates 
            (material_name, material_category, unit, old_cost_per_unit, new_cost_per_unit,
             cost_change_percent, region, quality_level, update_source, effective_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                update['material_name'],
                update['material_category'],
                update['unit'],
                old_cost,
                update['new_cost_per_unit'],
                cost_change_percent,
                update['region'],
                update['quality_level'],
                update['update_source'],
                update.get('effective_date', datetime.now().date()),
                update.get('notes', '')
            ))
            
            # Update current material cost
            cursor.execute('''
            INSERT OR REPLACE INTO material_costs 
            (material_name, material_category, unit, cost_per_unit, region, quality_level, source, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                update['material_name'],
                update['material_category'],
                update['unit'],
                update['new_cost_per_unit'],
                update['region'],
                update['quality_level'],
                update['update_source'],
                datetime.now()
            ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated {len(material_updates)} material costs")
        
    def get_data_quality_report(self) -> Dict:
        """Generate data quality report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get project data statistics
        cursor.execute('SELECT COUNT(*) FROM real_project_data')
        total_projects = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(confidence_score) FROM real_project_data')
        avg_confidence = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM real_project_data WHERE confidence_score > 0.8')
        high_confidence_projects = cursor.fetchone()[0]
        
        # Get material cost statistics
        cursor.execute('SELECT COUNT(*) FROM material_costs')
        total_materials = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM material_cost_updates WHERE update_date > date("now", "-30 days")')
        recent_updates = cursor.fetchone()[0]
        
        # Get data source statistics
        cursor.execute('SELECT source_name, COUNT(*) FROM real_project_data GROUP BY data_source')
        source_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_projects': total_projects,
            'avg_confidence': avg_confidence,
            'high_confidence_projects': high_confidence_projects,
            'total_materials': total_materials,
            'recent_updates': recent_updates,
            'source_breakdown': dict(source_stats),
            'data_quality_score': (avg_confidence + (high_confidence_projects / max(total_projects, 1))) / 2
        }
        
    def setup_automated_updates(self):
        """Setup automated data updates"""
        # Schedule daily material cost updates
        schedule.every().day.at("09:00").do(self._daily_material_cost_update)
        
        # Schedule weekly data quality check
        schedule.every().week.do(self._weekly_data_quality_check)
        
        # Schedule monthly data source health check
        schedule.every().month.do(self._monthly_data_source_check)
        
        logger.info("Automated updates scheduled")
        
    def _daily_material_cost_update(self):
        """Daily material cost update (placeholder for API integration)"""
        logger.info("Running daily material cost update...")
        # Here you would integrate with material cost APIs
        # For now, just log the action
        pass
        
    def _weekly_data_quality_check(self):
        """Weekly data quality check"""
        logger.info("Running weekly data quality check...")
        quality_report = self.get_data_quality_report()
        
        # Log quality metrics
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO data_quality_metrics (metric_name, metric_value, notes)
        VALUES (?, ?, ?)
        ''', (
            'data_quality_score',
            quality_report['data_quality_score'],
            f"Weekly check: {quality_report['total_projects']} projects, {quality_report['avg_confidence']:.2f} avg confidence"
        ))
        
        conn.commit()
        conn.close()
        
    def _monthly_data_source_check(self):
        """Monthly data source health check"""
        logger.info("Running monthly data source check...")
        # Check data source health and update status
        pass
        
    def run_scheduler(self):
        """Run the scheduler for automated updates"""
        logger.info("Starting automated data update scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Demo the real-time data manager"""
    print("🔄 Real-Time Data Manager for Property Cost Vector Database")
    print("=" * 60)
    
    # Initialize manager
    manager = RealTimeDataManager()
    
    # Add sample real project data
    sample_projects = [
        {
            'project_name': 'Villa Munich 2023',
            'property_type': 'villa',
            'size_sqm': 350,
            'bedrooms': 5,
            'bathrooms': 4,
            'floors': 2,
            'construction_year': 2023,
            'location': 'Munich',
            'quality_level': 'luxury',
            'actual_total_cost': 850000,
            'construction_start_date': '2023-01-15',
            'construction_end_date': '2023-12-20',
            'contractor_name': 'Bauhaus München',
            'project_status': 'completed',
            'data_source': 'contractor_quote'
        },
        {
            'project_name': 'Family House Berlin 2022',
            'property_type': 'family_house',
            'size_sqm': 180,
            'bedrooms': 4,
            'bathrooms': 2,
            'floors': 2,
            'construction_year': 2022,
            'location': 'Berlin',
            'quality_level': 'standard',
            'actual_total_cost': 320000,
            'construction_start_date': '2022-03-01',
            'construction_end_date': '2022-11-30',
            'contractor_name': 'Berlin Bau GmbH',
            'project_status': 'completed',
            'data_source': 'manual'
        }
    ]
    
    print("📊 Adding sample real project data...")
    for project in sample_projects:
        project_id = manager.add_real_project_data(project)
        print(f"   ✅ Added: {project['project_name']} (ID: {project_id})")
    
    # Update material costs
    material_updates = [
        {
            'material_name': 'Concrete Foundation',
            'material_category': 'structural',
            'unit': 'm3',
            'new_cost_per_unit': 125,  # Increased from 120
            'region': 'Germany',
            'quality_level': 'standard',
            'update_source': 'market_data',
            'notes': 'Price increase due to material shortage'
        },
        {
            'material_name': 'Brick Wall',
            'material_category': 'structural',
            'unit': 'm2',
            'new_cost_per_unit': 48,  # Increased from 45
            'region': 'Germany',
            'quality_level': 'standard',
            'update_source': 'supplier_price',
            'notes': 'Supplier price update'
        }
    ]
    
    print("\n💰 Updating material costs...")
    manager.update_material_costs(material_updates)
    
    # Generate data quality report
    print("\n📈 Data Quality Report:")
    quality_report = manager.get_data_quality_report()
    print(f"   Total Projects: {quality_report['total_projects']}")
    print(f"   Average Confidence: {quality_report['avg_confidence']:.2%}")
    print(f"   High Confidence Projects: {quality_report['high_confidence_projects']}")
    print(f"   Total Materials: {quality_report['total_materials']}")
    print(f"   Recent Updates: {quality_report['recent_updates']}")
    print(f"   Data Quality Score: {quality_report['data_quality_score']:.2%}")
    
    print(f"\n📊 Source Breakdown:")
    for source, count in quality_report['source_breakdown'].items():
        print(f"   {source}: {count} projects")
    
    print(f"\n✅ Real-time data manager initialized successfully!")
    print(f"💡 You can now add real project data and keep cost estimates updated!")

if __name__ == "__main__":
    main()
