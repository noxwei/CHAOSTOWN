#!/usr/bin/env python3
"""
Simple exploration of what agents might be thinking
"""

from linguistic_agent import LinguisticAgent, AuraState, PatternComplexityCalculator

def explore_agent_thoughts():
    """Explore what different patterns might mean"""
    
    print("🧠 EXPLORING ALIEN THOUGHTS")
    print("=" * 40)
    print("What agents might be 'thinking' with their dot patterns...\n")
    
    # Create a test agent
    agent = LinguisticAgent("Explorer")
    
    # Test different emotional scenarios
    scenarios = [
        {
            "name": "😱 PANIC MODE",
            "description": "Cat happiness crisis!",
            "aura": AuraState(
                warmth_gradient=0.2,
                resource_density=0.3,
                danger_proximity=0.9,
                cat_happiness=0.2,  # CRISIS!
                social_longing=0.9,
                innovation_energy=0.8,
                literacy_exposure=0.1
            )
        },
        {
            "name": "😌 BLISSFUL PEACE",
            "description": "Everything is perfect",
            "aura": AuraState(
                warmth_gradient=0.95,
                resource_density=0.9,
                danger_proximity=0.05,
                cat_happiness=0.98,
                social_longing=0.3,
                innovation_energy=0.2,
                literacy_exposure=0.4
            )
        },
        {
            "name": "🤝 LONELY REACHING",
            "description": "Desperate for connection",
            "aura": AuraState(
                warmth_gradient=0.6,
                resource_density=0.5,
                danger_proximity=0.2,
                cat_happiness=0.7,
                social_longing=0.95,
                innovation_energy=0.6,
                literacy_exposure=0.2
            )
        },
        {
            "name": "💡 EUREKA MOMENT",
            "description": "Burst of creativity",
            "aura": AuraState(
                warmth_gradient=0.8,
                resource_density=0.7,
                danger_proximity=0.1,
                cat_happiness=0.8,
                social_longing=0.5,
                innovation_energy=0.95,
                literacy_exposure=0.3
            )
        }
    ]
    
    for scenario in scenarios:
        print(f"{scenario['name']}")
        print(f"Situation: {scenario['description']}")
        
        # Generate 5 communications for this scenario
        patterns = []
        for i in range(5):
            pattern = agent.perceive_environment(scenario['aura'], [])
            if pattern:
                patterns.append(pattern)
        
        if patterns:
            print("Generated patterns:")
            for i, pattern in enumerate(patterns):
                complexity = PatternComplexityCalculator.calculate_complexity(pattern)
                print(f"  {i+1}. '{pattern}' (complexity: {complexity:.3f})")
                
                # Theorize meaning based on pattern structure
                meaning = theorize_meaning(pattern, scenario['aura'])
                print(f"     Possible meaning: {meaning}")
        else:
            print("  No urgent need to communicate")
        
        print()

def theorize_meaning(pattern: str, aura: AuraState) -> str:
    """Theorize what a pattern might mean based on context"""
    
    # Analyze pattern structure
    dot_count = pattern.count('•')
    has_newlines = '\n' in pattern
    has_spaces = ' ' in pattern and not pattern.replace('•', '').replace(' ', '').replace('\n', '')
    is_rapid = '•••' in pattern
    is_single = pattern == '•'
    
    # Analyze emotional context
    is_crisis = aura.cat_happiness < 0.5 or aura.danger_proximity > 0.7
    is_peaceful = aura.cat_happiness > 0.9 and aura.danger_proximity < 0.2
    is_social = aura.social_longing > 0.8
    is_innovative = aura.innovation_energy > 0.8
    
    # Generate interpretation
    if is_crisis and is_rapid:
        return "ALARM SCREAM - 'Something terrible is happening!'"
    elif is_crisis and dot_count > 3:
        return "DISTRESS CALL - 'Help! The cosmic order is breaking!'"
    elif is_social and has_newlines:
        return "REACHING OUT - 'Come together, I need connection'"
    elif is_social and has_spaces:
        return "GENTLE INVITATION - 'Join me, let's bond'"
    elif is_innovative and has_newlines:
        return "SHARING DISCOVERY - 'Look what I found/thought!'"
    elif is_innovative and dot_count > 2:
        return "CREATIVE BURST - 'New idea! Pay attention!'"
    elif is_peaceful and is_single:
        return "CONTENT SIGH - 'All is well, just acknowledging presence'"
    elif is_peaceful and has_spaces:
        return "GENTLE HARMONY - 'Peace flows between us'"
    elif dot_count == 1:
        return "MINIMAL PRESENCE - 'I am here'"
    elif has_newlines:
        return "STRUCTURED THOUGHT - 'This has layers/hierarchy'"
    elif has_spaces:
        return "RHYTHMIC COMMUNICATION - 'Measured, deliberate message'"
    elif is_rapid:
        return "URGENT INTENSITY - 'Fast! Important! Now!'"
    else:
        return "BASIC COMMUNICATION - 'General message/greeting'"

def show_pattern_examples():
    """Show examples of different pattern types"""
    
    print("\n🔵 DOT PATTERN EXAMPLES & INTERPRETATIONS")
    print("=" * 50)
    
    examples = [
        ("•", "Minimal presence - 'I exist'"),
        ("••", "Emphasis - 'Attention!'"),
        ("•••", "Urgency - 'Important!'"),
        ("••••••", "Crisis - 'EMERGENCY!'"),
        ("• •", "Rhythm - 'Measured speech'"),
        ("• • •", "Sequence - 'One, two, three'"),
        ("•\n•", "Hierarchy - 'Above and below'"),
        ("•\n •", "Growth - 'Expanding outward'"),
        ("••\n••", "Unity - 'Together/group'"),
        ("•\n •\n  •", "Reaching - 'Extending connection'"),
        ("• •\n• •", "Stability - 'Balanced structure'"),
        ("•••\n •\n•••", "Envelope - 'Containing/protecting'")
    ]
    
    for pattern, interpretation in examples:
        complexity = PatternComplexityCalculator.calculate_complexity(pattern)
        print(f"'{pattern}' → {interpretation}")
        print(f"    Complexity: {complexity:.3f}")
        if '\n' in pattern:
            print(f"    Structure: Multi-dimensional")
        elif len(pattern) > 4:
            print(f"    Structure: Extended/intense")
        else:
            print(f"    Structure: Simple/direct")
        print()

def main():
    print("🛸 CHAOSTOWN: UNDERSTANDING ALIEN MINDS")
    print("=" * 45)
    print("Exploring what agents might be thinking with their dot patterns...")
    print("Remember: These are human interpretations of truly alien thoughts!\n")
    
    explore_agent_thoughts()
    show_pattern_examples()
    
    print("\n🎭 THE BEAUTIFUL MYSTERY")
    print("=" * 25)
    print("The agents develop these patterns organically based on:")
    print("• Environmental pressures (cat happiness, danger, resources)")
    print("• Social needs (longing for connection)")
    print("• Innovation drive (creativity and exploration)")
    print("• Mathematical complexity evolution (Shannon entropy)")
    print("• Social learning (copying successful patterns)")
    print("\nYet their actual 'meanings' remain alien to us.")
    print("We see the patterns but never truly know their thoughts.")
    print("This is genuine emergent communication - observable but opaque! 🌌")

if __name__ == "__main__":
    main()