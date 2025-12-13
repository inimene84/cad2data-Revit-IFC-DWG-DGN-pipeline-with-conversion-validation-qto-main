#!/usr/bin/env python3
"""
OCR Service using Tesseract for construction drawings
"""

from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
from pathlib import Path
import base64
import platform
import shutil

app = Flask(__name__)

# Tesseract path - supports both Windows and Linux
if platform.system() == 'Windows':
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    # Linux/Docker - tesseract is in PATH
    TESSERACT_PATH = "tesseract"

@app.route('/health', methods=['GET'])
def health():
    # Check if tesseract is available
    tesseract_available = shutil.which("tesseract") is not None or (platform.system() == 'Windows' and Path(TESSERACT_PATH).exists())
    return jsonify({
        "status": "ok", 
        "tesseract_path": TESSERACT_PATH,
        "tesseract_available": tesseract_available,
        "platform": platform.system()
    }), 200

@app.route('/ocr', methods=['POST'])
def ocr():
    data = request.get_json(force=True)
    file_path = data.get('file_path')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "file_path not found", "file_path": file_path}), 400
    
    # Check if tesseract is available
    tesseract_cmd = shutil.which("tesseract") or (TESSERACT_PATH if platform.system() == 'Windows' and Path(TESSERACT_PATH).exists() else None)
    if not tesseract_cmd:
        return jsonify({"error": "Tesseract not found", "path": TESSERACT_PATH}), 500
    
    try:
        # Create temp output file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        # Use tesseract from PATH if available, otherwise use configured path
        tesseract_cmd = shutil.which("tesseract") or TESSERACT_PATH
        
        # Run Tesseract with construction-optimized settings
        cmd = [
            tesseract_cmd,
            file_path,
            output_path.replace('.txt', ''),  # Tesseract adds .txt automatically
            '--psm', '6',  # Uniform block of text
            '--oem', '1',  # LSTM OCR Engine
            '-l', 'eng',   # English language
            '--dpi', '300' # High DPI for construction drawings
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Read the output
        with open(output_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Clean up temp file
        os.unlink(output_path)
        
        # Extract text blocks and dimensions (simple regex)
        import re
        
        # Find dimensions (e.g., "120.5m", "45'6\"", "3.2m x 4.5m")
        dimensions = re.findall(r'\d+\.?\d*\s*[mM]\s*[xX×]\s*\d+\.?\d*\s*[mM]|\d+\.?\d*\s*[mM]|\d+\'\d+"', text)
        
        # Find material references
        materials = re.findall(r'(concrete|steel|wood|brick|insulation|membrane|bitumen|epdm)', text, re.IGNORECASE)
        
        # Find layer names (common in CAD)
        layers = re.findall(r'(ROOF|WALL|FOUNDATION|STRUCTURE|INSULATION|WATERPROOF)', text)
        
        return jsonify({
            "text": text,
            "dimensions": dimensions,
            "materials": list(set(materials)),
            "layers": list(set(layers)),
            "word_count": len(text.split()),
            "return_code": result.returncode,
            "stderr": result.stderr
        }), 200
        
    except subprocess.TimeoutExpired:
        return jsonify({"error": "OCR timeout", "timeout_sec": 300}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ocr-batch', methods=['POST'])
def ocr_batch():
    """Process multiple files"""
    data = request.get_json(force=True)
    file_paths = data.get('file_paths', [])
    
    results = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            # Process each file
            single_data = {"file_path": file_path}
            result = ocr()
            results.append({
                "file": file_path,
                "result": result[0].get_json() if result[1] == 200 else {"error": "Failed"},
                "status": result[1]
            })
        else:
            results.append({
                "file": file_path,
                "result": {"error": "File not found"},
                "status": 404
            })
    
    return jsonify({"results": results}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5056'))
    app.run(host='0.0.0.0', port=port, debug=True)
