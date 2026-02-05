#!/usr/bin/env python3
"""
Complete playthrough example
Shows a full game session with various actions
"""

import sys
import os
# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_engine.game_state import GameState
from game_engine.ui import GameUI


def automated_playthrough():
    """Run an automated playthrough showing game features"""
    
    # Create a game file that simulates user inputs
    print("=" * 70)
    print("ANCESTRAL HABITATION - AUTOMATED PLAYTHROUGH")
    print("=" * 70)
    print()
    
    state = GameState()
    state.tribe_name = "The Dawn Tribe"
    
    print("Starting Game...")
    print(f"Tribe: {state.tribe_name}")
    print(f"Year: {state.get_year_display()}")
    print(f"Population: {state.population}")
    print()
    
    # Year 1-5: Gather resources
    print("PHASE 1: Early Gathering (Years 1-5)")
    print("-" * 70)
    for i in range(5):
        state.advance_turn()
    print(f"✓ Year {state.get_year_display()}: Pop={state.population}, Food={state.resources['food']}")
    
    # Discover agriculture
    print("\nPHASE 2: Agricultural Revolution")
    print("-" * 70)
    if state.can_afford({'food': 100, 'wood': 50}):
        state.spend_resources({'food': 100, 'wood': 50})
        state.discover_technology('agriculture')
        print("✓ Discovered Agriculture!")
    
    # Build farms
    print("\nPHASE 3: Farm Construction")
    print("-" * 70)
    farms_built = 0
    for i in range(5):
        if state.can_afford({'wood': 50, 'stone': 30, 'food': 100}):
            state.spend_resources({'wood': 50, 'stone': 30, 'food': 100})
            state.farms += 1
            farms_built += 1
            if state.farms % 5 == 0:
                state.farming_level += 1
    print(f"✓ Built {farms_built} farms (Farming Level: {state.farming_level})")
    
    # Advance 20 years
    print("\nPHASE 4: Population Growth (Years 6-25)")
    print("-" * 70)
    for i in range(20):
        state.advance_turn()
    print(f"✓ Year {state.get_year_display()}: Pop={state.population}, Food={state.resources['food']}")
    
    # Research more technologies
    print("\nPHASE 5: Technological Development")
    print("-" * 70)
    techs = ['pottery', 'weaving', 'animal_husbandry']
    for tech_name in techs:
        from game_engine.technologies import TECHNOLOGIES
        if tech_name in TECHNOLOGIES:
            tech = TECHNOLOGIES[tech_name]
            if state.can_afford(tech.cost):
                state.spend_resources(tech.cost)
                state.discover_technology(tech_name)
                print(f"✓ Discovered {tech_name.replace('_', ' ').title()}")
    
    # Advance to show long-term development
    print("\nPHASE 6: Long-term Development (50 years)")
    print("-" * 70)
    for i in range(50):
        state.advance_turn()
    print(f"✓ Year {state.get_year_display()}: Pop={state.population}")
    
    # Check governance options
    print("\nPHASE 7: Governance Evolution")
    print("-" * 70)
    from game_engine.governance import get_available_governance_types
    available = get_available_governance_types(state.population, state.has_writing)
    print(f"Available governance types: {len(available)}")
    for gov in available:
        print(f"  • {gov.display_name}")
    
    # Final status
    print("\n" + "=" * 70)
    print("FINAL CIVILIZATION STATUS")
    print("=" * 70)
    print(f"Tribe: {state.tribe_name}")
    print(f"Year: {state.get_year_display()} (Turn {state.turn})")
    print(f"Population: {state.population}")
    print(f"Location: River Valley")
    print(f"Governance: {state.governance_type.replace('_', ' ').title()}")
    print(f"Stability: {state.governance_stability}%")
    print(f"\nTechnologies: {len(state.technologies)}")
    for tech in sorted(state.technologies):
        print(f"  ✓ {tech.replace('_', ' ').title()}")
    print(f"\nFarms: {state.farms} (Level {state.farming_level})")
    print(f"Culture Points: {state.culture_points}")
    print(f"\nResources:")
    for res, amount in sorted(state.resources.items()):
        print(f"  {res.capitalize()}: {amount}")
    
    print("\n" + "=" * 70)
    print("Playthrough Complete!")
    print("The game successfully simulates:")
    print("  ✓ Neolithic era (8000 BC - 1200 BC)")
    print("  ✓ Tribe building and population management")
    print("  ✓ Agricultural development")
    print("  ✓ Technology progression")
    print("  ✓ Resource management")
    print("  ✓ Governance structures")
    print("  ✓ Cultural development")
    print("=" * 70)


if __name__ == "__main__":
    automated_playthrough()
