#!/usr/bin/env python3
"""
Google Drive Auto-Provisioning Service for Construction Projects
Creates standardized folder structure per project
"""

from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Standard folder structure for construction projects
PROJECT_FOLDERS = [
    "01_Drawings",
    "02_RFIs", 
    "03_Site_Photos",
    "04_Reports",
    "05_Intake",
    "06_Processed",
    "07_Compliance",
    "08_Contracts",
    "09_Change_Orders",
    "10_Closeout"
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "drive_provisioner",
        "available_folders": PROJECT_FOLDERS
    }), 200

@app.route('/create-project', methods=['POST'])
def create_project():
    """Create project folder structure in Google Drive"""
    data = request.get_json(force=True)
    project_name = data.get('project_name')
    drive_root = data.get('drive_root', 'Drive/Projects')
    
    if not project_name:
        return jsonify({"error": "project_name required"}), 400
    
    # This would integrate with Google Drive API
    # For now, return the folder structure that n8n should create
    project_path = f"{drive_root}/{project_name}"
    
    folder_structure = {
        "project_name": project_name,
        "project_path": project_path,
        "created_at": datetime.now().isoformat(),
        "folders": []
    }
    
    for folder in PROJECT_FOLDERS:
        folder_structure["folders"].append({
            "name": folder,
            "path": f"{project_path}/{folder}",
            "description": get_folder_description(folder)
        })
    
    return jsonify(folder_structure), 200

@app.route('/check-project', methods=['POST'])
def check_project():
    """Check if project folders exist"""
    data = request.get_json(force=True)
    project_name = data.get('project_name')
    drive_root = data.get('drive_root', 'Drive/Projects')
    
    if not project_name:
        return jsonify({"error": "project_name required"}), 400
    
    # This would check Google Drive API
    # For now, return mock status
    return jsonify({
        "project_name": project_name,
        "project_path": f"{drive_root}/{project_name}",
        "exists": True,  # Mock - would check actual Drive
        "folders_created": len(PROJECT_FOLDERS),
        "last_checked": datetime.now().isoformat()
    }), 200

def get_folder_description(folder_name):
    """Get description for each folder type"""
    descriptions = {
        "01_Drawings": "Architectural, structural, MEP drawings and revisions",
        "02_RFIs": "Request for Information documents and responses",
        "03_Site_Photos": "Progress photos, drone footage, site documentation",
        "04_Reports": "Daily, weekly, monthly reports and analytics",
        "05_Intake": "Incoming documents from various sources",
        "06_Processed": "Processed and analyzed documents",
        "07_Compliance": "Safety, permits, inspections, certifications",
        "08_Contracts": "Contracts, agreements, legal documents",
        "09_Change_Orders": "Change orders and modifications",
        "10_Closeout": "Final documentation and project closeout"
    }
    return descriptions.get(folder_name, "Project documentation folder")

@app.route('/get-template', methods=['GET'])
def get_template():
    """Get folder template for manual creation"""
    return jsonify({
        "template": PROJECT_FOLDERS,
        "descriptions": {folder: get_folder_description(folder) for folder in PROJECT_FOLDERS}
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5057'))
    app.run(host='0.0.0.0', port=port, debug=True)
