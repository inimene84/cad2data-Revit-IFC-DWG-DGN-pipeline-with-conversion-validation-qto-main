# 🚀 Quick Start: Combine & Deploy to VPS

## 📋 Step-by-Step Guide

### **Step 1: Combine Projects Locally**

```bash
# Run the combination script
python combine_projects.py
```

This will:
- ✅ Create unified project structure
- ✅ Copy files from both projects
- ✅ Create Docker files
- ✅ Create deployment scripts
- ✅ Create environment template

### **Step 2: Configure Environment**

```bash
cd construction-platform
cp .env.production.example .env.production
# Edit .env.production with your actual values
```

**Required values:**
- PostgreSQL password
- Redis configuration
- Qdrant configuration
- OpenAI API key
- Google Drive credentials
- Domain name

### **Step 3: Test Locally (Optional)**

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### **Step 4: Deploy to VPS**

#### **On Your Local Machine:**

```bash
# SSH into VPS
ssh user@your-vps-ip

# Create project directory
mkdir -p ~/construction-platform
cd ~/construction-platform
```

#### **Copy Files to VPS:**

```bash
# From your local machine
scp -r construction-platform/* user@your-vps-ip:~/construction-platform/

# Or use rsync (faster)
rsync -avz construction-platform/ user@your-vps-ip:~/construction-platform/
```

#### **On VPS:**

```bash
# Install Docker (if not installed)
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Navigate to project
cd ~/construction-platform

# Create .env.production
cp .env.production.example .env.production
nano .env.production  # Edit with your values

# Deploy
./deployment/deploy.sh

# Check status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### **Step 5: Configure Domain & SSL**

#### **Add DNS Records:**

1. Go to your domain provider
2. Add A record: `yourdomain.com` → VPS IP
3. Add A record: `n8n.yourdomain.com` → VPS IP
4. Add A record: `api.yourdomain.com` → VPS IP

#### **Get SSL Certificate:**

```bash
# Install Certbot
sudo apt-get install -y certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d n8n.yourdomain.com -d api.yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./nginx/ssl/

# Restart Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### **Step 6: Configure Nginx**

Edit `nginx/nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    location / {
        proxy_pass http://ui:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /n8n {
        proxy_pass http://n8n:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Restart Nginx:
```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

### **Step 7: Verify Deployment**

```bash
# Check all services
docker-compose -f docker-compose.prod.yml ps

# Test endpoints
curl http://localhost:5678  # N8N
curl http://localhost:8000/health  # API
curl http://localhost:3000  # UI

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### **Step 8: Import n8n Workflows**

1. Access N8N: `http://yourdomain.com/n8n`
2. Go to **Workflows** → **Import from File**
3. Import all workflows from `n8n-workflows/` folder
4. Configure credentials for each workflow
5. Activate workflows

### **Step 9: Monitor Services**

```bash
# Access Grafana
http://yourdomain.com:3001

# Access Prometheus
http://yourdomain.com:9090

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🆘 Troubleshooting

### **Wine Issues**
```bash
# Test Wine
docker exec -it construction-dwg-service wine --version

# Test converter
docker exec -it construction-dwg-service wine /app/converters/DwgExporter.exe --help
```

### **Port Conflicts**
```bash
# Check ports
sudo netstat -tulpn | grep :5678

# Change ports in docker-compose.prod.yml
```

### **Database Issues**
```bash
# Check database
docker logs construction-postgres

# Test connection
docker exec -it construction-postgres psql -U construction_user -d construction_db
```

### **Service Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs [service-name]

# Restart service
docker-compose -f docker-compose.prod.yml restart [service-name]

# Rebuild service
docker-compose -f docker-compose.prod.yml build [service-name]
docker-compose -f docker-compose.prod.yml up -d [service-name]
```

---

## 📊 Services Checklist

- [ ] N8N running (port 5678)
- [ ] API running (port 8000)
- [ ] UI running (port 3000)
- [ ] DWG service running (port 5055)
- [ ] OCR service running (port 5056)
- [ ] Drive service running (port 5057)
- [ ] PostgreSQL running
- [ ] Redis running
- [ ] Qdrant running
- [ ] Prometheus running (port 9090)
- [ ] Grafana running (port 3001)
- [ ] Nginx running (ports 80, 443)

---

## 🎯 Next Steps

1. **Import n8n workflows** - Import all 22 workflows
2. **Configure credentials** - Set up API keys and credentials
3. **Test workflows** - Test each workflow
4. **Monitor performance** - Set up monitoring and alerts
5. **Optimize** - Optimize performance and costs

---

## 📞 Support

- **Documentation** - See `COMBINE_AND_DEPLOY_TO_VPS.md`
- **GitHub Issues** - Report bugs and issues
- **Community** - Join community discussions

---

**🎉 Ready to deploy your unified construction platform!**

