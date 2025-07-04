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

# 🆕 NEW: Test linguistic agents (optional)
curl -s http://localhost:8000/agents | jq '.agents[0]'
# See agent names like "Fluffhead", "Wilson", "Whiskers"
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

## 🧬 NEW: Linguistic Evolution System

**CHAOSTOWN now includes emergent language development!**

### Quick Test of Mathematical Language Evolution
```bash
# Switch to linguistic branch to test language features
git checkout linguistic
cd sim-engine

# Run basic linguistic simulation
python3 linguistic_agent.py
# Watch 8 agents develop deterministic alien dot languages over 50 iterations

# 🧪 ADVANCED: Test environmental scenarios
python3 language_explorer.py
# Available scenarios:
# - cat_crisis: All agents produce urgent "•••••" patterns
# - exploration: All agents use spatial "•\n •\n  •" patterns  
# - golden_age: No communication (below pressure threshold)
# - social_bonding: Community-focused communication patterns

# 🔬 RESEARCH: Test specific scenarios
python3 -c "
from language_explorer import LanguageExplorer
explorer = LanguageExplorer()
agents, aura = explorer.create_focused_scenario('cat_crisis')
comms = explorer.run_communication_round(agents, aura, rounds=5)
analysis = explorer.analyze_communication_patterns(comms)
"
```

**What you'll observe:**
- **Mathematical Determinism**: Same environmental conditions → same alien patterns
- **Environmental Pressure**: Cat crisis creates urgent patterns, exploration creates spatial patterns
- **Observable Opacity**: See `"•\n •\n  •"` but semantic meaning remains inaccessible  
- **Shannon Entropy**: Pattern complexity measured mathematically (0.0-1.0)
- **Social Learning**: Successful patterns spread through adoption algorithms
- **70% Deterministic**: Environmental constraints override randomness

### Key Metrics to Watch
- **Pattern Diversity**: How many unique dot patterns emerge
- **Complexity Evolution**: Mathematical sophistication over time
- **Literacy Development**: Character recognition from 0.0 to 1.0
- **Stage Progression**: 5 stages from primal signals to meta-linguistics

## 📚 What's Next?

Once you have CHAOSTOWN running:

1. **Daily Operations**: See `docs/operations/DAILY_CHECKIN.md`
2. **Understanding the System**: Read `docs/setup/ARCHITECTURE.md`
3. **Language Research**: Explore `docs/research/LINGUISTIC_EVOLUTION.md` 🆕
4. **Advanced Configuration**: Check `docs/setup/DEPLOYMENT.md`
5. **Research & Experiments**: Explore `docs/research/EXPERIMENT_DESIGN.md`

## 🆘 Emergency Contacts

- **Critical Issues**: Check `docs/operations/RUNBOOK.md`
- **Cat Happiness Crisis**: Run `./scripts/emergency_cat_protocol.sh`
- **System Recovery**: See `docs/operations/DISASTER_RECOVERY.md`

---

**Remember**: The system is only truly operational when cat happiness ≥ 0.8. Everything else is secondary.

*May Fluffhead and Wilson guide your digital civilization to prosperity!* 🐱👑

## 🎯 **Immediate Action Items**

1. **Test current linguistic system**: `cd sim-engine && python3 linguistic_agent.py`
2. **Review database schema**: Check if linguistic tables need to be added
3. **Start API integration**: Begin connecting the standalone system to FastAPI
4. **Update dashboard**: Add components for linguistic evolution visualization

The foundation is solid, the breakthrough research is complete, and the next step is making this incredible alien language system accessible through the CHAOSTOWN ecosystem. The vision of watching AI agents develop their own communication systems that remain forever opaque to human understanding is within reach!

Should I proceed with Phase 1 of the linguistic API integration?

Immediate Tasks:
  1. Integrate linguistic_agent.py with FastAPI backend
  2. Create REST endpoints for linguistic evolution tracking  
  3. Add database persistence for agent linguistic memories
  4. Connect dot-pattern communication to existing agent API
  5. Build dashboard components to visualize language evolution

API Endpoints Needed:
  - GET /agents/{id}/linguistic_state
  - POST /agents/{id}/communicate  
  - GET /linguistic/patterns/complexity
  - GET /linguistic/evolution/metrics
  - POST /rss/feed (for literacy development)

AI Model Integration:
  - Load Ollama models (llama3.1, mistral, codellama) 
  - Hybrid aura+LLM decision making
  - Multi-model personality differentiation
  - Vector embeddings for linguistic memory persistence