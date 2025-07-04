# Linguistic Evolution Database Schema

**PostgreSQL + TimescaleDB Schema for Emergent Language Evolution**

*Integrating dot-based language systems with the core CHAOSTOWN architecture*

---

## Overview

The linguistic evolution system extends the core CHAOSTOWN database with tables specifically designed for tracking emergent communication, language development, and alien semantic networks. This schema maintains the mathematical rigor of Shannon entropy calculations while providing full observability into language genesis without compromising semantic opacity.

## Core Linguistic Tables

### linguistic_agents
```sql
-- Extension of core agents table for linguistic capabilities
CREATE TABLE linguistic_agents (
    agent_id UUID PRIMARY KEY REFERENCES agents(id) ON DELETE CASCADE,
    
    -- Linguistic development metrics
    linguistic_stage INTEGER NOT NULL DEFAULT 1, -- 1-5 progression
    vocabulary_size INTEGER NOT NULL DEFAULT 0,
    total_communications INTEGER NOT NULL DEFAULT 0,
    innovation_tendency FLOAT NOT NULL DEFAULT 0.5,
    social_influence_susceptibility FLOAT NOT NULL DEFAULT 0.5,
    communication_threshold FLOAT NOT NULL DEFAULT 0.6,
    
    -- Literacy acquisition
    literacy_level FLOAT NOT NULL DEFAULT 0.0,
    character_recognition_count INTEGER NOT NULL DEFAULT 0,
    word_association_count INTEGER NOT NULL DEFAULT 0,
    
    -- Complexity evolution tracking
    average_pattern_complexity FLOAT NOT NULL DEFAULT 0.0,
    complexity_growth_rate FLOAT NOT NULL DEFAULT 0.01,
    
    -- Language family/dialect tracking
    primary_language_family UUID, -- Self-referencing for language groups
    dialect_variance FLOAT NOT NULL DEFAULT 0.0,
    
    -- Internal state (opaque semantic networks)
    internal_meanings JSONB NOT NULL DEFAULT '{}',
    aura_pattern_mappings JSONB NOT NULL DEFAULT '{}',
    social_pattern_preferences JSONB NOT NULL DEFAULT '{}',
    
    -- Metadata
    first_communication TIMESTAMPTZ,
    last_communication TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_linguistic_stage CHECK (linguistic_stage >= 1 AND linguistic_stage <= 5),
    CONSTRAINT valid_vocabulary_size CHECK (vocabulary_size >= 0),
    CONSTRAINT valid_literacy_level CHECK (literacy_level >= 0 AND literacy_level <= 1),
    CONSTRAINT valid_innovation_tendency CHECK (innovation_tendency >= 0 AND innovation_tendency <= 1),
    CONSTRAINT valid_social_susceptibility CHECK (social_influence_susceptibility >= 0 AND social_influence_susceptibility <= 1),
    CONSTRAINT valid_complexity CHECK (average_pattern_complexity >= 0 AND average_pattern_complexity <= 1)
);

-- Indexes for linguistic analysis
CREATE INDEX idx_linguistic_agents_stage ON linguistic_agents(linguistic_stage);
CREATE INDEX idx_linguistic_agents_vocabulary ON linguistic_agents(vocabulary_size);
CREATE INDEX idx_linguistic_agents_literacy ON linguistic_agents(literacy_level);
CREATE INDEX idx_linguistic_agents_family ON linguistic_agents(primary_language_family);
```

### communications
```sql
-- All agent communications with full context
CREATE TABLE communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Communication content
    dot_pattern TEXT NOT NULL,
    pattern_complexity FLOAT NOT NULL,
    pattern_hash VARCHAR(64) NOT NULL, -- For deduplication and tracking
    
    -- Context and triggers
    aura_context JSONB NOT NULL,
    social_context JSONB NOT NULL,
    internal_pressure FLOAT NOT NULL,
    communication_trigger VARCHAR(50) NOT NULL, -- danger, social, innovation, etc.
    
    -- Innovation tracking
    is_innovation BOOLEAN NOT NULL DEFAULT false,
    pattern_first_use BOOLEAN NOT NULL DEFAULT false,
    innovation_source VARCHAR(20), -- 'creation' or 'adaptation'
    
    -- Response and effectiveness
    response_count INTEGER NOT NULL DEFAULT 0,
    adoption_count INTEGER NOT NULL DEFAULT 0,
    success_indicators JSONB,
    
    -- RSS feed influence
    rss_influenced BOOLEAN DEFAULT false,
    rss_content_hash VARCHAR(64),
    literacy_boost FLOAT DEFAULT 0.0,
    
    -- Spatial and network data
    position_x FLOAT,
    position_y FLOAT,
    nearby_agents JSONB,
    
    -- Vector embeddings for semantic analysis (even though meanings are opaque)
    pattern_embedding VECTOR(384), -- Sentence transformer embeddings
    context_embedding VECTOR(384),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to TimescaleDB hypertable for time-series analysis
SELECT create_hypertable('communications', 'timestamp');

-- Indexes for linguistic research
CREATE INDEX idx_communications_agent ON communications(agent_id);
CREATE INDEX idx_communications_pattern_hash ON communications(pattern_hash);
CREATE INDEX idx_communications_complexity ON communications(pattern_complexity);
CREATE INDEX idx_communications_innovation ON communications(is_innovation);
CREATE INDEX idx_communications_trigger ON communications(communication_trigger);
CREATE INDEX idx_communications_tick ON communications(tick_number);

-- GIN index for aura context queries
CREATE INDEX idx_communications_aura_gin ON communications USING GIN (aura_context);
```

### dot_patterns
```sql
-- Registry of all unique dot patterns and their evolution
CREATE TABLE dot_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_hash VARCHAR(64) UNIQUE NOT NULL,
    dot_pattern TEXT NOT NULL,
    
    -- Mathematical properties
    complexity FLOAT NOT NULL,
    shannon_entropy FLOAT NOT NULL,
    spatial_dimensions INTEGER NOT NULL DEFAULT 1,
    character_count INTEGER NOT NULL,
    dot_count INTEGER NOT NULL,
    
    -- Pattern structure analysis
    has_newlines BOOLEAN NOT NULL DEFAULT false,
    has_spacing BOOLEAN NOT NULL DEFAULT false,
    is_repetitive BOOLEAN NOT NULL DEFAULT false,
    repetition_factor FLOAT,
    
    -- Usage statistics
    first_appearance TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_usage_count INTEGER NOT NULL DEFAULT 1,
    unique_users_count INTEGER NOT NULL DEFAULT 1,
    
    -- Innovation tracking
    created_by_agent UUID NOT NULL REFERENCES agents(id),
    innovation_context JSONB,
    
    -- Pattern family/evolution
    parent_pattern_id UUID REFERENCES dot_patterns(id), -- If evolved from another pattern
    child_patterns_count INTEGER NOT NULL DEFAULT 0,
    pattern_generation INTEGER NOT NULL DEFAULT 1,
    
    -- Adoption metrics
    adoption_rate FLOAT NOT NULL DEFAULT 0.0,
    success_rate FLOAT NOT NULL DEFAULT 0.0,
    cultural_penetration FLOAT NOT NULL DEFAULT 0.0,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for pattern analysis
CREATE INDEX idx_dot_patterns_complexity ON dot_patterns(complexity);
CREATE INDEX idx_dot_patterns_usage ON dot_patterns(total_usage_count);
CREATE INDEX idx_dot_patterns_creator ON dot_patterns(created_by_agent);
CREATE INDEX idx_dot_patterns_generation ON dot_patterns(pattern_generation);
CREATE INDEX idx_dot_patterns_first_appearance ON dot_patterns(first_appearance);
```

### language_families
```sql
-- Emergent language groups and dialects
CREATE TABLE language_families (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100), -- Human-assigned name for research
    
    -- Family characteristics
    founding_agents UUID[] NOT NULL, -- Array of founding agent IDs
    characteristic_patterns TEXT[] NOT NULL, -- Common pattern signatures
    emergence_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Mathematical signatures
    family_complexity_profile JSONB NOT NULL,
    pattern_diversity FLOAT NOT NULL DEFAULT 0.0,
    innovation_rate FLOAT NOT NULL DEFAULT 0.0,
    
    -- Social dynamics
    member_count INTEGER NOT NULL DEFAULT 0,
    internal_cohesion FLOAT NOT NULL DEFAULT 0.0,
    external_influence FLOAT NOT NULL DEFAULT 0.0,
    
    -- Evolution tracking
    parent_family_id UUID REFERENCES language_families(id),
    split_reason VARCHAR(100),
    split_timestamp TIMESTAMPTZ,
    
    -- Research notes (human observations)
    research_notes TEXT,
    dominant_communication_triggers JSONB,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for linguistic research
CREATE INDEX idx_language_families_emergence ON language_families(emergence_timestamp);
CREATE INDEX idx_language_families_members ON language_families(member_count);
CREATE INDEX idx_language_families_parent ON language_families(parent_family_id);
```

### linguistic_interactions
```sql
-- Special interactions focused on communication
CREATE TABLE linguistic_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    communication_id UUID NOT NULL REFERENCES communications(id),
    responding_agent_id UUID NOT NULL REFERENCES agents(id),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Interaction type
    interaction_type VARCHAR(50) NOT NULL, -- 'adoption', 'innovation', 'teaching', 'mimicry'
    
    -- Response details
    response_pattern TEXT,
    response_delay_ticks INTEGER NOT NULL DEFAULT 0,
    understanding_indicator FLOAT, -- How well the pattern was "understood"
    
    -- Learning outcomes
    pattern_adopted BOOLEAN DEFAULT false,
    pattern_modified BOOLEAN DEFAULT false,
    new_pattern_created BOOLEAN DEFAULT false,
    literacy_change FLOAT DEFAULT 0.0,
    
    -- Social influence
    influence_strength FLOAT NOT NULL DEFAULT 0.0,
    relationship_change FLOAT DEFAULT 0.0,
    
    -- Context
    distance FLOAT NOT NULL,
    aura_similarity FLOAT,
    interaction_context JSONB,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('linguistic_interactions', 'timestamp');

-- Indexes
CREATE INDEX idx_linguistic_interactions_comm ON linguistic_interactions(communication_id);
CREATE INDEX idx_linguistic_interactions_agent ON linguistic_interactions(responding_agent_id);
CREATE INDEX idx_linguistic_interactions_type ON linguistic_interactions(interaction_type);
```

### rss_linguistic_influence
```sql
-- Track how RSS feeds influence language development
CREATE TABLE rss_linguistic_influence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- RSS content
    rss_content_hash VARCHAR(64) NOT NULL,
    rss_content_summary TEXT,
    content_length INTEGER NOT NULL,
    
    -- Processing details
    vibes_extracted FLOAT NOT NULL,
    characters_recognized INTEGER NOT NULL DEFAULT 0,
    new_character_learning INTEGER NOT NULL DEFAULT 0,
    word_associations_formed INTEGER NOT NULL DEFAULT 0,
    
    -- Influence on communication
    triggered_communication BOOLEAN DEFAULT false,
    communication_id UUID REFERENCES communications(id),
    influence_strength FLOAT NOT NULL DEFAULT 0.0,
    
    -- Literacy development
    literacy_before FLOAT NOT NULL,
    literacy_after FLOAT NOT NULL,
    literacy_delta FLOAT GENERATED ALWAYS AS (literacy_after - literacy_before) STORED,
    
    -- Context
    aura_state_at_processing JSONB NOT NULL,
    processing_duration_ms INTEGER,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('rss_linguistic_influence', 'timestamp');

-- Indexes
CREATE INDEX idx_rss_influence_agent ON rss_linguistic_influence(agent_id);
CREATE INDEX idx_rss_influence_content_hash ON rss_linguistic_influence(rss_content_hash);
CREATE INDEX idx_rss_influence_literacy_delta ON rss_linguistic_influence(literacy_delta);
```

## Supporting Views and Functions

### linguistic_evolution_metrics
```sql
-- Real-time view of language evolution metrics
CREATE VIEW linguistic_evolution_metrics AS
SELECT 
    la.agent_id,
    a.name as agent_name,
    a.archetype,
    la.linguistic_stage,
    la.vocabulary_size,
    la.literacy_level,
    la.total_communications,
    
    -- Recent activity (last 24 hours)
    COUNT(c.id) FILTER (WHERE c.timestamp > NOW() - INTERVAL '24 hours') as communications_24h,
    AVG(c.pattern_complexity) FILTER (WHERE c.timestamp > NOW() - INTERVAL '24 hours') as avg_complexity_24h,
    COUNT(c.id) FILTER (WHERE c.is_innovation AND c.timestamp > NOW() - INTERVAL '24 hours') as innovations_24h,
    
    -- Language family info
    lf.name as language_family_name,
    la.dialect_variance,
    
    -- Last communication
    la.last_communication,
    
    -- Complexity trend
    la.average_pattern_complexity,
    la.complexity_growth_rate

FROM linguistic_agents la
JOIN agents a ON la.agent_id = a.id
LEFT JOIN language_families lf ON la.primary_language_family = lf.id
LEFT JOIN communications c ON la.agent_id = c.agent_id
WHERE a.death_time IS NULL  -- Only living agents
GROUP BY la.agent_id, a.name, a.archetype, la.linguistic_stage, la.vocabulary_size, 
         la.literacy_level, la.total_communications, lf.name, la.dialect_variance, 
         la.last_communication, la.average_pattern_complexity, la.complexity_growth_rate;
```

### pattern_popularity
```sql
-- View of most popular/successful patterns
CREATE VIEW pattern_popularity AS
SELECT 
    dp.dot_pattern,
    dp.complexity,
    dp.total_usage_count,
    dp.unique_users_count,
    dp.adoption_rate,
    dp.success_rate,
    dp.first_appearance,
    dp.pattern_generation,
    
    -- Creator info
    a.name as creator_name,
    a.archetype as creator_archetype,
    
    -- Recent usage
    COUNT(c.id) FILTER (WHERE c.timestamp > NOW() - INTERVAL '7 days') as uses_last_week,
    
    -- Cultural metrics
    dp.cultural_penetration,
    
    -- Innovation context
    dp.innovation_context

FROM dot_patterns dp
JOIN agents a ON dp.created_by_agent = a.id
LEFT JOIN communications c ON dp.pattern_hash = c.pattern_hash
GROUP BY dp.id, dp.dot_pattern, dp.complexity, dp.total_usage_count, dp.unique_users_count,
         dp.adoption_rate, dp.success_rate, dp.first_appearance, dp.pattern_generation,
         a.name, a.archetype, dp.cultural_penetration, dp.innovation_context
ORDER BY dp.total_usage_count DESC;
```

### linguistic_stage_evolution_function
```sql
-- Function to update agent linguistic stage based on metrics
CREATE OR REPLACE FUNCTION update_linguistic_stage(p_agent_id UUID)
RETURNS INTEGER AS $$
DECLARE
    current_stage INTEGER;
    total_comms INTEGER;
    vocab_size INTEGER;
    avg_complexity FLOAT;
    literacy_level FLOAT;
    new_stage INTEGER;
BEGIN
    -- Get current metrics
    SELECT 
        la.linguistic_stage,
        la.total_communications,
        la.vocabulary_size,
        la.average_pattern_complexity,
        la.literacy_level
    INTO current_stage, total_comms, vocab_size, avg_complexity, literacy_level
    FROM linguistic_agents la
    WHERE la.agent_id = p_agent_id;
    
    -- Stage progression logic (from LINGUISTIC_EVOLUTION.md)
    IF total_comms < 100 THEN
        new_stage := 1; -- Primal signals
    ELSIF total_comms < 500 THEN
        new_stage := 2; -- Emotional expression
    ELSIF total_comms < 2000 THEN
        new_stage := 3; -- Conceptual communication
    ELSIF total_comms < 5000 THEN
        new_stage := 4; -- Cultural language
    ELSE
        new_stage := 5; -- Meta-linguistic
    END IF;
    
    -- Adjust based on sophistication
    IF avg_complexity > 0.7 AND vocab_size > 20 THEN
        new_stage := LEAST(new_stage + 1, 5);
    END IF;
    
    -- Literacy also influences stage
    IF literacy_level > 0.5 THEN
        new_stage := LEAST(new_stage + 1, 5);
    END IF;
    
    -- Update if changed
    IF new_stage != current_stage THEN
        UPDATE linguistic_agents 
        SET linguistic_stage = new_stage, updated_at = NOW()
        WHERE agent_id = p_agent_id;
    END IF;
    
    RETURN new_stage;
END;
$$ LANGUAGE plpgsql;
```

### communication_trigger
```sql
-- Trigger to update linguistic metrics on new communications
CREATE OR REPLACE FUNCTION update_linguistic_metrics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update linguistic_agents metrics
    UPDATE linguistic_agents
    SET 
        total_communications = total_communications + 1,
        last_communication = NEW.timestamp,
        vocabulary_size = (
            SELECT COUNT(DISTINCT pattern_hash) 
            FROM communications 
            WHERE agent_id = NEW.agent_id
        ),
        average_pattern_complexity = (
            SELECT AVG(pattern_complexity)
            FROM communications 
            WHERE agent_id = NEW.agent_id
        ),
        updated_at = NOW()
    WHERE agent_id = NEW.agent_id;
    
    -- Update or insert dot_pattern record
    INSERT INTO dot_patterns (
        pattern_hash, dot_pattern, complexity, shannon_entropy,
        character_count, dot_count, has_newlines, has_spacing,
        created_by_agent, innovation_context
    ) VALUES (
        NEW.pattern_hash, NEW.dot_pattern, NEW.pattern_complexity,
        -- Calculate Shannon entropy here
        0.0, -- Placeholder, implement entropy calculation
        LENGTH(NEW.dot_pattern),
        LENGTH(NEW.dot_pattern) - LENGTH(REPLACE(NEW.dot_pattern, '•', '')),
        POSITION(E'\n' IN NEW.dot_pattern) > 0,
        POSITION(' ' IN NEW.dot_pattern) > 0,
        NEW.agent_id,
        jsonb_build_object('aura_context', NEW.aura_context, 'trigger', NEW.communication_trigger)
    ) ON CONFLICT (pattern_hash) DO UPDATE SET
        last_used = NEW.timestamp,
        total_usage_count = dot_patterns.total_usage_count + 1,
        updated_at = NOW();
    
    -- Update linguistic stage
    PERFORM update_linguistic_stage(NEW.agent_id);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER linguistic_metrics_update
    AFTER INSERT ON communications
    FOR EACH ROW EXECUTE FUNCTION update_linguistic_metrics();
```

## Research and Analytics Views

### language_family_analysis
```sql
-- Comprehensive language family analysis
CREATE MATERIALIZED VIEW language_family_analysis AS
SELECT 
    lf.id as family_id,
    lf.name as family_name,
    lf.emergence_timestamp,
    lf.member_count,
    
    -- Diversity metrics
    COUNT(DISTINCT dp.pattern_hash) as unique_patterns,
    AVG(dp.complexity) as avg_pattern_complexity,
    STDDEV(dp.complexity) as complexity_variance,
    
    -- Innovation metrics
    COUNT(*) FILTER (WHERE dp.pattern_generation = 1) as original_innovations,
    COUNT(*) FILTER (WHERE dp.pattern_generation > 1) as evolved_patterns,
    lf.innovation_rate,
    
    -- Usage patterns
    SUM(dp.total_usage_count) as total_family_communications,
    AVG(dp.adoption_rate) as avg_adoption_rate,
    
    -- Temporal activity
    COUNT(c.id) FILTER (WHERE c.timestamp > NOW() - INTERVAL '24 hours') as communications_24h,
    COUNT(c.id) FILTER (WHERE c.timestamp > NOW() - INTERVAL '7 days') as communications_7d,
    
    -- Cultural metrics
    AVG(lf.internal_cohesion) as family_cohesion,
    AVG(lf.external_influence) as family_influence

FROM language_families lf
LEFT JOIN linguistic_agents la ON lf.id = la.primary_language_family
LEFT JOIN communications c ON la.agent_id = c.agent_id
LEFT JOIN dot_patterns dp ON c.pattern_hash = dp.pattern_hash
GROUP BY lf.id, lf.name, lf.emergence_timestamp, lf.member_count, lf.innovation_rate, lf.internal_cohesion, lf.external_influence;

-- Refresh every hour
CREATE OR REPLACE FUNCTION refresh_linguistic_analytics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW language_family_analysis;
END;
$$ LANGUAGE plpgsql;
```

## Data Retention and Compression

### TimescaleDB Policies
```sql
-- Retention policies for linguistic data
SELECT add_retention_policy('communications', INTERVAL '1 year');
SELECT add_retention_policy('linguistic_interactions', INTERVAL '6 months');
SELECT add_retention_policy('rss_linguistic_influence', INTERVAL '6 months');

-- Compression policies
SELECT add_compression_policy('communications', INTERVAL '30 days');
SELECT add_compression_policy('linguistic_interactions', INTERVAL '7 days');
SELECT add_compression_policy('rss_linguistic_influence', INTERVAL '7 days');
```

## API Integration Points

### Agent Communication Endpoint Data
```sql
-- Query for /api/linguistic/agent/{id}/communications
SELECT 
    c.timestamp,
    c.dot_pattern,
    c.pattern_complexity,
    c.communication_trigger,
    c.is_innovation,
    c.response_count,
    c.aura_context
FROM communications c
WHERE c.agent_id = $1
ORDER BY c.timestamp DESC
LIMIT 50;
```

### Real-time Language Evolution Metrics
```sql
-- Query for /api/linguistic/evolution/metrics
SELECT 
    COUNT(*) as total_communications,
    COUNT(DISTINCT pattern_hash) as unique_patterns,
    AVG(pattern_complexity) as avg_complexity,
    COUNT(*) FILTER (WHERE is_innovation) as innovations_today,
    COUNT(DISTINCT agent_id) as active_communicators
FROM communications
WHERE timestamp > CURRENT_DATE;
```

### Pattern Analysis Endpoint
```sql
-- Query for /api/linguistic/patterns/analysis
SELECT 
    dp.dot_pattern,
    dp.complexity,
    dp.total_usage_count,
    dp.first_appearance,
    a.name as creator_name,
    a.archetype as creator_archetype,
    (
        SELECT jsonb_agg(DISTINCT communication_trigger)
        FROM communications c
        WHERE c.pattern_hash = dp.pattern_hash
    ) as usage_contexts
FROM dot_patterns dp
JOIN agents a ON dp.created_by_agent = a.id
ORDER BY dp.total_usage_count DESC
LIMIT 100;
```

---

## Extensibility Framework

### Plugin Architecture Support
```sql
-- Table for linguistic research plugins
CREATE TABLE linguistic_plugins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    
    -- Plugin configuration
    config_schema JSONB NOT NULL,
    analysis_functions JSONB NOT NULL,
    
    -- Research focus
    research_domain VARCHAR(50) NOT NULL, -- 'syntax', 'semantics', 'evolution', 'cultural'
    data_dependencies TEXT[] NOT NULL,
    
    -- Status
    active BOOLEAN DEFAULT true,
    last_execution TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Research Experiment Tracking
```sql
-- Track linguistic research experiments
CREATE TABLE linguistic_experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    hypothesis TEXT NOT NULL,
    
    -- Experiment parameters
    agent_selection_criteria JSONB NOT NULL,
    duration INTERVAL NOT NULL,
    variables_tracked TEXT[] NOT NULL,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'planned', -- planned, running, completed, failed
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    
    -- Results
    results_summary JSONB,
    statistical_significance FLOAT,
    conclusions TEXT,
    
    -- Metadata
    researcher_notes TEXT,
    created_by VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Installation and Initialization

### Setup Script
```sql
-- Initialize linguistic evolution schema
-- Run after core CHAOSTOWN schema is in place

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create all linguistic tables (include full schema here)
-- ... (tables from above)

-- Initialize default data
INSERT INTO linguistic_plugins (name, version, description, config_schema, analysis_functions, research_domain, data_dependencies) VALUES
('shannon_entropy_analyzer', '1.0', 'Calculate Shannon entropy for pattern complexity', '{}', '["calculate_entropy"]', 'syntax', '["communications"]'),
('social_learning_tracker', '1.0', 'Track pattern adoption and social influence', '{}', '["analyze_adoption", "track_influence"]', 'cultural', '["communications", "linguistic_interactions"]'),
('innovation_detector', '1.0', 'Identify and classify linguistic innovations', '{}', '["detect_innovations", "classify_patterns"]', 'evolution', '["dot_patterns", "communications"]');

-- Set up initial materialized view refresh
SELECT cron.schedule('refresh-linguistic-analytics', '0 * * * *', 'SELECT refresh_linguistic_analytics();');
```

---

*This schema creates a comprehensive framework for studying emergent language evolution while maintaining the alien semantic opacity that makes the system scientifically valuable. The architecture supports both real-time simulation and deep linguistic research.*

**Database designed for language genesis, optimized for alien thoughts.** 🔵🧠📊