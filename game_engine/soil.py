"""
Soil System
Defines soil types and their effects on agriculture
"""

from typing import Dict
import random


class SoilType:
    """Represents a soil type with agricultural characteristics"""
    
    def __init__(
        self,
        name: str,
        description: str,
        base_fertility: float,  # 0.6 to 1.4 (scaled from real-world fertility differences)
        water_retention: float,  # 0.6 to 1.3 (texture-driven available water)
        drainage: float,  # 0.6 to 1.3 (aeration and excess water removal)
        nutrient_depletion: float,  # 0.12 to 0.35 (leaching/erosion tendency)
        irrigation_benefit: float,  # 0.9 to 1.4 (irrigation impact on water-limited soils)
    ):
        self.name = name
        self.description = description
        self.base_fertility = base_fertility
        self.water_retention = water_retention
        self.drainage = drainage
        self.nutrient_depletion = nutrient_depletion
        self.irrigation_benefit = irrigation_benefit


# Available soil types
SOIL_TYPES = {
    'alluvial': SoilType(
        'Alluvial Soil',
        'Rich, dark soil deposited by rivers - excellent for farming',
        base_fertility=1.25,
        water_retention=1.1,
        drainage=1.05,
        nutrient_depletion=0.16,
        irrigation_benefit=1.1
    ),
    'loess': SoilType(
        'Loess',
        'Fine, windblown silt - fertile but prone to erosion',
        base_fertility=1.15,
        water_retention=1.0,
        drainage=1.05,
        nutrient_depletion=0.22,
        irrigation_benefit=1.15
    ),
    'black_earth': SoilType(
        'Black Earth (Chernozem)',
        'Dark, humus-rich soil - ideal for grain cultivation',
        base_fertility=1.3,
        water_retention=1.2,
        drainage=1.0,
        nutrient_depletion=0.12,
        irrigation_benefit=1.05
    ),
    'clay': SoilType(
        'Clay Soil',
        'Heavy soil that retains water but is hard to work',
        base_fertility=1.0,
        water_retention=1.25,
        drainage=0.7,
        nutrient_depletion=0.2,
        irrigation_benefit=0.9
    ),
    'sandy': SoilType(
        'Sandy Soil',
        'Light, well-draining soil that needs frequent watering',
        base_fertility=0.7,
        water_retention=0.65,
        drainage=1.25,
        nutrient_depletion=0.28,
        irrigation_benefit=1.35
    ),
    'volcanic': SoilType(
        'Volcanic Soil',
        'Mineral-rich soil from volcanic activity - highly fertile',
        base_fertility=1.35,
        water_retention=1.15,
        drainage=1.05,
        nutrient_depletion=0.14,
        irrigation_benefit=1.1
    ),
    'laterite': SoilType(
        'Laterite',
        'Iron-rich tropical soil - fertile when vegetated but degrades quickly',
        base_fertility=0.85,
        water_retention=0.9,
        drainage=1.15,
        nutrient_depletion=0.35,
        irrigation_benefit=1.2
    ),
    'limestone': SoilType(
        'Limestone Soil',
        'Rocky, alkaline soil - challenging but suitable for certain crops',
        base_fertility=0.9,
        water_retention=0.85,
        drainage=1.15,
        nutrient_depletion=0.24,
        irrigation_benefit=1.2
    ),
    'peat': SoilType(
        'Peat Soil',
        'Organic-rich wetland soil - acidic but very fertile when drained',
        base_fertility=1.2,
        water_retention=1.3,
        drainage=0.65,
        nutrient_depletion=0.18,
        irrigation_benefit=0.9
    ),
    'mountain': SoilType(
        'Mountain Soil',
        'Thin, rocky soil with limited depth - requires terracing',
        base_fertility=0.75,
        water_retention=0.7,
        drainage=1.2,
        nutrient_depletion=0.3,
        irrigation_benefit=1.25
    ),
}


# Map geography types to typical soil types
GEOGRAPHY_SOIL_MAP = {
    'river_valley': ['alluvial', 'clay'],
    'coastal': ['sandy', 'alluvial'],
    'plains': ['black_earth', 'loess'],
    'forest': ['peat', 'clay'],
    'hills': ['limestone', 'clay'],
    'mountains': ['mountain', 'volcanic'],
    'desert_edge': ['sandy', 'limestone'],
    'fertile_crescent': ['alluvial', 'loess'],
    'neolithic_europe': ['black_earth', 'loess', 'clay'],
    'indus_precursors': ['alluvial', 'sandy'],
    'mesoamerica': ['volcanic', 'laterite'],
    'andes': ['mountain', 'volcanic'],
    'yellow_river': ['loess', 'alluvial'],
    'yangtze_river': ['alluvial', 'clay', 'peat'],
}


def calculate_soil_productivity(
    soil_type: str,
    irrigation_level: int,
    climate: str,
    season_modifier: float,
    farming_level: int
) -> float:
    """
    Calculate the agricultural productivity based on multiple factors
    
    Args:
        soil_type: The type of soil
        irrigation_level: Irrigation technology level (0-3)
        climate: The climate type (affects water availability)
        season_modifier: Current season's effect on farming (0.6 to 1.3)
        farming_level: The farming skill level (0-5)
    
    Returns:
        Productivity multiplier for farm output
    """
    if soil_type not in SOIL_TYPES:
        return 1.0
    
    soil = SOIL_TYPES[soil_type]
    
    # Start with base fertility
    productivity = soil.base_fertility
    
    # Climate effects on water availability
    climate_water = {
        'temperate': 1.0,
        'subtropical': 1.1,
        'tropical': 1.2,
        'arid': 0.6,
        'hot': 0.7,
        'cold': 0.8,
    }
    water_factor = climate_water.get(climate, 1.0)
    
    # Apply water retention and drainage
    # Water availability scales with retention; oxygen availability scales with drainage.
    water_availability = soil.water_retention * water_factor
    oxygen_availability = soil.drainage
    water_balance = min(1.25, water_availability) * min(1.15, oxygen_availability)
    productivity *= water_balance
    
    # Irrigation benefit (helps especially in dry climates or poor water retention)
    if irrigation_level > 0:
        # Irrigation primarily boosts water availability rather than fertility directly.
        irrigation_boost = 0.1 * irrigation_level * soil.irrigation_benefit
        if climate in ['arid', 'hot']:
            irrigation_boost *= 1.3
        productivity *= (1.0 + irrigation_boost)
    
    # Apply seasonal modifier
    productivity *= season_modifier
    
    # Farming level reduces nutrient depletion impact
    depletion_resistance = 1.0 + (farming_level * 0.1)
    depletion_impact = max(0.5, 1.0 - (soil.nutrient_depletion / depletion_resistance))
    productivity *= depletion_impact
    
    # Farming level general bonus
    skill_bonus = 1.0 + (farming_level * 0.15)
    productivity *= skill_bonus
    
    return productivity


def get_geography_soil(geography_type: str) -> str:
    """Get a random soil type for the given geography"""
    available_soils = GEOGRAPHY_SOIL_MAP.get(geography_type, ['loess'])
    return random.choice(available_soils)


def get_soil_degradation_rate(soil_type: str, has_crop_rotation: bool) -> float:
    """
    Calculate how much soil quality degrades over time
    
    Returns:
        Degradation rate per 100 turns (0.0 to 1.0)
    """
    if soil_type not in SOIL_TYPES:
        return 0.1
    
    soil = SOIL_TYPES[soil_type]
    base_degradation = soil.nutrient_depletion
    
    # Advanced agriculture (crop rotation) reduces degradation significantly
    if has_crop_rotation:
        base_degradation *= 0.4
    
    return base_degradation
