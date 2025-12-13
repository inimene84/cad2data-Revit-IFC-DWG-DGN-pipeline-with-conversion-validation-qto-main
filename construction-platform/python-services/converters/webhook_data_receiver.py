#!/usr/bin/env python3
"""
Webhook Data Receiver for n8n Integration
Receives real project data from n8n workflows and updates the vector database
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
from real_time_data_manager import RealTimeDataManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
data_manager = RealTimeDataManager()

@app.route('/webhook/project-data', methods=['POST'])
def receive_project_data():
    """Receive real project data from n8n workflow"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Validate required fields
        required_fields = ['project_name', 'size_sqm', 'actual_total_cost', 'location']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}',
                'required_fields': required_fields
            }), 400
        
        # Add timestamp and source
        data['data_source'] = 'n8n_webhook'
        data['received_at'] = datetime.now().isoformat()
        
        # Add to database
        project_id = data_manager.add_real_project_data(data)
        
        logger.info(f"Received project data: {data['project_name']} (ID: {project_id})")
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'message': f'Project data added successfully: {data["project_name"]}',
            'confidence_score': data_manager._calculate_confidence_score(data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing project data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/material-costs', methods=['POST'])
def receive_material_costs():
    """Receive material cost updates from n8n workflow"""
    try:
        data = request.get_json()
        
        if not data or 'material_updates' not in data:
            return jsonify({'error': 'No material updates received'}), 400
        
        material_updates = data['material_updates']
        
        # Validate material update format
        for update in material_updates:
            required_fields = ['material_name', 'new_cost_per_unit', 'region']
            missing_fields = [field for field in required_fields if field not in update]
            
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields in material update: {missing_fields}',
                    'required_fields': required_fields
                }), 400
        
        # Update material costs
        data_manager.update_material_costs(material_updates)
        
        logger.info(f"Updated {len(material_updates)} material costs")
        
        return jsonify({
            'success': True,
            'message': f'Updated {len(material_updates)} material costs',
            'updated_materials': [update['material_name'] for update in material_updates]
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing material costs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects with optional filtering"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        location = request.args.get('location')
        property_type = request.args.get('property_type')
        min_confidence = request.args.get('min_confidence', 0.0, type=float)
        
        # Build query
        query = "SELECT * FROM real_project_data WHERE 1=1"
        params = []
        
        if location:
            query += " AND location = ?"
            params.append(location)
            
        if property_type:
            query += " AND property_type = ?"
            params.append(property_type)
            
        if min_confidence > 0:
            query += " AND confidence_score >= ?"
            params.append(min_confidence)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        # Execute query
        import sqlite3
        conn = sqlite3.connect(data_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        columns = [description[0] for description in cursor.description]
        projects = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'projects': projects,
            'count': len(projects)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/quality-report', methods=['GET'])
def get_quality_report():
    """Get data quality report"""
    try:
        report = data_manager.get_data_quality_report()
        return jsonify({
            'success': True,
            'quality_report': report
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting quality report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/estimate-cost', methods=['POST'])
def estimate_cost():
    """Estimate cost for a property using the vector database"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No property data received'}), 400
        
        # Use the vector database for cost estimation
        from vector_database_cost_estimation import PropertyCostVectorDB
        vector_db = PropertyCostVectorDB(data_manager.db_path)
        
        estimation = vector_db.estimate_cost(data)
        
        return jsonify({
            'success': True,
            'estimation': estimation
        }), 200
        
    except Exception as e:
        logger.error(f"Error estimating cost: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Property Cost Vector Database API',
        'version': '1.0.0',
        'endpoints': {
            'POST /webhook/project-data': 'Receive real project data',
            'POST /webhook/material-costs': 'Receive material cost updates',
            'GET /api/projects': 'Get all projects with filtering',
            'GET /api/quality-report': 'Get data quality report',
            'POST /api/estimate-cost': 'Estimate property cost',
            'GET /health': 'Health check'
        },
        'example_project_data': {
            'project_name': 'Sample House',
            'property_type': 'family_house',
            'size_sqm': 150,
            'bedrooms': 3,
            'bathrooms': 2,
            'floors': 2,
            'construction_year': 2024,
            'location': 'Munich',
            'quality_level': 'standard',
            'actual_total_cost': 300000,
            'contractor_name': 'Sample Contractor',
            'project_status': 'completed'
        }
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Property Cost Vector Database API Server...")
    print("📡 Webhook endpoints available:")
    print("   POST http://localhost:5000/webhook/project-data")
    print("   POST http://localhost:5000/webhook/material-costs")
    print("   GET  http://localhost:5000/api/projects")
    print("   GET  http://localhost:5000/api/quality-report")
    print("   POST http://localhost:5000/api/estimate-cost")
    print("   GET  http://localhost:5000/health")
    print("\n✅ Server ready to receive data!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
