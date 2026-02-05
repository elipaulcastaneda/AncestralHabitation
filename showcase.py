#!/usr/bin/env python3
"""
Interactive walkthrough for Ancestral Habitation
Shows a playthrough with better resource management
"""

import sys
import os
# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_engine.game_state import GameState
from game_engine.technologies import TECHNOLOGIES


def showcase_game():
    """Run a showcase of the game demonstrating all features"""
    print("=" * 70)
    print("ANCESTRAL HABITATION - FEATURE SHOWCASE")
    print("A Neolithic Era Strategy Game (8000 BC - 1200 BC)")
    print("=" * 70)
    print()
    
    state = GameState()
    state.tribe_name = "The Valley Dwellers"
    
    print("🏛️  STARTING SCENARIO")
    print("-" * 70)
    print(f"Tribe Name: {state.tribe_name}")
    print(f"Year: {state.get_year_display()}")
    print(f"Starting Population: {state.population}")
    print(f"Location: River Valley")
    print(f"Starting Technologies: {', '.join(sorted(state.technologies))}")
    print(f"Starting Resources: Food={state.resources['food']}, Wood={state.resources['wood']}, Stone={state.resources['stone']}")
    
    # Progress through early game
    print("\n\n📅 EARLY NEOLITHIC PERIOD (8000-6000 BC)")
    print("-" * 70)
    
    # Advance a few years to build up resources
    print("⏳ Advancing 10 years to gather resources...")
    for _ in range(10):
        state.advance_turn()
    
    print(f"Year: {state.get_year_display()}")
    print(f"Population: {state.population}")
    print(f"Resources: Food={state.resources['food']}, Wood={state.resources['wood']}")
    
    # Research Agriculture
    print("\n🔬 Discovering AGRICULTURE...")
    if state.can_afford({'food': 100, 'wood': 50}):
        state.spend_resources({'food': 100, 'wood': 50})
        state.discover_technology('agriculture')
        print("✅ Agriculture discovered!")
        print("   → Can now build farms to produce food")
        print("   → Culture points gained:", state.culture_points)
    
    # Build farms
    print("\n🌾 Building farms...")
    farms_built = 0
    for i in range(5):
        if state.can_afford({'wood': 50, 'stone': 30, 'food': 100}):
            state.spend_resources({'wood': 50, 'stone': 30, 'food': 100})
            state.farms += 1
            farms_built += 1
            if state.farms % 5 == 0:
                state.farming_level += 1
    
    print(f"✅ Built {farms_built} farms!")
    print(f"   → Total farms: {state.farms}")
    print(f"   → Farming level: {state.farming_level}")
    
    # Continue advancing
    print("\n⏳ Advancing 20 years with farming economy...")
    for _ in range(20):
        state.advance_turn()
    
    print(f"Year: {state.get_year_display()}")
    print(f"Population: {state.population} (growing with stable food supply)")
    print(f"Food stores: {state.resources['food']}")
    
    # Research more technologies
    print("\n🔬 Researching additional technologies...")
    
    techs_to_research = ['pottery', 'weaving', 'animal_husbandry']
    for tech_name in techs_to_research:
        tech = TECHNOLOGIES[tech_name]
        if state.can_afford(tech.cost):
            state.spend_resources(tech.cost)
            state.discover_technology(tech_name)
            print(f"✅ {tech_name.title()} discovered!")
            print(f"   → {tech.description}")
    
    # Middle Neolithic
    print("\n\n📅 MIDDLE NEOLITHIC PERIOD (6000-4000 BC)")
    print("-" * 70)
    
    # Advance to middle period
    years_to_advance = abs(-6000 - state.year)
    print(f"⏳ Advancing {years_to_advance} years...")
    for _ in range(years_to_advance):
        state.advance_turn()
    
    print(f"Year: {state.get_year_display()}")
    print(f"Population: {state.population}")
    
    # Research advanced techs
    if 'agriculture' in state.technologies and state.can_afford({'food': 200, 'wood': 100}):
        state.spend_resources({'food': 200, 'wood': 100})
        state.discover_technology('advanced_agriculture')
        print("✅ Advanced Agriculture discovered!")
    
    if 'agriculture' in state.technologies and state.can_afford({'wood': 150, 'stone': 100}):
        state.spend_resources({'wood': 150, 'stone': 100})
        state.discover_technology('irrigation')
        print("✅ Irrigation discovered!")
        print("   → Water management improves farming yields")
    
    # Check governance
    print("\n🏛️  GOVERNANCE DEVELOPMENT")
    print("-" * 70)
    from game_engine.governance import get_available_governance_types, GOVERNANCE_TYPES
    
    available = get_available_governance_types(state.population, state.has_writing)
    print(f"Population: {state.population}")
    print(f"Available governance types: {len(available)}")
    for gov in available:
        marker = "→" if gov.name == state.governance_type else " "
        print(f"  {marker} {gov.display_name} (pop req: {gov.population_requirement})")
    
    # Upgrade governance if possible
    if state.population >= 100:
        state.governance_type = 'chief'
        print("\n✅ Governance evolved to Chieftain!")
        print("   → Stronger leadership improves stability")
    
    # Late Neolithic
    print("\n\n📅 LATE NEOLITHIC PERIOD (4000-3000 BC)")
    print("-" * 70)
    
    years_to_advance = abs(-4000 - state.year)
    print(f"⏳ Advancing {years_to_advance} years...")
    for _ in range(years_to_advance):
        state.advance_turn()
    
    print(f"Year: {state.get_year_display()}")
    print(f"Population: {state.population}")
    
    # Try for advanced techs
    if state.can_afford({'clay': 100}):
        state.spend_resources({'clay': 100})
        state.discover_technology('proto_writing')
        print("✅ Proto-Writing discovered!")
        print("   → Early symbolic communication systems")
    
    # Chalcolithic / Copper Age
    print("\n\n📅 CHALCOLITHIC / COPPER AGE (3000-2000 BC)")
    print("-" * 70)
    
    years_to_advance = abs(-3000 - state.year)
    print(f"⏳ Advancing {years_to_advance} years...")
    for _ in range(years_to_advance):
        state.advance_turn()
    
    print(f"Year: {state.get_year_display()}")
    print(f"Population: {state.population}")
    
    # Try for writing
    if 'proto_writing' in state.technologies and state.can_afford({'clay': 200}):
        state.spend_resources({'clay': 200})
        state.discover_technology('writing')
        state.has_writing = True
        print("✅ WRITING discovered!")
        print("   → True writing systems developed")
        print("   → Advanced governance now available")
    
    # Geography showcase
    print("\n\n🗺️  GEOGRAPHY & MIGRATION")
    print("-" * 70)
    from game_engine.geography import GEOGRAPHIES
    
    print(f"Current location: {GEOGRAPHIES[state.geography_type].name}")
    print("\nAvailable geographical locations:")
    for key, geo in list(GEOGRAPHIES.items())[:3]:
        print(f"  • {geo.name} - {geo.climate} climate")
        print(f"    {geo.description}")
    
    # Final summary
    print("\n\n🏆 FINAL CIVILIZATION STATUS")
    print("=" * 70)
    print(f"Tribe: {state.tribe_name}")
    print(f"Final Year: {state.get_year_display()}")
    print(f"Final Population: {state.population}")
    print(f"Location: {GEOGRAPHIES[state.geography_type].name}")
    print(f"Governance: {GOVERNANCE_TYPES[state.governance_type].display_name}")
    print(f"Stability: {state.governance_stability}%")
    
    print(f"\n📚 Technologies Discovered ({len(state.technologies)}):")
    tech_list = sorted([t.replace('_', ' ').title() for t in state.technologies])
    for i in range(0, len(tech_list), 3):
        print("  ", ", ".join(tech_list[i:i+3]))
    
    print(f"\n🌾 Economic Development:")
    print(f"  Farms: {state.farms}")
    print(f"  Farming Level: {state.farming_level}/5")
    print(f"  Food Production: {state.farms * 50 * (1 + state.farming_level * 0.2):.0f} per year")
    
    print(f"\n💎 Culture & Development:")
    print(f"  Culture Points: {state.culture_points}")
    print(f"  Writing System: {'✅ Developed' if state.has_writing else '❌ Not yet'}")
    
    print(f"\n📦 Current Resources:")
    for resource, amount in sorted(state.resources.items()):
        print(f"  {resource.capitalize()}: {amount}")
    
    print("\n" + "=" * 70)
    print("Showcase complete! The game includes:")
    print("  ✓ Time progression from 8000 BC to Iron Age")
    print("  ✓ Population growth and management")
    print("  ✓ Resource gathering and production")
    print("  ✓ Technology research tree")
    print("  ✓ Farm building and agriculture")
    print("  ✓ Multiple geographical locations")
    print("  ✓ Governance evolution")
    print("  ✓ Writing system development")
    print("  ✓ Seasonal effects")
    print("  ✓ Random events")
    print("\nPlay the full game with: python3 game.py")
    print("=" * 70)


if __name__ == "__main__":
    showcase_game()
