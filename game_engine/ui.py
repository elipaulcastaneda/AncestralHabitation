"""
User Interface
Handles display and user input for the game
"""

from game_engine.game_state import GameState
from game_engine.technologies import get_available_technologies, TECHNOLOGIES
from game_engine.geography import GEOGRAPHIES, get_current_season, calculate_migration_success
from game_engine.governance import get_available_governance_types, GOVERNANCE_TYPES
from game_engine.graphics import (
    draw_game_title, draw_status_panel, draw_resource_bars, draw_action_menu,
    draw_terrain_map, draw_technology_tree, draw_location_details, draw_statistics,
    draw_event_notification, draw_success_message, draw_error_message, draw_info_message,
    draw_header, console
)


class GameUI:
    """Handles game UI and user interaction"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        
    def show_welcome(self):
        """Display welcome message"""
        draw_game_title()
        console.print("[bold cyan]Welcome to the dawn of civilization![/bold cyan]\n")
        console.print("You lead a small tribe at the beginning of the Neolithic era.")
        console.print("Guide your people through the development of farming, technology,")
        console.print("and governance as you build a thriving civilization.\n")
        
        # Get tribe name
        tribe_name = console.input("[bold cyan]What is the name of your tribe? (Press Enter for 'The First People'): [/bold cyan]").strip()
        if tribe_name:
            self.game_state.tribe_name = tribe_name
        
        draw_success_message(f"Welcome, {self.game_state.tribe_name}!")
        console.print()
        
    def display_game_status(self):
        """Display current game status"""
        console.print()
        draw_status_panel(self.game_state)
        
        # Display map
        draw_terrain_map(self.game_state.geography_type)
        
        # Display resources
        console.print()
        draw_resource_bars(self.game_state.resources)
        
    def process_turn(self):
        """Process a single turn"""
        draw_action_menu()
        
        choice = console.input("\n[bold cyan]What would you like to do? [/bold cyan]").strip()
        
        if choice == '1':
            self.advance_year()
        elif choice == '2':
            self.build_farm()
        elif choice == '3':
            self.research_technology()
        elif choice == '4':
            self.migrate()
        elif choice == '5':
            self.change_governance()
        elif choice == '6':
            self.view_technologies()
        elif choice == '7':
            self.view_locations()
        elif choice == '8':
            self.view_statistics()
        elif choice == '9':
            self.quit_game()
        else:
            draw_error_message("Invalid choice. Please try again.")
            
    def advance_year(self):
        """Advance to next year"""
        self.game_state.advance_turn()
        draw_success_message(f"Time passes... It is now {self.game_state.get_year_display()}")
        
        # Check for milestones
        if self.game_state.year == -1200 and 'bronze_working' not in self.game_state.technologies:
            draw_event_notification("Bronze Age Arrived", 
                                   "The Bronze Age has begun in other regions!\nYour tribe must advance or risk being left behind.")
        
    def build_farm(self):
        """Build a new farm"""
        cost = {'wood': 50, 'stone': 30, 'food': 100}
        
        console.print("\n[bold cyan]Building a farm requires:[/bold cyan]")
        for resource, amount in cost.items():
            console.print(f"  {resource.capitalize()}: {amount}")
        
        if not self.game_state.can_afford(cost):
            draw_error_message("You don't have enough resources!")
            return
        
        # Need agriculture technology
        if 'agriculture' not in self.game_state.technologies:
            draw_error_message("You need to research Agriculture first!")
            return
        
        confirm = console.input("\n[bold cyan]Build this farm? (y/n): [/bold cyan]").strip().lower()
        if confirm == 'y':
            self.game_state.spend_resources(cost)
            self.game_state.farms += 1
            draw_success_message(f"Farm built! You now have {self.game_state.farms} farm(s).")
            
            # Improve farming level occasionally
            if self.game_state.farms % 5 == 0 and self.game_state.farming_level < 5:
                self.game_state.farming_level += 1
                draw_success_message(f"Your farming techniques have improved! (Level {self.game_state.farming_level})")
    
    def research_technology(self):
        """Research a new technology"""
        available_techs = get_available_technologies(self.game_state.technologies)
        
        if not available_techs:
            draw_error_message("No technologies available to research right now.")
            draw_info_message("You may need to discover prerequisites first.")
            return
        
        console.print("\n[bold cyan]Available Technologies:[/bold cyan]")
        for i, tech in enumerate(available_techs, 1):
            cost_items = [f"{v} {k}" for k, v in tech.cost.items()]
            console.print(f"\n[bold cyan]{i}.[/bold cyan] {tech.name.replace('_', ' ').title()}")
            console.print(f"   {tech.description}")
            console.print(f"   [dim]Era: {tech.era.replace('_', ' ').title()}[/dim]")
            console.print(f"   [yellow]Cost: {', '.join(cost_items)}[/yellow]")
        
        choice = console.input("\n[bold cyan]Which technology to research? (number or 0 to cancel): [/bold cyan]").strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0:
                return
            if idx >= len(available_techs):
                draw_error_message("Invalid choice.")
                return
            
            tech = available_techs[idx]
            
            if not self.game_state.can_afford(tech.cost):
                draw_error_message("You don't have enough resources!")
                return
            
            self.game_state.spend_resources(tech.cost)
            self.game_state.discover_technology(tech.name)
            draw_success_message(f"Technology discovered: {tech.name.replace('_', ' ').title()}")
            console.print(f"{tech.description}")
            
            # Special effects
            if tech.name == 'writing':
                self.game_state.has_writing = True
                draw_success_message("Your civilization has developed writing!")
                draw_info_message("New governance options are now available.")
            
            if tech.name in ['agriculture', 'advanced_agriculture']:
                draw_info_message("You can now build farms to produce more food.")
                
        except (ValueError, IndexError):
            draw_error_message("Invalid choice.")
    
    def migrate(self):
        """Migrate to a new location"""
        console.print("\n[bold cyan]Available Locations:[/bold cyan]")
        locations = []
        for i, (key, geo) in enumerate(GEOGRAPHIES.items(), 1):
            if key != self.game_state.geography_type:
                locations.append(key)
                console.print(f"\n[bold cyan]{i}.[/bold cyan] {geo.name}")
                console.print(f"   {geo.description}")
                console.print(f"   [dim]Climate: {geo.climate} | Migration Difficulty: {geo.migration_difficulty}/10[/dim]")
        
        choice = console.input("\n[bold cyan]Where to migrate? (number or 0 to cancel): [/bold cyan]").strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0:
                return
            if idx >= len(locations):
                draw_error_message("Invalid choice.")
                return
            
            new_location = locations[idx]
            
            confirm = console.input(f"\n[bold yellow]Migration is risky and may result in casualties. Proceed? (y/n): [/bold yellow]").strip().lower()
            if confirm != 'y':
                return
            
            success, casualties = calculate_migration_success(
                self.game_state.population,
                self.game_state.geography_type,
                new_location
            )
            
            self.game_state.population = max(1, self.game_state.population - casualties)
            
            if success:
                self.game_state.geography_type = new_location
                geo = GEOGRAPHIES[new_location]
                draw_success_message("Migration successful!")
                console.print(f"Your tribe has moved to [cyan]{geo.name}[/cyan].")
                draw_info_message(f"Casualties during migration: {casualties}")
            else:
                draw_event_notification("Migration Failed", 
                                       f"Your tribe attempted to migrate but couldn't complete the journey.\nCasualties: {casualties}")
                
        except (ValueError, IndexError):
            draw_error_message("Invalid choice.")
    
    def change_governance(self):
        """Change governance structure"""
        available_govs = get_available_governance_types(
            self.game_state.population,
            self.game_state.has_writing
        )
        
        current_gov = GOVERNANCE_TYPES[self.game_state.governance_type]
        console.print(f"\n[bold cyan]Current Governance: {current_gov.display_name}[/bold cyan]")
        console.print("\n[bold cyan]Available Governance Types:[/bold cyan]")
        
        for i, gov in enumerate(available_govs, 1):
            if gov.name != self.game_state.governance_type:
                stability = f"{'+' if gov.stability_modifier >= 1 else ''}{(gov.stability_modifier - 1) * 100:.0f}%"
                production = f"{'+' if gov.production_modifier >= 1 else ''}{(gov.production_modifier - 1) * 100:.0f}%"
                console.print(f"\n[bold cyan]{i}.[/bold cyan] {gov.display_name}")
                console.print(f"   {gov.description}")
                console.print(f"   [dim]Population Required: {gov.population_requirement}[/dim]")
                console.print(f"   [yellow]Stability: {stability} | Production: {production}[/yellow]")
        
        choice = console.input("\n[bold cyan]Change to which governance? (number or 0 to cancel): [/bold cyan]").strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0:
                return
            if idx >= len(available_govs):
                draw_error_message("Invalid choice.")
                return
            
            new_gov = available_govs[idx]
            if new_gov.name == self.game_state.governance_type:
                draw_info_message("This is already your current governance.")
                return
            
            self.game_state.governance_type = new_gov.name
            draw_success_message(f"Governance changed to {new_gov.display_name}")
            console.print(f"{new_gov.description}")
            
        except (ValueError, IndexError):
            draw_error_message("Invalid choice.")
    
    def view_technologies(self):
        """View discovered and available technologies"""
        console.print()
        draw_technology_tree(TECHNOLOGIES, self.game_state.technologies)
        
        console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")
    
    def view_locations(self):
        """View all geographical locations"""
        console.print()
        draw_header("Geographical Locations", "Discover the world...")
        
        current = GEOGRAPHIES[self.game_state.geography_type]
        draw_location_details(self.game_state.geography_type, GEOGRAPHIES)
        
        console.print("\n[bold cyan]Other Available Locations:[/bold cyan]")
        for key, geo in GEOGRAPHIES.items():
            if key != self.game_state.geography_type:
                console.print(f"\n  [bold]{geo.name}[/bold]")
                console.print(f"    {geo.description}")
                console.print(f"    [dim]Climate: {geo.climate} | Migration Difficulty: {geo.migration_difficulty}/10[/dim]")
        
        console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")
    
    def view_statistics(self):
        """View detailed game statistics"""
        console.print()
        draw_statistics(self.game_state)
        
        console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")
    
    def quit_game(self):
        """Quit the game"""
        confirm = console.input("\n[bold cyan]Are you sure you want to quit? (y/n): [/bold cyan]").strip().lower()
        if confirm == 'y':
            self.game_state.is_running = False
            console.print()
            draw_header("Game Over", f"Your civilization's journey ends here")
            
            final_stats = f"""
[bold yellow]Final Statistics[/bold yellow]

Tribe: [cyan]{self.game_state.tribe_name}[/cyan]
Year: [cyan]{self.game_state.get_year_display()}[/cyan]
Final Population: [cyan]{self.game_state.population}[/cyan]
Technologies Discovered: [cyan]{len(self.game_state.technologies)}[/cyan]
Culture Points Earned: [cyan]{self.game_state.culture_points}[/cyan]
Farms Built: [cyan]{self.game_state.farms}[/cyan]

Thank you for playing Ancestral Habitation!
May your tribe be remembered through the ages!
"""
            console.print(final_stats)
