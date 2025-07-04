# Deployment Guide - CHAOSTOWN Infrastructure

**Production-Ready Deployment for Cat-Centric AI Civilization**

---

## Overview

This guide covers the complete deployment pipeline for CHAOSTOWN, from local development to production infrastructure. The system is designed for high availability, scalability, and most importantly, uninterrupted cat happiness monitoring.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CHAOSTOWN INFRASTRUCTURE                  │
├─────────────────────────────────────────────────────────────┤
│  Load Balancer (Nginx)                                     │
│  ├── API Gateway (FastAPI)                                 │
│  ├── Dashboard (React/Next.js)                             │
│  └── Media Upload Service                                  │
├─────────────────────────────────────────────────────────────┤
│  Simulation Engine                                          │
│  ├── Agent Manager (Python)                                │
│  ├── Conway Engine (Rust/Python)                           │
│  └── Decision Processing (8x Ollama Models)                │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                 │
│  ├── PostgreSQL + TimescaleDB                              │
│  ├── Redis (Caching)                                       │
│  └── Vector Database (Qdrant)                              │
├─────────────────────────────────────────────────────────────┤
│  Monitoring & Observability                                │
│  ├── Grafana (Dashboards)                                  │
│  ├── Prometheus (Metrics)                                  │
│  └── Loki (Logs)                                           │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### System Requirements
- **CPU**: 16 cores minimum (32 cores recommended)
- **RAM**: 32 GB minimum (64 GB recommended)
- **Storage**: 500 GB SSD minimum (1 TB recommended)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional but recommended)
- **Network**: 1 Gbps connection

### Software Dependencies
- Docker Engine 24.0+
- Docker Compose 2.20+
- NVIDIA Container Toolkit (if using GPU)
- Git 2.40+

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/chaostown.git
cd chaostown
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### 3. Environment Variables

```bash
# .env file
# =============================================================================
# CHAOSTOWN DEPLOYMENT CONFIGURATION
# =============================================================================

# Deployment Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info

# Database Configuration
DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/chaostown
DB_PASSWORD=your_secure_password_here
POSTGRES_DB=chaostown
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${DB_PASSWORD}

# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=your_redis_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=your_super_secret_key_here
API_CORS_ORIGINS=["http://localhost:3000", "https://your-domain.com"]

# Simulation Configuration
MAX_AGENTS=1000
TICK_RATE=1.0
TIME_ACCELERATION=16
DEFAULT_GRID_SIZE=100

# Ollama Configuration
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODELS=llama3.1,llama3.2,mistral,gemma2,qwen2.5,phi3.5,codellama,deepseek-coder

# OpenAI Configuration (for cat happiness analysis)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-vision-preview

# Monitoring Configuration
GRAFANA_ADMIN_PASSWORD=admin_password_here
PROMETHEUS_RETENTION_TIME=30d

# SSL/TLS Configuration
SSL_CERT_PATH=/certs/fullchain.pem
SSL_KEY_PATH=/certs/privkey.pem
DOMAIN=your-domain.com

# Backup Configuration
BACKUP_S3_BUCKET=chaostown-backups
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# Cat Media Configuration
MEDIA_STORAGE_PATH=/data/media
MAX_MEDIA_SIZE=50MB
ALLOWED_MEDIA_TYPES=image/jpeg,image/png,image/gif,image/webp

# Security Configuration
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
ENABLE_CORS=true
TRUSTED_PROXIES=["127.0.0.1", "10.0.0.0/8"]
```

## Docker Deployment

### 1. Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Load Balancer
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./data/media:/var/www/media:ro
    depends_on:
      - api
      - dashboard
    networks:
      - chaostown-network

  # API Gateway
  api:
    build:
      context: ./api
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OLLAMA_HOST=${OLLAMA_HOST}
    volumes:
      - ./data/media:/app/media
    depends_on:
      - db
      - redis
      - ollama
    networks:
      - chaostown-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Dashboard
  dashboard:
    build:
      context: ./dashboard
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - NEXT_PUBLIC_API_URL=https://${DOMAIN}/api
    networks:
      - chaostown-network

  # Simulation Engine
  sim-engine:
    build:
      context: ./sim-engine
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OLLAMA_HOST=${OLLAMA_HOST}
      - MAX_AGENTS=${MAX_AGENTS}
      - TICK_RATE=${TICK_RATE}
    depends_on:
      - db
      - redis
      - ollama
    networks:
      - chaostown-network

  # Ollama AI Models
  ollama:
    image: ollama/ollama:latest
    restart: unless-stopped
    volumes:
      - ./data/ollama:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    ports:
      - "11434:11434"
    networks:
      - chaostown-network
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # PostgreSQL + TimescaleDB
  db:
    image: timescale/timescaledb:latest-pg15
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - chaostown-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - ./data/redis:/data
    networks:
      - chaostown-network

  # Vector Database
  qdrant:
    image: qdrant/qdrant:latest
    restart: unless-stopped
    volumes:
      - ./data/qdrant:/qdrant/storage
    ports:
      - "6333:6333"
    networks:
      - chaostown-network

  # Monitoring: Prometheus
  prometheus:
    image: prom/prometheus:latest
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./data/prometheus:/prometheus
    ports:
      - "9090:9090"
    networks:
      - chaostown-network

  # Monitoring: Grafana
  grafana:
    image: grafana/grafana:latest
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - ./monitoring/grafana:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
    ports:
      - "3000:3000"
    networks:
      - chaostown-network

  # Log Aggregation: Loki
  loki:
    image: grafana/loki:latest
    restart: unless-stopped
    volumes:
      - ./monitoring/loki.yml:/etc/loki/loki.yml
      - ./data/loki:/loki
    ports:
      - "3100:3100"
    networks:
      - chaostown-network

  # Backup Service
  backup:
    build:
      context: ./backup
      dockerfile: Dockerfile
    restart: unless-stopped
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - BACKUP_S3_BUCKET=${BACKUP_S3_BUCKET}
    volumes:
      - ./data:/backup/data:ro
    depends_on:
      - db
    networks:
      - chaostown-network

networks:
  chaostown-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  ollama_data:
  qdrant_data:
  prometheus_data:
  grafana_data:
  loki_data:
```

### 2. Production Deployment Script
```bash
#!/bin/bash
# deploy.sh
set -e

echo "🐱 Starting CHAOSTOWN deployment..."

# Validate environment
if [[ ! -f .env ]]; then
    echo "❌ .env file not found"
    exit 1
fi

# Load environment variables
source .env

# Create data directories
mkdir -p data/{postgres,redis,ollama,qdrant,prometheus,grafana,loki,media}
mkdir -p logs

# Set permissions
chmod 755 data/media
chmod 700 data/postgres

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose -f docker-compose.prod.yml pull

# Build custom images
echo "🏗️  Building custom images..."
docker-compose -f docker-compose.prod.yml build

# Start services
echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database
echo "⏳ Waiting for database..."
sleep 30

# Initialize database
echo "🗄️  Initializing database..."
docker-compose -f docker-compose.prod.yml exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/init.sql

# Download Ollama models
echo "🤖 Downloading Ollama models..."
for model in llama3.1 llama3.2 mistral gemma2 qwen2.5 phi3.5 codellama deepseek-coder; do
    docker-compose -f docker-compose.prod.yml exec ollama ollama pull $model
done

# Run health checks
echo "🩺 Running health checks..."
sleep 60

# Check API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API is healthy"
else
    echo "❌ API health check failed"
    exit 1
fi

# Check database
if docker-compose -f docker-compose.prod.yml exec db pg_isready -U $POSTGRES_USER > /dev/null 2>&1; then
    echo "✅ Database is healthy"
else
    echo "❌ Database health check failed"
    exit 1
fi

echo "🎉 CHAOSTOWN deployment completed successfully!"
echo "📊 Dashboard: http://localhost:3000"
echo "🔧 API: http://localhost:8000"
echo "📈 Grafana: http://localhost:3000"
echo "🐱 May Fluffhead and Wilson reign supreme!"
```

## SSL/TLS Configuration

### 1. Let's Encrypt Setup
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificates
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Nginx Configuration
```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    upstream dashboard {
        server dashboard:3000;
    }

    upstream grafana {
        server grafana:3000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=media:10m rate=1r/s;

    # SSL redirect
    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    # Main application
    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Media upload
        location /media/ {
            limit_req zone=media burst=5 nodelay;
            client_max_body_size 50M;
            proxy_pass http://api/media/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Dashboard
        location / {
            proxy_pass http://dashboard/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Grafana
        location /grafana/ {
            proxy_pass http://grafana/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## Monitoring Setup

### 1. Prometheus Configuration
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'chaostown-api'
    static_configs:
      - targets: ['api:8000']
    scrape_interval: 30s
    metrics_path: '/metrics'

  - job_name: 'chaostown-sim'
    static_configs:
      - targets: ['sim-engine:8001']
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['db:5432']
    scrape_interval: 60s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 60s

  - job_name: 'ollama'
    static_configs:
      - targets: ['ollama:11434']
    scrape_interval: 60s
```

### 2. Grafana Dashboard Import
```bash
# Copy dashboards
cp monitoring/dashboards/*.json data/grafana/dashboards/

# Import via API
curl -X POST http://admin:${GRAFANA_ADMIN_PASSWORD}@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @monitoring/dashboards/chaostown-main.json
```

## Backup Strategy

### 1. Database Backup
```bash
#!/bin/bash
# backup/backup-db.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="chaostown_${DATE}.sql.gz"

# Create backup
docker-compose exec db pg_dump -U $POSTGRES_USER -d $POSTGRES_DB | gzip > /tmp/$BACKUP_FILE

# Upload to S3
aws s3 cp /tmp/$BACKUP_FILE s3://$BACKUP_S3_BUCKET/database/

# Clean up local file
rm /tmp/$BACKUP_FILE

# Retain only last 30 days
aws s3 ls s3://$BACKUP_S3_BUCKET/database/ | \
  while read -r line; do
    createDate=$(echo $line | awk '{print $1" "$2}')
    createDate=$(date -d "$createDate" +%s)
    olderThan=$(date -d "30 days ago" +%s)
    if [[ $createDate -lt $olderThan ]]; then
      fileName=$(echo $line | awk '{print $4}')
      aws s3 rm s3://$BACKUP_S3_BUCKET/database/$fileName
    fi
  done
```

### 2. Media Backup
```bash
#!/bin/bash
# backup/backup-media.sh
DATE=$(date +%Y%m%d_%H%M%S)

# Sync media to S3
aws s3 sync ./data/media s3://$BACKUP_S3_BUCKET/media/

# Create archive
tar -czf media_${DATE}.tar.gz -C data media
aws s3 cp media_${DATE}.tar.gz s3://$BACKUP_S3_BUCKET/archives/
rm media_${DATE}.tar.gz
```

## Production Hardening

### 1. Security Measures
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install fail2ban
sudo apt install fail2ban -y

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Disable password authentication
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl reload sshd
```

### 2. Resource Limits
```yaml
# Add to docker-compose.prod.yml services
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```

## Scaling Considerations

### 1. Horizontal Scaling
```bash
# Scale API instances
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# Scale simulation engines
docker-compose -f docker-compose.prod.yml up -d --scale sim-engine=2
```

### 2. Database Optimization
```sql
-- Optimize PostgreSQL configuration
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
SELECT pg_reload_conf();
```

## Troubleshooting

### 1. Common Issues

**Database Connection Errors**:
```bash
# Check database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U postgres -d chaostown -c "SELECT 1;"
```

**Ollama Model Issues**:
```bash
# Check available models
docker-compose exec ollama ollama list

# Re-pull model
docker-compose exec ollama ollama pull llama3.1
```

**High CPU Usage**:
```bash
# Check resource usage
docker stats

# Scale down agents
curl -X POST http://localhost:8000/simulation/scale -d '{"max_agents": 500}'
```

### 2. Emergency Procedures

**Cat Happiness Crisis**:
```bash
# Emergency cat media upload
curl -F type=image -F file=@emergency_cat.jpg http://localhost:8000/media

# Check happiness status
curl http://localhost:8000/metrics | grep happiness
```

**Resource Exhaustion**:
```bash
# Emergency population reduction
curl -X POST http://localhost:8000/simulation/emergency-reduce

# Check system resources
docker system df
```

## Maintenance Schedule

### Daily Tasks
- Monitor cat happiness levels
- Check backup completion
- Review error logs
- Verify disk space

### Weekly Tasks
- Update security patches
- Review performance metrics
- Clean up old logs
- Test backup restoration

### Monthly Tasks
- Update Docker images
- Review scaling needs
- Performance optimization
- Security audit

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database initialized
- [ ] Ollama models downloaded
- [ ] Backup system tested
- [ ] Monitoring dashboards configured
- [ ] Security measures implemented
- [ ] Health checks passing
- [ ] Cat happiness baseline established
- [ ] Emergency procedures documented

*Remember: The deployment is only successful when Fluffhead and Wilson achieve sustained happiness levels above 0.8. All technical metrics are secondary to feline contentment.*

**Deploy with confidence, monitor with vigilance, maintain with love.** 🐱🚀