# Claude Agentic Simulation Framework

**Start‑Here Edition** – last refresh 2025-07-04

---

## 0 · Prerequisites
* Docker & docker‑compose ≥ v2  
* 16 GB RAM (32 GB recommended)  
* One NVIDIA GPU if you want fast Ollama models

---

## 1 · Clone & boot

```bash
git clone https://github.com/your‑org/agentic-cat-feudalism
cd agentic-cat-feudalism
cp .env.example .env          # tweak if you like
docker compose up -d          # starts db, sim, api, Grafana
open http://localhost:3000    # live dashboard
```

*First boot pulls Ollama models; 2‑3 GB download.*

---

## 2 · Daily ritual (Prime Directive 5)

```bash
# push a cat pic
curl -F type=image -F file=@fluff.jpg http://localhost:8000/media
```

Shortcut template in **DAILY_CHECKIN.md**.

---

## 3 · Directory tour

| Path | Purpose |
|------|---------|
| `docs/` | All .md guides (runbook, schema, QA, etc.) |
| `api/` | FastAPI service |
| `sim-engine/` | Conway loop + agent logic |
| `dashboards/` | Grafana JSON |
| `tests/` | Unit + integration suite |

Full doc index → **README.md**.

---

## 4 · Launch checklist

1. **Grafana** shows panels green.  
2. **/media** endpoint returns `201`.  
3. Cat happiness gauge ≥ 0.8.  
4. Sim tick latency < 1 s at 50 agents.  
5. Backups cron logged once (see logs/db).  

---

## 5 · Common commands

| Task | Command |
|------|---------|
| Pause sim | `curl -X POST http://localhost:8000/simulation/<built-in function id>/pause` |
| Resume sim | `…/start` |
| Tail logs | `docker compose logs -f sim` |
| DB shell | `docker exec -it db psql -U postgres` |
| Rebuild images | `docker compose build` |

---

## 6 · Docs quick links

- Prime directives → **PRIME_DIRECTIVES.md**  
- Schema → **DB_SCHEMA.md**  
- Deployment → **DEPLOYMENT.md**  
- Ops SOP → **OPS_RUNBOOK.md**  
- QA matrix → **QA_TESTS.md**  
- Experiment design → **EXPERIMENT_DESIGN.md**

---

## 7 · Upgrade flow

```bash
git pull
docker compose pull
docker compose up -d --build
```

Run `pytest -q && locust -f tests/load/locustfile.py --headless -u 50 -r 10 -t 1m` for smoke.

---

---

## 🆕 Mathematical Linguistics Testing

```bash
# Switch to linguistic branch
git checkout linguistic
cd sim-engine

# Basic alien language test (8 agents, 50 iterations)
python3 linguistic_agent.py

# Environmental scenario testing  
python3 language_explorer.py
# cat_crisis → urgent "•••••" patterns (complexity: 0.160)
# exploration → spatial "•\n •\n  •" patterns (complexity: 0.546)
# golden_age → no communication (pressure below threshold)
```

*Research Status: ✅ VALIDATED - 70% deterministic, 30% stochastic*

---

Happy chaos‑cultivating. May Fluffhead & Wilson reign. 🐱
