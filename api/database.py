"""
Database configuration and connection management for CHAOSTOWN
"""

import asyncio
import os
import logging
from typing import Optional
import asyncpg
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages PostgreSQL database connections"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self._connection_params = self._get_connection_params()
    
    def _get_connection_params(self) -> dict:
        """Get database connection parameters from environment"""
        return {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "database": os.getenv("POSTGRES_DB", "chaostown"),
            "user": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "min_size": int(os.getenv("DB_POOL_MIN_SIZE", "5")),
            "max_size": int(os.getenv("DB_POOL_MAX_SIZE", "20")),
            "command_timeout": int(os.getenv("DB_COMMAND_TIMEOUT", "30"))
        }
    
    async def initialize(self) -> bool:
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                host=self._connection_params["host"],
                port=self._connection_params["port"],
                database=self._connection_params["database"],
                user=self._connection_params["user"],
                password=self._connection_params["password"],
                min_size=self._connection_params["min_size"],
                max_size=self._connection_params["max_size"],
                command_timeout=self._connection_params["command_timeout"]
            )
            
            # Test connection
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            
            logger.info("Database connection pool initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            return False
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.info("Database connection pool closed")
    
    async def health_check(self) -> dict:
        """Check database health"""
        if not self.pool:
            return {"status": "error", "message": "No connection pool"}
        
        try:
            async with self.pool.acquire() as conn:
                # Test basic query
                result = await conn.fetchval("SELECT 1")
                
                # Check if linguistic tables exist
                linguistic_tables = await conn.fetch("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('linguistic_agents', 'communications', 'dot_patterns')
                """)
                
                # Get pool stats
                pool_stats = {
                    "size": self.pool.get_size(),
                    "min_size": self.pool.get_min_size(),
                    "max_size": self.pool.get_max_size(),
                    "idle_size": self.pool.get_idle_size()
                }
                
                return {
                    "status": "healthy",
                    "connection_test": result == 1,
                    "linguistic_tables": len(linguistic_tables),
                    "pool_stats": pool_stats
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as conn:
            yield conn


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_pool() -> asyncpg.Pool:
    """Dependency for getting database pool"""
    if not db_manager.pool:
        raise RuntimeError("Database not initialized")
    return db_manager.pool


async def init_database() -> bool:
    """Initialize database for the application"""
    return await db_manager.initialize()


async def close_database():
    """Close database connections"""
    await db_manager.close()


async def get_db_health() -> dict:
    """Get database health status"""
    return await db_manager.health_check()