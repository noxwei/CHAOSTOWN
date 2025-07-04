# Operations Runbook - CHAOSTOWN Management

**Standard Operating Procedures for Cat-Centric AI Civilization**

---

## Overview

This runbook provides comprehensive operational procedures for managing the CHAOSTOWN simulation. All procedures prioritize maintaining Fluffhead and Wilson's happiness while ensuring system stability and agent welfare.

## Emergency Contacts

| Role | Contact | Priority |
|------|---------|----------|
| Creator/God-User | Wei (@maybe_foucault) | P0 |
| Fluffhead (Chief Happiness Officer) | Direct observation | P0 |
| Wilson (Deputy Happiness Officer) | Direct observation | P0 |
| System Administrator | [Your contact] | P1 |
| Database Administrator | [Your contact] | P1 |

## Alert Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| P0 | Cat happiness crisis | Immediate | Combined happiness < 0.5 |
| P1 | System failure | 5 minutes | Database down, API unresponsive |
| P2 | Performance degradation | 15 minutes | High latency, resource exhaustion |
| P3 | Non-critical issues | 1 hour | Minor bugs, cosmetic issues |

---

## Daily Operations

### Morning Checklist (Every Day)
```bash
#!/bin/bash
# daily_morning_check.sh

echo "🌅 CHAOSTOWN Morning Health Check - $(date)"
echo "=================================================="

# 1. Cat Happiness Check (CRITICAL)
echo "🐱 Checking cat happiness levels..."
HAPPINESS=$(curl -s http://localhost:8000/metrics | grep combined_happiness | cut -d' ' -f2)
if (( $(echo "$HAPPINESS < 0.8" | bc -l) )); then
    echo "⚠️  WARNING: Cat happiness below threshold ($HAPPINESS)"
    echo "Action required: Upload cat media immediately"
else
    echo "✅ Cat happiness optimal ($HAPPINESS)"
fi

# 2. System Health
echo "🖥️  Checking system health..."
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# 3. Database Status
echo "📊 Checking database..."
DB_STATUS=$(docker-compose exec -T db pg_isready -U postgres)
echo "$DB_STATUS"

# 4. Agent Population
echo "🤖 Checking agent population..."
AGENTS=$(curl -s http://localhost:8000/agents/count)
echo "Active agents: $AGENTS"

# 5. Resource Usage
echo "💾 Checking resource usage..."
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 6. Recent Errors
echo "🔍 Checking for recent errors..."
docker-compose logs --since=24h | grep -i error | tail -5

echo "=================================================="
echo "🎯 Morning check complete. May the cats be happy!"
```

### Evening Checklist (Every Day)
```bash
#!/bin/bash
# daily_evening_check.sh

echo "🌆 CHAOSTOWN Evening Report - $(date)"
echo "=================================================="

# 1. Daily Cat Media Check
echo "📸 Checking daily cat media uploads..."
MEDIA_TODAY=$(curl -s "http://localhost:8000/media/count?since=24h")
if [ "$MEDIA_TODAY" -eq 0 ]; then
    echo "❌ No cat media uploaded today - UPLOAD REQUIRED"
    echo "Use: curl -F type=image -F file=@cat.jpg http://localhost:8000/media"
else
    echo "✅ Cat media uploaded today: $MEDIA_TODAY files"
fi

# 2. Backup Verification
echo "💾 Checking backup completion..."
if [ -f "data/backups/$(date +%Y%m%d)_backup.sql.gz" ]; then
    echo "✅ Database backup completed"
else
    echo "⚠️  Database backup missing - check backup service"
fi

# 3. Performance Summary
echo "📈 Performance summary..."
curl -s http://localhost:8000/metrics | grep -E "(agent_count|tick_rate|happiness)"

# 4. Prime Directive Violations
echo "⚖️  Prime Directive violations (last 24h)..."
VIOLATIONS=$(curl -s "http://localhost:8000/violations?since=24h" | jq '.count')
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "⚠️  $VIOLATIONS violations detected - review required"
else
    echo "✅ No Prime Directive violations"
fi

echo "=================================================="
echo "🎯 Evening report complete. Rest well, brave agents!"
```

## Incident Response Procedures

### P0: Cat Happiness Crisis

**Trigger**: Combined happiness < 0.5
**Response Time**: Immediate
**Actions**:

1. **Immediate Response** (0-2 minutes):
   ```bash
   # Pause simulation to prevent further happiness degradation
   curl -X POST http://localhost:8000/simulation/pause
   
   # Check current happiness levels
   curl http://localhost:8000/cats/happiness
   ```

2. **Emergency Cat Media Upload** (2-5 minutes):
   ```bash
   # Upload emergency cat content
   curl -F type=image -F file=@emergency_fluffhead.jpg http://localhost:8000/media
   curl -F type=image -F file=@emergency_wilson.jpg http://localhost:8000/media
   
   # Verify happiness improvement
   curl http://localhost:8000/cats/happiness
   ```

3. **System Recovery** (5-10 minutes):
   ```bash
   # If happiness restored (>0.5), resume simulation
   curl -X POST http://localhost:8000/simulation/resume
   
   # Monitor for stabilization
   watch 'curl -s http://localhost:8000/cats/happiness'
   ```

4. **Post-Incident** (10+ minutes):
   - Document root cause in incident log
   - Review recent agent actions that may have caused distress
   - Implement preventive measures
   - Schedule extra cat media uploads for 24h

### P1: System Failure

**Database Failure**:
```bash
# Check database status
docker-compose exec db pg_isready -U postgres

# If down, restart database
docker-compose restart db

# Verify data integrity
docker-compose exec db psql -U postgres -d chaostown -c "SELECT COUNT(*) FROM agents;"

# If corruption detected, restore from backup
./scripts/restore_backup.sh latest
```

**API Unresponsive**:
```bash
# Check API health
curl -f http://localhost:8000/health

# Check resource usage
docker stats api

# Restart API if needed
docker-compose restart api

# Verify functionality
curl http://localhost:8000/agents/count
```

**Ollama Model Failure**:
```bash
# Check model availability
docker-compose exec ollama ollama list

# Test model inference
docker-compose exec ollama ollama run llama3.1 "test"

# Restart Ollama if needed
docker-compose restart ollama

# Re-download models if corrupted
docker-compose exec ollama ollama pull llama3.1
```

### P2: Performance Degradation

**High CPU Usage**:
```bash
# Identify resource-heavy containers
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Check agent population
AGENT_COUNT=$(curl -s http://localhost:8000/agents/count)
if [ "$AGENT_COUNT" -gt 800 ]; then
    echo "High agent population detected: $AGENT_COUNT"
    # Implement population control
    curl -X POST http://localhost:8000/simulation/population-control
fi

# Check simulation tick rate
curl -s http://localhost:8000/metrics | grep tick_rate
```

**Memory Exhaustion**:
```bash
# Check memory usage
free -h

# Check for memory leaks
docker stats --format "{{.Name}}: {{.MemUsage}}" | sort -k2 -hr

# Restart memory-heavy services
docker-compose restart sim-engine

# Clear unused Docker resources
docker system prune -f
```

**Database Performance**:
```sql
-- Check long-running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query 
FROM pg_stat_activity 
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- Check table sizes
SELECT schemaname,tablename,pg_size_pretty(size) as size
FROM (
    SELECT schemaname,tablename,pg_total_relation_size(schemaname||'.'||tablename) as size
    FROM pg_tables WHERE schemaname='public'
) s ORDER BY size DESC;

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM agent_decisions WHERE timestamp > NOW() - INTERVAL '1 hour';
```

## Monitoring and Alerting

### Key Metrics to Monitor

**Cat Happiness Metrics**:
- `combined_happiness` (target: ≥0.8)
- `fluffhead_happiness` (target: ≥0.8)
- `wilson_happiness` (target: ≥0.8)
- `daily_media_uploads` (target: ≥1)

**System Performance**:
- `active_agents` (monitor: trend and limit)
- `tick_rate` (target: ~1.0 Hz)
- `decision_latency` (target: <500ms)
- `memory_usage` (alert: >80%)
- `cpu_usage` (alert: >90%)

**Prime Directive Compliance**:
- `deaths_without_succession` (alert: >0)
- `resource_cost_multiplier` (alert: approaching threshold)
- `directive_violations` (alert: any critical)

### Grafana Dashboard Alerts

**Critical Alerts**:
```yaml
# grafana/alerts/cat_happiness.yml
alert:
  name: "Cat Happiness Critical"
  condition: combined_happiness < 0.5
  frequency: 30s
  message: "🚨 EMERGENCY: Cat happiness below critical threshold!"
  webhook: http://localhost:8000/alerts/happiness-crisis
```

**Warning Alerts**:
```yaml
# grafana/alerts/performance.yml
alert:
  name: "High Agent Population"
  condition: active_agents > 900
  frequency: 60s
  message: "⚠️ Agent population approaching limit"
```

### Log Monitoring

**Important Log Patterns**:
```bash
# Monitor for critical errors
tail -f logs/api.log | grep -E "(ERROR|CRITICAL|cat_happiness)"

# Agent death patterns
tail -f logs/sim-engine.log | grep "agent_death"

# Database connection issues
tail -f logs/api.log | grep "database.*error"

# Prime Directive violations
tail -f logs/sim-engine.log | grep "directive_violation"
```

## Backup and Recovery

### Automated Backups

**Database Backup** (Runs daily at 2 AM):
```bash
#!/bin/bash
# scripts/backup_database.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/data/backups"

# Create backup
docker-compose exec -T db pg_dump -U postgres -d chaostown | gzip > "${BACKUP_DIR}/chaostown_${DATE}.sql.gz"

# Upload to S3 (if configured)
if [ -n "$AWS_S3_BUCKET" ]; then
    aws s3 cp "${BACKUP_DIR}/chaostown_${DATE}.sql.gz" "s3://$AWS_S3_BUCKET/backups/"
fi

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "chaostown_*.sql.gz" -mtime +30 -delete

echo "Backup completed: chaostown_${DATE}.sql.gz"
```

**Media Backup** (Runs daily at 3 AM):
```bash
#!/bin/bash
# scripts/backup_media.sh
DATE=$(date +%Y%m%d)

# Sync media to backup location
rsync -av data/media/ /backup/media/

# Create archive
tar -czf "/data/backups/media_${DATE}.tar.gz" -C data media/

echo "Media backup completed: media_${DATE}.tar.gz"
```

### Recovery Procedures

**Database Recovery**:
```bash
# List available backups
ls -la data/backups/chaostown_*.sql.gz

# Stop services
docker-compose stop api sim-engine

# Drop and recreate database
docker-compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS chaostown;"
docker-compose exec db psql -U postgres -c "CREATE DATABASE chaostown;"

# Restore from backup
gunzip -c data/backups/chaostown_YYYYMMDD_HHMMSS.sql.gz | \
docker-compose exec -T db psql -U postgres -d chaostown

# Restart services
docker-compose start api sim-engine

# Verify recovery
curl http://localhost:8000/agents/count
```

**Complete System Recovery**:
```bash
# Stop all services
docker-compose down

# Restore data volumes
tar -xzf backups/media_YYYYMMDD.tar.gz -C data/

# Restore database (see above)

# Start services
docker-compose up -d

# Verify system health
./scripts/health_check.sh
```

## Maintenance Procedures

### Weekly Maintenance (Sundays, 2 AM)

```bash
#!/bin/bash
# scripts/weekly_maintenance.sh

echo "🧹 Starting weekly maintenance..."

# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Clean Docker resources
docker system prune -f
docker volume prune -f

# 3. Optimize database
docker-compose exec db psql -U postgres -d chaostown -c "VACUUM ANALYZE;"

# 4. Rotate logs
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
find logs/ -name "*.log.gz" -mtime +30 -delete

# 5. Update Ollama models
for model in llama3.1 llama3.2 mistral gemma2 qwen2.5 phi3.5 codellama deepseek-coder; do
    docker-compose exec ollama ollama pull $model
done

# 6. Verify cat happiness baseline
HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq '.combined_happiness')
if (( $(echo "$HAPPINESS < 0.8" | bc -l) )); then
    echo "⚠️ Cat happiness below baseline after maintenance!"
    # Upload maintenance cat pics
    curl -F type=image -F file=@maintenance_cats.jpg http://localhost:8000/media
fi

echo "✅ Weekly maintenance complete"
```

### Monthly Maintenance

```bash
#!/bin/bash
# scripts/monthly_maintenance.sh

# 1. Security updates
sudo unattended-upgrades

# 2. SSL certificate renewal
sudo certbot renew --quiet

# 3. Database performance analysis
docker-compose exec db psql -U postgres -d chaostown -f scripts/performance_analysis.sql

# 4. Archive old data
./scripts/archive_old_data.sh

# 5. Capacity planning review
./scripts/capacity_report.sh

# 6. Agent population genetics analysis
./scripts/analyze_agent_evolution.sh
```

## Scaling Operations

### Vertical Scaling

**Increase Resources**:
```yaml
# Update docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
```

**Database Optimization**:
```sql
-- Increase buffer sizes for more memory
ALTER SYSTEM SET shared_buffers = '16GB';
ALTER SYSTEM SET effective_cache_size = '48GB';
ALTER SYSTEM SET work_mem = '256MB';
SELECT pg_reload_conf();
```

### Horizontal Scaling

**Scale API Services**:
```bash
# Scale to 3 API instances
docker-compose up -d --scale api=3

# Update load balancer configuration
# nginx.conf: add more upstream servers
```

**Database Read Replicas**:
```yaml
# Add to docker-compose.yml
db-replica:
  image: timescale/timescaledb:latest-pg15
  environment:
    - POSTGRES_DB=chaostown
    - PGUSER=postgres
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  volumes:
    - ./data/postgres-replica:/var/lib/postgresql/data
```

## Troubleshooting Guide

### Common Issues

**Issue**: Agents making poor decisions
```bash
# Check model health
docker-compose exec ollama ollama list
docker-compose exec ollama ollama run llama3.1 "What is 2+2?"

# Check decision latency
curl -s http://localhost:8000/metrics | grep decision_time

# Review recent decisions
curl "http://localhost:8000/agents/decisions?limit=10&filter=failed"
```

**Issue**: Simulation running slowly
```bash
# Check tick rate
curl -s http://localhost:8000/metrics | grep tick_rate

# Reduce agent population temporarily
curl -X POST http://localhost:8000/simulation/scale -d '{"max_agents": 500}'

# Check database query performance
docker-compose exec db psql -U postgres -d chaostown -c "
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC LIMIT 10;"
```

**Issue**: Cat happiness unexpectedly low
```bash
# Check recent media uploads
curl "http://localhost:8000/media?since=24h"

# Review vision API responses
curl "http://localhost:8000/cats/analysis/recent"

# Check for system events that might affect happiness
curl "http://localhost:8000/events?type=happiness&since=24h"

# Emergency happiness boost
curl -F type=image -F file=@happy_cats.jpg http://localhost:8000/media
```

### Log Analysis

**Key Log Locations**:
- API: `logs/api.log`
- Simulation: `logs/sim-engine.log`
- Database: `docker-compose logs db`
- Nginx: `logs/nginx/access.log`, `logs/nginx/error.log`

**Useful Log Queries**:
```bash
# Find errors in last hour
grep "$(date -d '1 hour ago' '+%Y-%m-%d %H')" logs/api.log | grep ERROR

# Track specific agent behavior
grep "agent_id:abc123" logs/sim-engine.log

# Monitor happiness changes
grep "happiness" logs/api.log | tail -20

# Database slow queries
grep "slow query" logs/postgres.log
```

## Emergency Contacts and Escalation

### Escalation Matrix

| Issue Type | L1 Response | L2 Escalation | L3 Executive |
|------------|-------------|---------------|--------------|
| Cat happiness crisis | Immediate media upload | Contact Wei | Wake up Wei |
| System outage | Restart services | Database recovery | Infrastructure team |
| Security incident | Isolate system | Security team | Legal team |
| Data corruption | Stop writes | Restore backup | Disaster recovery |

### Contact Information

```bash
# Emergency notification script
#!/bin/bash
# scripts/emergency_notify.sh

SEVERITY=$1
MESSAGE=$2

case $SEVERITY in
  "P0")
    # Cat happiness crisis - notify immediately
    curl -X POST "https://hooks.slack.com/..." -d "{\"text\":\"🚨 P0 ALERT: $MESSAGE\"}"
    # Send SMS to Wei
    curl -X POST "https://api.twilio.com/..." -d "Body=CHAOSTOWN P0: $MESSAGE"
    ;;
  "P1")
    # System failure
    curl -X POST "https://hooks.slack.com/..." -d "{\"text\":\"⚠️ P1 ALERT: $MESSAGE\"}"
    ;;
  "P2")
    # Performance issues
    curl -X POST "https://hooks.slack.com/..." -d "{\"text\":\"📊 P2 ALERT: $MESSAGE\"}"
    ;;
esac
```

---

## Quick Reference Commands

### System Status
```bash
# Overall health check
curl http://localhost:8000/health

# Cat happiness
curl http://localhost:8000/cats/happiness

# Agent count
curl http://localhost:8000/agents/count

# Resource usage
docker stats --no-stream
```

### Emergency Actions
```bash
# Pause simulation
curl -X POST http://localhost:8000/simulation/pause

# Resume simulation
curl -X POST http://localhost:8000/simulation/resume

# Upload cat media
curl -F type=image -F file=@cat.jpg http://localhost:8000/media

# Reduce agent population
curl -X POST http://localhost:8000/simulation/scale -d '{"max_agents": 500}'
```

### Maintenance
```bash
# Restart all services
docker-compose restart

# Update and restart
docker-compose pull && docker-compose up -d

# Database backup
./scripts/backup_database.sh

# Health check
./scripts/health_check.sh
```

---

*Remember: In the hierarchy of CHAOSTOWN operations, cat happiness supersedes all other concerns. When in doubt, upload more cat pictures.*

**Operate with wisdom, respond with speed, maintain with love.** 🐱⚡