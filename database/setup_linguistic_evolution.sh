#!/bin/bash

# ======================================================================
# CHAOSTOWN Linguistic Evolution Database Setup Script
# Version: 1.0
# Description: Setup script for linguistic evolution database migration
# Author: Claude PostgreSQL Database Administrator
# Date: 2025-07-04
# ======================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="${POSTGRES_DB:-chaostown}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
MIGRATION_FILE="./migrations/001_linguistic_evolution.sql"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v psql &> /dev/null; then
        log_error "psql is not installed. Please install PostgreSQL client."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        log_warning "Docker not found. Make sure PostgreSQL is running manually."
    fi
    
    log_success "Dependencies check completed"
}

check_database_connection() {
    log_info "Checking database connection..."
    
    if PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; then
        log_success "Database connection established"
        return 0
    else
        log_error "Cannot connect to database. Please check:"
        echo "  - Database is running (try: docker compose up -d db)"
        echo "  - Connection parameters are correct"
        echo "  - POSTGRES_PASSWORD environment variable is set"
        return 1
    fi
}

check_existing_schema() {
    log_info "Checking existing CHAOSTOWN schema..."
    
    local agents_exists=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'agents');" 2>/dev/null | tr -d ' ')
    
    if [ "$agents_exists" = "t" ]; then
        log_success "Core CHAOSTOWN schema found"
        return 0
    else
        log_warning "Core CHAOSTOWN schema not found. You may need to run the base schema first."
        return 1
    fi
}

check_linguistic_schema() {
    log_info "Checking if linguistic evolution schema already exists..."
    
    local linguistic_exists=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'linguistic_agents');" 2>/dev/null | tr -d ' ')
    
    if [ "$linguistic_exists" = "t" ]; then
        log_warning "Linguistic evolution schema already exists"
        return 0
    else
        log_info "Linguistic evolution schema not found - ready for migration"
        return 1
    fi
}

verify_extensions() {
    log_info "Verifying required PostgreSQL extensions..."
    
    local extensions=("vector" "timescaledb")
    
    for ext in "${extensions[@]}"; do
        local ext_exists=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM pg_extension WHERE extname = '$ext');" 2>/dev/null | tr -d ' ')
        
        if [ "$ext_exists" = "t" ]; then
            log_success "Extension '$ext' is installed"
        else
            log_warning "Extension '$ext' is not installed (will be installed during migration)"
        fi
    done
}

run_migration() {
    log_info "Running linguistic evolution migration..."
    
    if [ ! -f "$MIGRATION_FILE" ]; then
        log_error "Migration file not found: $MIGRATION_FILE"
        exit 1
    fi
    
    # Run the migration
    if PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$MIGRATION_FILE" > migration.log 2>&1; then
        log_success "Migration completed successfully"
        
        # Show verification results
        log_info "Verifying migration..."
        PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM verify_linguistic_migration();"
        
    else
        log_error "Migration failed. Check migration.log for details:"
        cat migration.log
        exit 1
    fi
}

show_migration_status() {
    log_info "Checking migration status..."
    
    local tables=("linguistic_agents" "communications" "dot_patterns" "language_families" "linguistic_interactions" "rss_linguistic_influence")
    
    echo "Table Status:"
    echo "============="
    
    for table in "${tables[@]}"; do
        local exists=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$table');" 2>/dev/null | tr -d ' ')
        local count=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM $table;" 2>/dev/null | tr -d ' ')
        
        if [ "$exists" = "t" ]; then
            echo "  ✓ $table: EXISTS ($count rows)"
        else
            echo "  ✗ $table: NOT FOUND"
        fi
    done
}

rollback_migration() {
    log_warning "Rolling back linguistic evolution migration..."
    
    read -p "Are you sure you want to rollback the migration? This will delete all linguistic data. (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT rollback_linguistic_migration();" > rollback.log 2>&1; then
            log_success "Migration rolled back successfully"
        else
            log_error "Rollback failed. Check rollback.log for details:"
            cat rollback.log
            exit 1
        fi
    else
        log_info "Rollback cancelled"
    fi
}

create_sample_data() {
    log_info "Creating sample linguistic data..."
    
    cat << 'EOF' | PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
-- Insert sample agents if they don't exist
INSERT INTO agents (id, name, model, archetype, personality_tensor, position_x, position_y) VALUES
('11111111-1111-1111-1111-111111111111', 'Test_Agent_1', 'llama3.1', 'philosopher', '{"wisdom": 0.9, "curiosity": 0.8}', 0.0, 0.0),
('22222222-2222-2222-2222-222222222222', 'Test_Agent_2', 'mistral', 'creator', '{"creativity": 0.9, "innovation": 0.8}', 10.0, 10.0)
ON CONFLICT (id) DO NOTHING;

-- Insert sample linguistic agents
INSERT INTO linguistic_agents (agent_id, linguistic_stage, innovation_tendency, communication_threshold) VALUES
('11111111-1111-1111-1111-111111111111', 1, 0.7, 0.5),
('22222222-2222-2222-2222-222222222222', 1, 0.8, 0.6)
ON CONFLICT (agent_id) DO NOTHING;

-- Insert sample communications
INSERT INTO communications (
    agent_id, tick_number, dot_pattern, pattern_complexity, pattern_hash,
    aura_context, social_context, internal_pressure, communication_trigger
) VALUES
('11111111-1111-1111-1111-111111111111', 1, '•••', 0.2, '1234567890abcdef',
 '{"warmth_gradient": 0.8, "social_longing": 0.7}', '{}', 0.6, 'social'),
('22222222-2222-2222-2222-222222222222', 2, '• • •', 0.3, 'fedcba0987654321',
 '{"warmth_gradient": 0.6, "innovation_energy": 0.9}', '{}', 0.7, 'innovation')
ON CONFLICT (id) DO NOTHING;

SELECT 'Sample data created successfully' as status;
EOF

    log_success "Sample data created"
}

show_usage() {
    echo "CHAOSTOWN Linguistic Evolution Database Setup"
    echo "============================================="
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  setup     - Run complete setup (check + migrate)"
    echo "  migrate   - Run migration only"
    echo "  check     - Check system status"
    echo "  status    - Show migration status"
    echo "  rollback  - Rollback migration"
    echo "  sample    - Create sample data"
    echo "  help      - Show this help"
    echo
    echo "Environment Variables:"
    echo "  POSTGRES_DB       - Database name (default: chaostown)"
    echo "  POSTGRES_USER     - Database user (default: postgres)"
    echo "  POSTGRES_PASSWORD - Database password (required)"
    echo "  POSTGRES_HOST     - Database host (default: localhost)"
    echo "  POSTGRES_PORT     - Database port (default: 5432)"
    echo
    echo "Examples:"
    echo "  export POSTGRES_PASSWORD=chaostown_password"
    echo "  $0 setup"
    echo "  $0 status"
}

# Main execution
main() {
    echo "CHAOSTOWN Linguistic Evolution Database Setup"
    echo "============================================="
    echo
    
    case "${1:-setup}" in
        "setup")
            check_dependencies
            check_database_connection || exit 1
            check_existing_schema
            verify_extensions
            
            if check_linguistic_schema; then
                log_warning "Linguistic schema already exists. Use 'status' to check or 'rollback' to remove."
            else
                run_migration
            fi
            
            show_migration_status
            ;;
        
        "migrate")
            check_database_connection || exit 1
            run_migration
            ;;
        
        "check")
            check_dependencies
            check_database_connection || exit 1
            check_existing_schema
            verify_extensions
            ;;
        
        "status")
            check_database_connection || exit 1
            show_migration_status
            ;;
        
        "rollback")
            check_database_connection || exit 1
            rollback_migration
            ;;
        
        "sample")
            check_database_connection || exit 1
            create_sample_data
            ;;
        
        "help"|"-h"|"--help")
            show_usage
            ;;
        
        *)
            log_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"