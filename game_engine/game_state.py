"""
Game State Manager
Handles the overall game state including time, resources, population, and technologies
"""

import random
from typing import Dict, List, Set


class GameState:
    """Main game state class"""
    
    def __init__(self):
        # Time tracking (in years, negative = BC)
        self.year = -8000  # 8000 BC
        self.turn = 0
        self.is_running = True
        
        # Tribe name
        self.tribe_name = "The First People"
        
        # Population
        self.population = 50
        self.population_growth_rate = 0.02  # 2% per turn (year)
        
        # Resources
        self.resources = {
            'food': 500,
            'wood': 100,
            'stone': 50,
            'clay': 30,
            'hides': 20,
        }
        
        # Geography and settlements
        self.geography_type = "river_valley"  # Starting location
        self.settlements = ["Main Camp"]
        
        # Technologies discovered
        self.technologies: Set[str] = {
            'fire',
            'stone_tools',
            'hunting',
            'gathering',
        }
        
        # Farming and food production
        self.farms = 0
        self.farming_level = 0  # 0-5 representing development
        
        # Governance
        self.governance_type = "tribal_elder"  # Starting governance
        self.governance_stability = 70  # 0-100
        
        # Cultural development
        self.culture_points = 0
        self.has_writing = False
        
    def advance_turn(self):
        """Advance the game by one turn (year)"""
        self.turn += 1
        self.year += 1
        
        # Population growth
        births = int(self.population * self.population_growth_rate)
        # Natural deaths (reduced by technologies and farming)
        death_rate = max(0.01, 0.03 - (self.farming_level * 0.003))
        deaths = int(self.population * death_rate)
        self.population = max(1, self.population + births - deaths)
        
        # Resource production
        self._produce_resources()
        
        # Resource consumption
        self._consume_resources()
        
        # Random events
        self._check_random_events()
        
    def _produce_resources(self):
        """Produce resources based on population and technologies"""
        # Base gathering
        gatherers = self.population // 3
        self.resources['food'] += gatherers * 2
        self.resources['wood'] += (self.population // 5) * 1
        
        # Farming production
        if self.farms > 0:
            farm_output = self.farms * 50 * (1 + self.farming_level * 0.2)
            self.resources['food'] += int(farm_output)
        
        # Advanced gathering with technologies
        if 'advanced_foraging' in self.technologies:
            self.resources['food'] += gatherers
        
        if 'woodworking' in self.technologies:
            self.resources['wood'] += self.population // 10
            
        if 'pottery' in self.technologies:
            self.resources['clay'] += self.population // 20
            
    def _consume_resources(self):
        """Consume resources based on population needs"""
        # Food consumption (2 per person per year)
        food_needed = self.population * 2
        actual_consumption = min(food_needed, self.resources['food'])
        self.resources['food'] -= actual_consumption
        
        # Starvation check
        if actual_consumption < food_needed * 0.5:
            starvation_deaths = int(self.population * 0.1)
            self.population = max(1, self.population - starvation_deaths)
            self.governance_stability = max(0, self.governance_stability - 10)
            
    def _check_random_events(self):
        """Check for random events"""
        if random.random() < 0.05:  # 5% chance per turn
            event = random.choice([
                'good_harvest',
                'harsh_winter',
                'wildlife_found',
                'disease',
            ])
            
            if event == 'good_harvest':
                self.resources['food'] += 100
            elif event == 'harsh_winter':
                self.resources['food'] = max(0, self.resources['food'] - 150)
            elif event == 'wildlife_found':
                self.resources['hides'] += 20
            elif event == 'disease':
                deaths = int(self.population * 0.05)
                self.population = max(1, self.population - deaths)
                
    def can_afford(self, cost: Dict[str, int]) -> bool:
        """Check if we have enough resources"""
        for resource, amount in cost.items():
            if self.resources.get(resource, 0) < amount:
                return False
        return True
    
    def spend_resources(self, cost: Dict[str, int]):
        """Spend resources"""
        for resource, amount in cost.items():
            self.resources[resource] -= amount
            
    def discover_technology(self, tech_name: str):
        """Discover a new technology"""
        self.technologies.add(tech_name)
        self.culture_points += 10
        
    def get_year_display(self) -> str:
        """Get formatted year display"""
        if self.year < 0:
            return f"{abs(self.year)} BC"
        else:
            return f"{self.year} AD"
