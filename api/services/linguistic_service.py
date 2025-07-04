"""
CHAOSTOWN Linguistic Service Layer
Business logic for linguistic evolution system
"""

import asyncio
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID, uuid4
import logging
from collections import defaultdict, Counter
import asyncpg
from contextlib import asynccontextmanager

from models.linguistic import (
    LinguisticAgentModel, CommunicationModel, DotPatternModel,
    LanguageFamilyModel, LinguisticInteractionModel, RSSInfluenceModel,
    AuraStateModel, CommunicationTrigger, InteractionType, LinguisticStage,
    PopulationMetricsResponse, PatternAnalysisResponse, SystemStatusModel,
    AgentObservableState
)

logger = logging.getLogger(__name__)


class PatternComplexityCalculator:
    """Mathematical analysis of dot pattern complexity"""
    
    @staticmethod
    def calculate_complexity(pattern: str) -> float:
        """Calculate pattern complexity using multiple mathematical measures"""
        if not pattern or pattern.isspace():
            return 0.0
        
        # Shannon Entropy
        entropy = PatternComplexityCalculator._shannon_entropy(pattern)
        
        # Pattern length normalized
        length_score = min(len(pattern) / 50.0, 1.0)
        
        # Spatial complexity
        spatial_score = PatternComplexityCalculator._spatial_complexity(pattern)
        
        # Repetition penalty
        repetition_penalty = PatternComplexityCalculator._repetition_penalty(pattern)
        
        # Weighted combination
        complexity = (
            entropy * 0.4 +
            length_score * 0.2 +
            spatial_score * 0.3 +
            repetition_penalty * 0.1
        )
        
        return min(max(complexity, 0.0), 1.0)
    
    @staticmethod
    def _shannon_entropy(pattern: str) -> float:
        """Calculate Shannon entropy of character distribution"""
        if not pattern:
            return 0.0
        
        char_counts = Counter(pattern)
        total_chars = len(pattern)
        
        entropy = 0.0
        for count in char_counts.values():
            probability = count / total_chars
            if probability > 0:
                entropy -= probability * (probability.bit_length() - 1)
        
        max_entropy = (len(char_counts)).bit_length() - 1 if len(char_counts) > 1 else 0
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    @staticmethod
    def _spatial_complexity(pattern: str) -> float:
        """Measure 2D spatial arrangement complexity"""
        lines = pattern.split('\n')
        if len(lines) <= 1:
            return 0.2
        
        positions = []
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '•':
                    positions.append((row, col))
        
        if len(positions) < 2:
            return 0.1
        
        # Calculate variance
        center_row = sum(pos[0] for pos in positions) / len(positions)
        center_col = sum(pos[1] for pos in positions) / len(positions)
        
        variance = sum(
            (pos[0] - center_row)**2 + (pos[1] - center_col)**2
            for pos in positions
        ) / len(positions)
        
        return min(variance / 20.0, 1.0)
    
    @staticmethod
    def _repetition_penalty(pattern: str) -> float:
        """Penalize simple repetitive patterns"""
        if len(pattern) < 3:
            return 1.0
        
        for repeat_len in range(1, len(pattern) // 2 + 1):
            substring = pattern[:repeat_len]
            if pattern == substring * (len(pattern) // repeat_len):
                penalty = 1.0 - (repeat_len / len(pattern))
                return max(penalty, 0.1)
        
        return 1.0


class LinguisticService:
    """Core linguistic system service"""
    
    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool
        self.complexity_calculator = PatternComplexityCalculator()
        self.active_streams: Dict[str, asyncio.Queue] = {}
        self.system_metrics_cache: Dict[str, Any] = {}
        self.cache_timestamp = 0
        self.cache_ttl = 60  # 1 minute cache
    
    async def initialize_agent(self, agent_id: UUID, initial_characteristics: Dict[str, Any]) -> LinguisticAgentModel:
        """Initialize a new linguistic agent"""
        async with self.db_pool.acquire() as conn:
            # Check if agent already exists
            existing = await conn.fetchrow(
                "SELECT * FROM linguistic_agents WHERE agent_id = $1",
                agent_id
            )
            
            if existing:
                return await self._row_to_linguistic_agent(existing)
            
            # Create new linguistic agent
            now = datetime.utcnow()
            innovation_tendency = initial_characteristics.get('innovation_tendency', 0.5)
            social_susceptibility = initial_characteristics.get('social_influence_susceptibility', 0.5)
            communication_threshold = initial_characteristics.get('communication_threshold', 0.6)
            
            await conn.execute("""
                INSERT INTO linguistic_agents (
                    agent_id, linguistic_stage, vocabulary_size, total_communications,
                    innovation_tendency, social_influence_susceptibility, communication_threshold,
                    literacy_level, character_recognition_count, word_association_count,
                    average_pattern_complexity, complexity_growth_rate, dialect_variance,
                    internal_meanings, aura_pattern_mappings, social_pattern_preferences,
                    created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
            """, 
                agent_id, 1, 0, 0, innovation_tendency, social_susceptibility, communication_threshold,
                0.0, 0, 0, 0.0, 0.01, 0.0, {}, {}, {}, now, now
            )
            
            # Return the new agent
            agent_row = await conn.fetchrow(
                "SELECT * FROM linguistic_agents WHERE agent_id = $1",
                agent_id
            )
            return await self._row_to_linguistic_agent(agent_row)
    
    async def get_agent_linguistic_state(self, agent_id: UUID) -> Optional[LinguisticAgentModel]:
        """Get current linguistic state of an agent"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM linguistic_agents WHERE agent_id = $1",
                agent_id
            )
            if row:
                return await self._row_to_linguistic_agent(row)
            return None
    
    async def trigger_agent_communication(
        self, 
        agent_id: UUID, 
        aura_state: AuraStateModel,
        nearby_agents: List[UUID] = None,
        rss_feeds: List[str] = None,
        offerings: List[Dict[str, Any]] = None,
        force_communication: bool = False
    ) -> Tuple[bool, Optional[CommunicationModel], float]:
        """
        Trigger communication attempt for an agent
        Returns (success, communication, pressure)
        """
        async with self.db_pool.acquire() as conn:
            # Get agent state
            agent = await self.get_agent_linguistic_state(agent_id)
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Get recent communications from nearby agents
            nearby_communications = await self._get_nearby_communications(
                conn, agent_id, nearby_agents or []
            )
            
            # Process RSS feeds if provided
            if rss_feeds:
                for feed_text in rss_feeds:
                    await self._process_rss_feed(conn, agent_id, feed_text, aura_state)
            
            # Process offerings if provided
            if offerings:
                await self._process_offerings(conn, agent_id, offerings, aura_state)
            
            # Calculate communication pressure
            pressure = await self._calculate_communication_pressure(agent, aura_state)
            
            # Check if communication should occur
            should_communicate = force_communication or pressure > agent.communication_threshold
            
            if not should_communicate:
                return False, None, pressure
            
            # Generate communication
            communication = await self._generate_communication(
                conn, agent, aura_state, nearby_communications, pressure
            )
            
            # Broadcast to live streams
            await self._broadcast_communication(communication)
            
            return True, communication, pressure
    
    async def get_population_metrics(
        self, 
        time_range: str = "24h",
        include_trends: bool = True,
        include_families: bool = True,
        include_patterns: bool = True,
        agent_filter: Optional[List[UUID]] = None
    ) -> PopulationMetricsResponse:
        """Get population-level linguistic metrics"""
        
        # Check cache first
        cache_key = f"population_metrics_{time_range}_{include_trends}_{include_families}_{include_patterns}"
        if (time.time() - self.cache_timestamp < self.cache_ttl and 
            cache_key in self.system_metrics_cache):
            return self.system_metrics_cache[cache_key]
        
        async with self.db_pool.acquire() as conn:
            # Parse time range
            if time_range == "24h":
                since = datetime.utcnow() - timedelta(hours=24)
            elif time_range == "7d":
                since = datetime.utcnow() - timedelta(days=7)
            elif time_range == "30d":
                since = datetime.utcnow() - timedelta(days=30)
            else:
                since = datetime.utcnow() - timedelta(hours=24)
            
            # Base metrics
            total_agents = await conn.fetchval(
                "SELECT COUNT(*) FROM linguistic_agents"
            )
            
            active_agents = await conn.fetchval(
                "SELECT COUNT(*) FROM linguistic_agents WHERE last_communication > $1",
                since
            )
            
            total_communications = await conn.fetchval(
                "SELECT COUNT(*) FROM communications WHERE timestamp > $1",
                since
            )
            
            unique_patterns = await conn.fetchval(
                "SELECT COUNT(DISTINCT pattern_hash) FROM communications WHERE timestamp > $1",
                since
            )
            
            language_families = await conn.fetchval(
                "SELECT COUNT(*) FROM language_families"
            )
            
            # Stage distribution
            stage_rows = await conn.fetch(
                "SELECT linguistic_stage, COUNT(*) FROM linguistic_agents GROUP BY linguistic_stage"
            )
            stage_distribution = {LinguisticStage(row['linguistic_stage']): row['count'] for row in stage_rows}
            
            # Communication trends
            communication_trends = {}
            if include_trends:
                communication_trends = await self._get_communication_trends(conn, since)
            
            # Complexity trends
            complexity_trends = {}
            if include_trends:
                complexity_trends = await self._get_complexity_trends(conn, since)
            
            # Innovation trends
            innovation_trends = {}
            if include_trends:
                innovation_trends = await self._get_innovation_trends(conn, since)
            
            # Family metrics
            family_metrics = None
            if include_families:
                family_metrics = await self._get_family_metrics(conn, since)
            
            # Pattern metrics
            pattern_metrics = None
            if include_patterns:
                pattern_metrics = await self._get_pattern_metrics(conn, since)
            
            # System health
            system_health = await self._calculate_system_health(conn, since)
            
            response = PopulationMetricsResponse(
                total_agents=total_agents,
                active_agents=active_agents,
                total_communications=total_communications,
                unique_patterns=unique_patterns,
                language_families=language_families,
                stage_distribution=stage_distribution,
                communication_trends=communication_trends,
                complexity_trends=complexity_trends,
                innovation_trends=innovation_trends,
                family_metrics=family_metrics,
                pattern_metrics=pattern_metrics,
                system_health=system_health
            )
            
            # Cache the response
            self.system_metrics_cache[cache_key] = response
            self.cache_timestamp = time.time()
            
            return response
    
    async def analyze_patterns(
        self, 
        patterns: List[str],
        include_complexity: bool = True,
        include_similarity: bool = False,
        include_evolution: bool = False
    ) -> PatternAnalysisResponse:
        """Analyze dot patterns for complexity and relationships"""
        
        pattern_analyses = []
        complexities = []
        
        for pattern in patterns:
            analysis = {"pattern": pattern}
            
            if include_complexity:
                complexity = self.complexity_calculator.calculate_complexity(pattern)
                analysis["complexity"] = complexity
                analysis["shannon_entropy"] = self.complexity_calculator._shannon_entropy(pattern)
                analysis["spatial_complexity"] = self.complexity_calculator._spatial_complexity(pattern)
                analysis["repetition_penalty"] = self.complexity_calculator._repetition_penalty(pattern)
                complexities.append(complexity)
            
            if include_similarity:
                # Calculate similarity to other patterns
                similarities = []
                for other_pattern in patterns:
                    if other_pattern != pattern:
                        similarity = self._calculate_pattern_similarity(pattern, other_pattern)
                        similarities.append(similarity)
                analysis["avg_similarity"] = sum(similarities) / len(similarities) if similarities else 0.0
            
            if include_evolution:
                async with self.db_pool.acquire() as conn:
                    pattern_hash = hashlib.sha256(pattern.encode()).hexdigest()
                    evolution_data = await conn.fetchrow(
                        """SELECT parent_pattern_id, pattern_generation, child_patterns_count,
                           adoption_rate, success_rate, cultural_penetration
                           FROM dot_patterns WHERE pattern_hash = $1""",
                        pattern_hash
                    )
                    if evolution_data:
                        analysis["evolution"] = dict(evolution_data)
            
            pattern_analyses.append(analysis)
        
        # Summary statistics
        summary = {
            "total_patterns": len(patterns),
            "unique_patterns": len(set(patterns))
        }
        
        complexity_distribution = {}
        if complexities:
            complexity_distribution = {
                "min": min(complexities),
                "max": max(complexities),
                "avg": sum(complexities) / len(complexities),
                "distribution": self._get_complexity_distribution(complexities)
            }
        
        # Innovation metrics
        innovation_metrics = await self._get_innovation_metrics_for_patterns(patterns)
        
        return PatternAnalysisResponse(
            patterns=pattern_analyses,
            summary=summary,
            complexity_distribution=complexity_distribution,
            innovation_metrics=innovation_metrics
        )
    
    async def process_rss_feed(
        self, 
        agent_ids: List[UUID], 
        feed_content: str,
        feed_source: Optional[str] = None,
        quality_score: float = 1.0
    ) -> Dict[str, Any]:
        """Process RSS feed for multiple agents"""
        
        influences = []
        triggered_communications = []
        literacy_improvements = {}
        
        async with self.db_pool.acquire() as conn:
            for agent_id in agent_ids:
                # Get agent state
                agent = await self.get_agent_linguistic_state(agent_id)
                if not agent:
                    continue
                
                # Create aura state for processing
                aura_state = AuraStateModel(
                    warmth_gradient=0.6,
                    resource_density=0.5,
                    danger_proximity=0.1,
                    cat_happiness=0.8,
                    social_longing=0.7,
                    innovation_energy=0.6,
                    literacy_exposure=0.5
                )
                
                # Process RSS feed
                influence = await self._process_rss_feed(conn, agent_id, feed_content, aura_state)
                influences.append(influence)
                
                # Check if communication was triggered
                if influence.triggered_communication:
                    comm = await conn.fetchrow(
                        "SELECT * FROM communications WHERE id = $1",
                        influence.communication_id
                    )
                    if comm:
                        triggered_communications.append(await self._row_to_communication(comm))
                
                # Track literacy improvement
                literacy_improvements[agent_id] = influence.literacy_after - influence.literacy_before
        
        return {
            "processed_agents": len(agent_ids),
            "influences": influences,
            "triggered_communications": triggered_communications,
            "literacy_improvements": literacy_improvements,
            "summary": {
                "total_literacy_boost": sum(literacy_improvements.values()),
                "communications_triggered": len(triggered_communications),
                "avg_influence_strength": sum(i.influence_strength for i in influences) / len(influences) if influences else 0
            }
        }
    
    async def get_observable_agent_state(self, agent_id: UUID) -> Optional[AgentObservableState]:
        """Get observable state for human researchers (no internal meanings)"""
        async with self.db_pool.acquire() as conn:
            # Get agent data
            agent_row = await conn.fetchrow(
                "SELECT * FROM linguistic_agents WHERE agent_id = $1",
                agent_id
            )
            if not agent_row:
                return None
            
            # Get recent patterns
            recent_patterns = await conn.fetch(
                """SELECT dot_pattern FROM communications 
                   WHERE agent_id = $1 
                   ORDER BY timestamp DESC 
                   LIMIT 5""",
                agent_id
            )
            
            # Get complexity trend
            complexity_trend = await conn.fetch(
                """SELECT pattern_complexity FROM communications 
                   WHERE agent_id = $1 
                   ORDER BY timestamp DESC 
                   LIMIT 10""",
                agent_id
            )
            
            # Get family affiliation
            family_name = await conn.fetchval(
                """SELECT lf.name FROM language_families lf
                   JOIN linguistic_agents la ON lf.id = la.primary_language_family
                   WHERE la.agent_id = $1""",
                agent_id
            )
            
            # Stage progression metrics
            stage_metrics = {
                "vocabulary_size": agent_row['vocabulary_size'],
                "avg_pattern_complexity": agent_row['average_pattern_complexity'],
                "communication_frequency": agent_row['total_communications'],
                "innovation_rate": await conn.fetchval(
                    """SELECT COUNT(*) FROM dot_patterns 
                       WHERE created_by_agent = $1""",
                    agent_id
                ) or 0
            }
            
            return AgentObservableState(
                agent_id=agent_id,
                linguistic_stage=LinguisticStage(agent_row['linguistic_stage']),
                vocabulary_size=agent_row['vocabulary_size'],
                total_communications=agent_row['total_communications'],
                literacy_level=agent_row['literacy_level'],
                character_recognition_count=agent_row['character_recognition_count'],
                innovation_tendency=agent_row['innovation_tendency'],
                recent_patterns=[row['dot_pattern'] for row in recent_patterns],
                pattern_complexity_trend=[row['pattern_complexity'] for row in complexity_trend],
                stage_progression_metrics=stage_metrics,
                family_affiliation=family_name,
                last_activity=agent_row['last_communication']
            )
    
    # Stream management
    async def subscribe_to_live_stream(self, stream_id: str) -> asyncio.Queue:
        """Subscribe to live communication stream"""
        if stream_id not in self.active_streams:
            self.active_streams[stream_id] = asyncio.Queue()
        return self.active_streams[stream_id]
    
    async def unsubscribe_from_live_stream(self, stream_id: str):
        """Unsubscribe from live communication stream"""
        if stream_id in self.active_streams:
            del self.active_streams[stream_id]
    
    # Private helper methods
    async def _row_to_linguistic_agent(self, row) -> LinguisticAgentModel:
        """Convert database row to LinguisticAgentModel"""
        return LinguisticAgentModel(
            agent_id=row['agent_id'],
            linguistic_stage=LinguisticStage(row['linguistic_stage']),
            vocabulary_size=row['vocabulary_size'],
            total_communications=row['total_communications'],
            innovation_tendency=row['innovation_tendency'],
            social_influence_susceptibility=row['social_influence_susceptibility'],
            communication_threshold=row['communication_threshold'],
            literacy_level=row['literacy_level'],
            character_recognition_count=row['character_recognition_count'],
            word_association_count=row['word_association_count'],
            average_pattern_complexity=row['average_pattern_complexity'],
            complexity_growth_rate=row['complexity_growth_rate'],
            primary_language_family=row['primary_language_family'],
            dialect_variance=row['dialect_variance'],
            first_communication=row['first_communication'],
            last_communication=row['last_communication'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            internal_meanings=row['internal_meanings'],
            aura_pattern_mappings=row['aura_pattern_mappings'],
            social_pattern_preferences=row['social_pattern_preferences']
        )
    
    async def _row_to_communication(self, row) -> CommunicationModel:
        """Convert database row to CommunicationModel"""
        return CommunicationModel(
            id=row['id'],
            agent_id=row['agent_id'],
            tick_number=row['tick_number'],
            timestamp=row['timestamp'],
            dot_pattern=row['dot_pattern'],
            pattern_complexity=row['pattern_complexity'],
            pattern_hash=row['pattern_hash'],
            aura_context=AuraStateModel(**row['aura_context']),
            social_context=row['social_context'],
            internal_pressure=row['internal_pressure'],
            communication_trigger=CommunicationTrigger(row['communication_trigger']),
            is_innovation=row['is_innovation'],
            pattern_first_use=row['pattern_first_use'],
            innovation_source=row['innovation_source'],
            response_count=row['response_count'],
            adoption_count=row['adoption_count'],
            success_indicators=row['success_indicators'],
            rss_influenced=row['rss_influenced'],
            rss_content_hash=row['rss_content_hash'],
            literacy_boost=row['literacy_boost'],
            position_x=row['position_x'],
            position_y=row['position_y'],
            nearby_agents=row['nearby_agents'] or []
        )
    
    async def _get_nearby_communications(self, conn, agent_id: UUID, nearby_agents: List[UUID]) -> List[Tuple[str, str]]:
        """Get recent communications from nearby agents"""
        if not nearby_agents:
            return []
        
        rows = await conn.fetch(
            """SELECT agent_id, dot_pattern FROM communications 
               WHERE agent_id = ANY($1) AND timestamp > $2
               ORDER BY timestamp DESC LIMIT 10""",
            nearby_agents,
            datetime.utcnow() - timedelta(minutes=10)
        )
        
        return [(str(row['agent_id']), row['dot_pattern']) for row in rows]
    
    async def _calculate_communication_pressure(self, agent: LinguisticAgentModel, aura_state: AuraStateModel) -> float:
        """Calculate internal pressure to communicate"""
        social_pressure = aura_state.social_longing * 0.3
        danger_pressure = aura_state.danger_proximity * 0.4
        resource_pressure = (1.0 - aura_state.resource_density) * 0.2
        happiness_pressure = (1.0 - aura_state.cat_happiness) * 0.3
        innovation_pressure = aura_state.innovation_energy * agent.innovation_tendency * 0.2
        literacy_pressure = agent.literacy_level * 0.1
        
        total_pressure = (
            social_pressure + danger_pressure + resource_pressure + 
            happiness_pressure + innovation_pressure + literacy_pressure
        )
        
        return min(total_pressure, 1.0)
    
    async def _generate_communication(
        self, 
        conn, 
        agent: LinguisticAgentModel, 
        aura_state: AuraStateModel,
        nearby_communications: List[Tuple[str, str]],
        pressure: float
    ) -> CommunicationModel:
        """Generate a new communication"""
        
        # Simple pattern generation based on aura state
        if aura_state.danger_proximity > 0.7:
            pattern = "•••••"
        elif aura_state.warmth_gradient > 0.8:
            pattern = "• • •"
        elif aura_state.social_longing > 0.7:
            pattern = "•\n •\n  •"
        elif aura_state.cat_happiness < 0.5:
            pattern = "••\n••"
        else:
            pattern = "•"
        
        # Calculate complexity
        complexity = self.complexity_calculator.calculate_complexity(pattern)
        pattern_hash = hashlib.sha256(pattern.encode()).hexdigest()
        
        # Determine communication trigger
        if aura_state.danger_proximity > 0.6:
            trigger = CommunicationTrigger.DANGER_PROXIMITY
        elif aura_state.social_longing > 0.7:
            trigger = CommunicationTrigger.SOCIAL_LONGING
        elif aura_state.innovation_energy > 0.8:
            trigger = CommunicationTrigger.INNOVATION_DRIVE
        else:
            trigger = CommunicationTrigger.AURA_RESPONSE
        
        # Create communication record
        comm_id = uuid4()
        now = datetime.utcnow()
        
        await conn.execute(
            """INSERT INTO communications (
                id, agent_id, tick_number, timestamp, dot_pattern, pattern_complexity,
                pattern_hash, aura_context, social_context, internal_pressure,
                communication_trigger, is_innovation, pattern_first_use
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)""",
            comm_id, agent.agent_id, 0, now, pattern, complexity,
            pattern_hash, aura_state.dict(), {}, pressure,
            trigger.value, True, True
        )
        
        # Get the created communication
        comm_row = await conn.fetchrow(
            "SELECT * FROM communications WHERE id = $1",
            comm_id
        )
        
        return await self._row_to_communication(comm_row)
    
    async def _process_rss_feed(self, conn, agent_id: UUID, feed_content: str, aura_state: AuraStateModel) -> RSSInfluenceModel:
        """Process RSS feed for an agent"""
        
        # Get current agent state
        agent = await self.get_agent_linguistic_state(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Calculate vibes extracted
        vibes_extracted = self._extract_vibes_from_text(feed_content, aura_state)
        
        # Simulate character recognition improvement
        characters_recognized = len(set(c for c in feed_content.lower() if c.isalnum()))
        new_character_learning = max(0, characters_recognized - agent.character_recognition_count)
        
        # Update literacy
        literacy_before = agent.literacy_level
        literacy_boost = min(vibes_extracted * 0.1, 0.1)
        literacy_after = min(literacy_before + literacy_boost, 1.0)
        
        # Update agent literacy
        await conn.execute(
            """UPDATE linguistic_agents 
               SET literacy_level = $1, character_recognition_count = $2, updated_at = $3
               WHERE agent_id = $4""",
            literacy_after, 
            agent.character_recognition_count + new_character_learning,
            datetime.utcnow(),
            agent_id
        )
        
        # Create RSS influence record
        rss_id = uuid4()
        content_hash = hashlib.sha256(feed_content.encode()).hexdigest()
        
        await conn.execute(
            """INSERT INTO rss_linguistic_influence (
                id, agent_id, rss_content_hash, rss_content_summary, content_length,
                vibes_extracted, characters_recognized, new_character_learning,
                word_associations_formed, influence_strength, literacy_before,
                literacy_after, aura_state_at_processing
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)""",
            rss_id, agent_id, content_hash, feed_content[:200], len(feed_content),
            vibes_extracted, characters_recognized, new_character_learning,
            0, vibes_extracted, literacy_before, literacy_after, aura_state.dict()
        )
        
        return RSSInfluenceModel(
            id=rss_id,
            agent_id=agent_id,
            timestamp=datetime.utcnow(),
            rss_content_hash=content_hash,
            rss_content_summary=feed_content[:200],
            content_length=len(feed_content),
            vibes_extracted=vibes_extracted,
            characters_recognized=characters_recognized,
            new_character_learning=new_character_learning,
            word_associations_formed=0,
            triggered_communication=False,
            influence_strength=vibes_extracted,
            literacy_before=literacy_before,
            literacy_after=literacy_after,
            aura_state_at_processing=aura_state
        )
    
    def _extract_vibes_from_text(self, text: str, aura_context: AuraStateModel) -> float:
        """Extract vibes from text without understanding words"""
        length_factor = min(len(text) / 1000.0, 1.0)
        exclamation_count = text.count('!')
        question_count = text.count('?')
        punctuation_intensity = min((exclamation_count + question_count) / 10.0, 1.0)
        capitals_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        emphasis_factor = min(capitals_ratio * 3, 1.0)
        
        words = text.lower().split()
        word_counts = Counter(words)
        repetition_factor = len([w for w, c in word_counts.items() if c > 1]) / len(words) if words else 0
        
        vibe_strength = (
            length_factor * 0.3 +
            punctuation_intensity * 0.3 +
            emphasis_factor * 0.2 +
            repetition_factor * 0.2
        )
        
        vibe_strength *= (aura_context.social_longing + 0.5)
        return min(vibe_strength, 1.0)
    
    async def _process_offerings(self, conn, agent_id: UUID, offerings: List[Dict[str, Any]], aura_state: AuraStateModel):
        """Process special offerings for an agent"""
        for offering in offerings:
            if offering.get('type') == 'cat_media':
                # Boost aura state
                aura_state.cat_happiness = min(aura_state.cat_happiness + 0.1, 1.0)
                aura_state.social_longing = min(aura_state.social_longing + 0.2, 1.0)
                aura_state.warmth_gradient = min(aura_state.warmth_gradient + 0.15, 1.0)
    
    async def _broadcast_communication(self, communication: CommunicationModel):
        """Broadcast communication to all active streams"""
        message = {
            "event_type": "communication",
            "timestamp": communication.timestamp.isoformat(),
            "data": {
                "agent_id": str(communication.agent_id),
                "pattern": communication.dot_pattern,
                "complexity": communication.pattern_complexity,
                "trigger": communication.communication_trigger.value,
                "aura_context": communication.aura_context.dict()
            }
        }
        
        for stream_id, queue in self.active_streams.items():
            try:
                await queue.put(message)
            except Exception as e:
                logger.error(f"Failed to broadcast to stream {stream_id}: {e}")
    
    def _calculate_pattern_similarity(self, pattern1: str, pattern2: str) -> float:
        """Calculate similarity between two patterns"""
        if pattern1 == pattern2:
            return 1.0
        
        # Simple similarity based on character overlap
        set1 = set(pattern1)
        set2 = set(pattern2)
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def _get_complexity_distribution(self, complexities: List[float]) -> Dict[str, int]:
        """Get distribution of complexities"""
        bins = {"low": 0, "medium": 0, "high": 0}
        for complexity in complexities:
            if complexity < 0.33:
                bins["low"] += 1
            elif complexity < 0.66:
                bins["medium"] += 1
            else:
                bins["high"] += 1
        return bins
    
    async def _get_innovation_metrics_for_patterns(self, patterns: List[str]) -> Dict[str, Any]:
        """Get innovation metrics for patterns"""
        async with self.db_pool.acquire() as conn:
            pattern_hashes = [hashlib.sha256(p.encode()).hexdigest() for p in patterns]
            
            innovation_count = await conn.fetchval(
                """SELECT COUNT(*) FROM dot_patterns 
                   WHERE pattern_hash = ANY($1) AND pattern_generation = 1""",
                pattern_hashes
            )
            
            return {
                "innovation_count": innovation_count or 0,
                "innovation_rate": (innovation_count or 0) / len(patterns) if patterns else 0,
                "total_patterns": len(patterns)
            }
    
    async def _get_communication_trends(self, conn, since: datetime) -> Dict[str, Any]:
        """Get communication trends"""
        hourly_counts = await conn.fetch(
            """SELECT DATE_TRUNC('hour', timestamp) as hour, COUNT(*) as count
               FROM communications 
               WHERE timestamp > $1 
               GROUP BY hour 
               ORDER BY hour""",
            since
        )
        
        return {
            "hourly_counts": [{"hour": row['hour'].isoformat(), "count": row['count']} for row in hourly_counts],
            "total_trend": "increasing" if len(hourly_counts) > 1 and hourly_counts[-1]['count'] > hourly_counts[0]['count'] else "stable"
        }
    
    async def _get_complexity_trends(self, conn, since: datetime) -> Dict[str, Any]:
        """Get complexity evolution trends"""
        complexity_by_hour = await conn.fetch(
            """SELECT DATE_TRUNC('hour', timestamp) as hour, AVG(pattern_complexity) as avg_complexity
               FROM communications 
               WHERE timestamp > $1 
               GROUP BY hour 
               ORDER BY hour""",
            since
        )
        
        return {
            "hourly_complexity": [{"hour": row['hour'].isoformat(), "complexity": float(row['avg_complexity'])} for row in complexity_by_hour],
            "evolution_trend": "increasing" if len(complexity_by_hour) > 1 and complexity_by_hour[-1]['avg_complexity'] > complexity_by_hour[0]['avg_complexity'] else "stable"
        }
    
    async def _get_innovation_trends(self, conn, since: datetime) -> Dict[str, Any]:
        """Get innovation trends"""
        innovation_by_hour = await conn.fetch(
            """SELECT DATE_TRUNC('hour', timestamp) as hour, 
                      COUNT(*) FILTER (WHERE is_innovation) as innovations,
                      COUNT(*) as total_communications
               FROM communications 
               WHERE timestamp > $1 
               GROUP BY hour 
               ORDER BY hour""",
            since
        )
        
        return {
            "hourly_innovations": [
                {
                    "hour": row['hour'].isoformat(), 
                    "innovations": row['innovations'],
                    "rate": row['innovations'] / row['total_communications'] if row['total_communications'] > 0 else 0
                } 
                for row in innovation_by_hour
            ]
        }
    
    async def _get_family_metrics(self, conn, since: datetime) -> Dict[str, Any]:
        """Get language family metrics"""
        family_stats = await conn.fetch(
            """SELECT lf.name, lf.member_count, lf.internal_cohesion, lf.external_influence,
                      COUNT(c.id) as recent_communications
               FROM language_families lf
               LEFT JOIN linguistic_agents la ON lf.id = la.primary_language_family
               LEFT JOIN communications c ON la.agent_id = c.agent_id AND c.timestamp > $1
               GROUP BY lf.id, lf.name, lf.member_count, lf.internal_cohesion, lf.external_influence""",
            since
        )
        
        return {
            "families": [
                {
                    "name": row['name'],
                    "member_count": row['member_count'],
                    "cohesion": float(row['internal_cohesion']),
                    "influence": float(row['external_influence']),
                    "recent_activity": row['recent_communications']
                }
                for row in family_stats
            ]
        }
    
    async def _get_pattern_metrics(self, conn, since: datetime) -> Dict[str, Any]:
        """Get pattern usage metrics"""
        popular_patterns = await conn.fetch(
            """SELECT dp.dot_pattern, dp.complexity, dp.total_usage_count,
                      COUNT(c.id) as recent_usage
               FROM dot_patterns dp
               LEFT JOIN communications c ON dp.pattern_hash = c.pattern_hash AND c.timestamp > $1
               GROUP BY dp.id, dp.dot_pattern, dp.complexity, dp.total_usage_count
               ORDER BY recent_usage DESC
               LIMIT 10""",
            since
        )
        
        return {
            "popular_patterns": [
                {
                    "pattern": row['dot_pattern'],
                    "complexity": float(row['complexity']),
                    "total_usage": row['total_usage_count'],
                    "recent_usage": row['recent_usage']
                }
                for row in popular_patterns
            ]
        }
    
    async def _calculate_system_health(self, conn, since: datetime) -> Dict[str, Any]:
        """Calculate overall system health metrics"""
        
        # Agent activity health
        active_ratio = await conn.fetchval(
            """SELECT COUNT(*) FILTER (WHERE last_communication > $1)::float / COUNT(*)
               FROM linguistic_agents""",
            since
        )
        
        # Communication health
        avg_complexity = await conn.fetchval(
            """SELECT AVG(pattern_complexity) FROM communications WHERE timestamp > $1""",
            since
        )
        
        # Innovation health
        innovation_rate = await conn.fetchval(
            """SELECT COUNT(*) FILTER (WHERE is_innovation)::float / COUNT(*)
               FROM communications WHERE timestamp > $1""",
            since
        )
        
        # Overall health score
        health_score = (
            (active_ratio or 0) * 0.4 +
            (avg_complexity or 0) * 0.3 +
            (innovation_rate or 0) * 0.3
        )
        
        if health_score > 0.8:
            status = "excellent"
        elif health_score > 0.6:
            status = "good"
        elif health_score > 0.4:
            status = "fair"
        else:
            status = "poor"
        
        return {
            "overall_status": status,
            "health_score": health_score,
            "active_agent_ratio": active_ratio or 0,
            "avg_complexity": float(avg_complexity) if avg_complexity else 0,
            "innovation_rate": innovation_rate or 0,
            "recommendations": self._get_health_recommendations(active_ratio, avg_complexity, innovation_rate)
        }
    
    def _get_health_recommendations(self, active_ratio: float, avg_complexity: float, innovation_rate: float) -> List[str]:
        """Get health recommendations based on metrics"""
        recommendations = []
        
        if (active_ratio or 0) < 0.5:
            recommendations.append("Increase agent activity through RSS feeds or environmental stimulation")
        
        if (avg_complexity or 0) < 0.3:
            recommendations.append("Encourage pattern complexity through innovation challenges")
        
        if (innovation_rate or 0) < 0.2:
            recommendations.append("Boost innovation through environmental pressure or agent diversity")
        
        return recommendations