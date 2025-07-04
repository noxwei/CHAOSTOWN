# QUICKSTART - Get CHAOSTOWN Running in 10 Minutes

**Zero to Cat-Centric AI Civilization in 10 Minutes**

---

## Prerequisites Check

Before you begin, ensure you have:
- [ ] Docker & docker-compose ≥ v2.20
- [ ] 16+ GB RAM (32 GB recommended)
- [ ] 500+ GB free disk space
- [ ] NVIDIA GPU (optional but recommended)
- [ ] At least 3 cat photos ready 🐱

## 🚀 Quick Start Sequence

### Step 1: Clone & Setup (2 minutes)
```bash
# Clone the repository
git clone https://github.com/your-org/chaostown.git
cd chaostown

# Copy environment file
cp .env.example .env

# Edit critical settings (optional for quick start)
nano .env  # Set OPENAI_API_KEY if you have one
```

### Step 2: Boot the System (5 minutes)
```bash
# Start all services (this will download ~3GB of AI models)
docker compose up -d

# Wait for services to initialize
echo "⏳ Waiting for CHAOSTOWN to boot..."
sleep 30

# Check if everything is running
docker compose ps
```

### Step 3: Essential Cat Upload (1 minute)
```bash
# CRITICAL: Upload cat media to establish happiness baseline
curl -F type=image -F file=@your_cat_photo.jpg http://localhost:8000/media

# Verify cat happiness
curl -s http://localhost:8000/cats/happiness | jq '.combined_happiness'
# Should be ≥ 0.8 for safe operation
```

### Step 4: Start the Simulation (30 seconds)
```bash
# Initialize agent population
curl -X POST http://localhost:8000/agents/initialize

# Start the simulation
curl -X POST http://localhost:8000/simulation/start

# Check status
curl -s http://localhost:8000/simulation/status | jq
```

### Step 5: Access Dashboards (30 seconds)
```bash
# Open dashboards
open http://localhost:3000    # Main dashboard
open http://localhost:3000/grafana  # Metrics (admin/admin)
```

## ✅ Verification Checklist

Run this health check to ensure everything is working:
```bash
#!/bin/bash
echo "🔍 CHAOSTOWN Health Check"
echo "========================"

# 1. Services running
echo "Services status:"
docker compose ps --format "table {{.Name}}\t{{.Status}}"

# 2. Cat happiness (CRITICAL)
HAPPINESS=$(curl -s http://localhost:8000/cats/happiness 2>/dev/null | jq -r '.combined_happiness // "ERROR"')
echo "Cat happiness: $HAPPINESS"
if [[ "$HAPPINESS" == "ERROR" ]] || (( $(echo "$HAPPINESS < 0.8" | bc -l 2>/dev/null || echo 1) )); then
    echo "❌ CRITICAL: Cat happiness issue!"
else
    echo "✅ Cats are happy"
fi

# 3. Agent population
AGENTS=$(curl -s http://localhost:8000/agents/count 2>/dev/null || echo "ERROR")
echo "Active agents: $AGENTS"

# 4. Simulation running
SIM_STATUS=$(curl -s http://localhost:8000/simulation/status 2>/dev/null | jq -r '.running // "ERROR"')
echo "Simulation running: $SIM_STATUS"

echo "========================"
if [[ "$HAPPINESS" != "ERROR" ]] && (( $(echo "$HAPPINESS >= 0.8" | bc -l) )) && [[ "$SIM_STATUS" == "true" ]]; then
    echo "🎉 CHAOSTOWN is operational!"
    echo "Dashboard: http://localhost:3000"
else
    echo "⚠️  Issues detected - see troubleshooting below"
fi
```

## 🚨 Common Issues & Quick Fixes

### "Services won't start"
```bash
# Check Docker resources
docker system df
docker system prune -f  # Free up space if needed

# Restart with fresh containers
docker compose down
docker compose up -d --force-recreate
```

### "Cat happiness is low/ERROR"
```bash
# Upload emergency cat content
curl -F type=image -F file=@emergency_cat.jpg http://localhost:8000/media

# Check API is responding
curl http://localhost:8000/health
```

### "No agents/simulation not starting"
```bash
# Check if Ollama models downloaded
docker compose exec ollama ollama list

# Manually pull core models
docker compose exec ollama ollama pull llama3.1
docker compose exec ollama ollama pull mistral

# Restart simulation engine
docker compose restart sim-engine
```

### "Dashboard not loading"
```bash
# Check if ports are available
lsof -i :3000 -i :8000

# Restart frontend services
docker compose restart dashboard api
```

## 📚 What's Next?

Once you have CHAOSTOWN running:

1. **Daily Operations**: See `docs/operations/DAILY_CHECKIN.md`
2. **Understanding the System**: Read `docs/setup/ARCHITECTURE.md`
3. **Advanced Configuration**: Check `docs/setup/DEPLOYMENT.md`
4. **Research & Experiments**: Explore `docs/research/EXPERIMENT_DESIGN.md`

## 🆘 Emergency Contacts

- **Critical Issues**: Check `docs/operations/RUNBOOK.md`
- **Cat Happiness Crisis**: Run `./scripts/emergency_cat_protocol.sh`
- **System Recovery**: See `docs/operations/DISASTER_RECOVERY.md`

---

**Remember**: The system is only truly operational when cat happiness ≥ 0.8. Everything else is secondary.

*May Fluffhead and Wilson guide your digital civilization to prosperity!* 🐱👑