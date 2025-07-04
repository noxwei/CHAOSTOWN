import asyncio
import time
import requests
import json
import random
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationEngine:
    def __init__(self):
        self.api_url = "http://api:8000"
        self.running = False
        self.tick_rate = 1.0
        self.agents = []
        
    async def start(self):
        """Start the simulation engine"""
        logger.info("🚀 Starting CHAOSTOWN Simulation Engine")
        self.running = True
        
        while self.running:
            try:
                # Check if simulation should be running
                status = await self.check_simulation_status()
                
                if status and status.get("running"):
                    await self.simulation_tick()
                
                await asyncio.sleep(self.tick_rate)
                
            except Exception as e:
                logger.error(f"Error in simulation loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying
    
    async def check_simulation_status(self):
        """Check if simulation is running via API"""
        try:
            response = requests.get(f"{self.api_url}/simulation/status", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            logger.warning("Could not connect to API")
        return None
    
    async def simulation_tick(self):
        """Execute one simulation tick"""
        logger.info("🐱 Simulation tick executing...")
        
        # Simulate agent behaviors
        await self.update_agents()
        
        # Simulate cat happiness decay (cats need constant attention!)
        await self.decay_cat_happiness()
        
        # Log current state
        await self.log_simulation_state()
    
    async def update_agents(self):
        """Update agent states"""
        try:
            # Get current agents
            response = requests.get(f"{self.api_url}/agents", timeout=5)
            if response.status_code == 200:
                agents_data = response.json()
                self.agents = agents_data.get("agents", [])
                
                # Simulate agent activities
                for agent in self.agents:
                    # Random agent behavior simulation
                    if random.random() < 0.1:  # 10% chance of activity
                        activity = random.choice([
                            "exploring", "hunting", "napping", "socializing", "scheming"
                        ])
                        logger.info(f"🐾 Agent {agent['name']} is {activity}")
                        
                        # Slightly adjust agent stats
                        if activity == "napping":
                            agent["energy"] = min(1.0, agent["energy"] + 0.1)
                        elif activity == "socializing":
                            agent["happiness"] = min(1.0, agent["happiness"] + 0.05)
                        elif activity == "scheming":
                            agent["loyalty"] = max(0.0, agent["loyalty"] - 0.02)
                            
        except requests.RequestException as e:
            logger.warning(f"Could not update agents: {e}")
    
    async def decay_cat_happiness(self):
        """Gradually decay cat happiness (cats are needy!)"""
        try:
            # Get current happiness
            response = requests.get(f"{self.api_url}/cats/happiness", timeout=5)
            if response.status_code == 200:
                happiness_data = response.json()
                current_happiness = happiness_data.get("combined_happiness", 0.5)
                
                # Decay happiness by 0.01 per tick (cats need constant attention)
                new_happiness = max(0.0, current_happiness - 0.01)
                
                # Note: In a real implementation, we'd update this via API
                # For now, this is just logged
                if new_happiness < 0.8:
                    logger.warning(f"⚠️ Cat happiness declining: {new_happiness:.3f}")
                
        except requests.RequestException as e:
            logger.warning(f"Could not check cat happiness: {e}")
    
    async def log_simulation_state(self):
        """Log current simulation state"""
        try:
            response = requests.get(f"{self.api_url}/dashboard/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                logger.info(f"📊 Stats - Happiness: {stats.get('cat_happiness', 0):.3f}, "
                          f"Agents: {stats.get('agent_count', 0)}, "
                          f"Health: {stats.get('system_health', 'unknown')}")
        except requests.RequestException as e:
            logger.warning(f"Could not fetch stats: {e}")

async def main():
    """Main function to run the simulation engine"""
    engine = SimulationEngine()
    
    # Wait for API to be ready
    logger.info("Waiting for API to be ready...")
    while True:
        try:
            response = requests.get("http://api:8000/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ API is ready!")
                break
        except requests.RequestException:
            logger.info("⏳ Waiting for API...")
            await asyncio.sleep(5)
    
    # Start simulation
    await engine.start()

if __name__ == "__main__":
    asyncio.run(main())