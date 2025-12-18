# Unified Construction Platform

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
