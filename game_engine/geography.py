"""
Geography and Terrain System
Defines different geographical locations and their effects
"""

from typing import Dict, List, Optional
import random


class Geography:
    """Represents a geographical location type"""
    
    def __init__(
        self,
        name: str,
        description: str,
        resource_modifiers: Dict[str, float],
        climate: str,
        migration_difficulty: int,
        soil_types: Optional[List[str]] = None,
        domesticated: Optional[List[str]] = None,
        proto_languages: Optional[List[str]] = None,
        ethnicities: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.resource_modifiers = resource_modifiers
        self.climate = climate
        self.migration_difficulty = migration_difficulty  # 1-10
        self.soil_types = soil_types or ['loess']
        self.domesticated = domesticated or []
        self.proto_languages = proto_languages or []
        self.ethnicities = ethnicities or []


# Available geography types
GEOGRAPHIES = {
    'river_valley': Geography(
        'River Valley',
        'Fertile land near a river, ideal for early agriculture',
        {'food': 1.3, 'water': 1.5, 'clay': 1.2},
        'temperate',
        3,
        soil_types=['alluvial', 'clay']
    ),
    'coastal': Geography(
        'Coastal Region',
        'Near the sea with access to fishing and trade',
        {'food': 1.2, 'fish': 1.5, 'stone': 1.1},
        'temperate',
        4,
        soil_types=['sandy', 'alluvial']
    ),
    'plains': Geography(
        'Open Plains',
        'Flat grasslands suitable for herding and farming',
        {'food': 1.1, 'grass': 1.3, 'wood': 0.7},
        'temperate',
        2,
        soil_types=['black_earth', 'loess']
    ),
    'forest': Geography(
        'Dense Forest',
        'Forested area with abundant wood and game',
        {'wood': 1.5, 'game': 1.3, 'food': 1.0},
        'temperate',
        5,
        soil_types=['peat', 'clay']
    ),
    'hills': Geography(
        'Hilly Region',
        'Elevated terrain with stone deposits',
        {'stone': 1.4, 'food': 0.9, 'wood': 1.1},
        'temperate',
        6,
        soil_types=['limestone', 'clay']
    ),
    'mountains': Geography(
        'Mountain Foothills',
        'Near mountains with mineral resources but harsh conditions',
        {'stone': 1.6, 'minerals': 1.3, 'food': 0.7},
        'cold',
        8,
        soil_types=['mountain', 'volcanic']
    ),
    'desert_edge': Geography(
        'Desert Edge',
        'Semi-arid land requiring careful water management',
        {'food': 0.8, 'stone': 1.2, 'clay': 1.3},
        'hot',
        7,
        soil_types=['sandy', 'limestone']
    ),
    'fertile_crescent': Geography(
        'Fertile Crescent',
        'Early agriculture heartland with rich alluvial soils and river networks',
        {'food': 1.4, 'clay': 1.3, 'stone': 1.1, 'hides': 1.2, 'wood': 0.9},
        'temperate',
        5,
        soil_types=['alluvial', 'loess'],
        domesticated=[
            'emmer wheat', 'einkorn wheat', 'barley', 'lentils', 'peas', 'flax',
            'sheep', 'goats', 'cattle', 'pigs',
        ],
        proto_languages=[
            'Proto-Semitic', 'Proto-Hurrian', 'Proto-Anatolian',
        ],
        ethnicities=[
            'early Semitic communities', 'Hurrian peoples', 'Anatolian farmers',
        ],
    ),
    'neolithic_europe': Geography(
        'Neolithic Europe',
        'Farming frontiers and village cultures across temperate Europe',
        {'food': 1.2, 'wood': 1.2, 'stone': 1.2, 'hides': 1.1, 'clay': 1.0},
        'temperate',
        6,
        soil_types=['loess', 'black_earth', 'peat'],
        domesticated=[
            'wheat', 'barley', 'peas', 'cattle', 'sheep', 'goats', 'pigs',
        ],
        proto_languages=[
            'Pre-Indo-European (Old European)', 'Proto-Indo-European',
        ],
        ethnicities=[
            'early European farmers', 'Western hunter-gatherers',
        ],
    ),
    'indus_precursors': Geography(
        'Indus Precursors',
        'Early farming settlements that predate the Indus Valley Civilization',
        {'food': 1.3, 'clay': 1.4, 'stone': 1.1, 'hides': 1.0, 'wood': 0.9},
        'arid',
        6,
        soil_types=['alluvial', 'sandy'],
        domesticated=[
            'wheat', 'barley', 'sesame', 'zebu cattle', 'sheep', 'goats',
        ],
        proto_languages=[
            'Proto-Dravidian',
        ],
        ethnicities=[
            'pre-Harappan farming communities',
        ],
    ),
    'mesoamerica': Geography(
        'Mesoamerica',
        'Highland and lowland zones with early maize agriculture',
        {'food': 1.3, 'clay': 1.2, 'stone': 1.1, 'hides': 0.9, 'wood': 1.0},
        'tropical',
        7,
        soil_types=['volcanic', 'laterite', 'clay'],
        domesticated=[
            'maize', 'beans', 'squash', 'chili peppers', 'cacao', 'turkey',
        ],
        proto_languages=[
            'Proto-Mayan', 'Proto-Oto-Manguean',
        ],
        ethnicities=[
            'early Maya communities', 'Oto-Manguean peoples',
        ],
    ),
    'andes': Geography(
        'Andes',
        'High-altitude valleys with terraced farming and camelid herding',
        {'food': 1.1, 'stone': 1.4, 'hides': 1.2, 'wood': 0.8, 'clay': 0.9},
        'cold',
        8,
        soil_types=['mountain', 'volcanic'],
        domesticated=[
            'potato', 'quinoa', 'llama', 'alpaca', 'guinea pig',
        ],
        proto_languages=[
            'Proto-Quechuan', 'Proto-Aymaran',
        ],
        ethnicities=[
            'Andean highland peoples',
        ],
    ),
    'yellow_river': Geography(
        'Yellow River',
        'Loess plains supporting millet farming and early state formation',
        {'food': 1.3, 'clay': 1.2, 'stone': 1.1, 'wood': 0.9, 'hides': 1.0},
        'temperate',
        6,
        soil_types=['loess'],
        domesticated=[
            'millet', 'pigs', 'dogs',
        ],
        proto_languages=[
            'Proto-Sino-Tibetan',
        ],
        ethnicities=[
            'early Sino-Tibetan communities',
        ],
    ),
    'yangtze_river': Geography(
        'Yangtze River',
        'Riverine lowlands with early rice cultivation and wetlands',
        {'food': 1.4, 'clay': 1.1, 'wood': 1.1, 'stone': 0.9, 'hides': 1.0},
        'subtropical',
        6,
        soil_types=['alluvial', 'clay', 'peat'],
        domesticated=[
            'rice', 'pigs', 'water buffalo',
        ],
        proto_languages=[
            'Proto-Austroasiatic', 'Proto-Austronesian', 'Proto-Hmong-Mien', 'Proto-Tai-Kadai',
        ],
        ethnicities=[
            'early rice-farming communities of southern China',
        ],
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
