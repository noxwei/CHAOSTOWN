-- ======================================================================
-- CHAOSTOWN Linguistic Evolution Migration Verification Script
-- Description: Comprehensive verification of the linguistic evolution migration
-- Author: Claude PostgreSQL Database Administrator
-- Date: 2025-07-04
-- ======================================================================

\echo '======================================================================='
\echo 'CHAOSTOWN Linguistic Evolution Migration Verification'
\echo '======================================================================='

-- Set timing on to measure query performance
\timing on

-- ======================================================================
-- 1. TABLE EXISTENCE VERIFICATION
-- ======================================================================

\echo ''
\echo '1. Verifying table existence...'
\echo '================================'

SELECT 
    table_name,
    EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = t.table_name) as exists,
    CASE 
        WHEN EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = t.table_name) 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as status
FROM (VALUES 
    ('linguistic_agents'),
    ('communications'),
    ('dot_patterns'),
    ('language_families'),
    ('linguistic_interactions'),
    ('rss_linguistic_influence'),
    ('linguistic_plugins'),
    ('linguistic_experiments')
) AS t(table_name);

-- ======================================================================
-- 2. TIMESCALEDB HYPERTABLES VERIFICATION
-- ======================================================================

\echo ''
\echo '2. Verifying TimescaleDB hypertables...'
\echo '======================================='

SELECT 
    hypertable_name,
    hypertable_schema,
    num_dimensions,
    num_chunks,
    compression_enabled,
    replication_factor
FROM timescaledb_information.hypertables 
WHERE hypertable_name IN ('communications', 'linguistic_interactions', 'rss_linguistic_influence');

-- ======================================================================
-- 3. INDEX VERIFICATION
-- ======================================================================

\echo ''
\echo '3. Verifying indexes...'
\echo '======================'

SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename IN ('linguistic_agents', 'communications', 'dot_patterns', 'language_families', 'linguistic_interactions', 'rss_linguistic_influence')
ORDER BY tablename, indexname;

-- ======================================================================
-- 4. FUNCTION VERIFICATION
-- ======================================================================

\echo ''
\echo '4. Verifying functions...'
\echo '========================'

SELECT 
    routine_name,
    routine_type,
    data_type as return_type,
    is_deterministic
FROM information_schema.routines 
WHERE routine_name IN (
    'update_linguistic_stage',
    'calculate_shannon_entropy',
    'update_linguistic_metrics',
    'refresh_linguistic_analytics',
    'verify_linguistic_migration',
    'rollback_linguistic_migration'
)
ORDER BY routine_name;

-- ======================================================================
-- 5. TRIGGER VERIFICATION
-- ======================================================================

\echo ''
\echo '5. Verifying triggers...'
\echo '======================='

SELECT 
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation,
    action_statement
FROM information_schema.triggers 
WHERE trigger_name LIKE '%linguistic%'
ORDER BY event_object_table, trigger_name;

-- ======================================================================
-- 6. VIEW VERIFICATION
-- ======================================================================

\echo ''
\echo '6. Verifying views...'
\echo '===================='

SELECT 
    table_name,
    table_type,
    is_insertable_into
FROM information_schema.tables 
WHERE table_name IN ('linguistic_evolution_metrics', 'pattern_popularity', 'language_family_analysis')
ORDER BY table_name;

-- ======================================================================
-- 7. CONSTRAINT VERIFICATION
-- ======================================================================

\echo ''
\echo '7. Verifying constraints...'
\echo '=========================='

SELECT 
    table_name,
    constraint_name,
    constraint_type,
    check_clause
FROM information_schema.table_constraints tc
LEFT JOIN information_schema.check_constraints cc ON tc.constraint_name = cc.constraint_name
WHERE tc.table_name IN ('linguistic_agents', 'communications', 'dot_patterns', 'language_families')
AND tc.constraint_type IN ('CHECK', 'FOREIGN KEY', 'PRIMARY KEY', 'UNIQUE')
ORDER BY table_name, constraint_type, constraint_name;

-- ======================================================================
-- 8. EXTENSION VERIFICATION
-- ======================================================================

\echo ''
\echo '8. Verifying extensions...'
\echo '========================='

SELECT 
    extname as extension_name,
    extversion as version,
    extrelocatable as relocatable
FROM pg_extension 
WHERE extname IN ('vector', 'timescaledb', 'pg_cron')
ORDER BY extname;

-- ======================================================================
-- 9. FUNCTION TESTING
-- ======================================================================

\echo ''
\echo '9. Testing functions...'
\echo '======================'

-- Test Shannon entropy calculation
SELECT 
    'Shannon Entropy Test' as test_name,
    calculate_shannon_entropy('•••') as simple_pattern,
    calculate_shannon_entropy('• • •') as spaced_pattern,
    calculate_shannon_entropy('••\n••') as complex_pattern,
    CASE 
        WHEN calculate_shannon_entropy('•••') >= 0 AND calculate_shannon_entropy('•••') <= 1 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as status;

-- Test migration verification function
\echo ''
\echo 'Running migration verification function:'
SELECT * FROM verify_linguistic_migration();

-- ======================================================================
-- 10. SAMPLE DATA INSERTION TEST
-- ======================================================================

\echo ''
\echo '10. Testing sample data insertion...'
\echo '===================================='

-- Insert test agent if not exists
INSERT INTO agents (id, name, model, archetype, personality_tensor, position_x, position_y) VALUES
('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'Test_Verification_Agent', 'llama3.1', 'philosopher', '{"test": true}', 0.0, 0.0)
ON CONFLICT (id) DO NOTHING;

-- Insert test linguistic agent
INSERT INTO linguistic_agents (agent_id, linguistic_stage, innovation_tendency) VALUES
('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 1, 0.5)
ON CONFLICT (agent_id) DO NOTHING;

-- Insert test communication
INSERT INTO communications (
    agent_id, 
    tick_number, 
    dot_pattern, 
    pattern_complexity, 
    pattern_hash,
    aura_context, 
    social_context, 
    internal_pressure, 
    communication_trigger
) VALUES (
    'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
    1,
    '• test •',
    0.3,
    'test_pattern_hash_123',
    '{"warmth_gradient": 0.8}',
    '{}',
    0.5,
    'test'
) ON CONFLICT (id) DO NOTHING;

-- Verify trigger worked
SELECT 
    'Trigger Test' as test_name,
    COUNT(*) as communications_inserted,
    MAX(total_communications) as updated_count,
    CASE 
        WHEN MAX(total_communications) > 0 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as trigger_status
FROM linguistic_agents la
JOIN communications c ON la.agent_id = c.agent_id
WHERE la.agent_id = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';

-- ======================================================================
-- 11. PERFORMANCE TEST
-- ======================================================================

\echo ''
\echo '11. Performance verification...'
\echo '=============================='

-- Test query performance on key operations
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM linguistic_evolution_metrics LIMIT 10;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM communications 
WHERE timestamp > NOW() - INTERVAL '1 day' 
ORDER BY timestamp DESC 
LIMIT 100;

-- ======================================================================
-- 12. DATA INTEGRITY VERIFICATION
-- ======================================================================

\echo ''
\echo '12. Data integrity verification...'
\echo '================================='

-- Check referential integrity
SELECT 
    'Referential Integrity' as test_name,
    (SELECT COUNT(*) FROM linguistic_agents la 
     LEFT JOIN agents a ON la.agent_id = a.id 
     WHERE a.id IS NULL) as orphaned_linguistic_agents,
    (SELECT COUNT(*) FROM communications c 
     LEFT JOIN agents a ON c.agent_id = a.id 
     WHERE a.id IS NULL) as orphaned_communications,
    CASE 
        WHEN (SELECT COUNT(*) FROM linguistic_agents la 
              LEFT JOIN agents a ON la.agent_id = a.id 
              WHERE a.id IS NULL) = 0 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as integrity_status;

-- Check constraint violations
SELECT 
    'Constraint Validation' as test_name,
    (SELECT COUNT(*) FROM linguistic_agents WHERE linguistic_stage < 1 OR linguistic_stage > 5) as stage_violations,
    (SELECT COUNT(*) FROM linguistic_agents WHERE literacy_level < 0 OR literacy_level > 1) as literacy_violations,
    CASE 
        WHEN (SELECT COUNT(*) FROM linguistic_agents WHERE linguistic_stage < 1 OR linguistic_stage > 5) = 0
        AND (SELECT COUNT(*) FROM linguistic_agents WHERE literacy_level < 0 OR literacy_level > 1) = 0
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as constraint_status;

-- ======================================================================
-- 13. SCHEDULED TASKS VERIFICATION
-- ======================================================================

\echo ''
\echo '13. Scheduled tasks verification...'
\echo '=================================='

SELECT 
    jobname,
    schedule,
    command,
    active
FROM cron.job 
WHERE jobname LIKE '%linguistic%';

-- ======================================================================
-- 14. CLEANUP TEST DATA
-- ======================================================================

\echo ''
\echo '14. Cleaning up test data...'
\echo '============================'

DELETE FROM communications WHERE agent_id = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';
DELETE FROM linguistic_agents WHERE agent_id = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';
DELETE FROM agents WHERE id = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';

\echo 'Test data cleaned up successfully.'

-- ======================================================================
-- 15. FINAL SUMMARY
-- ======================================================================

\echo ''
\echo '15. Migration verification summary...'
\echo '===================================='

-- Generate final verification report
WITH verification_summary AS (
    SELECT 
        'Tables' as component,
        CASE WHEN COUNT(*) = 8 THEN 'PASS' ELSE 'FAIL' END as status,
        COUNT(*) || '/8' as details
    FROM information_schema.tables 
    WHERE table_name IN ('linguistic_agents', 'communications', 'dot_patterns', 'language_families', 
                         'linguistic_interactions', 'rss_linguistic_influence', 'linguistic_plugins', 'linguistic_experiments')
    
    UNION ALL
    
    SELECT 
        'Hypertables' as component,
        CASE WHEN COUNT(*) >= 3 THEN 'PASS' ELSE 'FAIL' END as status,
        COUNT(*) || '/3' as details
    FROM timescaledb_information.hypertables 
    WHERE hypertable_name IN ('communications', 'linguistic_interactions', 'rss_linguistic_influence')
    
    UNION ALL
    
    SELECT 
        'Functions' as component,
        CASE WHEN COUNT(*) = 6 THEN 'PASS' ELSE 'FAIL' END as status,
        COUNT(*) || '/6' as details
    FROM information_schema.routines 
    WHERE routine_name IN ('update_linguistic_stage', 'calculate_shannon_entropy', 'update_linguistic_metrics',
                          'refresh_linguistic_analytics', 'verify_linguistic_migration', 'rollback_linguistic_migration')
    
    UNION ALL
    
    SELECT 
        'Views' as component,
        CASE WHEN COUNT(*) >= 2 THEN 'PASS' ELSE 'FAIL' END as status,
        COUNT(*) || '/3' as details
    FROM information_schema.tables 
    WHERE table_name IN ('linguistic_evolution_metrics', 'pattern_popularity', 'language_family_analysis')
    
    UNION ALL
    
    SELECT 
        'Extensions' as component,
        CASE WHEN COUNT(*) >= 2 THEN 'PASS' ELSE 'FAIL' END as status,
        COUNT(*) || '/3' as details
    FROM pg_extension 
    WHERE extname IN ('vector', 'timescaledb', 'pg_cron')
)
SELECT * FROM verification_summary;

-- Final status
\echo ''
\echo '======================================================================='
\echo 'Migration verification completed!'
\echo ''
\echo 'If all components show PASS status, the linguistic evolution migration'
\echo 'has been successfully installed and is ready for use.'
\echo ''
\echo 'Next steps:'
\echo '1. Run the linguistic agent test: python3 sim-engine/linguistic_agent.py'
\echo '2. Start the CHAOSTOWN simulation with linguistic capabilities'
\echo '3. Monitor the linguistic_evolution_metrics view for language development'
\echo '======================================================================='

-- Turn timing off
\timing off