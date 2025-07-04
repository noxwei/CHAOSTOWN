"""
CHAOSTOWN Linguistic Evolution API Endpoints
Production-ready FastAPI implementation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID
import asyncpg
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from models.linguistic import (
    LinguisticAgentModel, CommunicationModel, DotPatternModel,
    CommunicationRequest, CommunicationResponse, PatternAnalysisRequest,
    PatternAnalysisResponse, PopulationMetricsRequest, PopulationMetricsResponse,
    RSSFeedRequest, RSSFeedResponse, AgentObservableState, SystemStatusModel,
    AuraStateModel, LinguisticStage, CommunicationTrigger
)
from services.linguistic_service import LinguisticService

logger = logging.getLogger(__name__)

# Router for linguistic endpoints
router = APIRouter(prefix="/api/linguistic", tags=["linguistic"])

# Dependency injection for database pool and service
async def get_db_pool():
    """Get database connection pool - to be overridden by main app"""
    # This will be injected by the main application
    pass

async def get_linguistic_service(db_pool: asyncpg.Pool = Depends(get_db_pool)) -> LinguisticService:
    """Get linguistic service instance"""
    return LinguisticService(db_pool)


# Agent Management Endpoints

@router.get("/agents/{agent_id}", response_model=LinguisticAgentModel)
async def get_agent_linguistic_state(
    agent_id: UUID,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get current linguistic state of an agent
    
    Returns detailed linguistic development metrics, vocabulary size,
    stage progression, and literacy levels without internal semantic meanings.
    """
    try:
        agent = await service.get_agent_linguistic_state(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        return agent
    except Exception as e:
        logger.error(f"Error getting agent state {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/observable", response_model=AgentObservableState)
async def get_agent_observable_state(
    agent_id: UUID,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get observable state for human researchers
    
    Returns only externally observable metrics without revealing
    internal semantic mappings or agent intentions.
    """
    try:
        state = await service.get_observable_agent_state(agent_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        return state
    except Exception as e:
        logger.error(f"Error getting observable state {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/initialize", response_model=LinguisticAgentModel)
async def initialize_agent_linguistic_capabilities(
    agent_id: UUID,
    characteristics: Dict[str, Any] = None,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Initialize linguistic capabilities for an existing agent
    
    Sets up initial linguistic parameters including innovation tendency,
    social influence susceptibility, and communication thresholds.
    """
    try:
        characteristics = characteristics or {}
        agent = await service.initialize_agent(agent_id, characteristics)
        return agent
    except Exception as e:
        logger.error(f"Error initializing agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Communication Endpoints

@router.post("/agents/{agent_id}/communicate", response_model=CommunicationResponse)
async def trigger_agent_communication(
    agent_id: UUID,
    request: CommunicationRequest = None,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Trigger communication attempt for an agent
    
    Processes environmental auras, nearby communications, RSS feeds,
    and special offerings to determine if communication should occur.
    Returns communication pattern if pressure exceeds threshold.
    """
    try:
        # Use request data or defaults
        if request is None:
            request = CommunicationRequest(agent_id=agent_id)
        
        # Default aura state if not provided
        aura_state = request.custom_aura_state
        if not aura_state:
            aura_state = AuraStateModel(
                warmth_gradient=0.6,
                resource_density=0.5,
                danger_proximity=0.2,
                cat_happiness=0.8,
                social_longing=0.7,
                innovation_energy=0.5,
                literacy_exposure=0.3
            )
        
        # Trigger communication
        success, communication, pressure = await service.trigger_agent_communication(
            agent_id=agent_id,
            aura_state=aura_state,
            rss_feeds=request.rss_feeds,
            offerings=request.offerings,
            force_communication=request.force_communication
        )
        
        # Get updated agent state
        agent_state = await service.get_agent_linguistic_state(agent_id)
        
        message = "Communication successful" if success else "No communication needed"
        if request.force_communication and not success:
            message = "Communication forced but failed"
        
        return CommunicationResponse(
            success=success,
            message=message,
            communication=communication,
            agent_state=agent_state,
            communication_pressure=pressure
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error triggering communication for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/communications/recent")
async def get_recent_communications(
    limit: int = 50,
    agent_id: Optional[UUID] = None,
    time_range: str = "1h",
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get recent communications across the population
    
    Returns observable communication patterns without revealing
    internal semantic meanings or agent intentions.
    """
    try:
        # This would need to be implemented in the service
        # For now, return placeholder
        return {
            "communications": [],
            "total": 0,
            "time_range": time_range,
            "message": "Recent communications endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting recent communications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Population Analytics Endpoints

@router.get("/evolution/metrics", response_model=PopulationMetricsResponse)
async def get_population_language_metrics(
    time_range: str = "24h",
    include_trends: bool = True,
    include_families: bool = True,
    include_patterns: bool = True,
    agent_filter: Optional[List[UUID]] = None,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get population-level language evolution metrics
    
    Returns comprehensive statistics on linguistic development including
    stage distribution, communication trends, complexity evolution,
    and innovation patterns across the agent population.
    """
    try:
        metrics = await service.get_population_metrics(
            time_range=time_range,
            include_trends=include_trends,
            include_families=include_families,
            include_patterns=include_patterns,
            agent_filter=agent_filter
        )
        return metrics
    except Exception as e:
        logger.error(f"Error getting population metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evolution/stage-distribution")
async def get_linguistic_stage_distribution(
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get distribution of agents across linguistic development stages
    
    Returns count of agents in each stage from primal signals
    to meta-linguistic communication.
    """
    try:
        metrics = await service.get_population_metrics(time_range="24h", include_trends=False)
        return {
            "stage_distribution": metrics.stage_distribution,
            "total_agents": metrics.total_agents,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stage distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evolution/complexity-trends")
async def get_complexity_evolution_trends(
    time_range: str = "24h",
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get mathematical complexity trends over time
    
    Returns temporal evolution of pattern complexity showing
    the mathematical sophistication development in the population.
    """
    try:
        metrics = await service.get_population_metrics(time_range=time_range, include_trends=True)
        return {
            "complexity_trends": metrics.complexity_trends,
            "time_range": time_range,
            "system_health": metrics.system_health
        }
    except Exception as e:
        logger.error(f"Error getting complexity trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Pattern Analysis Endpoints

@router.post("/patterns/analyze", response_model=PatternAnalysisResponse)
async def analyze_dot_patterns(
    request: PatternAnalysisRequest,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Analyze dot patterns for complexity and relationships
    
    Performs mathematical analysis of communication patterns including
    Shannon entropy, spatial complexity, repetition analysis, and
    pattern evolution tracking.
    """
    try:
        if not request.patterns:
            raise HTTPException(status_code=400, detail="No patterns provided for analysis")
        
        analysis = await service.analyze_patterns(
            patterns=request.patterns,
            include_complexity=request.include_complexity,
            include_similarity=request.include_similarity,
            include_evolution=request.include_evolution
        )
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/popular")
async def get_popular_patterns(
    limit: int = 20,
    time_range: str = "7d",
    min_usage: int = 1,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get most popular communication patterns
    
    Returns frequently used patterns with usage statistics,
    complexity metrics, and adoption rates across the population.
    """
    try:
        # This would need database queries - placeholder for now
        return {
            "patterns": [],
            "limit": limit,
            "time_range": time_range,
            "message": "Popular patterns endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting popular patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/innovations")
async def get_pattern_innovations(
    time_range: str = "24h",
    min_complexity: float = 0.3,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get recent pattern innovations
    
    Returns newly created patterns that represent linguistic innovations,
    tracking the emergence of novel communication forms.
    """
    try:
        # This would need database queries - placeholder for now
        return {
            "innovations": [],
            "time_range": time_range,
            "min_complexity": min_complexity,
            "message": "Pattern innovations endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting pattern innovations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# RSS Feed Processing Endpoints

@router.post("/rss/feed", response_model=RSSFeedResponse)
async def process_rss_feed_for_agents(
    request: RSSFeedRequest,
    background_tasks: BackgroundTasks,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Process RSS feed content for literacy development
    
    Exposes agents to text content for gradual literacy acquisition.
    Initially extracts emotional vibes, gradually building character
    recognition and word associations as agents develop.
    """
    try:
        if not request.agent_ids:
            raise HTTPException(status_code=400, detail="No agents specified for RSS processing")
        
        if not request.feed_content.strip():
            raise HTTPException(status_code=400, detail="No feed content provided")
        
        # Process RSS feed for agents
        if request.batch_process:
            # Process in background for large batches
            background_tasks.add_task(
                service.process_rss_feed,
                request.agent_ids,
                request.feed_content,
                request.feed_source,
                request.quality_score
            )
            
            return RSSFeedResponse(
                processed_agents=len(request.agent_ids),
                influences=[],
                triggered_communications=[],
                literacy_improvements={},
                summary={
                    "status": "processing",
                    "message": "RSS feed processing started in background"
                }
            )
        else:
            # Process synchronously
            result = await service.process_rss_feed(
                request.agent_ids,
                request.feed_content,
                request.feed_source,
                request.quality_score
            )
            
            return RSSFeedResponse(
                processed_agents=result["processed_agents"],
                influences=result["influences"],
                triggered_communications=result["triggered_communications"],
                literacy_improvements=result["literacy_improvements"],
                summary=result["summary"]
            )
            
    except Exception as e:
        logger.error(f"Error processing RSS feed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rss/impact")
async def get_rss_literacy_impact(
    agent_id: Optional[UUID] = None,
    time_range: str = "7d",
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get RSS feed impact on literacy development
    
    Returns metrics on how RSS feeds have influenced literacy
    acquisition and communication patterns across agents.
    """
    try:
        # This would need database queries - placeholder for now
        return {
            "literacy_improvements": {},
            "communication_influences": [],
            "time_range": time_range,
            "message": "RSS impact analysis endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting RSS impact: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Language Family Endpoints

@router.get("/families")
async def get_language_families(
    active_only: bool = True,
    min_members: int = 1,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get emergent language families and dialects
    
    Returns discovered language groups with their characteristics,
    founding agents, and cultural development patterns.
    """
    try:
        # This would need database queries - placeholder for now
        return {
            "families": [],
            "total": 0,
            "active_only": active_only,
            "message": "Language families endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting language families: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/families/{family_id}")
async def get_language_family_details(
    family_id: UUID,
    include_members: bool = True,
    include_patterns: bool = True,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get detailed information about a specific language family
    
    Returns comprehensive family analysis including member agents,
    characteristic patterns, and evolution history.
    """
    try:
        # This would need database queries - placeholder for now
        return {
            "family_id": str(family_id),
            "details": {},
            "message": "Language family details endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting language family {family_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# System Status and Health Endpoints

@router.get("/system/status", response_model=SystemStatusModel)
async def get_linguistic_system_status(
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get overall linguistic system health and status
    
    Returns comprehensive system metrics including active agents,
    communication rates, innovation levels, and performance indicators.
    """
    try:
        metrics = await service.get_population_metrics(time_range="24h")
        
        # Calculate performance metrics
        performance_metrics = {
            "communication_rate": metrics.total_communications / 24 if metrics.total_communications else 0,
            "innovation_rate": metrics.innovation_trends.get("hourly_innovations", [])[-1:] if metrics.innovation_trends else [],
            "complexity_growth": metrics.complexity_trends.get("evolution_trend", "stable") if metrics.complexity_trends else "stable",
            "system_load": "normal"  # This would be calculated based on actual system metrics
        }
        
        # Recent events placeholder
        recent_events = [
            {
                "type": "system_metric_update",
                "timestamp": datetime.utcnow().isoformat(),
                "description": "System metrics refreshed"
            }
        ]
        
        return SystemStatusModel(
            active_agents=metrics.active_agents,
            total_communications_24h=metrics.total_communications,
            unique_patterns_discovered=metrics.unique_patterns,
            language_families_active=metrics.language_families,
            average_complexity=metrics.complexity_trends.get("final_avg", 0.0) if metrics.complexity_trends else 0.0,
            innovation_rate=0.0,  # Would be calculated from innovation trends
            literacy_progression=0.0,  # Would be calculated from agent literacy levels
            system_health=metrics.system_health.get("overall_status", "unknown"),
            performance_metrics=performance_metrics,
            recent_events=recent_events
        )
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/health")
async def get_system_health_report(
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get detailed system health report
    
    Returns diagnostic information about linguistic system performance,
    potential issues, and optimization recommendations.
    """
    try:
        metrics = await service.get_population_metrics(time_range="24h")
        
        return {
            "overall_health": metrics.system_health,
            "diagnostics": {
                "agent_activity": "healthy" if metrics.active_agents > metrics.total_agents * 0.5 else "concerning",
                "communication_flow": "active" if metrics.total_communications > 100 else "low",
                "innovation_level": "normal",  # Would be calculated from innovation metrics
                "complexity_evolution": "progressing"  # Would be derived from complexity trends
            },
            "recommendations": metrics.system_health.get("recommendations", []),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting health report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Research and Experimentation Endpoints

@router.post("/experiments/create")
async def create_linguistic_experiment(
    name: str,
    description: str,
    hypothesis: str,
    agent_selection_criteria: Dict[str, Any],
    duration: str = "24h",
    variables_tracked: List[str] = None,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Create a new linguistic research experiment
    
    Sets up controlled experiments to test hypotheses about
    language evolution, social influence, or innovation patterns.
    """
    try:
        # This would need implementation in the service layer
        return {
            "experiment_id": "placeholder",
            "status": "created",
            "message": "Experiment creation endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error creating experiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/experiments/{experiment_id}/results")
async def get_experiment_results(
    experiment_id: UUID,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    Get results from a linguistic experiment
    
    Returns statistical analysis and conclusions from
    completed linguistic evolution experiments.
    """
    try:
        # This would need implementation in the service layer
        return {
            "experiment_id": str(experiment_id),
            "results": {},
            "message": "Experiment results endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error getting experiment results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Utility Endpoints

@router.get("/debug/agent/{agent_id}/internal-state")
async def get_agent_debug_info(
    agent_id: UUID,
    include_semantics: bool = False,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    DEBUG ONLY: Get internal agent state for research
    
    WARNING: This endpoint reveals internal semantic mappings
    and should only be used for research and debugging purposes.
    """
    try:
        agent = await service.get_agent_linguistic_state(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        debug_info = {
            "agent_id": str(agent_id),
            "observable_state": await service.get_observable_agent_state(agent_id),
            "warning": "This endpoint reveals internal semantic mappings for research purposes only"
        }
        
        if include_semantics:
            debug_info["internal_meanings"] = agent.internal_meanings
            debug_info["aura_pattern_mappings"] = agent.aura_pattern_mappings
            debug_info["social_pattern_preferences"] = agent.social_pattern_preferences
        
        return debug_info
        
    except Exception as e:
        logger.error(f"Error getting debug info for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debug/reset-agent/{agent_id}")
async def reset_agent_linguistic_state(
    agent_id: UUID,
    confirm: bool = False,
    service: LinguisticService = Depends(get_linguistic_service)
):
    """
    DEBUG ONLY: Reset agent linguistic state
    
    WARNING: This will erase all linguistic development
    for the specified agent. Use only for testing.
    """
    try:
        if not confirm:
            raise HTTPException(
                status_code=400, 
                detail="Must set confirm=true to reset agent state"
            )
        
        # This would need implementation in the service layer
        return {
            "agent_id": str(agent_id),
            "status": "reset_requested",
            "message": "Agent reset endpoint - to be implemented"
        }
        
    except Exception as e:
        logger.error(f"Error resetting agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Include the router in the main application
__all__ = ["router"]