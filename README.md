# Ancestral Habitation

A strategy video game that simulates the building of a tribe and Neolithic-era culture, covering the period from 8000 BC to the start of the Iron Age (approximately 1200 BC).

## Overview

Guide your tribe through the dawn of civilization! Make strategic decisions about:

- **Agriculture Development**: Transition from hunting-gathering to farming
- **Technology Research**: Discover pottery, weaving, metalworking, writing, and more
- **Migration**: Move your tribe to different geographical locations
- **Governance**: Evolve from tribal elders to complex state systems
- **Geography Adaptation**: Thrive in river valleys, plains, forests, coasts, and more
- **Resource Management**: Balance food, wood, stone, clay, and other resources
- **Population Growth**: Manage your growing population through the ages

## Features

### Time Period: 8000 BC - 1200 BC
Experience the full span of the Neolithic period through the beginning of the Bronze Age.

### Technology Tree
- **Early Neolithic** (8000-6000 BC): Agriculture, Animal Husbandry, Pottery, Weaving
- **Middle Neolithic** (6000-4000 BC): Advanced Agriculture, Irrigation, Woodworking
- **Late Neolithic** (4000-3000 BC): Megalithic Construction, Copper Working, Proto-Writing, The Wheel
- **Chalcolithic/Copper Age** (3000-2000 BC): Writing Systems, Bronze Working, Advanced Governance

### Geographic Diversity
Choose from various locations, each with unique challenges and benefits:
- River Valleys (fertile, ideal for early agriculture)
- Coastal Regions (fishing and trade opportunities)
- Open Plains (herding and farming)
- Dense Forests (abundant wood and game)
- Hilly Regions (stone deposits)
- Mountain Foothills (mineral resources)
- Desert Edge (water management challenges)

### Governance Evolution
Progress through different governance structures:
- Tribal Elder (basic tribal leadership)
- Chieftain (strong single leader)
- Council of Leaders (representative system)
- Priest-King (religious and political authority)
- Early State (bureaucratic system - requires writing)

### Writing System
Develop proto-writing and eventually full writing systems, unlocking advanced governance and cultural achievements.

## How to Play

### Requirements
- Python 3.7 or higher

### Running the Game

#### On Linux/Mac:
```bash
./run_game.sh
```

#### On Windows or directly with Python:
```bash
python3 game.py
```

### Game Controls

The game is text-based and menu-driven. Each turn you can:

1. **Advance to next year** - Progress time and see your civilization develop
2. **Build farm** - Construct farms to increase food production (requires Agriculture technology)
3. **Research technology** - Discover new technologies that unlock capabilities
4. **Migrate to new location** - Move your tribe to different geography (risky but potentially rewarding)
5. **Change governance** - Evolve your social and political structures
6. **View technologies** - See what you've discovered and what's available
7. **View available locations** - Learn about different geographical locations
8. **View statistics** - Check detailed information about your tribe
9. **Quit game** - End the game and view final statistics

### Strategy Tips

1. **Start with Agriculture**: Research agriculture early to enable farm building and food security
2. **Balance Resources**: Don't let food stores run too low - starvation reduces population
3. **Plan Your Tech Path**: Technologies have prerequisites - plan your research path carefully
4. **Consider Migration**: Different locations offer different resource bonuses
5. **Grow Before Governing**: More complex governance requires larger populations
6. **Culture Matters**: Technologies grant culture points that show your civilization's advancement
7. **Watch the Calendar**: The Bronze Age begins around 3000 BC - be ready!

## Game Mechanics

### Population
- Grows naturally each turn based on birth rate
- Affected by food availability (starvation causes deaths)
- Larger populations enable more advanced governance

### Resources
- **Food**: Essential for survival, produced by gathering and farming
- **Wood**: Used for construction and technology
- **Stone**: Required for advanced buildings and tools
- **Clay**: Needed for pottery and writing
- **Hides**: From hunting, used in various technologies

### Seasons
- Spring: Increased food production (20% bonus)
- Summer: Peak food production (30% bonus)
- Autumn: Good harvest period (10% bonus)
- Winter: Reduced food production (40% penalty), higher chance of harsh events

### Random Events
The game includes random events such as:
- Good harvests
- Harsh winters
- Wildlife discoveries
- Disease outbreaks

## Development

### Project Structure
```
AncestralHabitation/
├── game.py                 # Main game entry point
├── run_game.sh            # Convenience script to run the game
├── README.md              # This file
└── game_engine/           # Game engine modules
    ├── __init__.py
    ├── game_state.py      # Core game state management
    ├── technologies.py    # Technology definitions and system
    ├── geography.py       # Geography and terrain system
    ├── governance.py      # Governance structures
    └── ui.py              # User interface and game loop
```

## License

This project is open source and available for educational and entertainment purposes.

## Credits

Developed as a historical strategy simulation of the Neolithic period and the dawn of human civilization.
