"""
CHAOSTOWN Linguistic WebSocket Handlers
Real-time communication streams and live updates
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from uuid import UUID, uuid4
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from fastapi.routing import APIRouter
import asyncpg

from models.linguistic import (
    LiveStreamMessage, CommunicationModel, LinguisticAgentModel,
    DotPatternModel, SystemStatusModel, AuraStateModel
)
from services.linguistic_service import LinguisticService

logger = logging.getLogger(__name__)

# WebSocket router
ws_router = APIRouter()

class ConnectionManager:
    """Manages WebSocket connections for linguistic streams"""
    
    def __init__(self):
        # Active connections by stream type
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "live": set(),           # Live communication stream
            "metrics": set(),        # Population metrics updates
            "patterns": set(),       # Pattern emergence events
            "stages": set(),         # Agent stage progression
            "families": set(),       # Language family formation
            "innovations": set(),    # Innovation events
            "rss": set(),           # RSS feed influences
            "system": set()         # System health updates
        }
        
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
        # Message queues for each connection
        self.message_queues: Dict[WebSocket, asyncio.Queue] = {}
        
        # Stream filters and subscriptions
        self.stream_filters: Dict[WebSocket, Dict[str, Any]] = {}
        
    async def connect(self, websocket: WebSocket, stream_type: str, filters: Dict[str, Any] = None):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        if stream_type not in self.active_connections:
            stream_type = "live"  # Default to live stream
        
        self.active_connections[stream_type].add(websocket)
        self.connection_metadata[websocket] = {
            "stream_type": stream_type,
            "connected_at": datetime.utcnow(),
            "client_id": str(uuid4()),
            "filters": filters or {}
        }
        self.message_queues[websocket] = asyncio.Queue()
        self.stream_filters[websocket] = filters or {}
        
        logger.info(f"WebSocket connected to {stream_type} stream: {self.connection_metadata[websocket]['client_id']}")
        
        # Send welcome message
        await self.send_personal_message(websocket, {
            "event_type": "connection_established",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "stream_type": stream_type,
                "client_id": self.connection_metadata[websocket]["client_id"],
                "available_filters": self._get_available_filters(stream_type)
            }
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.connection_metadata:
            stream_type = self.connection_metadata[websocket]["stream_type"]
            client_id = self.connection_metadata[websocket]["client_id"]
            
            self.active_connections[stream_type].discard(websocket)
            del self.connection_metadata[websocket]
            del self.message_queues[websocket]
            del self.stream_filters[websocket]
            
            logger.info(f"WebSocket disconnected from {stream_type} stream: {client_id}")
    
    async def send_personal_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast_to_stream(self, stream_type: str, message: Dict[str, Any]):
        """Broadcast message to all connections of a specific stream type"""
        if stream_type not in self.active_connections:
            return
        
        disconnected = set()
        
        for websocket in self.active_connections[stream_type].copy():
            try:
                # Apply filters if any
                if self._should_send_message(websocket, message):
                    await websocket.send_text(json.dumps(message, default=str))
            except WebSocketDisconnect:
                disconnected.add(websocket)
            except Exception as e:
                logger.error(f"Error broadcasting to {stream_type}: {e}")
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_to_all(self, message: Dict[str, Any], exclude_streams: List[str] = None):
        """Broadcast message to all active connections"""
        exclude_streams = exclude_streams or []
        
        for stream_type in self.active_connections:
            if stream_type not in exclude_streams:
                await self.broadcast_to_stream(stream_type, message)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about active connections"""
        stats = {
            "total_connections": sum(len(connections) for connections in self.active_connections.values()),
            "connections_by_stream": {
                stream_type: len(connections) 
                for stream_type, connections in self.active_connections.items()
            },
            "active_streams": list(self.active_connections.keys())
        }
        return stats
    
    def _should_send_message(self, websocket: WebSocket, message: Dict[str, Any]) -> bool:
        """Check if message should be sent to websocket based on filters"""
        filters = self.stream_filters.get(websocket, {})
        
        if not filters:
            return True  # No filters, send everything
        
        # Agent filter
        if "agent_ids" in filters:
            agent_id = message.get("data", {}).get("agent_id")
            if agent_id and agent_id not in filters["agent_ids"]:
                return False
        
        # Event type filter
        if "event_types" in filters:
            event_type = message.get("event_type")
            if event_type not in filters["event_types"]:
                return False
        
        # Complexity filter
        if "min_complexity" in filters:
            complexity = message.get("data", {}).get("complexity", 0)
            if complexity < filters["min_complexity"]:
                return False
        
        # Stage filter
        if "stages" in filters:
            stage = message.get("data", {}).get("stage")
            if stage and stage not in filters["stages"]:
                return False
        
        return True
    
    def _get_available_filters(self, stream_type: str) -> Dict[str, Any]:
        """Get available filters for a stream type"""
        base_filters = {
            "agent_ids": "List of agent UUIDs to monitor",
            "event_types": "List of event types to include"
        }
        
        stream_specific_filters = {
            "live": {
                "min_complexity": "Minimum pattern complexity",
                "triggers": "Communication triggers to include",
                "innovations_only": "Only show innovation events"
            },
            "patterns": {
                "min_usage": "Minimum pattern usage count",
                "complexity_range": "Complexity range [min, max]"
            },
            "stages": {
                "stages": "Linguistic stages to monitor",
                "progression_only": "Only show stage advancements"
            },
            "families": {
                "min_members": "Minimum family member count",
                "family_ids": "Specific family IDs to monitor"
            }
        }
        
        return {**base_filters, **stream_specific_filters.get(stream_type, {})}


# Global connection manager
manager = ConnectionManager()


class LinguisticStreamService:
    """Service for managing linguistic event streams"""
    
    def __init__(self, linguistic_service: LinguisticService):
        self.linguistic_service = linguistic_service
        self.manager = manager
        
        # Background tasks
        self._metrics_task = None
        self._system_health_task = None
        
    async def start_background_tasks(self):
        """Start background tasks for periodic updates"""
        if not self._metrics_task:
            self._metrics_task = asyncio.create_task(self._periodic_metrics_update())
        
        if not self._system_health_task:
            self._system_health_task = asyncio.create_task(self._periodic_system_health_update())
    
    async def stop_background_tasks(self):
        """Stop background tasks"""
        if self._metrics_task:
            self._metrics_task.cancel()
            self._metrics_task = None
        
        if self._system_health_task:
            self._system_health_task.cancel()
            self._system_health_task = None
    
    async def broadcast_communication_event(self, communication: CommunicationModel):
        """Broadcast new communication event"""
        message = LiveStreamMessage(
            event_type="communication",
            timestamp=communication.timestamp,
            data={
                "id": str(communication.id),
                "agent_id": str(communication.agent_id),
                "pattern": communication.dot_pattern,
                "complexity": communication.pattern_complexity,
                "trigger": communication.communication_trigger.value,
                "is_innovation": communication.is_innovation,
                "aura_context": communication.aura_context.dict(),
                "pressure": communication.internal_pressure
            }
        )
        
        await self.manager.broadcast_to_stream("live", message.dict())
        
        # Also broadcast to innovation stream if it's an innovation
        if communication.is_innovation:
            await self.manager.broadcast_to_stream("innovations", message.dict())
    
    async def broadcast_pattern_emergence(self, pattern: DotPatternModel):
        """Broadcast new pattern emergence"""
        message = LiveStreamMessage(
            event_type="pattern_emergence",
            timestamp=pattern.first_appearance,
            data={
                "pattern": pattern.dot_pattern,
                "complexity": pattern.complexity,
                "creator_agent": str(pattern.created_by_agent),
                "pattern_hash": pattern.pattern_hash,
                "spatial_dimensions": pattern.spatial_dimensions,
                "innovation_context": pattern.innovation_context
            }
        )
        
        await self.manager.broadcast_to_stream("patterns", message.dict())
        await self.manager.broadcast_to_stream("live", message.dict())
    
    async def broadcast_stage_advancement(self, agent: LinguisticAgentModel, old_stage: int, new_stage: int):
        """Broadcast agent stage advancement"""
        message = LiveStreamMessage(
            event_type="stage_advancement",
            timestamp=datetime.utcnow(),
            data={
                "agent_id": str(agent.agent_id),
                "old_stage": old_stage,
                "new_stage": new_stage,
                "stage_name": agent.linguistic_stage.name,
                "vocabulary_size": agent.vocabulary_size,
                "total_communications": agent.total_communications,
                "literacy_level": agent.literacy_level
            }
        )
        
        await self.manager.broadcast_to_stream("stages", message.dict())
        await self.manager.broadcast_to_stream("live", message.dict())
    
    async def broadcast_family_formation(self, family_id: UUID, founding_agents: List[UUID], characteristic_patterns: List[str]):
        """Broadcast language family formation"""
        message = LiveStreamMessage(
            event_type="family_formation",
            timestamp=datetime.utcnow(),
            data={
                "family_id": str(family_id),
                "founding_agents": [str(agent_id) for agent_id in founding_agents],
                "characteristic_patterns": characteristic_patterns,
                "member_count": len(founding_agents)
            }
        )
        
        await self.manager.broadcast_to_stream("families", message.dict())
        await self.manager.broadcast_to_stream("live", message.dict())
    
    async def broadcast_rss_influence(self, agent_id: UUID, influence_strength: float, literacy_boost: float, triggered_communication: bool):
        """Broadcast RSS feed influence event"""
        message = LiveStreamMessage(
            event_type="rss_influence",
            timestamp=datetime.utcnow(),
            data={
                "agent_id": str(agent_id),
                "influence_strength": influence_strength,
                "literacy_boost": literacy_boost,
                "triggered_communication": triggered_communication
            }
        )
        
        await self.manager.broadcast_to_stream("rss", message.dict())
        
        # Also broadcast to live if significant influence
        if influence_strength > 0.5 or triggered_communication:
            await self.manager.broadcast_to_stream("live", message.dict())
    
    async def _periodic_metrics_update(self):
        """Periodic update of population metrics"""
        while True:
            try:
                await asyncio.sleep(30)  # Update every 30 seconds
                
                metrics = await self.linguistic_service.get_population_metrics(
                    time_range="1h", include_trends=True
                )
                
                message = LiveStreamMessage(
                    event_type="metrics_update",
                    timestamp=datetime.utcnow(),
                    data={
                        "total_agents": metrics.total_agents,
                        "active_agents": metrics.active_agents,
                        "total_communications": metrics.total_communications,
                        "unique_patterns": metrics.unique_patterns,
                        "language_families": metrics.language_families,
                        "stage_distribution": {str(k): v for k, v in metrics.stage_distribution.items()},
                        "system_health": metrics.system_health
                    }
                )
                
                await self.manager.broadcast_to_stream("metrics", message.dict())
                
            except Exception as e:
                logger.error(f"Error in periodic metrics update: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _periodic_system_health_update(self):
        """Periodic system health broadcast"""
        while True:
            try:
                await asyncio.sleep(60)  # Update every minute
                
                # Get connection stats
                connection_stats = self.manager.get_connection_stats()
                
                # Get system metrics
                metrics = await self.linguistic_service.get_population_metrics(time_range="1h")
                
                message = LiveStreamMessage(
                    event_type="system_health",
                    timestamp=datetime.utcnow(),
                    data={
                        "websocket_connections": connection_stats,
                        "system_health": metrics.system_health,
                        "performance": {
                            "active_agents": metrics.active_agents,
                            "communication_rate": metrics.total_communications / 60,  # per minute
                            "memory_usage": "normal",  # Would be actual system metrics
                            "database_performance": "good"  # Would be actual DB metrics
                        }
                    }
                )
                
                await self.manager.broadcast_to_stream("system", message.dict())
                
            except Exception as e:
                logger.error(f"Error in system health update: {e}")
                await asyncio.sleep(120)  # Wait longer on error


# WebSocket endpoints

@ws_router.websocket("/ws/linguistic/live")
async def websocket_live_stream(
    websocket: WebSocket,
    agent_filter: Optional[str] = None,
    min_complexity: Optional[float] = None,
    event_types: Optional[str] = None
):
    """
    Live communication stream WebSocket
    
    Streams real-time communication events, pattern emergence,
    and agent interactions as they occur.
    
    Query parameters:
    - agent_filter: Comma-separated list of agent UUIDs
    - min_complexity: Minimum pattern complexity to include
    - event_types: Comma-separated list of event types
    """
    
    # Parse filters
    filters = {}
    if agent_filter:
        try:
            filters["agent_ids"] = [UUID(aid.strip()) for aid in agent_filter.split(",")]
        except ValueError:
            await websocket.close(code=1008, reason="Invalid agent UUIDs")
            return
    
    if min_complexity is not None:
        filters["min_complexity"] = min_complexity
    
    if event_types:
        filters["event_types"] = [et.strip() for et in event_types.split(",")]
    
    await manager.connect(websocket, "live", filters)
    
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            
            try:
                client_message = json.loads(data)
                
                # Handle client commands
                if client_message.get("type") == "ping":
                    await manager.send_personal_message(websocket, {
                        "event_type": "pong",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": {"status": "alive"}
                    })
                
                elif client_message.get("type") == "update_filters":
                    new_filters = client_message.get("filters", {})
                    manager.stream_filters[websocket] = new_filters
                    await manager.send_personal_message(websocket, {
                        "event_type": "filters_updated",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": {"filters": new_filters}
                    })
                
            except json.JSONDecodeError:
                await manager.send_personal_message(websocket, {
                    "event_type": "error",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {"message": "Invalid JSON message"}
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@ws_router.websocket("/ws/linguistic/metrics")
async def websocket_metrics_stream(websocket: WebSocket):
    """
    Population metrics stream WebSocket
    
    Streams periodic updates of population-level metrics
    including stage distribution, communication trends,
    and system health indicators.
    """
    await manager.connect(websocket, "metrics")
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Handle ping/pong for keepalive
            if data == "ping":
                await manager.send_personal_message(websocket, {
                    "event_type": "pong",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {}
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@ws_router.websocket("/ws/linguistic/patterns")
async def websocket_patterns_stream(
    websocket: WebSocket,
    min_complexity: Optional[float] = None,
    innovations_only: bool = False
):
    """
    Pattern emergence stream WebSocket
    
    Streams new pattern discoveries, evolution events,
    and pattern adoption across the population.
    """
    filters = {}
    if min_complexity is not None:
        filters["min_complexity"] = min_complexity
    if innovations_only:
        filters["innovations_only"] = True
    
    await manager.connect(websocket, "patterns", filters)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await manager.send_personal_message(websocket, {
                    "event_type": "pong",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {}
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@ws_router.websocket("/ws/linguistic/stages")
async def websocket_stages_stream(
    websocket: WebSocket,
    agent_filter: Optional[str] = None,
    stages: Optional[str] = None
):
    """
    Linguistic stage progression stream WebSocket
    
    Streams agent stage advancement events and
    developmental milestone achievements.
    """
    filters = {}
    if agent_filter:
        try:
            filters["agent_ids"] = [UUID(aid.strip()) for aid in agent_filter.split(",")]
        except ValueError:
            await websocket.close(code=1008, reason="Invalid agent UUIDs")
            return
    
    if stages:
        try:
            filters["stages"] = [int(s.strip()) for s in stages.split(",")]
        except ValueError:
            await websocket.close(code=1008, reason="Invalid stage numbers")
            return
    
    await manager.connect(websocket, "stages", filters)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await manager.send_personal_message(websocket, {
                    "event_type": "pong",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {}
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@ws_router.websocket("/ws/linguistic/system")
async def websocket_system_stream(websocket: WebSocket):
    """
    System health and performance stream WebSocket
    
    Streams system health updates, performance metrics,
    and diagnostic information for monitoring.
    """
    await manager.connect(websocket, "system")
    
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await manager.send_personal_message(websocket, {
                    "event_type": "pong",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": manager.get_connection_stats()
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Utility functions for integration

async def get_stream_service(linguistic_service: LinguisticService) -> LinguisticStreamService:
    """Get linguistic stream service instance"""
    stream_service = LinguisticStreamService(linguistic_service)
    await stream_service.start_background_tasks()
    return stream_service


def get_connection_manager() -> ConnectionManager:
    """Get global connection manager"""
    return manager


# Export for use in main application
__all__ = [
    "ws_router", 
    "manager", 
    "LinguisticStreamService", 
    "get_stream_service",
    "get_connection_manager"
]