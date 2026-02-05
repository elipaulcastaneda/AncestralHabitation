"""
Governance System
Defines different governance structures and their effects
"""

from typing import Dict, List


class GovernanceType:
    """Represents a type of governance structure"""
    
    def __init__(self, name: str, display_name: str, description: str,
                 population_requirement: int, stability_modifier: float,
                 production_modifier: float):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.population_requirement = population_requirement
        self.stability_modifier = stability_modifier
        self.production_modifier = production_modifier


# Available governance types
GOVERNANCE_TYPES = {
    'tribal_elder': GovernanceType(
        'tribal_elder',
        'Tribal Elder',
        'Leadership by respected elders based on wisdom and experience',
        population_requirement=0,
        stability_modifier=1.0,
        production_modifier=1.0
    ),
    'chief': GovernanceType(
        'chief',
        'Chieftain',
        'Single strong leader who makes decisions for the tribe',
        population_requirement=100,
        stability_modifier=1.1,
        production_modifier=1.05
    ),
    'council': GovernanceType(
        'council',
        'Council of Leaders',
        'Group of leaders representing different families or clans',
        population_requirement=200,
        stability_modifier=1.2,
        production_modifier=0.95
    ),
    'priest_king': GovernanceType(
        'priest_king',
        'Priest-King',
        'Religious and political authority combined in one leader',
        population_requirement=500,
        stability_modifier=1.3,
        production_modifier=1.1
    ),
    'early_state': GovernanceType(
        'early_state',
        'Early State',
        'Complex bureaucratic system with specialized administrators',
        population_requirement=1000,
        stability_modifier=1.4,
        production_modifier=1.2
    ),
}


def get_available_governance_types(population: int, has_writing: bool) -> List[GovernanceType]:
    """Get list of governance types available based on population and tech"""
    available = []
    for gov_type in GOVERNANCE_TYPES.values():
        if population >= gov_type.population_requirement:
            # Early state requires writing
            if gov_type.name == 'early_state' and not has_writing:
                continue
            available.append(gov_type)
    return available
