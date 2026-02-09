#!/usr/bin/env python3
"""
Graphics Showcase - Demonstrates the enhanced graphics features
"""

from game_engine.graphics import (
    draw_game_title, draw_header, draw_status_panel, draw_resource_bars,
    draw_terrain_map, draw_technology_tree, draw_location_details,
    draw_statistics, draw_event_notification, draw_success_message,
    draw_error_message, draw_info_message, draw_action_menu, console
)
from game_engine.game_state import GameState
from game_engine.technologies import TECHNOLOGIES
from game_engine.geography import GEOGRAPHIES


def showcase_graphics():
    """Demonstrate all graphics features"""
    
    # Create a sample game state
    game_state = GameState()
    game_state.tribe_name = "The Innovators"
    game_state.population = 250
    game_state.resources = {
        'food': 1500,
        'wood': 450,
        'stone': 320,
        'clay': 180,
        'hides': 90,
    }
    game_state.farms = 3
    game_state.farming_level = 2
    game_state.have_writing = True
    game_state.culture_points = 85
    game_state.technologies.update(['agriculture', 'pottery', 'weaving', 'woodworking'])
    
    # Show game title
    draw_game_title()
    console.input("[bold cyan]Press Enter to see the graphics showcase...[/bold cyan]")
    console.clear() if hasattr(console, 'clear') else None
    
    # Show status panel
    draw_header("Civilization Status Display")
    draw_status_panel(game_state)
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show terrain map
    draw_header("Territory Map Visualization")
    draw_terrain_map(game_state.geography_type)
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show resource bars
    draw_header("Resource Visualization")
    draw_resource_bars(game_state.resources)
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show different terrain maps
    draw_header("Available Territories")
    console.print("[bold cyan]Here are different territory types you can migrate to:[/bold cyan]\n")
    
    terrains = ['coastal', 'plains', 'forest', 'hills', 'mountains']
    for terrain in terrains:
        draw_terrain_map(terrain)
    
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show technology tree
    draw_header("Technology Tree")
    draw_technology_tree(TECHNOLOGIES, game_state.technologies, game_state.population)
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show location details
    draw_header("Location Details")
    draw_location_details(game_state.geography_type, GEOGRAPHIES)
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show game statistics
    draw_header("Game Statistics")
    draw_statistics(game_state)
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show action menu
    draw_header("Action Menu")
    draw_action_menu()
    console.input("[bold cyan]Press Enter to continue...[/bold cyan]")
    
    # Show notification examples
    draw_header("Notification Examples")
    console.print()
    draw_success_message("Farm successfully built!")
    draw_error_message("Insufficient resources for this action.")
    draw_info_message("Your population is growing!")
    draw_event_notification("Harsh Winter", 
                           "This winter is particularly severe.\n-30% food production for 2 turns")
    
    console.input("[bold cyan]Press Enter to finish...[/bold cyan]")
    
    draw_header("Graphics Showcase Complete!")
    console.print("[bold green]Thank you for exploring the enhanced graphics features![/bold green]\n")


if __name__ == "__main__":
    showcase_graphics()
