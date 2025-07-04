from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import asyncio
from typing import Dict, List
import json
from datetime import datetime
import random
import logging
from contextlib import asynccontextmanager

# Import linguistic system components
from linguistic_api import router as linguistic_router
from websockets.linguistic_streams import ws_router, get_stream_service, get_connection_manager
from database import init_database, close_database, get_db_health, get_db_pool
from services.linguistic_service import LinguisticService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting CHAOSTOWN API with linguistic evolution system")
    
    # Initialize database
    db_success = await init_database()
    if not db_success:
        logger.error("Failed to initialize database")
        raise RuntimeError("Database initialization failed")
    
    # Start linguistic stream services
    try:
        db_pool = await get_db_pool()
        linguistic_service = LinguisticService(db_pool)
        app.state.linguistic_service = linguistic_service
        app.state.stream_service = await get_stream_service(linguistic_service)
        logger.info("Linguistic services initialized")
    except Exception as e:
        logger.error(f"Failed to initialize linguistic services: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CHAOSTOWN API")
    
    # Stop stream services
    if hasattr(app.state, 'stream_service'):
        await app.state.stream_service.stop_background_tasks()
    
    # Close database
    await close_database()
    logger.info("CHAOSTOWN API shutdown complete")


app = FastAPI(
    title="CHAOSTOWN API", 
    version="2.0.0",
    description="CHAOSTOWN Agentic Simulation with Mathematical Linguistic Evolution",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in production, this would be in a database)
cat_happiness = 0.5
agents = []
simulation_running = False
uploaded_media = []

@app.get("/")
async def root():
    return {"message": "CHAOSTOWN API is running", "status": "operational"}

@app.get("/health")
async def health_check():
    """Comprehensive health check including linguistic services"""
    # Get database health
    db_health = await get_db_health()
    
    # Get WebSocket connection stats
    connection_manager = get_connection_manager()
    ws_stats = connection_manager.get_connection_stats()
    
    # Check linguistic services
    linguistic_status = "unknown"
    if hasattr(app.state, 'linguistic_service'):
        linguistic_status = "running"
    
    return {
        "status": "healthy" if db_health["status"] == "healthy" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "database": db_health["status"],
            "linguistic_system": linguistic_status,
            "websocket_streams": "active" if ws_stats["total_connections"] > 0 else "standby",
            "cat_happiness": cat_happiness
        },
        "database": db_health,
        "websockets": ws_stats,
        "version": "2.0.0"
    }

@app.post("/media")
async def upload_media(file: UploadFile = File(...), type: str = "image"):
    """Upload cat media to boost happiness"""
    global cat_happiness
    
    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Save file
        media_dir = "/app/media"
        os.makedirs(media_dir, exist_ok=True)
        
        file_path = os.path.join(media_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Boost cat happiness
        cat_happiness = min(1.0, cat_happiness + 0.3)
        
        uploaded_media.append({
            "filename": file.filename,
            "type": type,
            "uploaded_at": datetime.now().isoformat(),
            "happiness_boost": 0.3
        })
        
        return {
            "message": "Cat media uploaded successfully! Happiness increased!",
            "filename": file.filename,
            "new_happiness": cat_happiness,
            "status": "success"
        }
    else:
        raise HTTPException(status_code=400, detail="Only image files are allowed")

@app.get("/cats/happiness")
async def get_cat_happiness():
    """Get current cat happiness level"""
    return {
        "combined_happiness": cat_happiness,
        "status": "critical" if cat_happiness < 0.8 else "healthy",
        "last_updated": datetime.now().isoformat()
    }

@app.post("/agents/initialize")
async def initialize_agents():
    """Initialize agent population"""
    global agents
    
    agent_names = [
        "Fluffhead", "Wilson", "Whiskers", "Shadow", "Mittens",
        "Patches", "Luna", "Oreo", "Simba", "Nala"
    ]
    
    agents = []
    for i in range(10):
        agent = {
            "id": i + 1,
            "name": agent_names[i % len(agent_names)],
            "type": "cat_citizen",
            "happiness": random.uniform(0.6, 1.0),
            "energy": random.uniform(0.7, 1.0),
            "loyalty": random.uniform(0.5, 1.0),
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        agents.append(agent)
    
    return {
        "message": f"Initialized {len(agents)} agents",
        "agents": agents,
        "status": "success"
    }

@app.get("/agents/count")
async def get_agent_count():
    """Get current agent count"""
    return len(agents)

@app.get("/agents")
async def get_agents():
    """Get all agents"""
    return {
        "agents": agents,
        "count": len(agents),
        "active_count": len([a for a in agents if a["status"] == "active"])
    }

@app.post("/simulation/start")
async def start_simulation():
    """Start the simulation"""
    global simulation_running
    
    if cat_happiness < 0.8:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot start simulation: cat happiness ({cat_happiness}) is below minimum threshold (0.8). Please upload more cat photos!"
        )
    
    if len(agents) == 0:
        raise HTTPException(
            status_code=400,
            detail="No agents found. Please initialize agents first."
        )
    
    simulation_running = True
    return {
        "message": "Simulation started successfully!",
        "running": simulation_running,
        "agent_count": len(agents),
        "cat_happiness": cat_happiness
    }

@app.post("/simulation/pause")
async def pause_simulation():
    """Pause the simulation"""
    global simulation_running
    simulation_running = False
    return {"message": "Simulation paused", "running": simulation_running}

@app.get("/simulation/status")
async def get_simulation_status():
    """Get simulation status"""
    return {
        "running": simulation_running,
        "agent_count": len(agents),
        "cat_happiness": cat_happiness,
        "uptime": "running" if simulation_running else "paused",
        "last_updated": datetime.now().isoformat()
    }

@app.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get stats for dashboard"""
    # Get linguistic metrics if available
    linguistic_stats = {}
    if hasattr(app.state, 'linguistic_service'):
        try:
            metrics = await app.state.linguistic_service.get_population_metrics(time_range="1h")
            linguistic_stats = {
                "total_linguistic_agents": metrics.total_agents,
                "active_linguistic_agents": metrics.active_agents,
                "total_communications": metrics.total_communications,
                "unique_patterns": metrics.unique_patterns,
                "language_families": metrics.language_families
            }
        except Exception as e:
            logger.error(f"Error getting linguistic stats: {e}")
            linguistic_stats = {"error": "linguistic_stats_unavailable"}
    
    return {
        "cat_happiness": cat_happiness,
        "agent_count": len(agents),
        "simulation_running": simulation_running,
        "uploaded_media_count": len(uploaded_media),
        "system_health": "excellent" if cat_happiness >= 0.8 else "concerning",
        "linguistic_evolution": linguistic_stats
    }


# Include linguistic API routes
app.include_router(linguistic_router, tags=["linguistic-evolution"])

# Include WebSocket routes
app.include_router(ws_router, tags=["websockets"])


@app.get("/api/status")
async def get_api_status():
    """Get comprehensive API status"""
    db_health = await get_db_health()
    connection_manager = get_connection_manager()
    ws_stats = connection_manager.get_connection_stats()
    
    return {
        "api_version": "2.0.0",
        "features": {
            "core_simulation": True,
            "linguistic_evolution": hasattr(app.state, 'linguistic_service'),
            "websocket_streams": True,
            "database_integration": db_health["status"] == "healthy"
        },
        "database": db_health,
        "websockets": ws_stats,
        "endpoints": {
            "core": ["/", "/health", "/media", "/agents", "/simulation"],
            "linguistic": [
                "/api/linguistic/agents/{id}",
                "/api/linguistic/agents/{id}/communicate", 
                "/api/linguistic/evolution/metrics",
                "/api/linguistic/patterns/analyze",
                "/api/linguistic/rss/feed"
            ],
            "websockets": [
                "/ws/linguistic/live",
                "/ws/linguistic/metrics", 
                "/ws/linguistic/patterns",
                "/ws/linguistic/stages",
                "/ws/linguistic/system"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)