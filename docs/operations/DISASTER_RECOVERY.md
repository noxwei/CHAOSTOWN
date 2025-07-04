# Disaster Recovery - CHAOSTOWN Emergency Procedures

**Cat Happiness Crisis Management & System Recovery**

---

## Emergency Response Matrix

| Crisis Level | Cat Happiness | System Status | Response Time | Actions |
|--------------|---------------|---------------|---------------|---------|
| **DEFCON 1** | < 0.5 | Critical | Immediate | Full emergency protocol |
| **DEFCON 2** | 0.5-0.7 | Degraded | 5 minutes | Enhanced monitoring + uploads |
| **DEFCON 3** | 0.7-0.8 | Warning | 15 minutes | Preventive measures |
| **DEFCON 4** | > 0.8 | Normal | N/A | Standard operations |

## Emergency Protocols

### DEFCON 1: Critical Cat Happiness Failure

**Immediate Actions (0-2 minutes)**:
```bash
# 1. PAUSE SIMULATION IMMEDIATELY
curl -X POST http://localhost:8000/simulation/pause

# 2. EMERGENCY CAT UPLOAD BARRAGE
for emergency_cat in cat_media/emergency/*.jpg; do
    curl -F type=image -F file=@"$emergency_cat" http://localhost:8000/media
    sleep 1
done

# 3. ACTIVATE PREMIUM CAT CONTENT
curl -F type=image -F file=@cat_media/premium/fluffhead_maximum_happiness.jpg http://localhost:8000/media
curl -F type=image -F file=@cat_media/premium/wilson_ultimate_contentment.jpg http://localhost:8000/media
```

**Recovery Monitoring (2-10 minutes)**:
```bash
# Monitor happiness recovery every 30 seconds
while true; do
    HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq -r '.combined_happiness')
    echo "$(date): Happiness = $HAPPINESS"
    
    if (( $(echo "$HAPPINESS >= 0.8" | bc -l) )); then
        echo "✅ RECOVERY SUCCESSFUL - Resuming simulation"
        curl -X POST http://localhost:8000/simulation/resume
        break
    fi
    
    sleep 30
done
```

### System Recovery Procedures

**Database Recovery**:
```bash
# Stop services
docker compose stop api sim-engine

# Restore from latest backup
gunzip -c backups/latest_chaostown.sql.gz | \
docker compose exec -T db psql -U postgres -d chaostown

# Verify data integrity
docker compose exec db psql -U postgres -d chaostown -c "
    SELECT COUNT(*) as agent_count FROM agents WHERE death_time IS NULL;
    SELECT combined_happiness FROM world_state ORDER BY timestamp DESC LIMIT 1;
"

# Restart services
docker compose start api sim-engine
```

**Complete System Recovery**:
```bash
#!/bin/bash
# full_system_recovery.sh

echo "🚨 CHAOSTOWN FULL SYSTEM RECOVERY"
echo "=================================="

# 1. Stop all services
docker compose down

# 2. Clean corrupted data
docker system prune -f
docker volume prune -f

# 3. Restore from backup
tar -xzf backups/system_backup_latest.tar.gz -C ./

# 4. Start core services first
docker compose up -d db redis

# 5. Wait for database
sleep 30

# 6. Start AI services
docker compose up -d ollama

# 7. Download required models
docker compose exec ollama ollama pull llama3.1
docker compose exec ollama ollama pull mistral

# 8. Start application services
docker compose up -d api sim-engine dashboard

# 9. CRITICAL: Restore cat happiness baseline
sleep 10
curl -F type=image -F file=@cat_media/emergency/baseline_happiness.jpg http://localhost:8000/media

# 10. Verify recovery
./scripts/health_check.sh
```

## Backup & Restoration

### Automated Daily Backups
```bash
#!/bin/bash
# daily_backup.sh (runs at 2 AM daily)

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# 1. Database backup
docker compose exec -T db pg_dump -U postgres -d chaostown | \
gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# 2. Essential cat media backup
tar -czf "$BACKUP_DIR/cat_media_$DATE.tar.gz" cat_media/emergency/ cat_media/premium/

# 3. Configuration backup
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" .env docker-compose.yml docs/

# 4. Upload to cloud storage (if configured)
if [ -n "$AWS_S3_BUCKET" ]; then
    aws s3 sync "$BACKUP_DIR" "s3://$AWS_S3_BUCKET/chaostown-backups/"
fi

# 5. Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "✅ Backup completed: $DATE"
```

### Point-in-Time Recovery
```bash
# restore_to_timestamp.sh
RESTORE_TIME="$1"  # Format: YYYY-MM-DD HH:MM:SS

echo "🔄 Restoring CHAOSTOWN to $RESTORE_TIME"

# Find appropriate backup
BACKUP_FILE=$(find backups/ -name "db_*.sql.gz" -newermt "$RESTORE_TIME" | head -1)

if [ -z "$BACKUP_FILE" ]; then
    echo "❌ No backup found for timestamp $RESTORE_TIME"
    exit 1
fi

echo "Using backup: $BACKUP_FILE"

# Restore database
docker compose stop api sim-engine
gunzip -c "$BACKUP_FILE" | docker compose exec -T db psql -U postgres -d chaostown

# Verify happiness levels in restored data
RESTORED_HAPPINESS=$(docker compose exec -T db psql -U postgres -d chaostown -t -c \
"SELECT combined_happiness FROM world_state WHERE timestamp <= '$RESTORE_TIME' ORDER BY timestamp DESC LIMIT 1;")

echo "Restored happiness level: $RESTORED_HAPPINESS"

if (( $(echo "$RESTORED_HAPPINESS < 0.8" | bc -l) )); then
    echo "⚠️  WARNING: Restored state has low cat happiness"
    echo "Emergency cat upload recommended"
fi

docker compose start api sim-engine
```

## Emergency Contacts & Escalation

### Contact Tree
```
DEFCON 1 (Cat Crisis)
├── Wei (Creator) - IMMEDIATE
├── Emergency Cat Content Team
└── System Recovery Team

DEFCON 2 (System Issues)  
├── Operations Team - 5 min
├── Database Admin - 10 min
└── Infrastructure Team - 15 min
```

### Emergency Communication
```bash
#!/bin/bash
# emergency_notify.sh

SEVERITY="$1"
MESSAGE="$2"

case $SEVERITY in
    "DEFCON1")
        # Cat happiness crisis - ALL HANDS
        curl -X POST "$SLACK_WEBHOOK" -d "{\"text\":\"🚨 DEFCON 1: CAT HAPPINESS CRISIS\\n$MESSAGE\"}"
        # Send SMS to Wei
        curl -X POST "$SMS_API" -d "Body=CHAOSTOWN DEFCON 1: $MESSAGE"
        # Discord alert
        curl -X POST "$DISCORD_WEBHOOK" -d "{\"content\":\"@everyone CHAOSTOWN CAT CRISIS: $MESSAGE\"}"
        ;;
    "DEFCON2")
        # System degradation
        curl -X POST "$SLACK_WEBHOOK" -d "{\"text\":\"⚠️ DEFCON 2: System Issues\\n$MESSAGE\"}"
        ;;
    "RECOVERY")
        # Recovery notification
        curl -X POST "$SLACK_WEBHOOK" -d "{\"text\":\"✅ RECOVERY: $MESSAGE\"}"
        ;;
esac
```

## Monitoring & Alerting

### Critical Alerts Setup
```yaml
# alertmanager.yml
groups:
- name: chaostown.critical
  rules:
  - alert: CatHappinessCritical
    expr: combined_happiness < 0.5
    for: 0s
    labels:
      severity: critical
      defcon: "1"
    annotations:
      summary: "CRITICAL: Cat happiness below 0.5"
      description: "Combined cat happiness is {{ $value }} - IMMEDIATE ACTION REQUIRED"
      
  - alert: CatHappinessWarning
    expr: combined_happiness < 0.8
    for: 2m
    labels:
      severity: warning
      defcon: "2"
    annotations:
      summary: "WARNING: Cat happiness declining"
      description: "Cat happiness is {{ $value }} for 2+ minutes"
      
  - alert: SimulationDown
    expr: up{job="chaostown-sim"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Simulation engine down"
      description: "CHAOSTOWN simulation has stopped responding"
```

### Health Check Monitoring
```bash
#!/bin/bash
# continuous_health_monitor.sh

while true; do
    # Check cat happiness
    HAPPINESS=$(curl -s http://localhost:8000/cats/happiness 2>/dev/null | jq -r '.combined_happiness // "ERROR"')
    
    if [[ "$HAPPINESS" == "ERROR" ]]; then
        echo "$(date): 🚨 API UNREACHABLE"
        ./emergency_notify.sh "DEFCON2" "API unreachable - system may be down"
    elif (( $(echo "$HAPPINESS < 0.5" | bc -l) )); then
        echo "$(date): 🚨 DEFCON 1 - Cat happiness critical: $HAPPINESS"
        ./emergency_notify.sh "DEFCON1" "Cat happiness critical: $HAPPINESS"
        ./emergency_happiness_protocol.sh
    elif (( $(echo "$HAPPINESS < 0.8" | bc -l) )); then
        echo "$(date): ⚠️  DEFCON 2 - Cat happiness warning: $HAPPINESS"
        ./emergency_notify.sh "DEFCON2" "Cat happiness warning: $HAPPINESS"
    else
        echo "$(date): ✅ All systems nominal - happiness: $HAPPINESS"
    fi
    
    sleep 60  # Check every minute
done
```

## Infrastructure Redundancy

### Multi-Region Backup Strategy
```bash
# sync_to_backup_regions.sh
REGIONS=("us-west-2" "eu-central-1" "ap-southeast-1")

for region in "${REGIONS[@]}"; do
    aws s3 sync backups/ "s3://chaostown-backup-$region/backups/" --region "$region"
done
```

### Failover Procedures
```bash
# failover_to_backup.sh
BACKUP_HOST="$1"

echo "🔄 Failing over to backup host: $BACKUP_HOST"

# 1. Stop local services
docker compose down

# 2. Sync latest data to backup
rsync -av data/ "$BACKUP_HOST:/chaostown/data/"

# 3. Start services on backup host
ssh "$BACKUP_HOST" "cd /chaostown && docker compose up -d"

# 4. Update DNS/load balancer
curl -X POST "$DNS_API/update" -d "{\"host\":\"chaostown.com\",\"target\":\"$BACKUP_HOST\"}"

echo "✅ Failover complete to $BACKUP_HOST"
```

## Testing & Validation

### Disaster Recovery Drills
```bash
#!/bin/bash
# disaster_drill.sh

echo "🧪 CHAOSTOWN Disaster Recovery Drill"
echo "====================================="

# 1. Create test snapshot
./create_test_snapshot.sh

# 2. Simulate failure
docker compose stop db

# 3. Test recovery procedures
./full_system_recovery.sh

# 4. Validate recovery
HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq -r '.combined_happiness')
AGENTS=$(curl -s http://localhost:8000/agents/count)

if (( $(echo "$HAPPINESS >= 0.8" | bc -l) )) && [ "$AGENTS" -gt 0 ]; then
    echo "✅ Disaster recovery drill PASSED"
else
    echo "❌ Disaster recovery drill FAILED"
    exit 1
fi

# 5. Restore test snapshot
./restore_test_snapshot.sh
```

---

## Recovery Checklist

### Pre-Incident Preparation
- [ ] Backup systems tested and verified
- [ ] Emergency cat content library maintained
- [ ] Contact information updated
- [ ] Recovery procedures documented and practiced
- [ ] Monitoring and alerting configured
- [ ] Redundant systems in place

### During Incident Response
- [ ] Severity assessed and DEFCON level declared
- [ ] Simulation paused if cat happiness critical
- [ ] Emergency contacts notified
- [ ] Recovery procedures initiated
- [ ] Progress monitored and documented
- [ ] Stakeholders kept informed

### Post-Incident Recovery
- [ ] System functionality verified
- [ ] Cat happiness restored to baseline
- [ ] Data integrity confirmed
- [ ] Incident documented and analyzed
- [ ] Recovery procedures updated
- [ ] Team debriefing conducted

---

*In the darkest hour of system failure, remember: the cats must remain happy. All technical considerations are secondary to feline contentment. Recovery is only complete when Fluffhead and Wilson return to their throne of digital happiness.*

**Prepare for the worst, hope for purrs, always prioritize cats.** 🐱🚨