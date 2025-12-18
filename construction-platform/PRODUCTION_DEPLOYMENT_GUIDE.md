# Production Deployment Guide
# construction-platform/PRODUCTION_DEPLOYMENT_GUIDE.md

## Production Deployment Guide

### Prerequisites

1. **Server Requirements:**
   - Ubuntu 20.04 LTS or later
   - 4+ CPU cores
   - 16GB+ RAM
   - 100GB+ SSD storage
   - Docker and Docker Compose installed

2. **Domain and SSL:**
   - Domain name configured
   - SSL certificate (Let's Encrypt recommended)
   - DNS records configured

3. **Services:**
   - PostgreSQL 15+
   - Redis 7+
   - Qdrant 1.8+
   - Nginx (reverse proxy)

### Deployment Steps

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt install nginx -y
```

#### 2. Clone Repository

```bash
# Clone repository
git clone <repository-url>
cd construction-platform

# Create environment file
cp .env.production.example .env.production
# Edit .env.production with your values
```

#### 3. Configure Environment

```bash
# Edit .env.production
nano .env.production

# Required variables:
# - DATABASE_URL
# - REDIS_HOST
# - QDRANT_URL
# - SECRET_KEY
# - ALLOWED_ORIGINS
# - API_KEYS
```

#### 4. Database Setup

```bash
# Initialize database
docker-compose exec postgres psql -U postgres -d construction_ai -f /sql/schema.sql

# Run migrations (if any)
# docker-compose exec api python manage.py migrate
```

#### 5. Build and Start Services

```bash
# Build services
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

#### 6. Configure Nginx

```bash
# Copy Nginx configuration
sudo cp nginx/nginx.conf /etc/nginx/sites-available/construction-ai
sudo ln -s /etc/nginx/sites-available/construction-ai /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### 7. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

#### 8. Monitoring Setup

```bash
# Start Prometheus and Grafana
docker-compose -f docker-compose.prod.yml up -d prometheus grafana

# Access Grafana
# http://yourdomain.com:3001
# Default credentials: admin/admin
```

#### 9. Backup Setup

```bash
# Create backup directory
mkdir -p backups

# Setup automated backups (cron)
crontab -e

# Add backup job (daily at 2 AM)
0 2 * * * cd /path/to/construction-platform && docker-compose exec api python -c "from backup_recovery import backup_manager; backup_manager.backup_database('postgresql://...')"
```

#### 10. Security Hardening

```bash
# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Install fail2ban
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Monitoring

#### Health Checks

```bash
# Check API health
curl https://yourdomain.com/health

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f api
```

#### Metrics

- Prometheus: http://yourdomain.com:9090
- Grafana: http://yourdomain.com:3001
- Jaeger: http://yourdomain.com:16686

### Backup & Recovery

#### Manual Backup

```bash
# Backup database
docker-compose exec api python -c "from backup_recovery import backup_manager; backup_manager.backup_database('postgresql://...')"

# Backup files
docker-compose exec api python -c "from backup_recovery import backup_manager; backup_manager.backup_files('/app/uploads')"
```

#### Manual Restore

```bash
# Restore database
docker-compose exec api python -c "from backup_recovery import backup_manager; backup_manager.restore_database('backups/db_backup.sql', 'postgresql://...')"

# Restore files
docker-compose exec api python -c "from backup_recovery import backup_manager; backup_manager.restore_files('backups/files_backup.tar.gz', '/app/uploads')"
```

### Troubleshooting

#### Service Not Starting

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs -f <service-name>

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Restart service
docker-compose -f docker-compose.prod.yml restart <service-name>
```

#### Database Connection Issues

```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -c "SELECT version();"

# Check connection
docker-compose -f docker-compose.prod.yml exec api python -c "import psycopg2; psycopg2.connect('postgresql://...')"
```

#### Redis Connection Issues

```bash
# Check Redis status
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping

# Check connection
docker-compose -f docker-compose.prod.yml exec api python -c "import redis; redis.Redis(host='redis', port=6379).ping()"
```

### Scaling

#### Horizontal Scaling

```bash
# Scale API service
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# Scale N8N service
docker-compose -f docker-compose.prod.yml up -d --scale n8n=2
```

#### Load Balancing

```bash
# Configure Nginx load balancing
# Edit nginx/nginx.conf
# Add upstream servers
```

### Maintenance

#### Update Services

```bash
# Pull latest changes
git pull

# Rebuild services
docker-compose -f docker-compose.prod.yml build

# Restart services
docker-compose -f docker-compose.prod.yml up -d
```

#### Cleanup

```bash
# Remove old containers
docker-compose -f docker-compose.prod.yml down

# Remove old images
docker image prune -a

# Cleanup backups
docker-compose exec api python -c "from backup_recovery import backup_manager; backup_manager.cleanup_old_backups()"
```

### Support

For issues or questions:
- Check logs: `docker-compose -f docker-compose.prod.yml logs -f`
- Check documentation: `README.md`
- Contact support: support@yourdomain.com
