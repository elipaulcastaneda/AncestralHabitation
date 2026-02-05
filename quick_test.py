#!/usr/bin/env python3
"""
Quick automated test of game playthrough
"""

import sys
sys.path.insert(0, '/home/runner/work/AncestralHabitation/AncestralHabitation')

from game_engine.game_state import GameState


def quick_test():
    """Quick test of 100 years of gameplay"""
    state = GameState()
    state.tribe_name = "Test Tribe"
    
    print(f"Starting: {state.get_year_display()}, Pop: {state.population}, Food: {state.resources['food']}")
    
    # Play 100 years
    for i in range(100):
        state.advance_turn()
        if i % 10 == 0:
            print(f"Year {state.get_year_display()}: Pop={state.population}, Food={state.resources['food']}, Wood={state.resources['wood']}")
    
    print(f"\nFinal: {state.get_year_display()}, Pop: {state.population}")
    print(f"Technologies: {len(state.technologies)}")
    
    # Test with farms
    print("\n--- Testing with farms ---")
    state2 = GameState()
    state2.discover_technology('agriculture')
    state2.farms = 10
    state2.farming_level = 3
    
    print(f"Starting: Pop: {state2.population}, Farms: {state2.farms}")
    
    for i in range(100):
        state2.advance_turn()
        if i % 10 == 0:
            print(f"Year {state2.get_year_display()}: Pop={state2.population}, Food={state2.resources['food']}")
    
    print(f"\nFinal: Pop: {state2.population}, Food: {state2.resources['food']}")


if __name__ == "__main__":
    quick_test()
