# CHAOSTOWN Linguistic Evolution API Integration

**Complete FastAPI implementation of mathematical linguistic evolution system**

## Overview

This implementation provides a production-ready FastAPI integration of the CHAOSTOWN linguistic evolution system, seamlessly bridging the standalone research system with the database and providing real-time WebSocket streams for live monitoring.

## Architecture

```
api/
├── main.py                              # Enhanced main FastAPI application
├── database.py                          # PostgreSQL connection management
├── linguistic_api.py                    # Complete linguistic API endpoints
├── models/
│   └── linguistic.py                    # Pydantic models for linguistic data
├── services/
│   └── linguistic_service.py            # Business logic & complexity calculations
├── websockets/
│   └── linguistic_streams.py            # Real-time WebSocket handlers
└── requirements.txt                     # Updated dependencies
```

## Key Features

### 🧠 Mathematical Linguistic System
- **70% deterministic, 30% stochastic** language evolution
- **Shannon entropy** and spatial complexity calculations
- **5-stage linguistic development** (Primal → Meta-linguistic)
- **Semantic opacity** - internal meanings hidden from observers
- **RSS literacy acquisition** with gradual character recognition

### 🚀 Production API Endpoints

#### Agent Management
- `GET /api/linguistic/agents/{id}` - Get agent linguistic state
- `GET /api/linguistic/agents/{id}/observable` - Human-observable metrics only
- `POST /api/linguistic/agents/{id}/initialize` - Initialize linguistic capabilities
- `POST /api/linguistic/agents/{id}/communicate` - Trigger communication

#### Population Analytics
- `GET /api/linguistic/evolution/metrics` - Population-level metrics
- `GET /api/linguistic/evolution/stage-distribution` - Stage progression stats
- `GET /api/linguistic/evolution/complexity-trends` - Mathematical complexity evolution

#### Pattern Analysis
- `POST /api/linguistic/patterns/analyze` - Mathematical pattern analysis
- `GET /api/linguistic/patterns/popular` - Most-used patterns
- `GET /api/linguistic/patterns/innovations` - Recent innovations

#### RSS Processing
- `POST /api/linguistic/rss/feed` - Process RSS feeds for literacy
- `GET /api/linguistic/rss/impact` - Literacy development impact

#### System Monitoring
- `GET /api/linguistic/system/status` - System health & performance
- `GET /api/linguistic/system/health` - Diagnostic information

### 🔄 Real-time WebSocket Streams

#### Available Streams
- `ws://localhost:8000/ws/linguistic/live` - Live communications
- `ws://localhost:8000/ws/linguistic/metrics` - Population metrics
- `ws://localhost:8000/ws/linguistic/patterns` - Pattern emergence
- `ws://localhost:8000/ws/linguistic/stages` - Stage progressions
- `ws://localhost:8000/ws/linguistic/system` - System health

#### Stream Filtering
```javascript
// Connect with filters
const ws = new WebSocket('ws://localhost:8000/ws/linguistic/live?agent_filter=uuid1,uuid2&min_complexity=0.5');

// Update filters dynamically
ws.send(JSON.stringify({
    type: "update_filters",
    filters: {
        "agent_ids": ["agent-uuid"],
        "event_types": ["communication", "innovation"],
        "min_complexity": 0.3
    }
}));
```

### 🗄️ Database Integration

#### TimescaleDB Hypertables
- `communications` - All communication events (time-series)
- `linguistic_interactions` - Agent interaction events
- `rss_linguistic_influence` - RSS feed impact tracking

#### Core Tables
- `linguistic_agents` - Agent linguistic capabilities
- `dot_patterns` - Pattern registry with mathematical properties
- `language_families` - Emergent language groups

## API Usage Examples

### Initialize Agent
```bash
curl -X POST "http://localhost:8000/api/linguistic/agents/uuid/initialize" \
  -H "Content-Type: application/json" \
  -d '{
    "innovation_tendency": 0.7,
    "social_influence_susceptibility": 0.6,
    "communication_threshold": 0.5
  }'
```

### Trigger Communication
```bash
curl -X POST "http://localhost:8000/api/linguistic/agents/uuid/communicate" \
  -H "Content-Type: application/json" \
  -d '{
    "force_communication": false,
    "custom_aura_state": {
      "warmth_gradient": 0.8,
      "resource_density": 0.6,
      "danger_proximity": 0.1,
      "cat_happiness": 0.9,
      "social_longing": 0.7,
      "innovation_energy": 0.6,
      "literacy_exposure": 0.4
    },
    "rss_feeds": ["Breaking: Scientists discover new happiness measurement!"]
  }'
```

### Analyze Patterns
```bash
curl -X POST "http://localhost:8000/api/linguistic/patterns/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "patterns": ["•••••", "• • •", "•\n •\n  •"],
    "include_complexity": true,
    "include_similarity": true,
    "include_evolution": true
  }'
```

### Get Population Metrics
```bash
curl "http://localhost:8000/api/linguistic/evolution/metrics?time_range=24h&include_trends=true"
```

### Process RSS Feed
```bash
curl -X POST "http://localhost:8000/api/linguistic/rss/feed" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_ids": ["uuid1", "uuid2"],
    "feed_content": "Technology: AI agents learning fascinating communication patterns!",
    "feed_source": "tech_news",
    "quality_score": 1.0
  }'
```

## Mathematical Properties

### Pattern Complexity Calculation
```python
complexity = (
    shannon_entropy * 0.4 +      # Information content
    length_score * 0.2 +         # Normalized length
    spatial_complexity * 0.3 +   # 2D arrangement
    repetition_penalty * 0.1     # Anti-repetition
)
```

### Communication Pressure Formula
```python
pressure = (
    social_longing * 0.3 +
    danger_proximity * 0.4 +
    resource_need * 0.2 +
    happiness_concern * 0.3 +
    innovation_drive * tendency * 0.2 +
    literacy_expression * 0.1
)
```

### Stage Progression Logic
- **Stage 1** (Primal): < 100 communications
- **Stage 2** (Emotional): 100-500 communications  
- **Stage 3** (Conceptual): 500-2000 communications
- **Stage 4** (Cultural): 2000-5000 communications
- **Stage 5** (Meta-linguistic): > 5000 communications

*Modifiers: complexity > 0.7 + vocab > 20 → +1 stage, literacy > 0.5 → +1 stage*

## WebSocket Event Types

### Live Stream Events
```json
{
  "event_type": "communication",
  "timestamp": "2025-07-04T12:00:00Z",
  "data": {
    "agent_id": "uuid",
    "pattern": "•••••",
    "complexity": 0.46,
    "trigger": "danger_proximity",
    "is_innovation": true,
    "aura_context": {...},
    "pressure": 0.78
  }
}
```

### Pattern Emergence
```json
{
  "event_type": "pattern_emergence", 
  "data": {
    "pattern": "•\n •\n  •",
    "complexity": 0.546,
    "creator_agent": "uuid",
    "spatial_dimensions": 2,
    "innovation_context": {...}
  }
}
```

### Stage Advancement
```json
{
  "event_type": "stage_advancement",
  "data": {
    "agent_id": "uuid",
    "old_stage": 2,
    "new_stage": 3,
    "stage_name": "CONCEPTUAL_COMMUNICATION",
    "vocabulary_size": 15,
    "literacy_level": 0.34
  }
}
```

## System Health Monitoring

### Health Check Response
```json
{
  "status": "healthy",
  "services": {
    "api": "running",
    "database": "healthy", 
    "linguistic_system": "running",
    "websocket_streams": "active"
  },
  "database": {
    "linguistic_tables": 6,
    "pool_stats": {...}
  },
  "websockets": {
    "total_connections": 12,
    "connections_by_stream": {...}
  }
}
```

### System Status
```json
{
  "active_agents": 47,
  "total_communications_24h": 342,
  "unique_patterns_discovered": 28,
  "language_families_active": 3,
  "average_complexity": 0.423,
  "innovation_rate": 0.167,
  "system_health": "excellent"
}
```

## Environment Configuration

### Database Settings
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chaostown
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_POOL_MIN_SIZE=5
DB_POOL_MAX_SIZE=20
DB_COMMAND_TIMEOUT=30
```

### Application Settings
```bash
API_VERSION=2.0.0
LOG_LEVEL=INFO
WEBSOCKET_PING_INTERVAL=30
METRICS_CACHE_TTL=60
STREAM_BUFFER_SIZE=1000
```

## Integration with Existing CHAOSTOWN

### Enhanced Dashboard Stats
The `/dashboard/stats` endpoint now includes linguistic metrics:
```json
{
  "cat_happiness": 0.9,
  "agent_count": 10,
  "linguistic_evolution": {
    "total_linguistic_agents": 10,
    "active_linguistic_agents": 8,
    "total_communications": 156,
    "unique_patterns": 23,
    "language_families": 2
  }
}
```

### Bridge to Simulation Engine
Linguistic agents can be connected to the main simulation through:
1. Agent initialization during simulation startup
2. Environmental aura state synchronization
3. RSS feed processing for external stimuli
4. WebSocket broadcasts to live dashboards

## Research Applications

### Alien Language Study
- **Semantic Opacity**: Internal meanings remain hidden
- **Mathematical Determinism**: 70% environmental pressure influence
- **Pattern Evolution**: Track complexity growth over time
- **Cultural Emergence**: Observe language family formation

### Data Collection
- All communications logged with full context
- Pattern complexity calculated mathematically
- Stage progressions tracked automatically
- RSS influence measured precisely

### Experimental Design
- Controlled environmental manipulation
- Agent characteristic variation
- RSS feed content experiments
- Innovation pressure testing

## Security & Privacy

### Semantic Protection
- Internal agent meanings never exposed via API
- Observable state endpoints filter sensitive data
- Debug endpoints clearly marked and restricted

### Database Security
- Connection pooling with timeouts
- Parameterized queries prevent injection
- TimescaleDB compression and retention policies

### WebSocket Security
- Connection limits and rate limiting
- Message validation and filtering
- Automatic cleanup of disconnected clients

## Performance Optimization

### Caching Strategy
- Population metrics cached for 60 seconds
- Database connection pooling (5-20 connections)
- Background tasks for periodic updates

### TimescaleDB Benefits
- Time-series data compression
- Automatic data retention policies
- Optimized queries for temporal analysis

### Async Architecture
- Non-blocking database operations
- Background WebSocket broadcasting
- Concurrent pattern analysis

## Deployment Ready

The implementation is production-ready with:
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Health checks and monitoring
- ✅ Database migration support
- ✅ WebSocket connection management
- ✅ Graceful startup/shutdown

## Next Steps

1. **Deploy to staging environment**
2. **Run database migration**: `001_linguistic_evolution.sql`
3. **Initialize agent population** via `/agents/initialize`
4. **Connect to WebSocket streams** for live monitoring
5. **Start feeding RSS content** for literacy development
6. **Monitor system health** via status endpoints

The linguistic evolution system is now fully integrated and ready for alien language research! 🛸👽🗣️