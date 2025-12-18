#!/bin/bash
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
