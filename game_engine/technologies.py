"""
Technology System
Defines all available technologies and their requirements
"""

from typing import Dict, List, Set


class Technology:
    """Represents a technology that can be researched"""
    
    def __init__(self, name: str, description: str, cost: Dict[str, int],
                 prerequisites: Set[str], era: str, population_required: int = 0):
        self.name = name
        self.description = description
        self.cost = cost
        self.prerequisites = prerequisites
        self.era = era
        self.population_required = population_required


# Define all technologies in the game
TECHNOLOGIES = {
    # Early Neolithic (8000-6000 BC)
    'agriculture': Technology(
        'agriculture',
        'Domestication of plants and beginning of farming',
        {'food': 100, 'wood': 50},
        {'gathering'},
        'early_neolithic',
        population_required=50
    ),
    'animal_husbandry': Technology(
        'animal_husbandry',
        'Domestication of animals for food and labor',
        {'food': 150, 'hides': 30},
        {'hunting'},
        'early_neolithic',
        population_required=60
    ),
    'pottery': Technology(
        'pottery',
        'Creation of ceramic vessels for storage',
        {'clay': 50, 'wood': 30},
        {'fire'},
        'early_neolithic',
        population_required=40
    ),
    'weaving': Technology(
        'weaving',
        'Creation of textiles from plant fibers',
        {'food': 50},
        {'gathering'},
        'early_neolithic',
        population_required=40
    ),
    
    # Middle Neolithic (6000-4000 BC)
    'advanced_agriculture': Technology(
        'advanced_agriculture',
        'Improved farming techniques and crop rotation',
        {'food': 200, 'wood': 100},
        {'agriculture'},
        'middle_neolithic',
        population_required=100
    ),
    'irrigation': Technology(
        'irrigation',
        'Control of water for farming',
        {'wood': 150, 'stone': 100},
        {'agriculture'},
        'middle_neolithic',
        population_required=150
    ),
    'woodworking': Technology(
        'woodworking',
        'Advanced wood tools and construction',
        {'wood': 100, 'stone': 50},
        {'stone_tools'},
        'middle_neolithic',
        population_required=80
    ),
    'advanced_foraging': Technology(
        'advanced_foraging',
        'Better knowledge of wild plants and gathering',
        {'food': 100},
        {'gathering'},
        'middle_neolithic',
        population_required=70
    ),
    
    # Late Neolithic (4000-3000 BC)
    'megalithic_construction': Technology(
        'megalithic_construction',
        'Building large stone monuments',
        {'stone': 500, 'wood': 200},
        {'woodworking'},
        'late_neolithic',
        population_required=300
    ),
    'copper_working': Technology(
        'copper_working',
        'First metalworking - copper tools',
        {'stone': 200, 'wood': 100},
        {'fire', 'pottery'},
        'late_neolithic',
        population_required=200
    ),
    'proto_writing': Technology(
        'proto_writing',
        'Early symbolic communication systems',
        {'clay': 100},
        {'pottery'},
        'late_neolithic',
        population_required=250
    ),
    'wheel': Technology(
        'wheel',
        'Invention of the wheel for transport',
        {'wood': 150, 'stone': 50},
        {'woodworking'},
        'late_neolithic',
        population_required=180
    ),
    
    # Chalcolithic / Copper Age (3000-2000 BC)
    'writing': Technology(
        'writing',
        'Development of true writing systems',
        {'clay': 200},
        {'proto_writing'},
        'chalcolithic',
        population_required=500
    ),
    'bronze_working': Technology(
        'bronze_working',
        'Alloying copper with tin to create bronze',
        {'stone': 300},
        {'copper_working'},
        'chalcolithic',
        population_required=400
    ),
    'advanced_governance': Technology(
        'advanced_governance',
        'Complex administrative systems',
        {'food': 500},
        {'proto_writing'},
        'chalcolithic',
        population_required=600
    ),
}


def get_available_technologies(discovered_techs: Set[str], population: int = 0) -> List[Technology]:
    """Get list of technologies that can be researched"""
    available = []
    for tech in TECHNOLOGIES.values():
        if tech.name not in discovered_techs:
            # Check if all prerequisites are met
            if tech.prerequisites.issubset(discovered_techs):
                # Check population requirement (0 means show all, for viewing)
                if population == 0 or population >= tech.population_required:
                    available.append(tech)
    return available
