#!/usr/bin/env python3
"""
Demo/walkthrough script for Ancestral Habitation
Shows a sample playthrough of the game
"""

import sys
sys.path.insert(0, '/home/runner/work/AncestralHabitation/AncestralHabitation')

from game_engine.game_state import GameState
from game_engine.ui import GameUI


def demo_game():
    """Run a demo of the game with automated actions"""
    print("=" * 60)
    print("ANCESTRAL HABITATION - DEMO PLAYTHROUGH")
    print("=" * 60)
    print()
    
    # Initialize game
    state = GameState()
    state.tribe_name = "The River People"
    ui = GameUI(state)
    
    print(f"Starting demo with tribe: {state.tribe_name}")
    print()
    
    # Show initial status
    print("\n--- INITIAL STATE (Year 8000 BC) ---")
    ui.display_game_status()
    
    # Simulate some years of development
    print("\n\n--- ADVANCING 5 YEARS ---")
    for i in range(5):
        state.advance_turn()
    ui.display_game_status()
    
    # Research agriculture
    print("\n\n--- RESEARCHING AGRICULTURE ---")
    if state.can_afford({'food': 100, 'wood': 50}):
        state.spend_resources({'food': 100, 'wood': 50})
        state.discover_technology('agriculture')
        print("✓ Agriculture discovered!")
    ui.display_game_status()
    
    # Build some farms
    print("\n\n--- BUILDING FARMS ---")
    for i in range(3):
        if state.can_afford({'wood': 50, 'stone': 30, 'food': 100}):
            state.spend_resources({'wood': 50, 'stone': 30, 'food': 100})
            state.farms += 1
            print(f"✓ Farm {state.farms} built!")
    ui.display_game_status()
    
    # Advance more years
    print("\n\n--- ADVANCING 10 YEARS ---")
    for i in range(10):
        state.advance_turn()
    ui.display_game_status()
    
    # Research pottery
    print("\n\n--- RESEARCHING POTTERY ---")
    if state.can_afford({'clay': 50, 'wood': 30}):
        state.spend_resources({'clay': 50, 'wood': 30})
        state.discover_technology('pottery')
        print("✓ Pottery discovered!")
    
    # Research animal husbandry
    print("\n--- RESEARCHING ANIMAL HUSBANDRY ---")
    if state.can_afford({'food': 150, 'hides': 30}):
        state.spend_resources({'food': 150, 'hides': 30})
        state.discover_technology('animal_husbandry')
        print("✓ Animal Husbandry discovered!")
    
    ui.display_game_status()
    
    # Advance to show population growth
    print("\n\n--- ADVANCING 20 YEARS ---")
    for i in range(20):
        state.advance_turn()
    ui.display_game_status()
    
    # Change governance if possible
    print("\n\n--- CHECKING GOVERNANCE OPTIONS ---")
    from game_engine.governance import get_available_governance_types, GOVERNANCE_TYPES
    available_govs = get_available_governance_types(state.population, state.has_writing)
    print(f"Available governance types: {len(available_govs)}")
    for gov in available_govs:
        print(f"  - {gov.display_name} (requires pop: {gov.population_requirement})")
    
    # Final statistics
    print("\n\n--- FINAL DEMO STATISTICS ---")
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    
    print(f"\nTribe: {state.tribe_name}")
    print(f"Year: {state.get_year_display()}")
    print(f"Turn: {state.turn}")
    print(f"Population: {state.population}")
    print(f"Culture Points: {state.culture_points}")
    
    print(f"\nTechnologies Discovered: {len(state.technologies)}")
    for tech in sorted(state.technologies):
        print(f"  - {tech.replace('_', ' ').title()}")
    
    print(f"\nFarms: {state.farms}")
    print(f"Farming Level: {state.farming_level}/5")
    
    print("\n\nDemo completed!")
    print(f"Final year: {state.get_year_display()}")
    print(f"Final population: {state.population}")
    print(f"Technologies discovered: {len(state.technologies)}")
    print(f"Farms built: {state.farms}")
    print(f"Culture points: {state.culture_points}")


if __name__ == "__main__":
    demo_game()
