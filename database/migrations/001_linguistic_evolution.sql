-- ======================================================================
-- CHAOSTOWN Linguistic Evolution Database Migration
-- Version: 001
-- Description: Extends CHAOSTOWN database with linguistic evolution capabilities
-- Author: Claude PostgreSQL Database Administrator
-- Date: 2025-07-04
-- ======================================================================

-- MIGRATION HEADER
-- This migration extends the existing CHAOSTOWN database schema with
-- linguistic evolution tables, indexes, functions, and triggers.
-- It maintains compatibility with existing TimescaleDB hypertables.

BEGIN;

-- ======================================================================
-- ENABLE REQUIRED EXTENSIONS
-- ======================================================================

-- Enable vector extension for embeddings (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable TimescaleDB (if not already enabled)
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Enable pg_cron for scheduled tasks (if not already enabled)
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- ======================================================================
-- CREATE LINGUISTIC EVOLUTION TABLES
-- ======================================================================

-- Extension of core agents table for linguistic capabilities
CREATE TABLE IF NOT EXISTS linguistic_agents (
    agent_id UUID PRIMARY KEY REFERENCES agents(id) ON DELETE CASCADE,
    
    -- Linguistic development metrics
    linguistic_stage INTEGER NOT NULL DEFAULT 1,
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
    primary_language_family UUID,
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

-- All agent communications with full context
CREATE TABLE IF NOT EXISTS communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Communication content
    dot_pattern TEXT NOT NULL,
    pattern_complexity FLOAT NOT NULL,
    pattern_hash VARCHAR(64) NOT NULL,
    
    -- Context and triggers
    aura_context JSONB NOT NULL,
    social_context JSONB NOT NULL,
    internal_pressure FLOAT NOT NULL,
    communication_trigger VARCHAR(50) NOT NULL,
    
    -- Innovation tracking
    is_innovation BOOLEAN NOT NULL DEFAULT false,
    pattern_first_use BOOLEAN NOT NULL DEFAULT false,
    innovation_source VARCHAR(20),
    
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
    
    -- Vector embeddings for semantic analysis
    pattern_embedding VECTOR(384),
    context_embedding VECTOR(384),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Registry of all unique dot patterns and their evolution
CREATE TABLE IF NOT EXISTS dot_patterns (
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
    parent_pattern_id UUID REFERENCES dot_patterns(id),
    child_patterns_count INTEGER NOT NULL DEFAULT 0,
    pattern_generation INTEGER NOT NULL DEFAULT 1,
    
    -- Adoption metrics
    adoption_rate FLOAT NOT NULL DEFAULT 0.0,
    success_rate FLOAT NOT NULL DEFAULT 0.0,
    cultural_penetration FLOAT NOT NULL DEFAULT 0.0,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Emergent language groups and dialects
CREATE TABLE IF NOT EXISTS language_families (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    
    -- Family characteristics
    founding_agents UUID[] NOT NULL,
    characteristic_patterns TEXT[] NOT NULL,
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
    
    -- Research notes
    research_notes TEXT,
    dominant_communication_triggers JSONB,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Special interactions focused on communication
CREATE TABLE IF NOT EXISTS linguistic_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    communication_id UUID NOT NULL REFERENCES communications(id),
    responding_agent_id UUID NOT NULL REFERENCES agents(id),
    tick_number BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Interaction type
    interaction_type VARCHAR(50) NOT NULL,
    
    -- Response details
    response_pattern TEXT,
    response_delay_ticks INTEGER NOT NULL DEFAULT 0,
    understanding_indicator FLOAT,
    
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

-- Track how RSS feeds influence language development
CREATE TABLE IF NOT EXISTS rss_linguistic_influence (
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

-- Plugin architecture support
CREATE TABLE IF NOT EXISTS linguistic_plugins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    
    -- Plugin configuration
    config_schema JSONB NOT NULL,
    analysis_functions JSONB NOT NULL,
    
    -- Research focus
    research_domain VARCHAR(50) NOT NULL,
    data_dependencies TEXT[] NOT NULL,
    
    -- Status
    active BOOLEAN DEFAULT true,
    last_execution TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Track linguistic research experiments
CREATE TABLE IF NOT EXISTS linguistic_experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    hypothesis TEXT NOT NULL,
    
    -- Experiment parameters
    agent_selection_criteria JSONB NOT NULL,
    duration INTERVAL NOT NULL,
    variables_tracked TEXT[] NOT NULL,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
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

-- ======================================================================
-- CREATE TIMESCALEDB HYPERTABLES
-- ======================================================================

-- Convert time-series tables to TimescaleDB hypertables
SELECT create_hypertable('communications', 'timestamp', if_not_exists => true);
SELECT create_hypertable('linguistic_interactions', 'timestamp', if_not_exists => true);
SELECT create_hypertable('rss_linguistic_influence', 'timestamp', if_not_exists => true);

-- ======================================================================
-- CREATE INDEXES FOR PERFORMANCE
-- ======================================================================

-- Indexes for linguistic_agents
CREATE INDEX IF NOT EXISTS idx_linguistic_agents_stage ON linguistic_agents(linguistic_stage);
CREATE INDEX IF NOT EXISTS idx_linguistic_agents_vocabulary ON linguistic_agents(vocabulary_size);
CREATE INDEX IF NOT EXISTS idx_linguistic_agents_literacy ON linguistic_agents(literacy_level);
CREATE INDEX IF NOT EXISTS idx_linguistic_agents_family ON linguistic_agents(primary_language_family);

-- Indexes for communications
CREATE INDEX IF NOT EXISTS idx_communications_agent ON communications(agent_id);
CREATE INDEX IF NOT EXISTS idx_communications_pattern_hash ON communications(pattern_hash);
CREATE INDEX IF NOT EXISTS idx_communications_complexity ON communications(pattern_complexity);
CREATE INDEX IF NOT EXISTS idx_communications_innovation ON communications(is_innovation);
CREATE INDEX IF NOT EXISTS idx_communications_trigger ON communications(communication_trigger);
CREATE INDEX IF NOT EXISTS idx_communications_tick ON communications(tick_number);

-- GIN index for aura context queries
CREATE INDEX IF NOT EXISTS idx_communications_aura_gin ON communications USING GIN (aura_context);

-- Indexes for dot_patterns
CREATE INDEX IF NOT EXISTS idx_dot_patterns_complexity ON dot_patterns(complexity);
CREATE INDEX IF NOT EXISTS idx_dot_patterns_usage ON dot_patterns(total_usage_count);
CREATE INDEX IF NOT EXISTS idx_dot_patterns_creator ON dot_patterns(created_by_agent);
CREATE INDEX IF NOT EXISTS idx_dot_patterns_generation ON dot_patterns(pattern_generation);
CREATE INDEX IF NOT EXISTS idx_dot_patterns_first_appearance ON dot_patterns(first_appearance);

-- Indexes for language_families
CREATE INDEX IF NOT EXISTS idx_language_families_emergence ON language_families(emergence_timestamp);
CREATE INDEX IF NOT EXISTS idx_language_families_members ON language_families(member_count);
CREATE INDEX IF NOT EXISTS idx_language_families_parent ON language_families(parent_family_id);

-- Indexes for linguistic_interactions
CREATE INDEX IF NOT EXISTS idx_linguistic_interactions_comm ON linguistic_interactions(communication_id);
CREATE INDEX IF NOT EXISTS idx_linguistic_interactions_agent ON linguistic_interactions(responding_agent_id);
CREATE INDEX IF NOT EXISTS idx_linguistic_interactions_type ON linguistic_interactions(interaction_type);

-- Indexes for rss_linguistic_influence
CREATE INDEX IF NOT EXISTS idx_rss_influence_agent ON rss_linguistic_influence(agent_id);
CREATE INDEX IF NOT EXISTS idx_rss_influence_content_hash ON rss_linguistic_influence(rss_content_hash);
CREATE INDEX IF NOT EXISTS idx_rss_influence_literacy_delta ON rss_linguistic_influence(literacy_delta);

-- ======================================================================
-- CREATE FUNCTIONS FOR LINGUISTIC PROCESSING
-- ======================================================================

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
    
    -- Stage progression logic
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

-- Function to calculate Shannon entropy for patterns
CREATE OR REPLACE FUNCTION calculate_shannon_entropy(pattern TEXT)
RETURNS FLOAT AS $$
DECLARE
    char_count INTEGER;
    total_chars INTEGER;
    entropy FLOAT := 0.0;
    max_entropy FLOAT;
    char_prob FLOAT;
    distinct_chars INTEGER;
BEGIN
    IF pattern IS NULL OR LENGTH(pattern) = 0 THEN
        RETURN 0.0;
    END IF;
    
    total_chars := LENGTH(pattern);
    
    -- Count distinct characters
    SELECT COUNT(DISTINCT c.char) INTO distinct_chars
    FROM (SELECT SUBSTRING(pattern FROM i FOR 1) as char
          FROM generate_series(1, total_chars) i) c;
    
    -- Calculate entropy for each character
    FOR char_count IN 
        SELECT COUNT(*) 
        FROM (SELECT SUBSTRING(pattern FROM i FOR 1) as char
              FROM generate_series(1, total_chars) i) c
        GROUP BY c.char
    LOOP
        char_prob := char_count::FLOAT / total_chars;
        entropy := entropy - (char_prob * log(2, char_prob));
    END LOOP;
    
    -- Normalize to 0-1 range
    max_entropy := log(2, distinct_chars);
    IF max_entropy > 0 THEN
        entropy := entropy / max_entropy;
    END IF;
    
    RETURN LEAST(entropy, 1.0);
END;
$$ LANGUAGE plpgsql;

-- Function to update linguistic metrics on new communications
CREATE OR REPLACE FUNCTION update_linguistic_metrics()
RETURNS TRIGGER AS $$
DECLARE
    pattern_exists BOOLEAN;
    new_entropy FLOAT;
BEGIN
    -- Calculate Shannon entropy for the pattern
    new_entropy := calculate_shannon_entropy(NEW.dot_pattern);
    
    -- Update linguistic_agents metrics
    INSERT INTO linguistic_agents (agent_id, total_communications, last_communication, updated_at)
    VALUES (NEW.agent_id, 1, NEW.timestamp, NOW())
    ON CONFLICT (agent_id) DO UPDATE SET
        total_communications = linguistic_agents.total_communications + 1,
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
        updated_at = NOW();
    
    -- Update first_communication if this is the first
    UPDATE linguistic_agents 
    SET first_communication = NEW.timestamp
    WHERE agent_id = NEW.agent_id 
    AND first_communication IS NULL;
    
    -- Update or insert dot_pattern record
    INSERT INTO dot_patterns (
        pattern_hash, dot_pattern, complexity, shannon_entropy,
        character_count, dot_count, has_newlines, has_spacing,
        created_by_agent, innovation_context
    ) VALUES (
        NEW.pattern_hash, NEW.dot_pattern, NEW.pattern_complexity,
        new_entropy,
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

-- Function to refresh linguistic analytics
CREATE OR REPLACE FUNCTION refresh_linguistic_analytics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW IF EXISTS language_family_analysis;
    REFRESH MATERIALIZED VIEW IF EXISTS linguistic_evolution_metrics;
END;
$$ LANGUAGE plpgsql;

-- ======================================================================
-- CREATE TRIGGERS
-- ======================================================================

-- Trigger to update linguistic metrics on new communications
CREATE TRIGGER linguistic_metrics_update
    AFTER INSERT ON communications
    FOR EACH ROW EXECUTE FUNCTION update_linguistic_metrics();

-- ======================================================================
-- CREATE VIEWS FOR ANALYSIS
-- ======================================================================

-- Real-time view of language evolution metrics
CREATE OR REPLACE VIEW linguistic_evolution_metrics AS
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
WHERE a.death_time IS NULL
GROUP BY la.agent_id, a.name, a.archetype, la.linguistic_stage, la.vocabulary_size, 
         la.literacy_level, la.total_communications, lf.name, la.dialect_variance, 
         la.last_communication, la.average_pattern_complexity, la.complexity_growth_rate;

-- View of most popular/successful patterns
CREATE OR REPLACE VIEW pattern_popularity AS
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

-- ======================================================================
-- CREATE MATERIALIZED VIEWS
-- ======================================================================

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
    lf.internal_cohesion as family_cohesion,
    lf.external_influence as family_influence

FROM language_families lf
LEFT JOIN linguistic_agents la ON lf.id = la.primary_language_family
LEFT JOIN communications c ON la.agent_id = c.agent_id
LEFT JOIN dot_patterns dp ON c.pattern_hash = dp.pattern_hash
GROUP BY lf.id, lf.name, lf.emergence_timestamp, lf.member_count, lf.innovation_rate, lf.internal_cohesion, lf.external_influence;

-- ======================================================================
-- SETUP TIMESCALEDB POLICIES
-- ======================================================================

-- Retention policies for linguistic data
SELECT add_retention_policy('communications', INTERVAL '1 year', if_not_exists => true);
SELECT add_retention_policy('linguistic_interactions', INTERVAL '6 months', if_not_exists => true);
SELECT add_retention_policy('rss_linguistic_influence', INTERVAL '6 months', if_not_exists => true);

-- Compression policies
SELECT add_compression_policy('communications', INTERVAL '30 days', if_not_exists => true);
SELECT add_compression_policy('linguistic_interactions', INTERVAL '7 days', if_not_exists => true);
SELECT add_compression_policy('rss_linguistic_influence', INTERVAL '7 days', if_not_exists => true);

-- ======================================================================
-- INITIALIZE DEFAULT DATA
-- ======================================================================

-- Add foreign key constraint after language_families table exists
ALTER TABLE linguistic_agents 
ADD CONSTRAINT fk_linguistic_agents_family 
FOREIGN KEY (primary_language_family) REFERENCES language_families(id);

-- Initialize default linguistic plugins
INSERT INTO linguistic_plugins (name, version, description, config_schema, analysis_functions, research_domain, data_dependencies) VALUES
('shannon_entropy_analyzer', '1.0', 'Calculate Shannon entropy for pattern complexity', '{}', '["calculate_entropy"]', 'syntax', '["communications"]'),
('social_learning_tracker', '1.0', 'Track pattern adoption and social influence', '{}', '["analyze_adoption", "track_influence"]', 'cultural', '["communications", "linguistic_interactions"]'),
('innovation_detector', '1.0', 'Identify and classify linguistic innovations', '{}', '["detect_innovations", "classify_patterns"]', 'evolution', '["dot_patterns", "communications"]')
ON CONFLICT (name) DO NOTHING;

-- ======================================================================
-- SETUP SCHEDULED TASKS
-- ======================================================================

-- Schedule materialized view refresh every hour
SELECT cron.schedule(
    'refresh-linguistic-analytics',
    '0 * * * *',
    'SELECT refresh_linguistic_analytics();'
) WHERE NOT EXISTS (
    SELECT 1 FROM cron.job WHERE jobname = 'refresh-linguistic-analytics'
);

-- ======================================================================
-- MIGRATION VERIFICATION
-- ======================================================================

-- Function to verify migration success
CREATE OR REPLACE FUNCTION verify_linguistic_migration()
RETURNS TABLE(
    table_name TEXT,
    exists BOOLEAN,
    row_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'linguistic_agents'::TEXT,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'linguistic_agents'),
        (SELECT COUNT(*) FROM linguistic_agents);
    
    RETURN QUERY
    SELECT 
        'communications'::TEXT,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'communications'),
        (SELECT COUNT(*) FROM communications);
    
    RETURN QUERY
    SELECT 
        'dot_patterns'::TEXT,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'dot_patterns'),
        (SELECT COUNT(*) FROM dot_patterns);
    
    RETURN QUERY
    SELECT 
        'language_families'::TEXT,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'language_families'),
        (SELECT COUNT(*) FROM language_families);
    
    RETURN QUERY
    SELECT 
        'linguistic_interactions'::TEXT,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'linguistic_interactions'),
        (SELECT COUNT(*) FROM linguistic_interactions);
    
    RETURN QUERY
    SELECT 
        'rss_linguistic_influence'::TEXT,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'rss_linguistic_influence'),
        (SELECT COUNT(*) FROM rss_linguistic_influence);
END;
$$ LANGUAGE plpgsql;

-- ======================================================================
-- ROLLBACK PROCEDURES
-- ======================================================================

-- Function to rollback linguistic migration (for emergency use)
CREATE OR REPLACE FUNCTION rollback_linguistic_migration()
RETURNS TEXT AS $$
BEGIN
    -- Drop tables in reverse dependency order
    DROP TABLE IF EXISTS linguistic_experiments CASCADE;
    DROP TABLE IF EXISTS linguistic_plugins CASCADE;
    DROP TABLE IF EXISTS rss_linguistic_influence CASCADE;
    DROP TABLE IF EXISTS linguistic_interactions CASCADE;
    DROP TABLE IF EXISTS language_families CASCADE;
    DROP TABLE IF EXISTS dot_patterns CASCADE;
    DROP TABLE IF EXISTS communications CASCADE;
    DROP TABLE IF EXISTS linguistic_agents CASCADE;
    
    -- Drop functions
    DROP FUNCTION IF EXISTS verify_linguistic_migration() CASCADE;
    DROP FUNCTION IF EXISTS update_linguistic_stage(UUID) CASCADE;
    DROP FUNCTION IF EXISTS calculate_shannon_entropy(TEXT) CASCADE;
    DROP FUNCTION IF EXISTS update_linguistic_metrics() CASCADE;
    DROP FUNCTION IF EXISTS refresh_linguistic_analytics() CASCADE;
    
    -- Drop views
    DROP VIEW IF EXISTS linguistic_evolution_metrics CASCADE;
    DROP VIEW IF EXISTS pattern_popularity CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS language_family_analysis CASCADE;
    
    -- Remove scheduled job
    DELETE FROM cron.job WHERE jobname = 'refresh-linguistic-analytics';
    
    RETURN 'Linguistic migration rolled back successfully';
END;
$$ LANGUAGE plpgsql;

-- ======================================================================
-- COMMIT MIGRATION
-- ======================================================================

-- Verify migration before committing
DO $$
DECLARE
    verification_result RECORD;
    failed_tables TEXT[] := '{}';
BEGIN
    FOR verification_result IN SELECT * FROM verify_linguistic_migration() LOOP
        IF NOT verification_result.exists THEN
            failed_tables := array_append(failed_tables, verification_result.table_name);
        END IF;
    END LOOP;
    
    IF array_length(failed_tables, 1) > 0 THEN
        RAISE EXCEPTION 'Migration failed: tables not created: %', array_to_string(failed_tables, ', ');
    END IF;
    
    RAISE NOTICE 'Linguistic evolution migration completed successfully!';
END;
$$;

COMMIT;

-- ======================================================================
-- POST-MIGRATION NOTES
-- ======================================================================

-- Migration completed successfully
-- 
-- Tables created:
-- - linguistic_agents (extends agents with linguistic capabilities)
-- - communications (TimescaleDB hypertable for all communications)
-- - dot_patterns (registry of unique patterns)
-- - language_families (emergent language groups)
-- - linguistic_interactions (communication-focused interactions)
-- - rss_linguistic_influence (RSS feed impact tracking)
-- - linguistic_plugins (plugin architecture support)
-- - linguistic_experiments (research experiment tracking)
--
-- Functions created:
-- - update_linguistic_stage() - Stage progression logic
-- - calculate_shannon_entropy() - Pattern complexity calculation
-- - update_linguistic_metrics() - Automatic metric updates
-- - refresh_linguistic_analytics() - Scheduled analytics refresh
-- - verify_linguistic_migration() - Migration verification
-- - rollback_linguistic_migration() - Emergency rollback
--
-- Views created:
-- - linguistic_evolution_metrics - Real-time language evolution view
-- - pattern_popularity - Popular patterns analysis
-- - language_family_analysis - Comprehensive family analysis (materialized)
--
-- Scheduled tasks:
-- - Hourly refresh of linguistic analytics
--
-- TimescaleDB policies:
-- - Retention policies for time-series data
-- - Compression policies for performance
--
-- The migration is complete and ready for use with the CHAOSTOWN
-- linguistic evolution system.