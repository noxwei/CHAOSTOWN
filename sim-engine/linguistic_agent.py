#!/usr/bin/env python3
"""
CHAOSTOWN Linguistic Agent System
Mathematical implementation of emergent dot-based language evolution
"""

import random
import time
import json
import math
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
# import numpy as np  # Removed to avoid dependencies

@dataclass
class AuraState:
    """Environmental and internal aura readings"""
    warmth_gradient: float      # 0.0-1.0 comfort level
    resource_density: float     # 0.0-1.0 resources nearby
    danger_proximity: float     # 0.0-1.0 threat detection
    cat_happiness: float        # 0.0-1.0 prime directive
    social_longing: float       # 0.0-1.0 need to communicate
    innovation_energy: float    # 0.0-1.0 creativity drive
    literacy_exposure: float    # 0.0-1.0 accumulated text exposure

@dataclass
class DotPattern:
    """A communication pattern in dot language"""
    pattern: str                # The actual dot sequence
    complexity: float           # Mathematical complexity score
    created_by: str            # Agent ID who created it
    timestamp: float           # When it was first used
    usage_count: int           # How often it's been used
    success_rate: float        # Communication effectiveness

class PatternComplexityCalculator:
    """Mathematical analysis of dot pattern complexity"""
    
    @staticmethod
    def calculate_complexity(pattern: str) -> float:
        """
        Calculate pattern complexity using multiple mathematical measures
        """
        if not pattern or pattern.isspace():
            return 0.0
        
        # 1. Shannon Entropy (information content)
        entropy = PatternComplexityCalculator._shannon_entropy(pattern)
        
        # 2. Pattern length normalized
        length_score = min(len(pattern) / 50.0, 1.0)  # Cap at 50 chars
        
        # 3. Spatial complexity (2D arrangement)
        spatial_score = PatternComplexityCalculator._spatial_complexity(pattern)
        
        # 4. Repetition penalty (simple patterns score lower)
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
        
        # Count character frequencies
        char_counts = Counter(pattern)
        total_chars = len(pattern)
        
        # Calculate entropy
        entropy = 0.0
        for count in char_counts.values():
            probability = count / total_chars
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Normalize to 0-1 range
        max_entropy = math.log2(len(char_counts)) if len(char_counts) > 1 else 0
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    @staticmethod
    def _spatial_complexity(pattern: str) -> float:
        """Measure 2D spatial arrangement complexity"""
        lines = pattern.split('\n')
        if len(lines) <= 1:
            return 0.2  # Linear patterns are simple
        
        # Calculate spatial variance
        positions = []
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '•':
                    positions.append((row, col))
        
        if len(positions) < 2:
            return 0.1
        
        # Calculate center of mass and variance
        center_row = sum(pos[0] for pos in positions) / len(positions)
        center_col = sum(pos[1] for pos in positions) / len(positions)
        
        variance = sum(
            (pos[0] - center_row)**2 + (pos[1] - center_col)**2
            for pos in positions
        ) / len(positions)
        
        # Normalize spatial complexity
        return min(variance / 20.0, 1.0)  # Empirical normalization
    
    @staticmethod
    def _repetition_penalty(pattern: str) -> float:
        """Penalize simple repetitive patterns"""
        if len(pattern) < 3:
            return 1.0
        
        # Check for simple repetitions
        for repeat_len in range(1, len(pattern) // 2 + 1):
            substring = pattern[:repeat_len]
            if pattern == substring * (len(pattern) // repeat_len):
                # Found exact repetition
                penalty = 1.0 - (repeat_len / len(pattern))
                return max(penalty, 0.1)
        
        return 1.0  # No simple repetition found

class LiteracyAcquisition:
    """Manages gradual literacy development through RSS feeds and offerings"""
    
    def __init__(self):
        self.text_fragments = []  # Accumulated text exposure
        self.character_recognition = {}  # char -> familiarity (0.0-1.0)
        self.word_associations = {}  # word -> aura associations
        self.literacy_level = 0.0  # Overall reading ability (0.0-1.0)
    
    def process_rss_feed(self, text_content: str, aura_context: AuraState) -> float:
        """
        Process RSS feed text and extract vibes/auras initially,
        gradually building character recognition
        """
        if not text_content:
            return 0.0
        
        # Initially, only extract emotional/contextual vibes
        vibes_extracted = self._extract_vibes_from_text(text_content, aura_context)
        
        # Gradually build character familiarity based on exposure
        self._update_character_recognition(text_content)
        
        # As literacy improves, start associating words with auras
        if self.literacy_level > 0.3:
            self._associate_words_with_auras(text_content, aura_context)
        
        # Return vibe strength extracted
        return vibes_extracted
    
    def _extract_vibes_from_text(self, text: str, aura_context: AuraState) -> float:
        """
        Mathematical extraction of emotional vibes from text
        without understanding specific words
        """
        # Text length suggests importance
        length_factor = min(len(text) / 1000.0, 1.0)
        
        # Punctuation suggests emotional intensity
        exclamation_count = text.count('!')
        question_count = text.count('?')
        punctuation_intensity = min((exclamation_count + question_count) / 10.0, 1.0)
        
        # Capital letters suggest emphasis/emotion
        capitals_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        emphasis_factor = min(capitals_ratio * 3, 1.0)
        
        # Word repetition suggests emphasis
        words = text.lower().split()
        word_counts = Counter(words)
        repetition_factor = len([w for w, c in word_counts.items() if c > 1]) / len(words) if words else 0
        
        # Combine factors with current aura state
        vibe_strength = (
            length_factor * 0.3 +
            punctuation_intensity * 0.3 +
            emphasis_factor * 0.2 +
            repetition_factor * 0.2
        )
        
        # Modulate by current social longing (need for information)
        vibe_strength *= (aura_context.social_longing + 0.5)
        
        return min(vibe_strength, 1.0)
    
    def _update_character_recognition(self, text: str):
        """Gradually build familiarity with individual characters"""
        for char in text:
            if char.isalnum():  # Only track alphanumeric characters
                if char not in self.character_recognition:
                    self.character_recognition[char] = 0.0
                
                # Increase familiarity slowly
                self.character_recognition[char] += 0.01
                self.character_recognition[char] = min(self.character_recognition[char], 1.0)
        
        # Update overall literacy level
        if self.character_recognition:
            self.literacy_level = sum(self.character_recognition.values()) / (26 + 10)  # a-z + 0-9
            self.literacy_level = min(self.literacy_level, 1.0)
    
    def _associate_words_with_auras(self, text: str, aura_context: AuraState):
        """Associate specific words with current aura states (literacy phase)"""
        if self.literacy_level < 0.3:
            return
        
        words = text.lower().split()
        for word in words:
            # Only process words if we recognize most characters
            char_familiarity = sum(
                self.character_recognition.get(c, 0.0) for c in word if c.isalnum()
            ) / len(word) if word else 0
            
            if char_familiarity > 0.5:  # Can partially "read" this word
                if word not in self.word_associations:
                    self.word_associations[word] = {}
                
                # Associate word with current aura context
                for aura_name in ['warmth_gradient', 'resource_density', 'danger_proximity', 
                                 'cat_happiness', 'social_longing']:
                    aura_value = getattr(aura_context, aura_name)
                    if word not in self.word_associations:
                        self.word_associations[word] = {}
                    if aura_name not in self.word_associations[word]:
                        self.word_associations[word][aura_name] = []
                    
                    self.word_associations[word][aura_name].append(aura_value)

class LinguisticAgent:
    """
    Mathematical model of an agent developing language from aura-based perception
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.creation_time = time.time()
        
        # Core linguistic state
        self.dot_vocabulary: Dict[str, DotPattern] = {}  # Known patterns
        self.communication_history: List[Tuple[float, str, Dict]] = []  # Time, pattern, context
        self.linguistic_stage = 1  # Development stage (1-5)
        
        # Personal characteristics
        self.innovation_tendency = random.uniform(0.1, 0.9)  # Creativity vs imitation
        self.social_influence_susceptibility = random.uniform(0.2, 0.8)
        self.communication_threshold = random.uniform(0.4, 0.8)  # When to speak
        
        # Pattern generation parameters
        self.base_pattern_complexity = 0.1  # Starting simple
        self.complexity_growth_rate = 0.01  # How fast patterns evolve
        
        # Literacy development
        self.literacy = LiteracyAcquisition()
        
        # Internal semantic network (opaque to humans)
        self._internal_meanings: Dict[str, Dict] = {}  # Pattern -> internal concept
        self._aura_to_pattern_mappings: Dict[str, List[str]] = defaultdict(list)
        self._social_pattern_preferences: Dict[str, float] = {}  # Agent ID -> preference
    
    def perceive_environment(self, aura_state: AuraState, nearby_communications: List[Tuple[str, str]], 
                           rss_feeds: List[str] = None, offerings: List[Dict] = None) -> Optional[str]:
        """
        Main perception and communication loop
        
        Args:
            aura_state: Current environmental auras
            nearby_communications: List of (agent_id, pattern) from nearby agents
            rss_feeds: Text content from RSS feeds (if any)
            offerings: Special offerings that boost learning
            
        Returns:
            Dot pattern to communicate, or None if no communication needed
        """
        
        # 1. Process RSS feeds and offerings for literacy development
        if rss_feeds:
            for feed_text in rss_feeds:
                vibe_strength = self.literacy.process_rss_feed(feed_text, aura_state)
                # Vibes influence aura state
                aura_state.social_longing += vibe_strength * 0.1
                aura_state.innovation_energy += vibe_strength * 0.05
        
        if offerings:
            self._process_offerings(offerings, aura_state)
        
        # 2. Learn from nearby communications
        self._observe_communications(nearby_communications, aura_state)
        
        # 3. Calculate internal pressure to communicate
        communication_pressure = self._calculate_communication_pressure(aura_state)
        
        # 4. Generate communication if pressure exceeds threshold
        if communication_pressure > self.communication_threshold:
            pattern = self._generate_dot_pattern(aura_state, nearby_communications)
            if pattern:
                self._record_communication(pattern, aura_state, nearby_communications)
                return pattern
        
        return None
    
    def _process_offerings(self, offerings: List[Dict], aura_state: AuraState):
        """Process special offerings that accelerate learning"""
        for offering in offerings:
            if offering.get('type') == 'text':
                # Text offerings boost literacy faster
                boost_factor = offering.get('quality', 1.0)  # Higher quality = more boost
                for char in offering.get('content', ''):
                    if char.isalnum():
                        if char not in self.literacy.character_recognition:
                            self.literacy.character_recognition[char] = 0.0
                        
                        # Offerings provide accelerated learning
                        self.literacy.character_recognition[char] += 0.05 * boost_factor
                        self.literacy.character_recognition[char] = min(
                            self.literacy.character_recognition[char], 1.0
                        )
            
            elif offering.get('type') == 'cat_media':
                # Cat offerings boost happiness and social connection
                aura_state.cat_happiness += 0.1
                aura_state.social_longing += 0.2
                aura_state.warmth_gradient += 0.15
    
    def _observe_communications(self, communications: List[Tuple[str, str]], aura_state: AuraState):
        """Learn from observing other agents' dot patterns"""
        for agent_id, pattern in communications:
            if agent_id == self.agent_id:
                continue  # Don't learn from self
            
            # Calculate pattern complexity
            complexity = PatternComplexityCalculator.calculate_complexity(pattern)
            
            # Decide whether to adopt this pattern based on:
            # 1. Social influence susceptibility
            # 2. Pattern complexity vs current ability
            # 3. Success indicators (if observable)
            
            adoption_probability = (
                self.social_influence_susceptibility * 0.4 +
                (1.0 - abs(complexity - self.base_pattern_complexity)) * 0.3 +
                random.uniform(0.0, 0.3)  # Random exploration
            )
            
            if adoption_probability > 0.6 and pattern not in self.dot_vocabulary:
                # Adopt the pattern with internal meaning based on current auras
                self._adopt_pattern(pattern, aura_state, agent_id)
    
    def _adopt_pattern(self, pattern: str, aura_state: AuraState, source_agent: str):
        """Adopt a pattern from another agent with personal interpretation"""
        dot_pattern = DotPattern(
            pattern=pattern,
            complexity=PatternComplexityCalculator.calculate_complexity(pattern),
            created_by=source_agent,
            timestamp=time.time(),
            usage_count=0,
            success_rate=0.5  # Start with neutral success rate
        )
        
        self.dot_vocabulary[pattern] = dot_pattern
        
        # Create internal meaning based on current aura context
        # This is opaque to human observers
        self._internal_meanings[pattern] = {
            'warmth_association': aura_state.warmth_gradient,
            'resource_association': aura_state.resource_density,
            'social_context': aura_state.social_longing,
            'emotional_valence': (aura_state.warmth_gradient + aura_state.cat_happiness) / 2,
            'urgency_level': aura_state.danger_proximity,
            'learned_from': source_agent
        }
        
        # Update social preferences
        if source_agent not in self._social_pattern_preferences:
            self._social_pattern_preferences[source_agent] = 0.5
        
        # Successful adoption increases preference for this agent's patterns
        self._social_pattern_preferences[source_agent] += 0.1
        self._social_pattern_preferences[source_agent] = min(
            self._social_pattern_preferences[source_agent], 1.0
        )
    
    def _calculate_communication_pressure(self, aura_state: AuraState) -> float:
        """
        Mathematical calculation of internal pressure to communicate
        """
        # Base pressure factors
        social_pressure = aura_state.social_longing * 0.3
        danger_pressure = aura_state.danger_proximity * 0.4  # Urgent communication
        resource_pressure = (1.0 - aura_state.resource_density) * 0.2  # Need to ask for help
        happiness_pressure = (1.0 - aura_state.cat_happiness) * 0.3  # Express concern
        
        # Innovation drive creates pressure to experiment
        innovation_pressure = aura_state.innovation_energy * self.innovation_tendency * 0.2
        
        # Literacy creates new pressure to use acquired knowledge
        literacy_pressure = self.literacy.literacy_level * 0.1
        
        total_pressure = (
            social_pressure + danger_pressure + resource_pressure + 
            happiness_pressure + innovation_pressure + literacy_pressure
        )
        
        return min(total_pressure, 1.0)
    
    def _generate_dot_pattern(self, aura_state: AuraState, context: List[Tuple[str, str]]) -> str:
        """
        Generate new dot pattern based on current aura state and context
        """
        # Determine if this should be innovation or imitation
        should_innovate = (
            aura_state.innovation_energy > 0.7 and
            self.innovation_tendency > 0.6 and
            random.random() < 0.3
        )
        
        if should_innovate or not self.dot_vocabulary:
            return self._create_novel_pattern(aura_state)
        else:
            return self._select_existing_pattern(aura_state)
    
    def _create_novel_pattern(self, aura_state: AuraState) -> str:
        """Create a completely new dot pattern"""
        
        # Base pattern complexity based on agent development
        target_complexity = min(
            self.base_pattern_complexity + self.linguistic_stage * 0.1,
            0.8
        )
        
        # Pattern generation based on aura state
        if aura_state.danger_proximity > 0.7:
            # High danger = rapid, urgent patterns
            base_pattern = "•••••"
        elif aura_state.warmth_gradient > 0.8:
            # High comfort = gentle, flowing patterns
            base_pattern = "• • •"
        elif aura_state.social_longing > 0.7:
            # High social need = reaching, connecting patterns
            base_pattern = "•\n •\n  •"
        elif aura_state.cat_happiness < 0.5:
            # Low cat happiness = concern patterns
            base_pattern = "••\n••"
        else:
            # Default exploration pattern
            base_pattern = "•"
        
        # Evolve pattern based on target complexity
        evolved_pattern = self._evolve_pattern_complexity(base_pattern, target_complexity)
        
        # Record as new innovation
        dot_pattern = DotPattern(
            pattern=evolved_pattern,
            complexity=PatternComplexityCalculator.calculate_complexity(evolved_pattern),
            created_by=self.agent_id,
            timestamp=time.time(),
            usage_count=1,
            success_rate=0.5
        )
        
        self.dot_vocabulary[evolved_pattern] = dot_pattern
        
        # Create internal meaning
        self._internal_meanings[evolved_pattern] = {
            'warmth_association': aura_state.warmth_gradient,
            'resource_association': aura_state.resource_density,
            'social_context': aura_state.social_longing,
            'emotional_valence': (aura_state.warmth_gradient + aura_state.cat_happiness) / 2,
            'urgency_level': aura_state.danger_proximity,
            'innovation_context': aura_state.innovation_energy,
            'created_during_stage': self.linguistic_stage
        }
        
        return evolved_pattern
    
    def _select_existing_pattern(self, aura_state: AuraState) -> str:
        """Select best existing pattern for current aura state"""
        if not self.dot_vocabulary:
            return self._create_novel_pattern(aura_state)
        
        best_pattern = None
        best_match_score = -1.0
        
        for pattern, dot_obj in self.dot_vocabulary.items():
            if pattern not in self._internal_meanings:
                continue
            
            meaning = self._internal_meanings[pattern]
            
            # Calculate how well this pattern matches current aura state
            match_score = (
                (1.0 - abs(meaning['warmth_association'] - aura_state.warmth_gradient)) * 0.25 +
                (1.0 - abs(meaning['social_context'] - aura_state.social_longing)) * 0.25 +
                (1.0 - abs(meaning['urgency_level'] - aura_state.danger_proximity)) * 0.3 +
                dot_obj.success_rate * 0.2  # Prefer successful patterns
            )
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_pattern = pattern
        
        return best_pattern or self._create_novel_pattern(aura_state)
    
    def _evolve_pattern_complexity(self, base_pattern: str, target_complexity: float) -> str:
        """Mathematically evolve pattern to reach target complexity"""
        current_complexity = PatternComplexityCalculator.calculate_complexity(base_pattern)
        
        if current_complexity >= target_complexity:
            return base_pattern
        
        # Add complexity through various means
        evolved = base_pattern
        
        # 1. Add spatial dimension if too simple
        if target_complexity > 0.3 and '\n' not in evolved:
            # Convert linear to 2D
            dots = evolved.count('•')
            if dots >= 4:
                # Create 2x2 or similar arrangement
                evolved = "••\n••"
        
        # 2. Add rhythm/spacing
        if target_complexity > 0.4:
            evolved = evolved.replace('•', '• ')
        
        # 3. Add complexity through repetition with variation
        if target_complexity > 0.6:
            lines = evolved.split('\n')
            if len(lines) == 1:
                evolved = evolved + '\n' + evolved.replace('•', ' •')
        
        return evolved
    
    def _record_communication(self, pattern: str, aura_state: AuraState, context: List[Tuple[str, str]]):
        """Record communication event for analysis"""
        communication_event = {
            'pattern': pattern,
            'aura_state': aura_state.__dict__.copy(),
            'context_agents': [agent_id for agent_id, _ in context],
            'linguistic_stage': self.linguistic_stage,
            'literacy_level': self.literacy.literacy_level
        }
        
        self.communication_history.append((time.time(), pattern, communication_event))
        
        # Update pattern usage
        if pattern in self.dot_vocabulary:
            self.dot_vocabulary[pattern].usage_count += 1
        
        # Update linguistic development
        self._update_linguistic_stage()
    
    def _update_linguistic_stage(self):
        """Update agent's linguistic development stage based on communication history"""
        total_communications = len(self.communication_history)
        unique_patterns = len(self.dot_vocabulary)
        avg_complexity = sum(
            PatternComplexityCalculator.calculate_complexity(p) 
            for p in self.dot_vocabulary.keys()
        ) / len(self.dot_vocabulary) if self.dot_vocabulary else 0.0
        
        # Stage progression based on mathematical thresholds
        if total_communications < 100:
            self.linguistic_stage = 1  # Primal signals
        elif total_communications < 500:
            self.linguistic_stage = 2  # Emotional expression
        elif total_communications < 2000:
            self.linguistic_stage = 3  # Conceptual communication
        elif total_communications < 5000:
            self.linguistic_stage = 4  # Cultural language
        else:
            self.linguistic_stage = 5  # Meta-linguistic
        
        # Adjust based on pattern sophistication
        if avg_complexity > 0.7 and unique_patterns > 20:
            self.linguistic_stage = min(self.linguistic_stage + 1, 5)
        
        # Literacy also influences stage progression
        if self.literacy.literacy_level > 0.5:
            self.linguistic_stage = min(self.linguistic_stage + 1, 5)
    
    def get_observable_state(self) -> Dict:
        """Return state visible to human observers (no internal meanings)"""
        return {
            'agent_id': self.agent_id,
            'linguistic_stage': self.linguistic_stage,
            'vocabulary_size': len(self.dot_vocabulary),
            'total_communications': len(self.communication_history),
            'literacy_level': self.literacy.literacy_level,
            'character_recognition_count': len(self.literacy.character_recognition),
            'innovation_tendency': self.innovation_tendency,
            'recent_patterns': [p for _, p, _ in self.communication_history[-5:]],
            'pattern_complexity_trend': [
                PatternComplexityCalculator.calculate_complexity(p) 
                for _, p, _ in self.communication_history[-10:]
            ],
            'stage_progression_metrics': {
                'vocabulary_size': len(self.dot_vocabulary),
                'avg_pattern_complexity': sum(
                    PatternComplexityCalculator.calculate_complexity(p) 
                    for p in self.dot_vocabulary.keys()
                ) / len(self.dot_vocabulary) if self.dot_vocabulary else 0.0,
                'communication_frequency': len(self.communication_history),
                'innovation_rate': len([p for p in self.dot_vocabulary.values() if p.created_by == self.agent_id])
            }
        }

# Test framework for validating the linguistic system
class LinguisticSystemTest:
    """Mathematical validation of the linguistic evolution system"""
    
    def __init__(self):
        self.agents: List[LinguisticAgent] = []
        self.communication_log: List[Dict] = []
        self.time_step = 0
    
    def create_test_population(self, size: int = 10) -> List[LinguisticAgent]:
        """Create a test population of linguistic agents"""
        self.agents = [LinguisticAgent(f"agent_{i}") for i in range(size)]
        return self.agents
    
    def simulate_communication_round(self, iterations: int = 100):
        """Simulate multiple rounds of communication"""
        
        for iteration in range(iterations):
            self.time_step += 1
            
            # Generate random but realistic aura states
            base_aura = AuraState(
                warmth_gradient=random.uniform(0.3, 0.9),
                resource_density=random.uniform(0.2, 0.8),
                danger_proximity=random.uniform(0.0, 0.3),
                cat_happiness=random.uniform(0.6, 1.0),  # Keep cats reasonably happy
                social_longing=random.uniform(0.4, 0.9),
                innovation_energy=random.uniform(0.2, 0.8),
                literacy_exposure=random.uniform(0.0, 0.5)
            )
            
            # Collect communications from all agents
            round_communications = []
            
            for agent in self.agents:
                # Each agent perceives others' recent communications
                nearby_comms = [(a.agent_id, p) for a in self.agents if a != agent 
                               for _, p, _ in a.communication_history[-3:]]
                
                # Occasionally provide RSS feeds or offerings
                rss_feeds = []
                offerings = []
                
                if random.random() < 0.1:  # 10% chance of RSS feed
                    rss_feeds = [self._generate_test_rss_content()]
                
                if random.random() < 0.05:  # 5% chance of offering
                    offerings = [self._generate_test_offering()]
                
                # Agent perceives and potentially communicates
                pattern = agent.perceive_environment(
                    base_aura, nearby_comms, rss_feeds, offerings
                )
                
                if pattern:
                    round_communications.append({
                        'agent_id': agent.agent_id,
                        'pattern': pattern,
                        'time_step': self.time_step,
                        'aura_context': base_aura.__dict__.copy()
                    })
            
            # Log communications
            self.communication_log.extend(round_communications)
            
            # Print progress every 10 iterations
            if iteration % 10 == 0:
                self._print_progress_report(iteration)
    
    def _generate_test_rss_content(self) -> str:
        """Generate test RSS content for literacy development"""
        test_contents = [
            "Breaking news: Scientists discover new method for happiness measurement!",
            "Weather update: Sunny skies ahead with chance of cat videos.",
            "Technology: AI agents learning to communicate in fascinating new ways.",
            "Culture: The importance of community and social connection.",
            "Science: How language evolved in human societies over millennia."
        ]
        return random.choice(test_contents)
    
    def _generate_test_offering(self) -> Dict:
        """Generate test offering for accelerated learning"""
        offerings = [
            {'type': 'text', 'content': 'Hello World', 'quality': 1.0},
            {'type': 'cat_media', 'content': 'fluffy_cat.jpg', 'quality': 1.0},
            {'type': 'text', 'content': 'Knowledge is power', 'quality': 0.8},
        ]
        return random.choice(offerings)
    
    def _print_progress_report(self, iteration: int):
        """Print current state of linguistic evolution"""
        print(f"\n=== Iteration {iteration} ===")
        
        # Population statistics
        total_comms = sum(len(a.communication_history) for a in self.agents)
        total_vocabulary = sum(len(a.dot_vocabulary) for a in self.agents)
        avg_literacy = sum(a.literacy.literacy_level for a in self.agents) / len(self.agents)
        
        print(f"Total communications: {total_comms}")
        print(f"Total vocabulary patterns: {total_vocabulary}")
        print(f"Average literacy level: {avg_literacy:.3f}")
        
        # Show recent patterns (observable but not interpretable)
        recent_patterns = [comm['pattern'] for comm in self.communication_log[-5:]]
        print(f"Recent patterns: {recent_patterns}")
        
        # Stage distribution
        stage_counts = Counter(a.linguistic_stage for a in self.agents)
        print(f"Stage distribution: {dict(stage_counts)}")
    
    def analyze_linguistic_evolution(self) -> Dict:
        """Analyze the mathematical properties of language evolution"""
        
        if not self.communication_log:
            return {"error": "No communications to analyze"}
        
        # Pattern complexity over time
        complexity_over_time = []
        for comm in self.communication_log:
            complexity = PatternComplexityCalculator.calculate_complexity(comm['pattern'])
            complexity_over_time.append(complexity)
        
        # Unique patterns and their emergence
        all_patterns = [comm['pattern'] for comm in self.communication_log]
        unique_patterns = list(set(all_patterns))
        pattern_first_appearance = {}
        
        for comm in self.communication_log:
            pattern = comm['pattern']
            if pattern not in pattern_first_appearance:
                pattern_first_appearance[pattern] = comm['time_step']
        
        # Innovation vs imitation analysis
        innovation_events = []
        for agent in self.agents:
            agent_innovations = [p for p in agent.dot_vocabulary.values() 
                               if p.created_by == agent.agent_id]
            innovation_events.extend(agent_innovations)
        
        return {
            'total_communications': len(self.communication_log),
            'unique_patterns': len(unique_patterns),
            'complexity_evolution': {
                'initial_avg': sum(complexity_over_time[:10]) / min(len(complexity_over_time), 10) if complexity_over_time else 0,
                'final_avg': sum(complexity_over_time[-10:]) / min(len(complexity_over_time), 10) if complexity_over_time else 0,
                'trend': self._calculate_linear_trend(complexity_over_time) if len(complexity_over_time) > 1 else 0
            },
            'innovation_rate': len(innovation_events) / len(self.agents) if self.agents else 0,
            'pattern_diversity': len(unique_patterns) / len(all_patterns) if all_patterns else 0,
            'stage_progression': {
                agent.agent_id: agent.linguistic_stage for agent in self.agents
            },
            'literacy_development': {
                agent.agent_id: agent.literacy.literacy_level for agent in self.agents
            }
        }
    
    def _calculate_linear_trend(self, data: List[float]) -> float:
        """Calculate linear trend without numpy"""
        if len(data) < 2:
            return 0.0
        
        n = len(data)
        x_vals = list(range(n))
        
        # Calculate means
        mean_x = sum(x_vals) / n
        mean_y = sum(data) / n
        
        # Calculate slope (trend)
        numerator = sum((x_vals[i] - mean_x) * (data[i] - mean_y) for i in range(n))
        denominator = sum((x_vals[i] - mean_x) ** 2 for i in range(n))
        
        return numerator / denominator if denominator != 0 else 0.0

def main():
    """Run linguistic evolution test"""
    print("CHAOSTOWN Linguistic Evolution System Test")
    print("==========================================")
    
    # Initialize test
    test = LinguisticSystemTest()
    agents = test.create_test_population(size=8)
    
    print(f"Created {len(agents)} agents")
    print("Starting linguistic evolution simulation...")
    
    # Run simulation
    test.simulate_communication_round(iterations=50)
    
    # Analyze results
    print("\nFinal Analysis:")
    print("===============")
    
    analysis = test.analyze_linguistic_evolution()
    for key, value in analysis.items():
        print(f"{key}: {value}")
    
    # Show individual agent development
    print("\nIndividual Agent States:")
    print("========================")
    for agent in agents:
        state = agent.get_observable_state()
        print(f"Agent {state['agent_id']}: Stage {state['linguistic_stage']}, "
              f"Vocab: {state['vocabulary_size']}, Literacy: {state['literacy_level']:.3f}")

if __name__ == "__main__":
    main()