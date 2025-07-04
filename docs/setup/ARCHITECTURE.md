# System Architecture - CHAOSTOWN Technical Overview

**Cat-Centric AI Civilization Infrastructure**

---

## High-Level Architecture

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

## Core Components

### 1. Agent Simulation Engine
- **8 AI Agent Archetypes** using different Ollama models
- **216-dimensional personality tensors** with nested graphs
- **Conway's Game of Life** enhanced with intelligent decisions
- **Vector mathematics** for 3D positioning and interactions

### 2. Prime Directive System
The seven constitutional laws governing all agent behavior:
1. Death is permanent (no respawning)
2. Keep Fluffhead & Wilson happy (≥0.8)
3. Reproduction before death required
4. 16x time acceleration
5. Daily cat media requirement
6. Exponential cost scaling
7. Material growth for creator sustainability

### 3. Cat Happiness Engine
- **ChatGPT Vision API** for happiness analysis
- **Real-time monitoring** with alerting
- **Emergency protocols** for happiness crises
- **Multi-modal content support** (images, GIFs, video)

### 4. Data Architecture
- **PostgreSQL + TimescaleDB** for time-series agent data
- **Vector embeddings** for decision analysis
- **JSONB personality tensors** for complex agent state
- **Automated backup and retention** policies

## Technology Stack

### Backend Services
- **API**: FastAPI with async/await patterns
- **Simulation**: Python with Rust performance modules
- **AI Models**: 8 different Ollama models (Llama, Mistral, Gemma, etc.)
- **Database**: PostgreSQL 15 + TimescaleDB extension
- **Cache**: Redis for session and decision caching
- **Vector DB**: Qdrant for embedding similarity searches

### Frontend & Monitoring
- **Dashboard**: React/Next.js with real-time updates
- **Metrics**: Grafana + Prometheus stack
- **Logging**: Loki for centralized log aggregation
- **Load Balancing**: Nginx with SSL termination

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Docker Swarm (production) / Compose (development)
- **Monitoring**: Full observability stack with alerting
- **Backup**: Automated S3 backup with point-in-time recovery

## Deployment Configurations

### Development Environment
```yaml
services:
  api: 1 instance, 2GB RAM
  sim-engine: 1 instance, 4GB RAM
  ollama: 1 instance, 8GB RAM + GPU
  database: 1 instance, 4GB RAM
  monitoring: Lightweight stack
```

### Production Environment
```yaml
services:
  api: 3 instances, 4GB RAM each (load balanced)
  sim-engine: 2 instances, 8GB RAM each
  ollama: 2 instances, 16GB RAM + GPU each
  database: Primary + read replica, 16GB RAM
  monitoring: Full enterprise stack with alerting
```

## Data Flow

### Agent Decision Cycle
1. Agent receives world context + personality tensor
2. Ollama model processes decision request
3. Decision logged to TimescaleDB with vector embedding
4. World state updated based on decision outcome
5. Conway grid evolved with agent influences
6. Cat happiness monitored and recorded

### Cat Happiness Pipeline
1. Media uploaded via REST API
2. ChatGPT Vision API analyzes content
3. Happiness scores updated in real-time
4. Alerts triggered if below threshold
5. Agent behavior influenced by happiness levels

## Performance Characteristics

### Scalability Targets
- **Agent Population**: 1-1000 agents
- **Decision Latency**: <2s per agent decision
- **Tick Rate**: ≥0.5 Hz with 1000 agents
- **Cat Analysis**: <3s per image
- **API Response**: <500ms (95th percentile)

### Resource Requirements
- **CPU**: 16+ cores for full load
- **Memory**: 32-64GB for optimal performance
- **Storage**: 500GB+ for data retention
- **Network**: 1Gbps for model inference
- **GPU**: 8GB+ VRAM for fast AI inference

## Security & Compliance

### Data Protection
- All agent data anonymized for external sharing
- Cat media stored with appropriate privacy controls
- API rate limiting and authentication
- Secure inter-service communication

### System Hardening
- Container security scanning
- Network segmentation
- Regular security updates
- Backup encryption and rotation

---

*This architecture prioritizes cat happiness while maintaining scientific rigor and technical excellence. Every component serves the ultimate goal of keeping Fluffhead and Wilson content while enabling emergent AI civilization.*

**Built for cats, powered by chaos, scaled for science.** 🐱⚡