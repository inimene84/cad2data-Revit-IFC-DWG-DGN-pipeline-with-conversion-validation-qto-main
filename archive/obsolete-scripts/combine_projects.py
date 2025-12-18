#!/usr/bin/env python3
"""
Combine CAD2Data and Construction Projects
Prepares unified project structure for VPS deployment
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class ProjectCombiner:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.cad2data_path = Path(r"C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main")
        self.construction_path = Path(r"C:\Users\valgu\Desktop\Construction")
        self.output_path = self.base_dir / "construction-platform"
        
    def create_directory_structure(self):
        """Create unified directory structure"""
        directories = [
            "cad-converters",
            "n8n-workflows/cad-bim",
            "n8n-workflows/construction",
            "python-services/api",
            "python-services/converters",
            "python-services/ocr",
            "python-services/analytics",
            "web-react",
            "deployment",
            "monitoring/grafana/dashboards",
            "monitoring/grafana/datasources",
            "nginx/ssl",
            "nginx/logs",
            "uploads",
            "output",
            "sql",
            "config",
            "secrets",
        ]
        
        for directory in directories:
            (self.output_path / directory).mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
    
    def copy_cad2data_files(self):
        """Copy files from CAD2Data project"""
        print("\nCopying CAD2Data project files...")
        
        # Copy converters
        converter_dirs = [
            "DDC_Converter_Revit",
            "DDC_Converter_IFC",
            "DDC_Converter_DWG",
            "DDC_Converter_DGN"
        ]
        
        for converter_dir in converter_dirs:
            src = self.cad2data_path / converter_dir
            dst = self.output_path / "cad-converters" / converter_dir
            if src.exists():
                shutil.copytree(src, dst, dirs_exist_ok=True)
                print(f"Copied converter: {converter_dir}")
        
        # Copy n8n workflows
        workflow_files = list(self.cad2data_path.glob("n8n_*.json"))
        for workflow_file in workflow_files:
            dst = self.output_path / "n8n-workflows" / "cad-bim" / workflow_file.name
            shutil.copy2(workflow_file, dst)
            print(f"Copied workflow: {workflow_file.name}")
        
        # Copy Python services
        services_dir = self.cad2data_path / "services"
        if services_dir.exists():
            for service_file in services_dir.glob("*.py"):
                dst = self.output_path / "python-services" / "converters" / service_file.name
                shutil.copy2(service_file, dst)
                print(f"Copied service: {service_file.name}")
        
        # Copy Python scripts
        python_scripts = [
            "vector_database_cost_estimation.py",
            "real_time_data_manager.py",
            "webhook_data_receiver.py",
            "batch_dwg_processor.py",
            "quick_excel_generator.py",
            "excel_cleanup_script.py",
            "revit_excel_integration.py",
            "project_data_extractor.py",
            "price_estimation_simple.py"
        ]
        
        for script in python_scripts:
            src = self.cad2data_path / script
            if src.exists():
                dst = self.output_path / "python-services" / "converters" / script
                shutil.copy2(src, dst)
                print(f"Copied script: {script}")
    
    def copy_construction_files(self):
        """Copy files from Construction project"""
        print("\nCopying Construction project files...")
        
        # Copy React UI
        react_dir = self.construction_path / "web-react"
        if react_dir.exists():
            dst = self.output_path / "web-react"
            shutil.copytree(react_dir, dst, dirs_exist_ok=True)
            print(f"Copied React UI")
        
        # Copy Python services
        python_services_dir = self.construction_path / "python-services"
        if python_services_dir.exists():
            for service_file in python_services_dir.glob("*.py"):
                dst = self.output_path / "python-services" / "api" / service_file.name
                shutil.copy2(service_file, dst)
                print(f"Copied service: {service_file.name}")
            
            # Copy requirements.txt
            requirements_file = python_services_dir / "requirements.txt"
            if requirements_file.exists():
                dst = self.output_path / "python-services" / "api" / "requirements.txt"
                shutil.copy2(requirements_file, dst)
                print(f"Copied requirements.txt")
        
        # Copy n8n workflows
        workflows_dir = self.construction_path / "n8n-workflows"
        if workflows_dir.exists():
            for workflow_file in workflows_dir.glob("*.json"):
                dst = self.output_path / "n8n-workflows" / "construction" / workflow_file.name
                shutil.copy2(workflow_file, dst)
                print(f"Copied workflow: {workflow_file.name}")
        
        # Copy Docker files
        docker_files = [
            "docker-compose.yml",
            "docker-compose.prod.yml",
            "Dockerfile.api",
            "Dockerfile.n8n",
            "Dockerfile.ui"
        ]
        
        for docker_file in docker_files:
            src = self.construction_path / docker_file
            if src.exists():
                dst = self.output_path / docker_file
                shutil.copy2(src, dst)
                print(f"Copied Docker file: {docker_file}")
        
        # Copy monitoring
        monitoring_dir = self.construction_path / "monitoring"
        if monitoring_dir.exists():
            dst = self.output_path / "monitoring"
            shutil.copytree(monitoring_dir, dst, dirs_exist_ok=True)
            print(f"Copied monitoring")
        
        # Copy nginx
        nginx_dir = self.construction_path / "nginx"
        if nginx_dir.exists():
            dst = self.output_path / "nginx"
            shutil.copytree(nginx_dir, dst, dirs_exist_ok=True)
            print(f"Copied nginx")
        
        # Copy SQL
        sql_dir = self.construction_path / "sql"
        if sql_dir.exists():
            dst = self.output_path / "sql"
            shutil.copytree(sql_dir, dst, dirs_exist_ok=True)
            print(f"Copied SQL")
        
        # Copy config
        config_dir = self.construction_path / "config"
        if config_dir.exists():
            dst = self.output_path / "config"
            shutil.copytree(config_dir, dst, dirs_exist_ok=True)
            print(f"Copied config")
    
    def create_dockerfile_converter(self):
        """Create Dockerfile for CAD converters with Wine"""
        dockerfile_content = """# Multi-stage build for CAD converters with Wine
FROM ubuntu:22.04 AS base

# Install Wine and dependencies
RUN apt-get update && \\
    apt-get install -y --no-install-recommends \\
        wine \\
        winetricks \\
        wine64 \\
        wine32 \\
        xvfb \\
        python3 \\
        python3-pip \\
        curl \\
        wget \\
    && rm -rf /var/lib/apt/lists/*

# Set up Wine
ENV WINEPREFIX=/root/.wine
ENV WINEARCH=win64
ENV DISPLAY=:99

# Initialize Wine
RUN winecfg && winetricks -q vcrun2019

# Install Python dependencies
COPY python-services/converters/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir flask flask-cors requests pandas openpyxl

# Copy CAD converters
COPY cad-converters/ /app/converters/

# Copy converter services
COPY python-services/converters/ /app/services/

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 converter && \\
    chown -R converter:converter /app

USER converter

EXPOSE 5055 5056 5057

# Start converter service
CMD ["python3", "services/dwg_service.py"]
"""
        
        dockerfile_path = self.output_path / "Dockerfile.converter"
        dockerfile_path.write_text(dockerfile_content, encoding='utf-8')
        print(f"Created Dockerfile.converter")
    
    def create_unified_docker_compose(self):
        """Create unified Docker Compose file"""
        compose_content = """version: '3.8'

services:
  # ===== N8N Workflow Automation =====
  n8n:
    build:
      context: .
      dockerfile: Dockerfile.n8n
    container_name: construction-n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    env_file:
      - .env.production
    environment:
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.yourdomain.com/
      - N8N_METRICS=true
      - N8N_REDIS_URL=redis://redis:6379
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n-workflows:/workflows
      - ./cad-converters:/converters
    networks:
      - construction-network
    depends_on:
      - redis
      - postgres
      - qdrant

  # ===== FastAPI Backend =====
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: construction-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    volumes:
      - ./uploads:/app/uploads
      - ./python-services:/app
      - ./cad-converters:/app/converters
      - ./output:/app/output
    networks:
      - construction-network
    depends_on:
      - postgres
      - redis
      - qdrant

  # ===== React Web UI =====
  ui:
    build:
      context: ./web-react
      dockerfile: Dockerfile
    container_name: construction-ui
    restart: unless-stopped
    ports:
      - "3000:80"
    env_file:
      - .env.production
    environment:
      - REACT_APP_API_URL=http://api:8000
      - REACT_APP_N8N_URL=http://n8n:5678
    networks:
      - construction-network
    depends_on:
      - api

  # ===== CAD Converter Services =====
  dwg-service:
    build:
      context: .
      dockerfile: Dockerfile.converter
    container_name: construction-dwg-service
    restart: unless-stopped
    ports:
      - "5055:5055"
    env_file:
      - .env.production
    volumes:
      - ./cad-converters:/app/converters
      - ./uploads:/app/uploads
      - ./output:/app/output
    networks:
      - construction-network

  ocr-service:
    build:
      context: .
      dockerfile: Dockerfile.converter
    container_name: construction-ocr-service
    restart: unless-stopped
    ports:
      - "5056:5056"
    env_file:
      - .env.production
    volumes:
      - ./uploads:/app/uploads
    networks:
      - construction-network

  drive-service:
    build:
      context: .
      dockerfile: Dockerfile.converter
    container_name: construction-drive-service
    restart: unless-stopped
    ports:
      - "5057:5057"
    env_file:
      - .env.production
    networks:
      - construction-network

  # ===== Databases =====
  postgres:
    image: postgres:15-alpine
    container_name: construction-postgres
    restart: unless-stopped
    env_file:
      - .env.production
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - construction-network

  redis:
    image: redis:7-alpine
    container_name: construction-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - construction-network

  qdrant:
    image: qdrant/qdrant:v1.8.1
    container_name: construction-qdrant
    restart: unless-stopped
    env_file:
      - .env.production
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - construction-network

  # ===== Monitoring =====
  prometheus:
    image: prom/prometheus:latest
    container_name: construction-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - construction-network

  grafana:
    image: grafana/grafana:latest
    container_name: construction-grafana
    restart: unless-stopped
    ports:
      - "3001:3000"
    env_file:
      - .env.production
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    networks:
      - construction-network
    depends_on:
      - prometheus

  # ===== Nginx Reverse Proxy =====
  nginx:
    image: nginx:alpine
    container_name: construction-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    networks:
      - construction-network
    depends_on:
      - ui
      - api
      - n8n

volumes:
  n8n_data:
  postgres_data:
  redis_data:
  qdrant_data:
  prometheus_data:
  grafana_data:

networks:
  construction-network:
    driver: bridge
"""
        
        compose_path = self.output_path / "docker-compose.prod.yml"
        compose_path.write_text(compose_content, encoding='utf-8')
        print(f"Created docker-compose.prod.yml")
    
    def create_env_template(self):
        """Create environment file template"""
        env_content = """# Database
POSTGRES_USER=construction_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=construction_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# N8N
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.yourdomain.com/
N8N_REDIS_URL=redis://redis:6379

# API
API_HOST=0.0.0.0
API_PORT=8000

# CAD Converters
DWG_CONVERTER_PATH=/app/converters/DDC_Converter_DWG/datadrivenlibs/DwgExporter.exe
IFC_CONVERTER_PATH=/app/converters/DDC_Converter_IFC/datadrivenlibs/IfcExporter.exe
REVIT_CONVERTER_PATH=/app/converters/DDC_Converter_Revit/datadrivenlibs/RvtExporter.exe
DGN_CONVERTER_PATH=/app/converters/DDC_Converter_DGN/datadrivenlibs/DgnExporter.exe

# Wine
WINEPREFIX=/root/.wine
WINEARCH=win64
DISPLAY=:99

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Google Drive
GOOGLE_DRIVE_CREDENTIALS_PATH=/app/config/credentials.json

# Domain
DOMAIN=yourdomain.com

# Grafana
GF_SECURITY_ADMIN_PASSWORD=your_grafana_password_here
"""
        
        env_path = self.output_path / ".env.production.example"
        env_path.write_text(env_content, encoding='utf-8')
        print(f"Created .env.production.example")
    
    def create_requirements_txt(self):
        """Create unified requirements.txt"""
        requirements_content = """# Core FastAPI
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
pydantic>=2.0.0
aiofiles>=23.2.1

# Data processing
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.2

# Flask for converter services
flask>=3.0.0
flask-cors>=4.0.0

# Prometheus monitoring
prometheus-client>=0.19.0
prometheus-fastapi-instrumentator>=7.0.0

# AI/ML
google-generativeai>=0.3.0
sentence-transformers>=2.2.0

# Vector DB
qdrant-client>=1.7.0

# Database
redis>=5.0.0
psycopg2-binary>=2.9.0

# OCR for construction documents
pytesseract>=0.3.10
Pillow>=10.0.0
pdf2image>=1.16.0
PyMuPDF>=1.23.0
reportlab>=1.0.0

# Testing
pytest>=7.4.3
httpx>=0.25.1
"""
        
        requirements_path = self.output_path / "python-services" / "requirements.txt"
        requirements_path.write_text(requirements_content, encoding='utf-8')
        print(f"Created requirements.txt")
    
    def create_deployment_script(self):
        """Create deployment script"""
        script_content = """#!/bin/bash
# Deployment script for VPS

set -e

echo "🚀 Starting deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env.production if it doesn't exist
if [ ! -f .env.production ]; then
    echo "📝 Creating .env.production from example..."
    cp .env.production.example .env.production
    echo "⚠️  Please edit .env.production with your actual values!"
    exit 1
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo "✅ Deployment complete!"
echo "📊 Services:"
echo "  - N8N: http://localhost:5678"
echo "  - API: http://localhost:8000"
echo "  - UI: http://localhost:3000"
echo "  - Grafana: http://localhost:3001"

echo "📝 Check logs with: docker-compose -f docker-compose.prod.yml logs -f"
"""
        
        script_path = self.output_path / "deployment" / "deploy.sh"
        script_path.write_text(script_content, encoding='utf-8')
        if os.name != 'nt':  # Unix-like systems
            script_path.chmod(0o755)
        print(f"Created deployment script")
    
    def create_readme(self):
        """Create README for combined project"""
        readme_content = """# Unified Construction Platform

## 📋 Overview

This is a unified construction platform combining:
- **CAD2Data Project** - CAD/BIM conversion pipeline
- **Construction Project** - React UI + FastAPI + n8n workflows

## 🚀 Quick Start

### 1. Combine Projects
```bash
python combine_projects.py
```

### 2. Configure Environment
```bash
cp .env.production.example .env.production
# Edit .env.production with your values
```

### 3. Deploy to VPS
```bash
cd construction-platform
./deployment/deploy.sh
```

## 📁 Project Structure

```
construction-platform/
├── cad-converters/          # CAD/BIM converters
├── n8n-workflows/          # n8n workflows (22 total)
├── python-services/        # Python services
├── web-react/              # React Web UI
├── docker-compose.prod.yml # Production Docker Compose
└── deployment/             # Deployment scripts
```

## 🔧 Services

- **N8N** - Workflow automation (port 5678)
- **API** - FastAPI backend (port 8000)
- **UI** - React Web UI (port 3000)
- **DWG Service** - CAD converter (port 5055)
- **OCR Service** - OCR service (port 5056)
- **Drive Service** - Google Drive (port 5057)
- **PostgreSQL** - Database
- **Redis** - Cache
- **Qdrant** - Vector database
- **Prometheus** - Monitoring
- **Grafana** - Dashboards

## 📚 Documentation

- See `COMBINE_AND_DEPLOY_TO_VPS.md` for detailed deployment guide

## 🆘 Support

- Check logs: `docker-compose logs -f`
- Check service status: `docker-compose ps`
- Restart services: `docker-compose restart`
"""
        
        readme_path = self.output_path / "README.md"
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"Created README.md")
    
    def run(self):
        """Run the combination process"""
        import sys
        import io
        # Fix encoding for Windows
        if sys.platform == 'win32':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        print("Combining CAD2Data and Construction Projects")
        print("=" * 60)
        
        # Create directory structure
        self.create_directory_structure()
        
        # Copy files from both projects
        self.copy_cad2data_files()
        self.copy_construction_files()
        
        # Create Docker files
        self.create_dockerfile_converter()
        self.create_unified_docker_compose()
        self.create_env_template()
        self.create_requirements_txt()
        self.create_deployment_script()
        self.create_readme()
        
        print("\n" + "=" * 60)
        print("Project combination complete!")
        print(f"Output directory: {self.output_path}")
        print("\nNext steps:")
        print("1. Edit .env.production with your values")
        print("2. Test locally: docker-compose up -d")
        print("3. Deploy to VPS: ./deployment/deploy.sh")

if __name__ == "__main__":
    combiner = ProjectCombiner()
    combiner.run()

