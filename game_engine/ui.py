"""
User Interface
Handles display and user input for the game
"""

from game_engine.game_state import GameState
from game_engine.technologies import get_available_technologies, TECHNOLOGIES
from game_engine.geography import GEOGRAPHIES, get_current_season, calculate_migration_success
from game_engine.governance import get_available_governance_types, GOVERNANCE_TYPES


class GameUI:
    """Handles game UI and user interaction"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        
    def show_welcome(self):
        """Display welcome message"""
        print("Welcome to the dawn of civilization!")
        print()
        print("You lead a small tribe at the beginning of the Neolithic era.")
        print("Guide your people through the development of farming, technology,")
        print("and governance as you build a thriving civilization.")
        print()
        
        # Get tribe name
        tribe_name = input("What is the name of your tribe? (Press Enter for 'The First People'): ").strip()
        if tribe_name:
            self.game_state.tribe_name = tribe_name
        
        print(f"\nWelcome, {self.game_state.tribe_name}!")
        print()
        
    def display_game_status(self):
        """Display current game status"""
        print("\n" + "=" * 60)
        print(f"Year: {self.game_state.get_year_display()} | Turn: {self.game_state.turn}")
        print(f"Tribe: {self.game_state.tribe_name}")
        print("=" * 60)
        
        # Population
        print(f"\nPopulation: {self.game_state.population}")
        
        # Resources
        print("\nResources:")
        for resource, amount in sorted(self.game_state.resources.items()):
            print(f"  {resource.capitalize()}: {amount}")
        
        # Geography
        geo = GEOGRAPHIES[self.game_state.geography_type]
        season = get_current_season(self.game_state.turn)
        print(f"\nLocation: {geo.name} (Climate: {geo.climate}, Season: {season.name})")
        
        # Governance
        gov = GOVERNANCE_TYPES[self.game_state.governance_type]
        print(f"Governance: {gov.display_name} (Stability: {self.game_state.governance_stability}%)")
        
        # Farms
        if self.game_state.farms > 0:
            print(f"Farms: {self.game_state.farms} (Level {self.game_state.farming_level})")
        
        # Writing
        if self.game_state.has_writing:
            print("✓ Writing system developed")
        
        # Culture
        print(f"Culture Points: {self.game_state.culture_points}")
        
    def process_turn(self):
        """Process a single turn"""
        print("\n" + "-" * 60)
        print("Available Actions:")
        print("  1. Advance to next year")
        print("  2. Build farm")
        print("  3. Research technology")
        print("  4. Migrate to new location")
        print("  5. Change governance")
        print("  6. View technologies")
        print("  7. View available locations")
        print("  8. View statistics")
        print("  9. Quit game")
        print("-" * 60)
        
        choice = input("\nWhat would you like to do? ").strip()
        
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
            print("Invalid choice. Please try again.")
            
    def advance_year(self):
        """Advance to next year"""
        self.game_state.advance_turn()
        print(f"\nTime passes... It is now {self.game_state.get_year_display()}")
        
        # Check for milestones
        if self.game_state.year == -1200 and 'bronze_working' not in self.game_state.technologies:
            print("\n*** The Bronze Age has begun in other regions! ***")
            print("Your tribe must advance or risk being left behind.")
        
    def build_farm(self):
        """Build a new farm"""
        cost = {'wood': 50, 'stone': 30, 'food': 100}
        
        print("\nBuilding a farm requires:")
        for resource, amount in cost.items():
            print(f"  {resource.capitalize()}: {amount}")
        
        if not self.game_state.can_afford(cost):
            print("\nYou don't have enough resources!")
            return
        
        # Need agriculture technology
        if 'agriculture' not in self.game_state.technologies:
            print("\nYou need to research Agriculture first!")
            return
        
        confirm = input("\nBuild this farm? (y/n): ").strip().lower()
        if confirm == 'y':
            self.game_state.spend_resources(cost)
            self.game_state.farms += 1
            print(f"\nFarm built! You now have {self.game_state.farms} farm(s).")
            
            # Improve farming level occasionally
            if self.game_state.farms % 5 == 0 and self.game_state.farming_level < 5:
                self.game_state.farming_level += 1
                print(f"Your farming techniques have improved! (Level {self.game_state.farming_level})")
    
    def research_technology(self):
        """Research a new technology"""
        available_techs = get_available_technologies(self.game_state.technologies)
        
        if not available_techs:
            print("\nNo technologies available to research right now.")
            print("You may need to discover prerequisites first.")
            return
        
        print("\nAvailable Technologies:")
        for i, tech in enumerate(available_techs, 1):
            print(f"\n{i}. {tech.name.replace('_', ' ').title()}")
            print(f"   {tech.description}")
            print(f"   Era: {tech.era.replace('_', ' ').title()}")
            print("   Cost:", end=" ")
            cost_items = [f"{v} {k}" for k, v in tech.cost.items()]
            print(", ".join(cost_items))
        
        choice = input("\nWhich technology to research? (number or 0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0:
                return
            if idx >= len(available_techs):
                print("Invalid choice.")
                return
            
            tech = available_techs[idx]
            
            if not self.game_state.can_afford(tech.cost):
                print("\nYou don't have enough resources!")
                return
            
            self.game_state.spend_resources(tech.cost)
            self.game_state.discover_technology(tech.name)
            print(f"\n*** Technology discovered: {tech.name.replace('_', ' ').title()} ***")
            print(f"{tech.description}")
            
            # Special effects
            if tech.name == 'writing':
                self.game_state.has_writing = True
                print("\nYour civilization has developed writing!")
                print("New governance options are now available.")
            
            if tech.name in ['agriculture', 'advanced_agriculture']:
                print("\nYou can now build farms to produce more food.")
                
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def migrate(self):
        """Migrate to a new location"""
        print("\nAvailable Locations:")
        locations = []
        for i, (key, geo) in enumerate(GEOGRAPHIES.items(), 1):
            if key != self.game_state.geography_type:
                locations.append(key)
                print(f"\n{i}. {geo.name}")
                print(f"   {geo.description}")
                print(f"   Climate: {geo.climate}")
                print(f"   Migration Difficulty: {geo.migration_difficulty}/10")
        
        choice = input("\nWhere to migrate? (number or 0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0:
                return
            if idx >= len(locations):
                print("Invalid choice.")
                return
            
            new_location = locations[idx]
            
            confirm = input(f"\nMigration is risky and may result in casualties. Proceed? (y/n): ").strip().lower()
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
                print(f"\n*** Migration successful! ***")
                print(f"Your tribe has moved to {geo.name}.")
                print(f"Casualties during migration: {casualties}")
            else:
                print(f"\n*** Migration failed! ***")
                print(f"Your tribe attempted to migrate but couldn't complete the journey.")
                print(f"Casualties: {casualties}")
                print(f"Your tribe remains at the current location.")
                
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def change_governance(self):
        """Change governance structure"""
        available_govs = get_available_governance_types(
            self.game_state.population,
            self.game_state.has_writing
        )
        
        current_gov = GOVERNANCE_TYPES[self.game_state.governance_type]
        print(f"\nCurrent Governance: {current_gov.display_name}")
        print("\nAvailable Governance Types:")
        
        for i, gov in enumerate(available_govs, 1):
            if gov.name != self.game_state.governance_type:
                print(f"\n{i}. {gov.display_name}")
                print(f"   {gov.description}")
                print(f"   Requires population: {gov.population_requirement}")
                print(f"   Stability: {'+' if gov.stability_modifier >= 1 else ''}{(gov.stability_modifier - 1) * 100:.0f}%")
                print(f"   Production: {'+' if gov.production_modifier >= 1 else ''}{(gov.production_modifier - 1) * 100:.0f}%")
        
        choice = input("\nChange to which governance? (number or 0 to cancel): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0:
                return
            if idx >= len(available_govs):
                print("Invalid choice.")
                return
            
            new_gov = available_govs[idx]
            if new_gov.name == self.game_state.governance_type:
                print("This is already your current governance.")
                return
            
            self.game_state.governance_type = new_gov.name
            print(f"\n*** Governance changed to {new_gov.display_name} ***")
            print(f"{new_gov.description}")
            
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def view_technologies(self):
        """View discovered and available technologies"""
        print("\n" + "=" * 60)
        print("TECHNOLOGIES")
        print("=" * 60)
        
        print("\nDiscovered Technologies:")
        for tech_name in sorted(self.game_state.technologies):
            if tech_name in TECHNOLOGIES:
                tech = TECHNOLOGIES[tech_name]
                print(f"  ✓ {tech.name.replace('_', ' ').title()} - {tech.description}")
            else:
                print(f"  ✓ {tech_name.replace('_', ' ').title()}")
        
        available_techs = get_available_technologies(self.game_state.technologies)
        if available_techs:
            print("\nAvailable for Research:")
            for tech in available_techs:
                print(f"  • {tech.name.replace('_', ' ').title()} - {tech.description}")
        
        input("\nPress Enter to continue...")
    
    def view_locations(self):
        """View all geographical locations"""
        print("\n" + "=" * 60)
        print("GEOGRAPHICAL LOCATIONS")
        print("=" * 60)
        
        current = GEOGRAPHIES[self.game_state.geography_type]
        print(f"\nCurrent Location: {current.name}")
        print(f"  {current.description}")
        print(f"  Climate: {current.climate}")
        
        print("\nOther Locations:")
        for key, geo in GEOGRAPHIES.items():
            if key != self.game_state.geography_type:
                print(f"\n  {geo.name}")
                print(f"    {geo.description}")
                print(f"    Climate: {geo.climate}")
                print(f"    Migration Difficulty: {geo.migration_difficulty}/10")
        
        input("\nPress Enter to continue...")
    
    def view_statistics(self):
        """View detailed game statistics"""
        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)
        
        print(f"\nTribe: {self.game_state.tribe_name}")
        print(f"Year: {self.game_state.get_year_display()}")
        print(f"Turn: {self.game_state.turn}")
        print(f"Population: {self.game_state.population}")
        print(f"Culture Points: {self.game_state.culture_points}")
        
        print(f"\nTechnologies Discovered: {len(self.game_state.technologies)}")
        print(f"Farms: {self.game_state.farms}")
        print(f"Farming Level: {self.game_state.farming_level}/5")
        
        gov = GOVERNANCE_TYPES[self.game_state.governance_type]
        print(f"\nGovernance: {gov.display_name}")
        print(f"Stability: {self.game_state.governance_stability}%")
        
        geo = GEOGRAPHIES[self.game_state.geography_type]
        print(f"\nLocation: {geo.name}")
        print(f"Climate: {geo.climate}")
        
        if self.game_state.has_writing:
            print("\n✓ Writing System: Developed")
        else:
            print("\n✗ Writing System: Not yet developed")
        
        # Calculate progress to Iron Age
        years_to_iron_age = -1200 - self.game_state.year
        if years_to_iron_age > 0:
            print(f"\nYears until Iron Age begins: {years_to_iron_age}")
        else:
            print("\nThe Iron Age has arrived!")
        
        input("\nPress Enter to continue...")
    
    def quit_game(self):
        """Quit the game"""
        confirm = input("\nAre you sure you want to quit? (y/n): ").strip().lower()
        if confirm == 'y':
            self.game_state.is_running = False
            print("\nGame Over!")
            print(f"\nFinal Statistics:")
            print(f"  Tribe: {self.game_state.tribe_name}")
            print(f"  Final Year: {self.game_state.get_year_display()}")
            print(f"  Final Population: {self.game_state.population}")
            print(f"  Technologies: {len(self.game_state.technologies)}")
            print(f"  Culture Points: {self.game_state.culture_points}")
