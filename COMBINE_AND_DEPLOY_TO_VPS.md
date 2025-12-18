# 🚀 Combine CAD2Data + Construction Projects & Deploy to VPS

## 📋 Overview

This guide combines two construction projects:
1. **CAD2Data Project** - CAD/BIM conversion pipeline with n8n workflows
2. **Construction Project** - React UI + FastAPI + 13 n8n workflows + Docker setup

And deploys them to a VPS with a unified architecture.

---

## 🎯 Project Analysis

### **CAD2Data Project** (Current Location)
```
C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\
```
**Components:**
- ✅ 9 n8n workflows (CAD/BIM conversion)
- ✅ Python scripts (data processing)
- ✅ Windows converters (RvtExporter.exe, IfcExporter.exe, DwgExporter.exe, DgnExporter.exe)
- ✅ Microservices (DWG, OCR, Drive Provisioner)
- ✅ Vector database (cost estimation)
- ✅ 276,931 processed elements

### **Construction Project** (Desktop)
```
C:\Users\valgu\Desktop\Construction\
```
**Components:**
- ✅ React Web UI
- ✅ FastAPI backend
- ✅ 13 n8n workflows (construction agents)
- ✅ Docker Compose setup
- ✅ PostgreSQL, Redis, Qdrant
- ✅ Prometheus + Grafana monitoring
- ✅ VPS deployment scripts

---

## 🔄 Combination Strategy

### **1. Unified Project Structure**
```
construction-platform/
├── cad-converters/          # CAD/BIM converters (Windows executables)
├── n8n-workflows/          # Combined n8n workflows (22 total)
│   ├── cad-bim/            # CAD2Data workflows (9)
│   └── construction/       # Construction workflows (13)
├── python-services/        # Combined Python services
│   ├── api/                # FastAPI backend
│   ├── converters/         # CAD converter services
│   ├── ocr/                # OCR service
│   └── analytics/          # Analytics service
├── web-react/              # React Web UI
├── docker-compose.yml      # Unified Docker Compose
├── docker-compose.prod.yml # Production Docker Compose
└── deployment/             # Deployment scripts
```

### **2. Key Challenges & Solutions**

#### **Challenge 1: Windows Executables on Linux VPS**
**Problem:** CAD converters are Windows executables (.exe)
**Solutions:**
1. **Wine + Docker** (Recommended)
   - Run Windows executables in Wine container
   - Isolated from host system
   - Docker image with Wine pre-installed

2. **Wine in Dockerfile**
   ```dockerfile
   FROM ubuntu:22.04
   RUN apt-get update && apt-get install -y wine winetricks
   COPY cad-converters/ /app/converters/
   ```

3. **Alternative: Native Linux Converters**
   - Contact DataDrivenConstruction for Linux versions
   - Or use Wine as fallback

#### **Challenge 2: Port Conflicts**
**Problem:** Both projects use similar ports
**Solution:** Unified port mapping
```yaml
services:
  n8n: 5678
  api: 8000
  ui: 3000
  dwg-service: 5055
  ocr-service: 5056
  drive-service: 5057
```

#### **Challenge 3: n8n Workflow Integration**
**Problem:** 22 workflows need to work together
**Solution:**
- Merge workflow folders
- Update webhook URLs
- Share credentials
- Use workflow tags for organization

#### **Challenge 4: Database Integration**
**Problem:** Multiple databases (SQLite, PostgreSQL, Qdrant)
**Solution:**
- Use PostgreSQL for all relational data
- Use Qdrant for vector search
- Migrate SQLite data to PostgreSQL
- Keep separate databases for different purposes

---

## 🐳 Docker Architecture

### **Unified Docker Compose**
```yaml
version: '3.8'

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
      dockerfile: Dockerfile.ocr
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
      dockerfile: Dockerfile.drive
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
```

---

## 🐍 Dockerfile for CAD Converters (Wine)

### **Dockerfile.converter**
```dockerfile
# Multi-stage build for CAD converters with Wine
FROM ubuntu:22.04 AS base

# Install Wine and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wine \
        winetricks \
        wine64 \
        wine32 \
        xvfb \
        python3 \
        python3-pip \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Set up Wine
ENV WINEPREFIX=/root/.wine
ENV WINEARCH=win64
RUN winecfg

# Install Python dependencies
COPY python-services/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy CAD converters
COPY cad-converters/ /app/converters/

# Copy converter service
COPY services/dwg_service.py /app/dwg_service.py
COPY services/ocr_service.py /app/ocr_service.py
COPY services/drive_provisioner.py /app/drive_provisioner.py

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 converter && \
    chown -R converter:converter /app

USER converter

EXPOSE 5055 5056 5057

# Start converter services
CMD ["python3", "dwg_service.py"]
```

---

## 📦 Deployment Steps

### **Step 1: Prepare Local Environment**

```bash
# Create unified project directory
mkdir -p construction-platform
cd construction-platform

# Create directory structure
mkdir -p cad-converters n8n-workflows/cad-bim n8n-workflows/construction
mkdir -p python-services/api python-services/converters python-services/ocr
mkdir -p python-services/analytics web-react deployment monitoring nginx
```

### **Step 2: Copy Files from Both Projects**

#### **From CAD2Data Project:**
```bash
# Copy converters
cp -r "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\DDC_Converter_*" ./cad-converters/

# Copy n8n workflows
cp "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\n8n_*.json" ./n8n-workflows/cad-bim/

# Copy Python services
cp "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\services\*.py" ./python-services/converters/

# Copy Python scripts
cp "C:\Users\valgu\Documents\GitHub\cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto-main\*.py" ./python-services/
```

#### **From Construction Project:**
```bash
# Copy React UI
cp -r "C:\Users\valgu\Desktop\Construction\web-react" ./

# Copy Python services
cp -r "C:\Users\valgu\Desktop\Construction\python-services\*" ./python-services/api/

# Copy n8n workflows
cp "C:\Users\valgu\Desktop\Construction\n8n-workflows\*.json" ./n8n-workflows/construction/

# Copy Docker files
cp "C:\Users\valgu\Desktop\Construction\docker-compose.yml" ./
cp "C:\Users\valgu\Desktop\Construction\Dockerfile.*" ./

# Copy monitoring
cp -r "C:\Users\valgu\Desktop\Construction\monitoring" ./

# Copy nginx
cp -r "C:\Users\valgu\Desktop\Construction\nginx" ./
```

### **Step 3: Create Unified Docker Files**

Create the Dockerfiles as shown above.

### **Step 4: Create Environment File**

```bash
# .env.production
# Database
POSTGRES_USER=construction_user
POSTGRES_PASSWORD=your_secure_password
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

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google Drive
GOOGLE_DRIVE_CREDENTIALS_PATH=/app/config/credentials.json

# Domain
DOMAIN=yourdomain.com
```

### **Step 5: Update Python Services**

#### **Update Converter Service for Wine**
```python
# python-services/converters/dwg_service.py
import os
import subprocess
import wine

DWG_CONVERTER = os.environ.get('DWG_CONVERTER_PATH', '/app/converters/DwgExporter.exe')

def convert_dwg_wine(input_path, output_dir):
    """Convert DWG using Wine"""
    # Use Wine to run Windows executable
    cmd = f'wine {DWG_CONVERTER} "{input_path}" "{output_dir}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0
```

### **Step 6: Update n8n Workflows**

#### **Update Webhook URLs**
- Change localhost URLs to service names
- Update file paths to use Docker volumes
- Update converter paths to use Wine

### **Step 7: Deploy to VPS**

#### **On VPS:**
```bash
# SSH into VPS
ssh user@your-vps-ip

# Create project directory
mkdir -p ~/construction-platform
cd ~/construction-platform

# Copy files from local (use scp or rsync)
# From local machine:
scp -r construction-platform/* user@your-vps-ip:~/construction-platform/

# On VPS, install Docker and Docker Compose
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

---

## 🔧 VPS Deployment Configuration

### **Nginx Reverse Proxy**
```nginx
# nginx/nginx.conf
upstream ui {
    server ui:80;
}

upstream api {
    server api:8000;
}

upstream n8n {
    server n8n:5678;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # React UI
    location / {
        proxy_pass http://ui;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API
    location /api {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # N8N
    location /n8n {
        proxy_pass http://n8n;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **SSL Certificate (Let's Encrypt)**
```bash
# Install Certbot
sudo apt-get install -y certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates to nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./nginx/ssl/
```

---

## 📊 Monitoring & Logging

### **Prometheus Configuration**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'api'
    static_configs:
      - targets: ['api:8000']

  - job_name: 'n8n'
    static_configs:
      - targets: ['n8n:5678']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
```

### **Grafana Dashboards**
- Import dashboards from `monitoring/grafana/dashboards/`
- Configure datasources in `monitoring/grafana/datasources/`

---

## 🚀 Deployment Checklist

### **Pre-Deployment**
- [ ] Combine both projects locally
- [ ] Test Docker Compose locally
- [ ] Update all configuration files
- [ ] Test CAD converters with Wine
- [ ] Update n8n workflows
- [ ] Create environment file
- [ ] Set up SSL certificates
- [ ] Configure domain DNS

### **Deployment**
- [ ] SSH into VPS
- [ ] Install Docker and Docker Compose
- [ ] Copy project files to VPS
- [ ] Create environment file on VPS
- [ ] Start Docker Compose
- [ ] Verify all services are running
- [ ] Test API endpoints
- [ ] Test n8n workflows
- [ ] Test React UI
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL certificates
- [ ] Configure monitoring
- [ ] Set up backups

### **Post-Deployment**
- [ ] Test all workflows
- [ ] Monitor logs
- [ ] Check performance metrics
- [ ] Set up automated backups
- [ ] Configure monitoring alerts
- [ ] Document deployment process

---

## 🆘 Troubleshooting

### **Wine Issues**
```bash
# Test Wine installation
docker exec -it construction-dwg-service wine --version

# Test converter
docker exec -it construction-dwg-service wine /app/converters/DwgExporter.exe --help
```

### **Port Conflicts**
```bash
# Check port usage
sudo netstat -tulpn | grep :5678

# Change ports in docker-compose.yml
```

### **Database Connection Issues**
```bash
# Check database logs
docker logs construction-postgres

# Test connection
docker exec -it construction-postgres psql -U construction_user -d construction_db
```

### **n8n Workflow Issues**
```bash
# Check n8n logs
docker logs construction-n8n

# Access n8n UI
http://your-vps-ip:5678
```

---

## 📈 Performance Optimization

### **Resource Limits**
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

### **Caching**
- Use Redis for caching
- Enable Docker layer caching
- Use CDN for static assets

### **Scaling**
- Use Docker Swarm or Kubernetes
- Horizontal scaling for API
- Vertical scaling for databases

---

## 🎯 Next Steps

1. **Combine Projects Locally** - Test everything locally first
2. **Create Docker Images** - Build and test Docker images
3. **Deploy to VPS** - Deploy to VPS and test
4. **Monitor Performance** - Set up monitoring and alerts
5. **Optimize** - Optimize performance and costs

---

## 📞 Support

- **GitHub Issues** - Report bugs and issues
- **Documentation** - Check project documentation
- **Community** - Join community discussions

---

**🎉 Ready to deploy your unified construction platform to VPS!**

