"""
Buildings System
Defines different building types and their requirements
"""

from typing import Dict, Set


class Building:
    """Represents a building type that can be constructed"""
    
    def __init__(
        self,
        name: str,
        description: str,
        cost: Dict[str, int],
        population_required: int,
        tech_prerequisites: Set[str],
        benefit_description: str
    ):
        self.name = name
        self.description = description
        self.cost = cost
        self.population_required = population_required
        self.tech_prerequisites = tech_prerequisites
        self.benefit_description = benefit_description


# Define all building types in the game
BUILDINGS = {
    'farm': Building(
        'Farm',
        'Agricultural field for growing crops',
        {'wood': 50, 'stone': 30, 'food': 100},
        population_required=75,
        tech_prerequisites={'agriculture'},
        benefit_description='+50 food per turn (scales with farming level)'
    ),
    'workshop': Building(
        'Workshop',
        'Specialized area for crafting and tool making',
        {'wood': 100, 'stone': 80},
        population_required=100,
        tech_prerequisites={'woodworking'},
        benefit_description='+20% wood and stone production'
    ),
    'pottery_kiln': Building(
        'Pottery Kiln',
        'Specialized structure for firing clay vessels',
        {'clay': 80, 'stone': 60, 'wood': 40},
        population_required=80,
        tech_prerequisites={'pottery'},
        benefit_description='+30% clay production'
    ),
    'marketplace': Building(
        'Marketplace',
        'Central area for trade and commerce',
        {'wood': 150, 'stone': 100},
        population_required=200,
        tech_prerequisites={'advanced_governance'},
        benefit_description='+10% all resource production, +5 culture points per turn'
    ),
    'temple': Building(
        'Temple',
        'Religious structure for worship and ceremonies',
        {'stone': 300, 'wood': 200},
        population_required=250,
        tech_prerequisites={'megalithic_construction'},
        benefit_description='+10 culture points per turn, +15% governance stability'
    ),
    'granary': Building(
        'Granary',
        'Storage facility for food preservation',
        {'wood': 80, 'stone': 60, 'clay': 40},
        population_required=120,
        tech_prerequisites={'pottery', 'advanced_agriculture'},
        benefit_description='Reduces food waste, +15% food storage capacity'
    ),
    'forge': Building(
        'Forge',
        'Metalworking facility for bronze tools and weapons',
        {'stone': 200, 'wood': 100, 'clay': 50},
        population_required=300,
        tech_prerequisites={'bronze_working'},
        benefit_description='+25% production efficiency, +15 culture points per turn'
    ),
}


def get_available_buildings(
    discovered_techs: Set[str],
    population: int,
    built_buildings: Dict[str, int]
) -> list[Building]:
    """Get list of buildings that can be constructed"""
    available = []
    for building_key, building in BUILDINGS.items():
        # Check if tech prerequisites are met
        if building.tech_prerequisites.issubset(discovered_techs):
            # Check population requirement
            if population >= building.population_required:
                available.append((building_key, building))
    return available
