"""
Geography and Terrain System
Defines different geographical locations and their effects
"""

from typing import Dict
import random


class Geography:
    """Represents a geographical location type"""
    
    def __init__(self, name: str, description: str, resource_modifiers: Dict[str, float],
                 climate: str, migration_difficulty: int):
        self.name = name
        self.description = description
        self.resource_modifiers = resource_modifiers
        self.climate = climate
        self.migration_difficulty = migration_difficulty  # 1-10


# Available geography types
GEOGRAPHIES = {
    'river_valley': Geography(
        'River Valley',
        'Fertile land near a river, ideal for early agriculture',
        {'food': 1.3, 'water': 1.5, 'clay': 1.2},
        'temperate',
        3
    ),
    'coastal': Geography(
        'Coastal Region',
        'Near the sea with access to fishing and trade',
        {'food': 1.2, 'fish': 1.5, 'stone': 1.1},
        'temperate',
        4
    ),
    'plains': Geography(
        'Open Plains',
        'Flat grasslands suitable for herding and farming',
        {'food': 1.1, 'grass': 1.3, 'wood': 0.7},
        'temperate',
        2
    ),
    'forest': Geography(
        'Dense Forest',
        'Forested area with abundant wood and game',
        {'wood': 1.5, 'game': 1.3, 'food': 1.0},
        'temperate',
        5
    ),
    'hills': Geography(
        'Hilly Region',
        'Elevated terrain with stone deposits',
        {'stone': 1.4, 'food': 0.9, 'wood': 1.1},
        'temperate',
        6
    ),
    'mountains': Geography(
        'Mountain Foothills',
        'Near mountains with mineral resources but harsh conditions',
        {'stone': 1.6, 'minerals': 1.3, 'food': 0.7},
        'cold',
        8
    ),
    'desert_edge': Geography(
        'Desert Edge',
        'Semi-arid land requiring careful water management',
        {'food': 0.8, 'stone': 1.2, 'clay': 1.3},
        'hot',
        7
    ),
}


class Season:
    """Represents seasonal effects"""
    
    def __init__(self, name: str, food_modifier: float, event_chance: float):
        self.name = name
        self.food_modifier = food_modifier
        self.event_chance = event_chance


SEASONS = {
    'spring': Season('Spring', 1.2, 0.05),
    'summer': Season('Summer', 1.3, 0.03),
    'autumn': Season('Autumn', 1.1, 0.08),
    'winter': Season('Winter', 0.6, 0.12),
}


def get_current_season(turn: int) -> Season:
    """Get current season based on turn number"""
    season_index = (turn % 4)
    season_names = ['spring', 'summer', 'autumn', 'winter']
    return SEASONS[season_names[season_index]]


def calculate_migration_success(population: int, geography_from: str, 
                                geography_to: str) -> tuple[bool, int]:
    """
    Calculate if migration is successful
    Returns (success, casualties)
    """
    base_difficulty = GEOGRAPHIES[geography_to].migration_difficulty
    
    # Larger populations have more difficulty migrating
    population_factor = min(2.0, population / 100)
    
    success_chance = max(0.3, 1.0 - (base_difficulty * population_factor / 20))
    
    if random.random() < success_chance:
        # Successful migration, but some casualties
        casualties = int(population * random.uniform(0.05, 0.15))
        return True, casualties
    else:
        # Failed migration, more casualties
        casualties = int(population * random.uniform(0.2, 0.4))
        return False, casualties
