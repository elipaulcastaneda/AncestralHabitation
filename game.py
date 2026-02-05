#!/usr/bin/env python3
"""
Ancestral Habitation - A Neolithic Era Strategy Game
Main game entry point
"""

from game_engine.game_state import GameState
from game_engine.ui import GameUI


def main():
    """Main game loop"""
    print("=" * 60)
    print("ANCESTRAL HABITATION")
    print("A Neolithic Era Strategy Game (8000 BC - 1200 BC)")
    print("=" * 60)
    print()
    
    # Initialize game
    game_state = GameState()
    ui = GameUI(game_state)
    
    # Show welcome message
    ui.show_welcome()
    
    # Main game loop
    while game_state.is_running:
        ui.display_game_status()
        ui.process_turn()
    
    print("\nThank you for playing Ancestral Habitation!")


if __name__ == "__main__":
    main()
