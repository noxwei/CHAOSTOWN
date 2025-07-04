# Database Schema - CHAOSTOWN Architecture

**PostgreSQL + TimescaleDB Schema for Agentic Simulation**

---

## Overview

The CHAOSTOWN database architecture combines PostgreSQL's relational capabilities with TimescaleDB's time-series optimization to handle agent behavior, world state, and metrics at scale. The schema supports 216-dimensional personality tensors, vector embeddings, and real-time analytics.

## Core Tables

### agents
```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    model VARCHAR(100) NOT NULL, -- llama3, mistral, etc.
    archetype VARCHAR(50) NOT NULL, -- philosopher, competitor, etc.
    
    -- Personality tensor (216 dimensions)
    personality_tensor JSONB NOT NULL,
    
    -- Position and state
    position_x FLOAT NOT NULL DEFAULT 0,
    position_y FLOAT NOT NULL DEFAULT 0,
    position_z FLOAT NOT NULL DEFAULT 0,
    health FLOAT NOT NULL DEFAULT 100.0,
    energy FLOAT NOT NULL DEFAULT 100.0,
    
    -- Lifecycle
    birth_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    death_time TIMESTAMPTZ,
    parent_id UUID REFERENCES agents(id),
    reproduction_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_health CHECK (health >= 0 AND health <= 100),
    CONSTRAINT valid_energy CHECK (energy >= 0 AND energy <= 100),
    CONSTRAINT valid_reproduction CHECK (reproduction_count >= 0)
);

-- Indexes
CREATE INDEX idx_agents_archetype ON agents(archetype);
CREATE INDEX idx_agents_model ON agents(model);
CREATE INDEX idx_agents_health ON agents(health);
CREATE INDEX idx_agents_birth_time ON agents(birth_time);
CREATE INDEX idx_agents_parent_id ON agents(parent_id);
```

### world_state
```sql
CREATE TABLE world_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Grid state (Conway's Game of Life)
    grid_state JSONB NOT NULL,
    grid_width INTEGER NOT NULL DEFAULT 100,
    grid_height INTEGER NOT NULL DEFAULT 100,
    
    -- Population metrics
    total_agents INTEGER NOT NULL DEFAULT 0,
    active_agents INTEGER NOT NULL DEFAULT 0,
    dead_agents INTEGER NOT NULL DEFAULT 0,
    
    -- Prime Directive metrics
    fluffhead_happiness FLOAT NOT NULL DEFAULT 0.8,
    wilson_happiness FLOAT NOT NULL DEFAULT 0.8,
    combined_happiness FLOAT GENERATED ALWAYS AS ((fluffhead_happiness + wilson_happiness) / 2) STORED,
    
    -- Resource tracking
    cost_multiplier FLOAT NOT NULL DEFAULT 1.0,
    total_cost FLOAT NOT NULL DEFAULT 0.0,
    
    -- RSS and world data
    rss_headlines JSONB,
    external_data JSONB,
    
    -- Constraints
    CONSTRAINT valid_happiness CHECK (fluffhead_happiness >= 0 AND fluffhead_happiness <= 1),
    CONSTRAINT valid_wilson CHECK (wilson_happiness >= 0 AND wilson_happiness <= 1),
    CONSTRAINT valid_cost_mult CHECK (cost_multiplier >= 0)
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('world_state', 'timestamp');

-- Indexes
CREATE INDEX idx_world_state_tick ON world_state(tick_number);
CREATE INDEX idx_world_state_happiness ON world_state(combined_happiness);
```

### agent_decisions
```sql
CREATE TABLE agent_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Decision context
    decision_type VARCHAR(50) NOT NULL, -- move, reproduce, interact, etc.
    context_data JSONB NOT NULL,
    
    -- AI model response
    model_input JSONB NOT NULL,
    model_output JSONB NOT NULL,
    processing_time_ms INTEGER NOT NULL,
    
    -- Decision outcome
    decision_result JSONB NOT NULL,
    success BOOLEAN NOT NULL DEFAULT false,
    
    -- Vector embeddings for decision analysis
    decision_embedding VECTOR(1536), -- OpenAI embeddings
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('agent_decisions', 'timestamp');

-- Indexes
CREATE INDEX idx_agent_decisions_agent_id ON agent_decisions(agent_id);
CREATE INDEX idx_agent_decisions_type ON agent_decisions(decision_type);
CREATE INDEX idx_agent_decisions_tick ON agent_decisions(tick_number);
```

### interactions
```sql
CREATE TABLE interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Participants
    agent_a_id UUID NOT NULL REFERENCES agents(id),
    agent_b_id UUID NOT NULL REFERENCES agents(id),
    
    -- Interaction details
    interaction_type VARCHAR(50) NOT NULL, -- communication, conflict, cooperation, reproduction
    strength FLOAT NOT NULL DEFAULT 0.0,
    
    -- Outcomes
    outcome_data JSONB NOT NULL,
    agent_a_delta JSONB, -- changes to agent A
    agent_b_delta JSONB, -- changes to agent B
    
    -- Distance and positioning
    distance FLOAT NOT NULL,
    position_data JSONB NOT NULL,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_strength CHECK (strength >= -1.0 AND strength <= 1.0),
    CONSTRAINT different_agents CHECK (agent_a_id != agent_b_id)
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('interactions', 'timestamp');

-- Indexes
CREATE INDEX idx_interactions_agent_a ON interactions(agent_a_id);
CREATE INDEX idx_interactions_agent_b ON interactions(agent_b_id);
CREATE INDEX idx_interactions_type ON interactions(interaction_type);
```

### cat_media
```sql
CREATE TABLE cat_media (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Media details
    media_type VARCHAR(20) NOT NULL, -- image, gif, video, text
    file_path VARCHAR(500),
    content_text TEXT,
    
    -- Happiness analysis
    fluffhead_detected BOOLEAN DEFAULT false,
    wilson_detected BOOLEAN DEFAULT false,
    fluffhead_happiness FLOAT,
    wilson_happiness FLOAT,
    
    -- Vision API response
    vision_analysis JSONB,
    analysis_timestamp TIMESTAMPTZ,
    
    -- Metadata
    file_size_bytes INTEGER,
    mime_type VARCHAR(100),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_media_type CHECK (media_type IN ('image', 'gif', 'video', 'text')),
    CONSTRAINT valid_fluffhead_happiness CHECK (fluffhead_happiness IS NULL OR (fluffhead_happiness >= 0 AND fluffhead_happiness <= 1)),
    CONSTRAINT valid_wilson_happiness CHECK (wilson_happiness IS NULL OR (wilson_happiness >= 0 AND wilson_happiness <= 1))
);

-- Indexes
CREATE INDEX idx_cat_media_upload_time ON cat_media(upload_time);
CREATE INDEX idx_cat_media_type ON cat_media(media_type);
CREATE INDEX idx_cat_media_happiness ON cat_media(fluffhead_happiness, wilson_happiness);
```

### prime_directive_violations
```sql
CREATE TABLE prime_directive_violations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Violation details
    directive_number INTEGER NOT NULL,
    violation_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    
    -- Context
    agent_id UUID REFERENCES agents(id),
    tick_number BIGINT,
    context_data JSONB NOT NULL,
    
    -- Resolution
    resolved BOOLEAN DEFAULT false,
    resolution_time TIMESTAMPTZ,
    resolution_method VARCHAR(100),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_directive CHECK (directive_number >= 1 AND directive_number <= 7),
    CONSTRAINT valid_severity CHECK (severity IN ('low', 'medium', 'high', 'critical'))
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('prime_directive_violations', 'timestamp');

-- Indexes
CREATE INDEX idx_violations_directive ON prime_directive_violations(directive_number);
CREATE INDEX idx_violations_severity ON prime_directive_violations(severity);
CREATE INDEX idx_violations_resolved ON prime_directive_violations(resolved);
```

## Supporting Tables

### models
```sql
CREATE TABLE models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL, -- llama, mistral, gemma, etc.
    version VARCHAR(50) NOT NULL,
    
    -- Performance characteristics
    avg_response_time_ms INTEGER,
    token_limit INTEGER,
    context_window INTEGER,
    
    -- Configuration
    temperature FLOAT DEFAULT 0.7,
    top_p FLOAT DEFAULT 0.9,
    config_params JSONB,
    
    -- Status
    active BOOLEAN DEFAULT true,
    last_health_check TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Default models
INSERT INTO models (name, type, version, token_limit, context_window) VALUES
('llama3.1', 'llama', '3.1', 8192, 8192),
('llama3.2', 'llama', '3.2', 8192, 8192),
('mistral', 'mistral', '7b', 8192, 8192),
('gemma2', 'gemma', '2b', 8192, 8192),
('qwen2.5', 'qwen', '2.5', 8192, 8192),
('phi3.5', 'phi', '3.5', 8192, 8192),
('codellama', 'llama', 'code', 8192, 8192),
('deepseek-coder', 'deepseek', 'coder', 8192, 8192);
```

### archetypes
```sql
CREATE TABLE archetypes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    
    -- Behavioral parameters
    personality_template JSONB NOT NULL,
    decision_weights JSONB NOT NULL,
    
    -- Associated model
    preferred_model VARCHAR(100) REFERENCES models(name),
    
    -- Characteristics
    cooperation_tendency FLOAT DEFAULT 0.5,
    aggression_tendency FLOAT DEFAULT 0.5,
    curiosity_tendency FLOAT DEFAULT 0.5,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_cooperation CHECK (cooperation_tendency >= 0 AND cooperation_tendency <= 1),
    CONSTRAINT valid_aggression CHECK (aggression_tendency >= 0 AND aggression_tendency <= 1),
    CONSTRAINT valid_curiosity CHECK (curiosity_tendency >= 0 AND curiosity_tendency <= 1)
);

-- Default archetypes
INSERT INTO archetypes (name, description, personality_template, decision_weights, preferred_model, cooperation_tendency, aggression_tendency, curiosity_tendency) VALUES
('philosopher', 'Deep thinking, questions everything, seeks truth', '{"wisdom": 0.9, "curiosity": 0.8, "patience": 0.7}', '{"exploration": 0.8, "cooperation": 0.7, "competition": 0.2}', 'llama3.1', 0.7, 0.1, 0.9),
('competitor', 'Aggressive, seeks dominance, resource acquisition', '{"ambition": 0.9, "aggression": 0.8, "confidence": 0.7}', '{"competition": 0.9, "resource_gathering": 0.8, "cooperation": 0.2}', 'mistral', 0.2, 0.9, 0.3),
('collaborator', 'Cooperative, builds relationships, seeks harmony', '{"empathy": 0.9, "cooperation": 0.8, "diplomacy": 0.7}', '{"cooperation": 0.9, "mediation": 0.8, "competition": 0.1}', 'gemma2', 0.9, 0.1, 0.6),
('creator', 'Innovative, builds systems, problem solver', '{"creativity": 0.9, "innovation": 0.8, "persistence": 0.7}', '{"creation": 0.9, "problem_solving": 0.8, "optimization": 0.7}', 'codellama', 0.6, 0.2, 0.8),
('analyst', 'Data-driven, logical, pattern recognition', '{"logic": 0.9, "analysis": 0.8, "objectivity": 0.7}', '{"analysis": 0.9, "pattern_recognition": 0.8, "optimization": 0.7}', 'qwen2.5', 0.5, 0.2, 0.7),
('explorer', 'Curious, risk-taking, seeks new experiences', '{"curiosity": 0.9, "adventure": 0.8, "adaptability": 0.7}', '{"exploration": 0.9, "risk_taking": 0.8, "discovery": 0.7}', 'phi3.5', 0.4, 0.3, 0.9),
('guardian', 'Protective, defensive, maintains order', '{"protection": 0.9, "loyalty": 0.8, "vigilance": 0.7}', '{"defense": 0.9, "protection": 0.8, "order": 0.7}', 'llama3.2', 0.6, 0.6, 0.3),
('mystic', 'Intuitive, spiritual, seeks meaning', '{"intuition": 0.9, "spirituality": 0.8, "wisdom": 0.7}', '{"contemplation": 0.9, "meaning_seeking": 0.8, "guidance": 0.7}', 'deepseek-coder', 0.5, 0.1, 0.8);
```

## Views and Functions

### Active Agents View
```sql
CREATE VIEW active_agents AS
SELECT 
    a.*,
    m.name as model_name,
    m.type as model_type,
    ar.name as archetype_name,
    ar.description as archetype_description
FROM agents a
JOIN models m ON a.model = m.name
JOIN archetypes ar ON a.archetype = ar.name
WHERE a.death_time IS NULL;
```

### Population Health View
```sql
CREATE VIEW population_health AS
SELECT 
    COUNT(*) as total_agents,
    COUNT(*) FILTER (WHERE death_time IS NULL) as active_agents,
    COUNT(*) FILTER (WHERE death_time IS NOT NULL) as dead_agents,
    AVG(health) FILTER (WHERE death_time IS NULL) as avg_health,
    AVG(energy) FILTER (WHERE death_time IS NULL) as avg_energy,
    COUNT(*) FILTER (WHERE reproduction_count > 0) as reproducers
FROM agents;
```

### Happiness Monitoring Function
```sql
CREATE OR REPLACE FUNCTION check_happiness_threshold()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.combined_happiness < 0.5 THEN
        INSERT INTO prime_directive_violations (directive_number, violation_type, severity, context_data)
        VALUES (2, 'critical_happiness_failure', 'critical', 
                jsonb_build_object('happiness', NEW.combined_happiness, 'tick', NEW.tick_number));
    ELSIF NEW.combined_happiness < 0.8 THEN
        INSERT INTO prime_directive_violations (directive_number, violation_type, severity, context_data)
        VALUES (2, 'happiness_warning', 'medium', 
                jsonb_build_object('happiness', NEW.combined_happiness, 'tick', NEW.tick_number));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER happiness_monitor
    AFTER INSERT OR UPDATE ON world_state
    FOR EACH ROW EXECUTE FUNCTION check_happiness_threshold();
```

## Data Retention Policies

### TimescaleDB Retention
```sql
-- Keep detailed data for 90 days, then compress
SELECT add_retention_policy('world_state', INTERVAL '90 days');
SELECT add_retention_policy('agent_decisions', INTERVAL '90 days');
SELECT add_retention_policy('interactions', INTERVAL '90 days');
SELECT add_retention_policy('prime_directive_violations', INTERVAL '365 days');

-- Compression policies
SELECT add_compression_policy('world_state', INTERVAL '7 days');
SELECT add_compression_policy('agent_decisions', INTERVAL '7 days');
SELECT add_compression_policy('interactions', INTERVAL '7 days');
```

## Performance Optimizations

### Partitioning
```sql
-- Partition agents by archetype for better query performance
CREATE TABLE agents_philosopher PARTITION OF agents FOR VALUES IN ('philosopher');
CREATE TABLE agents_competitor PARTITION OF agents FOR VALUES IN ('competitor');
-- ... continue for all archetypes
```

### Materialized Views
```sql
-- Hourly population statistics
CREATE MATERIALIZED VIEW hourly_population AS
SELECT 
    date_trunc('hour', timestamp) as hour,
    AVG(total_agents) as avg_population,
    AVG(combined_happiness) as avg_happiness,
    AVG(cost_multiplier) as avg_cost
FROM world_state
GROUP BY date_trunc('hour', timestamp);

-- Refresh every hour
CREATE OR REPLACE FUNCTION refresh_hourly_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW hourly_population;
END;
$$ LANGUAGE plpgsql;
```

## Backup and Recovery

### Daily Backup Script
```bash
#!/bin/bash
# backup_chaostown.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U postgres -d chaostown | gzip > /backups/chaostown_${DATE}.sql.gz
```

### Point-in-Time Recovery
```sql
-- Enable WAL archiving for PITR
archive_mode = on
archive_command = 'cp %p /archives/%f'
wal_level = replica
```

---

## Usage Examples

### Query Agent Interactions
```sql
-- Find all interactions between specific archetypes
SELECT 
    i.timestamp,
    i.interaction_type,
    i.strength,
    a1.name as agent_a_name,
    a1.archetype as agent_a_type,
    a2.name as agent_b_name,
    a2.archetype as agent_b_type
FROM interactions i
JOIN agents a1 ON i.agent_a_id = a1.id
JOIN agents a2 ON i.agent_b_id = a2.id
WHERE a1.archetype = 'philosopher' AND a2.archetype = 'competitor'
ORDER BY i.timestamp DESC
LIMIT 100;
```

### Monitor Prime Directive Compliance
```sql
-- Check recent violations
SELECT 
    directive_number,
    COUNT(*) as violation_count,
    MAX(timestamp) as last_violation
FROM prime_directive_violations
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY directive_number
ORDER BY violation_count DESC;
```

### Analyze Decision Patterns
```sql
-- Agent decision success rates by archetype
SELECT 
    a.archetype,
    COUNT(*) as total_decisions,
    AVG(CASE WHEN ad.success THEN 1 ELSE 0 END) as success_rate,
    AVG(ad.processing_time_ms) as avg_processing_time
FROM agent_decisions ad
JOIN agents a ON ad.agent_id = a.id
WHERE ad.timestamp > NOW() - INTERVAL '7 days'
GROUP BY a.archetype
ORDER BY success_rate DESC;
```

---

*This schema supports the complete CHAOSTOWN simulation ecosystem, from individual agent personalities to emergent civilization dynamics, all while maintaining the sacred duty of keeping Fluffhead and Wilson supremely happy.*

**Database optimized for chaos, structured for cats.** 🐱📊