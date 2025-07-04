#!/usr/bin/env python3
"""
CHAOSTOWN Language Explorer
Deep dive into what agents might be "thinking" with their dot patterns
"""

import random
import time
from linguistic_agent import LinguisticAgent, AuraState, PatternComplexityCalculator
from typing import Dict, List, Tuple

class LanguageExplorer:
    """Explore and interpret the alien dot language system"""
    
    def __init__(self):
        self.agents = []
        self.communication_archive = []
        self.pattern_interpretations = {}
    
    def create_focused_scenario(self, scenario_name: str) -> List[LinguisticAgent]:
        """Create agents in specific emotional/environmental scenarios"""
        
        scenarios = {
            "cat_crisis": {
                "description": "Cat happiness has dropped critically low",
                "aura_base": AuraState(
                    warmth_gradient=0.2,
                    resource_density=0.3,
                    danger_proximity=0.8,
                    cat_happiness=0.3,  # CRISIS!
                    social_longing=0.9,
                    innovation_energy=0.7,
                    literacy_exposure=0.1
                )
            },
            "golden_age": {
                "description": "Perfect harmony - cats are blissful, resources abundant",
                "aura_base": AuraState(
                    warmth_gradient=0.95,
                    resource_density=0.9,
                    danger_proximity=0.1,
                    cat_happiness=0.95,
                    social_longing=0.6,
                    innovation_energy=0.4,
                    literacy_exposure=0.2
                )
            },
            "exploration": {
                "description": "Agents discovering new territories, high curiosity",
                "aura_base": AuraState(
                    warmth_gradient=0.6,
                    resource_density=0.4,
                    danger_proximity=0.3,
                    cat_happiness=0.7,
                    social_longing=0.8,
                    innovation_energy=0.9,
                    literacy_exposure=0.3
                )
            },
            "social_bonding": {
                "description": "Community gathering, high social needs",
                "aura_base": AuraState(
                    warmth_gradient=0.8,
                    resource_density=0.6,
                    danger_proximity=0.2,
                    cat_happiness=0.8,
                    social_longing=0.95,
                    innovation_energy=0.5,
                    literacy_exposure=0.15
                )
            }
        }
        
        if scenario_name not in scenarios:
            print(f"Unknown scenario. Available: {list(scenarios.keys())}")
            return []
        
        scenario = scenarios[scenario_name]
        print(f"\n🎭 SCENARIO: {scenario_name}")
        print(f"📝 {scenario['description']}")
        print(f"🌡️  Warmth: {scenario['aura_base'].warmth_gradient:.2f}")
        print(f"🏛️  Resources: {scenario['aura_base'].resource_density:.2f}")
        print(f"⚠️  Danger: {scenario['aura_base'].danger_proximity:.2f}")
        print(f"😺 Cat Happiness: {scenario['aura_base'].cat_happiness:.2f}")
        print(f"🤝 Social Longing: {scenario['aura_base'].social_longing:.2f}")
        print(f"💡 Innovation: {scenario['aura_base'].innovation_energy:.2f}")
        print(f"📚 Literacy: {scenario['aura_base'].literacy_exposure:.2f}")
        
        # Create 6 agents with different personalities
        agent_personalities = [
            ("Fluffhead", 0.9, 0.3),    # High innovation, low social influence
            ("Wilson", 0.3, 0.8),       # Low innovation, high social influence  
            ("Whiskers", 0.7, 0.6),     # Balanced
            ("Shadow", 0.5, 0.4),       # Conservative
            ("Mittens", 0.8, 0.7),      # Social innovator
            ("Luna", 0.2, 0.9)          # Pure follower
        ]
        
        agents = []
        for name, innovation, social_susceptibility in agent_personalities:
            agent = LinguisticAgent(name)
            agent.innovation_tendency = innovation
            agent.social_influence_susceptibility = social_susceptibility
            agents.append(agent)
        
        return agents, scenario["aura_base"]
    
    def run_communication_round(self, agents: List[LinguisticAgent], base_aura: AuraState, 
                               rounds: int = 15) -> List[Dict]:
        """Run focused communication rounds and capture what happens"""
        
        communications = []
        
        print(f"\n🗣️  RUNNING {rounds} COMMUNICATION ROUNDS...")
        print("=" * 50)
        
        for round_num in range(rounds):
            # Add some variation to auras each round
            current_aura = AuraState(
                warmth_gradient=max(0, min(1, base_aura.warmth_gradient + random.uniform(-0.1, 0.1))),
                resource_density=max(0, min(1, base_aura.resource_density + random.uniform(-0.1, 0.1))),
                danger_proximity=max(0, min(1, base_aura.danger_proximity + random.uniform(-0.05, 0.05))),
                cat_happiness=max(0, min(1, base_aura.cat_happiness + random.uniform(-0.05, 0.05))),
                social_longing=max(0, min(1, base_aura.social_longing + random.uniform(-0.1, 0.1))),
                innovation_energy=max(0, min(1, base_aura.innovation_energy + random.uniform(-0.1, 0.1))),
                literacy_exposure=max(0, min(1, base_aura.literacy_exposure + random.uniform(0, 0.02)))
            )
            
            round_communications = []
            
            # Each agent gets a chance to communicate
            for agent in agents:
                # Get recent communications from other agents
                recent_comms = [(other.agent_id, comm['pattern']) 
                               for other in agents if other != agent
                               for comm in communications[-5:] 
                               if comm['agent_id'] == other.agent_id]
                
                # Occasionally provide RSS feeds
                rss_feeds = []
                if random.random() < 0.2:  # 20% chance
                    rss_feeds = [self._generate_contextual_rss(current_aura)]
                
                # Agent perceives and potentially communicates
                pattern = agent.perceive_environment(current_aura, recent_comms, rss_feeds)
                
                if pattern:
                    comm_event = {
                        'round': round_num,
                        'agent_id': agent.agent_id,
                        'pattern': pattern,
                        'complexity': PatternComplexityCalculator.calculate_complexity(pattern),
                        'aura_context': current_aura.__dict__.copy(),
                        'internal_pressure': self._estimate_internal_pressure(agent, current_aura),
                        'innovation_flag': pattern not in [c['pattern'] for c in communications],
                        'social_context': len(recent_comms)
                    }
                    
                    round_communications.append(comm_event)
                    communications.append(comm_event)
            
            # Print round summary
            if round_communications:
                print(f"\nRound {round_num + 1}:")
                for comm in round_communications:
                    innovation_marker = "🆕" if comm['innovation_flag'] else "🔄"
                    complexity_level = "●" * min(int(comm['complexity'] * 5), 5)
                    print(f"  {innovation_marker} {comm['agent_id']}: '{comm['pattern']}' [{complexity_level}]")
        
        return communications
    
    def _generate_contextual_rss(self, aura: AuraState) -> str:
        """Generate RSS content that matches the current emotional context"""
        
        if aura.cat_happiness < 0.5:
            return random.choice([
                "Emergency veterinary care: Signs of feline distress",
                "Breaking: Local cat shelter needs urgent donations",
                "Weather alert: Cold front approaching, protect outdoor cats"
            ])
        elif aura.danger_proximity > 0.7:
            return random.choice([
                "Safety protocol: Emergency response procedures",
                "Alert: Unusual activity detected in sector 7",
                "Security update: New threat assessment protocols"
            ])
        elif aura.social_longing > 0.8:
            return random.choice([
                "Community event: Neighborhood gathering this weekend",
                "Social study: The importance of connection and belonging",
                "Local news: Community center hosting friendship activities"
            ])
        elif aura.innovation_energy > 0.8:
            return random.choice([
                "Science breakthrough: New discovery in communication theory",
                "Technology: Innovation leads to unexpected solutions",
                "Research: Creative thinking drives social progress"
            ])
        else:
            return random.choice([
                "Daily update: All systems operating normally",
                "Weather: Pleasant conditions expected to continue",
                "Community: Local harmony index remains stable"
            ])
    
    def _estimate_internal_pressure(self, agent: LinguisticAgent, aura: AuraState) -> float:
        """Estimate the internal communication pressure"""
        social_pressure = aura.social_longing * 0.3
        danger_pressure = aura.danger_proximity * 0.4
        resource_pressure = (1.0 - aura.resource_density) * 0.2
        happiness_pressure = (1.0 - aura.cat_happiness) * 0.3
        innovation_pressure = aura.innovation_energy * agent.innovation_tendency * 0.2
        
        return min(social_pressure + danger_pressure + resource_pressure + happiness_pressure + innovation_pressure, 1.0)
    
    def analyze_communication_patterns(self, communications: List[Dict]) -> Dict:
        """Analyze what the communications might mean"""
        
        if not communications:
            return {"error": "No communications to analyze"}
        
        print(f"\n🔍 DEEP ANALYSIS OF {len(communications)} COMMUNICATIONS")
        print("=" * 60)
        
        # Pattern analysis
        all_patterns = [c['pattern'] for c in communications]
        unique_patterns = list(set(all_patterns))
        pattern_usage = {pattern: all_patterns.count(pattern) for pattern in unique_patterns}
        
        print(f"\n📊 Pattern Statistics:")
        print(f"   Total communications: {len(communications)}")
        print(f"   Unique patterns: {len(unique_patterns)}")
        print(f"   Pattern reuse rate: {(len(communications) - len(unique_patterns)) / len(communications) * 100:.1f}%")
        
        # Most common patterns
        print(f"\n🔥 Most Popular Patterns:")
        for pattern, count in sorted(pattern_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
            complexity = PatternComplexityCalculator.calculate_complexity(pattern)
            print(f"   '{pattern}' → used {count} times (complexity: {complexity:.3f})")
        
        # Innovation analysis
        innovations = [c for c in communications if c['innovation_flag']]
        print(f"\n💡 Innovation Analysis:")
        print(f"   New patterns created: {len(innovations)}")
        print(f"   Innovation rate: {len(innovations) / len(communications) * 100:.1f}%")
        
        if innovations:
            print(f"   Top innovators:")
            innovator_counts = {}
            for innov in innovations:
                innovator_counts[innov['agent_id']] = innovator_counts.get(innov['agent_id'], 0) + 1
            for agent, count in sorted(innovator_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"     {agent}: {count} new patterns")
        
        # Context analysis
        print(f"\n🌡️  Contextual Triggers:")
        high_pressure_comms = [c for c in communications if c['internal_pressure'] > 0.7]
        print(f"   High-pressure communications: {len(high_pressure_comms)} ({len(high_pressure_comms)/len(communications)*100:.1f}%)")
        
        # Complexity evolution
        complexities = [c['complexity'] for c in communications]
        if len(complexities) > 5:
            early_avg = sum(complexities[:5]) / 5
            late_avg = sum(complexities[-5:]) / 5
            trend = "increasing" if late_avg > early_avg else "decreasing"
            print(f"   Complexity trend: {trend} ({early_avg:.3f} → {late_avg:.3f})")
        
        return {
            'total_communications': len(communications),
            'unique_patterns': len(unique_patterns),
            'pattern_usage': pattern_usage,
            'innovations': len(innovations),
            'complexity_trend': complexities
        }
    
    def theorize_semantic_meanings(self, communications: List[Dict]) -> Dict:
        """Theorize about what the patterns might mean to the agents"""
        
        print(f"\n🧠 SEMANTIC THEORY: What They Might Be Thinking")
        print("=" * 60)
        print("⚠️  IMPORTANT: These are human interpretations of alien thoughts!")
        print("    The actual meanings remain opaque and emergent.\n")
        
        theories = {}
        
        # Analyze patterns by context
        pattern_contexts = {}
        for comm in communications:
            pattern = comm['pattern']
            if pattern not in pattern_contexts:
                pattern_contexts[pattern] = {
                    'high_danger': 0,
                    'low_cat_happiness': 0,
                    'high_social_longing': 0,
                    'high_innovation': 0,
                    'high_pressure': 0,
                    'total_uses': 0
                }
            
            ctx = pattern_contexts[pattern]
            ctx['total_uses'] += 1
            
            aura = comm['aura_context']
            if aura['danger_proximity'] > 0.6:
                ctx['high_danger'] += 1
            if aura['cat_happiness'] < 0.6:
                ctx['low_cat_happiness'] += 1
            if aura['social_longing'] > 0.7:
                ctx['high_social_longing'] += 1
            if aura['innovation_energy'] > 0.7:
                ctx['high_innovation'] += 1
            if comm['internal_pressure'] > 0.7:
                ctx['high_pressure'] += 1
        
        # Generate theories for each pattern
        for pattern, ctx in pattern_contexts.items():
            complexity = PatternComplexityCalculator.calculate_complexity(pattern)
            theory = {"pattern": pattern, "complexity": complexity, "uses": ctx['total_uses']}
            
            # Determine primary emotional association
            max_context = max(ctx.items(), key=lambda x: x[1] if x[0] != 'total_uses' else 0)
            context_type, context_count = max_context
            context_percentage = context_count / ctx['total_uses'] * 100
            
            if context_percentage > 50:  # Strong association
                if context_type == 'high_danger':
                    theory['possible_meaning'] = "DANGER/ALARM signal"
                    theory['human_interpretation'] = "Like shouting 'HELP!' or 'WATCH OUT!'"
                elif context_type == 'low_cat_happiness':
                    theory['possible_meaning'] = "DISTRESS about cosmic order"
                    theory['human_interpretation'] = "Like saying 'Something is very wrong with the universe'"
                elif context_type == 'high_social_longing':
                    theory['possible_meaning'] = "SOCIAL REACH/connection desire"
                    theory['human_interpretation'] = "Like saying 'I need companionship' or 'Come together'"
                elif context_type == 'high_innovation':
                    theory['possible_meaning'] = "DISCOVERY/new idea sharing"
                    theory['human_interpretation'] = "Like saying 'I found something!' or 'Look at this!'"
                elif context_type == 'high_pressure':
                    theory['possible_meaning'] = "URGENCY/intense need"
                    theory['human_interpretation'] = "Like saying 'This is important!' or 'Act now!'"
                
                theory['confidence'] = context_percentage
            else:
                theory['possible_meaning'] = "GENERAL COMMUNICATION"
                theory['human_interpretation'] = "Like a general greeting or neutral statement"
                theory['confidence'] = context_percentage
            
            # Add pattern structure analysis
            if '\n' in pattern:
                theory['structure_note'] = "Multi-dimensional (spatial/hierarchical)"
            elif len(pattern) == 1:
                theory['structure_note'] = "Minimal/urgent"
            elif '•••' in pattern:
                theory['structure_note'] = "Rapid/intense"
            elif '• •' in pattern:
                theory['structure_note'] = "Rhythmic/measured"
            
            theories[pattern] = theory
        
        # Print theories
        for pattern, theory in sorted(theories.items(), key=lambda x: x[1]['uses'], reverse=True):
            print(f"Pattern: '{pattern}'")
            print(f"  Uses: {theory['uses']} times")
            print(f"  Complexity: {theory['complexity']:.3f}")
            print(f"  Structure: {theory['structure_note']}")
            print(f"  Possible meaning: {theory['possible_meaning']}")
            print(f"  Human analogy: {theory['human_interpretation']}")
            print(f"  Confidence: {theory['confidence']:.1f}%")
            print()
        
        return theories

def main():
    """Explore the alien language system"""
    
    explorer = LanguageExplorer()
    
    print("🛸 CHAOSTOWN ALIEN LANGUAGE EXPLORER")
    print("===================================")
    print("Diving deep into what agents might be thinking...")
    
    # Test different scenarios
    scenarios = ["cat_crisis", "golden_age", "exploration", "social_bonding"]
    
    for scenario in scenarios:
        print(f"\n" + "="*80)
        print(f"🎬 EXPLORING SCENARIO: {scenario.upper()}")
        print("="*80)
        
        agents, base_aura = explorer.create_focused_scenario(scenario)
        
        if agents:
            communications = explorer.run_communication_round(agents, base_aura, 10)
            
            if communications:
                analysis = explorer.analyze_communication_patterns(communications)
                theories = explorer.theorize_semantic_meanings(communications)
                
                print(f"\n🎯 SCENARIO SUMMARY: {scenario}")
                print(f"   Generated {len(communications)} communications")
                print(f"   {analysis['unique_patterns']} unique patterns emerged")
                print(f"   {analysis['innovations']} innovations created")
            else:
                print("   No communications generated in this scenario")
        
        print("\n" + "⏸️ " * 20)
        input("Press Enter to continue to next scenario...")

if __name__ == "__main__":
    main()