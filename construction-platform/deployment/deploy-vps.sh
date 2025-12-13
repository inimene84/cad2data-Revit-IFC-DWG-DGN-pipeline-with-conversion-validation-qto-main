#!/bin/bash
# VPS Deployment Script for construction.thorspark.cloud
# Run this script on the Hostinger VPS after cloning the repository

set -e

echo "🚀 Starting VPS Deployment for construction.thorspark.cloud"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    exit 1
fi

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Running without root. Some commands may fail."
fi

# Navigate to project directory
cd /root/construction-platform

# Step 1: Setup environment file
if [ ! -f .env.production ]; then
    echo "📝 Creating .env.production from .env.vps template..."
    cp .env.vps .env.production
    echo ""
    echo "⚠️  IMPORTANT: Edit .env.production with your actual passwords!"
    echo "   nano .env.production"
    echo ""
    echo "   Change these values:"
    echo "   - POSTGRES_PASSWORD"
    echo "   - GF_SECURITY_ADMIN_PASSWORD"
    echo "   - OPENAI_API_KEY (if using AI features)"
    echo ""
    read -p "Press Enter after editing .env.production..."
fi

# Step 2: Check existing network
echo "🔍 Checking Docker networks..."
EXISTING_NETWORK=$(docker network ls --format "{{.Name}}" | grep -E "^root_default$" || echo "")

if [ -z "$EXISTING_NETWORK" ]; then
    echo "⚠️  Network 'root_default' not found. Creating it..."
    docker network create root_default
else
    echo "✅ Found existing network: root_default"
fi

# Step 3: Build services
echo "🔨 Building Docker images (this may take a few minutes)..."
docker compose -f docker-compose.vps.yml build

# Step 4: Start services
echo "🚀 Starting services..."
docker compose -f docker-compose.vps.yml up -d

# Step 5: Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Step 6: Check status
echo ""
echo "📊 Service Status:"
docker compose -f docker-compose.vps.yml ps

echo ""
echo "✅ Deployment Complete!"
echo "=============================================="
echo ""
echo "🌐 Your services are available at:"
echo "   • App UI:     https://construction.thorspark.cloud"
echo "   • API:        https://api.construction.thorspark.cloud"
echo "   • Grafana:    https://grafana.construction.thorspark.cloud"
echo "   • Prometheus: https://prometheus.construction.thorspark.cloud"
echo ""
echo "📝 Existing services (already running):"
echo "   • N8N:        https://n8n.construction.thorspark.cloud (port 5678)"
echo "   • Qdrant:     http://localhost:6333"
echo ""
echo "🔧 Useful commands:"
echo "   • View logs:  docker compose -f docker-compose.vps.yml logs -f"
echo "   • Restart:    docker compose -f docker-compose.vps.yml restart"
echo "   • Stop:       docker compose -f docker-compose.vps.yml down"
echo ""
