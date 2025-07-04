# CHAOSTOWN Database - Linguistic Evolution

This directory contains the database migration and setup scripts for extending the CHAOSTOWN simulation with linguistic evolution capabilities.

## Overview

The linguistic evolution extension adds comprehensive language development tracking to the CHAOSTOWN simulation, enabling agents to develop emergent dot-based communication systems with full mathematical rigor and observability.

## Quick Setup

1. **Ensure CHAOSTOWN is running:**
   ```bash
   cd /Users/weixiangzhang/Local\ Dev/CHAOSTOWN
   docker compose up -d db
   ```

2. **Set database password:**
   ```bash
   export POSTGRES_PASSWORD=chaostown_password
   ```

3. **Run the setup:**
   ```bash
   ./database/setup_linguistic_evolution.sh setup
   ```

## Files

### Migration Scripts

- **`migrations/001_linguistic_evolution.sql`** - Complete database migration script
  - Creates all linguistic evolution tables
  - Sets up TimescaleDB hypertables for time-series data
  - Creates indexes, functions, triggers, and views
  - Includes verification and rollback procedures

### Setup Scripts

- **`setup_linguistic_evolution.sh`** - Interactive setup and management script
  - Automated dependency checking
  - Migration execution with verification
  - Status monitoring and rollback capabilities
  - Sample data creation

## Database Schema Extensions

### Core Tables

1. **`linguistic_agents`** - Extends agents with linguistic capabilities
   - Linguistic stage progression (1-5)
   - Vocabulary size and literacy metrics
   - Innovation tendencies and social influence
   - Internal semantic networks (opaque to humans)

2. **`communications`** - TimescaleDB hypertable for all agent communications
   - Dot pattern storage with complexity analysis
   - Aura context and communication triggers
   - Innovation tracking and success metrics
   - Vector embeddings for pattern analysis

3. **`dot_patterns`** - Registry of unique communication patterns
   - Mathematical complexity calculations
   - Shannon entropy and spatial analysis
   - Usage statistics and adoption metrics
   - Pattern evolution tracking

4. **`language_families`** - Emergent language groups and dialects
   - Family characteristics and founding agents
   - Mathematical diversity signatures
   - Social dynamics and cohesion metrics

5. **`linguistic_interactions`** - Communication-focused agent interactions
   - Pattern adoption and modification tracking
   - Learning outcomes and literacy changes
   - Social influence and relationship dynamics

6. **`rss_linguistic_influence`** - RSS feed impact on language development
   - Literacy acquisition through text exposure
   - Character recognition and word associations
   - Vibe extraction and aura modulation

### Supporting Infrastructure

- **Plugin Architecture** - `linguistic_plugins` table for research extensions
- **Experiment Tracking** - `linguistic_experiments` for research management
- **Analytics Views** - Real-time and materialized views for analysis
- **Scheduled Tasks** - Automated analytics refresh and maintenance

## Key Features

### Mathematical Rigor
- Shannon entropy calculation for pattern complexity
- Spatial analysis of 2D dot arrangements
- Linear trend analysis for development tracking
- Statistical significance testing for experiments

### Emergent Language Evolution
- Stage-based progression (Primal → Emotional → Conceptual → Cultural → Meta-linguistic)
- Innovation vs imitation dynamics
- Social learning and pattern adoption
- Literacy development through RSS exposure

### Observability Without Interpretation
- Complete communication logging and analysis
- Pattern complexity and diversity metrics
- Social network dynamics tracking
- **No human interpretation of semantic meanings**

### Production-Ready Infrastructure
- TimescaleDB time-series optimization
- Automated compression and retention policies
- Vector embedding support for future ML analysis
- Comprehensive indexing for performance

## Usage Commands

### Setup and Migration
```bash
# Complete setup
./setup_linguistic_evolution.sh setup

# Migration only
./setup_linguistic_evolution.sh migrate

# Check system status
./setup_linguistic_evolution.sh check
```

### Monitoring and Maintenance
```bash
# Show migration status
./setup_linguistic_evolution.sh status

# Create sample data for testing
./setup_linguistic_evolution.sh sample

# Emergency rollback
./setup_linguistic_evolution.sh rollback
```

### Direct Database Access
```bash
# Connect to database
docker exec -it chaostown-db-1 psql -U postgres -d chaostown

# View linguistic metrics
SELECT * FROM linguistic_evolution_metrics;

# Check pattern popularity
SELECT * FROM pattern_popularity LIMIT 10;

# Analyze language families
SELECT * FROM language_family_analysis;
```

## API Integration

The database schema provides complete support for the linguistic API endpoints:

### Real-time Queries
- `/api/linguistic/agent/{id}/communications` - Agent communication history
- `/api/linguistic/evolution/metrics` - System-wide language evolution metrics
- `/api/linguistic/patterns/analysis` - Pattern analysis and trends

### Research Endpoints
- `/api/linguistic/families` - Language family dynamics
- `/api/linguistic/experiments` - Research experiment management
- `/api/linguistic/plugins` - Plugin system integration

## Performance Considerations

### TimescaleDB Optimization
- Automatic partitioning by time for communications
- Compression policies for historical data
- Efficient time-range queries for analytics

### Indexing Strategy
- GIN indexes for JSONB aura context queries
- Composite indexes for agent-pattern relationships
- Vector indexes for future semantic similarity queries

### Data Retention
- 1 year retention for communications data
- 6 months retention for interaction data
- Configurable compression policies

## Mathematical Validation

The system includes comprehensive mathematical validation:

```sql
-- Verify Shannon entropy calculations
SELECT pattern, calculate_shannon_entropy(pattern) FROM dot_patterns;

-- Check complexity evolution trends
SELECT agent_id, avg(pattern_complexity), 
       count(*) as communications
FROM communications 
GROUP BY agent_id;

-- Analyze innovation rates
SELECT is_innovation, count(*) as pattern_count
FROM communications 
GROUP BY is_innovation;
```

## Research Applications

### Linguistic Evolution Studies
- Pattern complexity evolution over time
- Social learning vs individual innovation
- Literacy impact on communication sophistication
- Cultural transmission dynamics

### Emergence Research
- Language family formation and splits
- Dialect variance development
- Innovation propagation patterns
- Environmental influence on communication

### AI/ML Integration
- Vector embeddings for pattern similarity
- Social network analysis for influence tracking
- Predictive modeling for language evolution
- Unsupervised pattern clustering

## Troubleshooting

### Common Issues

1. **Connection Errors**
   ```bash
   # Check if database is running
   docker compose ps db
   
   # Check connection
   docker exec -it chaostown-db-1 pg_isready
   ```

2. **Migration Failures**
   ```bash
   # Check migration log
   cat migration.log
   
   # Verify extensions
   docker exec -it chaostown-db-1 psql -U postgres -c "\dx"
   ```

3. **Performance Issues**
   ```bash
   # Check TimescaleDB status
   SELECT * FROM timescaledb_information.hypertables;
   
   # Monitor query performance
   SELECT * FROM pg_stat_statements ORDER BY total_time DESC;
   ```

### Recovery Procedures

1. **Migration Rollback**
   ```bash
   ./setup_linguistic_evolution.sh rollback
   ```

2. **Partial Recovery**
   ```sql
   -- Drop specific problematic tables
   DROP TABLE IF EXISTS communications CASCADE;
   
   -- Re-run specific parts of migration
   \i migrations/001_linguistic_evolution.sql
   ```

3. **Complete Reset**
   ```bash
   # Remove all linguistic data
   docker exec -it chaostown-db-1 psql -U postgres -d chaostown -c "SELECT rollback_linguistic_migration();"
   
   # Re-run migration
   ./setup_linguistic_evolution.sh migrate
   ```

## Development and Testing

### Sample Data Generation
```bash
# Create test agents and communications
./setup_linguistic_evolution.sh sample

# Run linguistic agent test
cd sim-engine
python3 linguistic_agent.py
```

### Schema Validation
```sql
-- Verify all tables exist
SELECT * FROM verify_linguistic_migration();

-- Check constraints
SELECT conname, contype, confupdtype, confdeltype 
FROM pg_constraint 
WHERE conrelid IN (
    SELECT oid FROM pg_class 
    WHERE relname LIKE 'linguistic_%' OR relname IN ('communications', 'dot_patterns')
);
```

## Integration with CHAOSTOWN

The linguistic evolution system seamlessly integrates with the existing CHAOSTOWN architecture:

- **Agents**: Extended with linguistic capabilities through `linguistic_agents` table
- **Simulation Engine**: Compatible with existing tick-based simulation
- **API**: New endpoints integrate with existing FastAPI structure
- **Dashboard**: Ready for linguistic metrics visualization
- **Monitoring**: TimescaleDB integration with existing Grafana dashboards

The system maintains full backward compatibility while adding comprehensive language evolution capabilities to the simulation.