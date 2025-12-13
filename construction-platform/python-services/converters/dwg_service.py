#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
import uuid
from pathlib import Path

app = Flask(__name__)

# Configure default path to DwgExporter.exe
DWG_EXPORTER = os.environ.get('DWG_EXPORTER_PATH', r"C:\\Users\\valgu\\Documents\\GitHub\\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\\DDC_Converter_DWG\\datadrivenlibs\\DwgExporter.exe")

@app.route('/health', methods=['GET'])
def health():
	return jsonify({"status": "ok", "dwg_exporter": DWG_EXPORTER, "exists": Path(DWG_EXPORTER).exists()}), 200

@app.route('/convert-dwg', methods=['POST'])
def convert_dwg():
	data = request.get_json(force=True)
	input_path = data.get('input_path')
	output_dir = data.get('output_dir')
	options = data.get('options', {})

	if not input_path or not os.path.exists(input_path):
		return jsonify({"error": "input_path not found", "input_path": input_path}), 400
	if not output_dir:
		output_dir = os.path.join(tempfile.gettempdir(), f"dwg_export_{uuid.uuid4().hex}")
	os.makedirs(output_dir, exist_ok=True)

	if not Path(DWG_EXPORTER).exists():
		return jsonify({"error": "DwgExporter.exe not found", "path": DWG_EXPORTER}), 500

	# Command: DwgExporter.exe "input.dwg" "output_folder"
	cmd = f'"{DWG_EXPORTER}" "{input_path}" "{output_dir}"'
	try:
		proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=1800)
		stdout = proc.stdout
		stderr = proc.stderr
		code = proc.returncode
		# Collect outputs
		xlsx = list(Path(output_dir).glob('*.xlsx'))
		dae = list(Path(output_dir).glob('*.dae'))
		return jsonify({
			"return_code": code,
			"stdout": stdout,
			"stderr": stderr,
			"output_dir": output_dir,
			"xlsx": [str(p) for p in xlsx],
			"dae": [str(p) for p in dae]
		}), 200 if code == 0 else 500
	except subprocess.TimeoutExpired:
		return jsonify({"error": "conversion_timeout", "timeout_sec": 1800}), 504
	except Exception as e:
		return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
	port = int(os.environ.get('PORT', '5055'))
	app.run(host='0.0.0.0', port=port, debug=True)
