#!/usr/bin/env python3
"""
Test script for Ancestral Habitation
Tests basic game functionality
"""

import sys
sys.path.insert(0, '/home/runner/work/AncestralHabitation/AncestralHabitation')

from game_engine.game_state import GameState
from game_engine.technologies import get_available_technologies, TECHNOLOGIES
from game_engine.geography import GEOGRAPHIES, get_current_season, calculate_migration_success
from game_engine.governance import get_available_governance_types, GOVERNANCE_TYPES


def test_game_state():
    """Test basic game state functionality"""
    print("Testing GameState...")
    state = GameState()
    
    assert state.year == -8000, "Starting year should be 8000 BC"
    assert state.population > 0, "Should have initial population"
    assert state.is_running == True, "Game should be running"
    assert 'fire' in state.technologies, "Should start with fire"
    
    # Test turn advancement
    initial_year = state.year
    initial_pop = state.population
    state.advance_turn()
    assert state.year == initial_year + 1, "Year should advance"
    assert state.turn == 1, "Turn should increment"
    
    print("✓ GameState tests passed")


def test_technologies():
    """Test technology system"""
    print("\nTesting Technologies...")
    
    initial_techs = {'fire', 'stone_tools', 'hunting', 'gathering'}
    available = get_available_technologies(initial_techs)
    
    assert len(available) > 0, "Should have technologies available"
    
    # Check agriculture is available
    agriculture_available = any(tech.name == 'agriculture' for tech in available)
    assert agriculture_available, "Agriculture should be available with starting techs"
    
    # Check that writing requires prerequisites
    writing_available = any(tech.name == 'writing' for tech in available)
    assert not writing_available, "Writing should not be available yet"
    
    print("✓ Technology tests passed")


def test_geography():
    """Test geography system"""
    print("\nTesting Geography...")
    
    assert 'river_valley' in GEOGRAPHIES, "River valley should exist"
    assert len(GEOGRAPHIES) > 1, "Should have multiple geographies"
    
    # Test seasons
    spring = get_current_season(0)
    assert spring.name == 'Spring', "Turn 0 should be spring"
    
    winter = get_current_season(3)
    assert winter.name == 'Winter', "Turn 3 should be winter"
    
    print("✓ Geography tests passed")


def test_governance():
    """Test governance system"""
    print("\nTesting Governance...")
    
    # Small population
    available = get_available_governance_types(50, False)
    assert len(available) >= 1, "Should have at least tribal elder"
    
    # Large population
    available = get_available_governance_types(1000, True)
    assert len(available) > 1, "Should have more governance options with larger population"
    
    # Early state requires writing
    has_early_state = any(g.name == 'early_state' for g in available)
    assert has_early_state, "Early state should be available with population 1000 and writing"
    
    available_no_writing = get_available_governance_types(1000, False)
    has_early_state_no_writing = any(g.name == 'early_state' for g in available_no_writing)
    assert not has_early_state_no_writing, "Early state should not be available without writing"
    
    print("✓ Governance tests passed")


def test_resource_management():
    """Test resource management"""
    print("\nTesting Resource Management...")
    
    state = GameState()
    
    # Test can_afford
    assert state.can_afford({'food': 100}), "Should be able to afford 100 food"
    assert not state.can_afford({'food': 10000}), "Should not be able to afford 10000 food"
    
    # Test spend_resources
    initial_food = state.resources['food']
    state.spend_resources({'food': 50})
    assert state.resources['food'] == initial_food - 50, "Food should decrease"
    
    print("✓ Resource management tests passed")


def test_game_progression():
    """Test game progression over multiple turns"""
    print("\nTesting Game Progression...")
    
    state = GameState()
    initial_pop = state.population
    
    # Simulate 10 years
    for _ in range(10):
        state.advance_turn()
    
    assert state.year == -7990, "Should be at 7990 BC after 10 turns"
    assert state.turn == 10, "Should be turn 10"
    # Population should generally grow (though random events might affect it)
    
    print("✓ Game progression tests passed")


def test_technology_progression():
    """Test discovering technologies"""
    print("\nTesting Technology Progression...")
    
    state = GameState()
    
    # Discover agriculture
    state.discover_technology('agriculture')
    assert 'agriculture' in state.technologies, "Agriculture should be discovered"
    assert state.culture_points > 0, "Should have culture points"
    
    # Check for advanced agriculture
    available = get_available_technologies(state.technologies)
    has_advanced_ag = any(tech.name == 'advanced_agriculture' for tech in available)
    assert has_advanced_ag, "Advanced agriculture should be available after agriculture"
    
    print("✓ Technology progression tests passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Ancestral Habitation Tests")
    print("=" * 60)
    
    try:
        test_game_state()
        test_technologies()
        test_geography()
        test_governance()
        test_resource_management()
        test_game_progression()
        test_technology_progression()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
