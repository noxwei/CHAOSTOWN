from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from typing import Dict, List
import json
from datetime import datetime
import random

app = FastAPI(title="CHAOSTOWN API", version="1.0.0")

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
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "database": "connected",
            "cat_happiness": cat_happiness
        }
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
    return {
        "cat_happiness": cat_happiness,
        "agent_count": len(agents),
        "simulation_running": simulation_running,
        "uploaded_media_count": len(uploaded_media),
        "system_health": "excellent" if cat_happiness >= 0.8 else "concerning"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)