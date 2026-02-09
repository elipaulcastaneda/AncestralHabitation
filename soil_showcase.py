"""Showcase soil system features"""
from game_engine.game_state import GameState
from game_engine.ui import GameUI
from game_engine.soil import SOIL_TYPES
from game_engine.geography import GEOGRAPHIES

# Start game
game = GameState()
ui = GameUI(game)

print("\n" + "="*60)
print("SOIL SYSTEM DEMONSTRATION".center(60))
print("="*60)

# Show status with soil display
ui.display_game_status()

# Show soil details
print("\n" + "-"*60)
print("SOIL ANALYSIS".center(60))
print("-"*60)
soil = SOIL_TYPES[game.soil_type]
print(f"\nYour settlement has {soil.name}:")
print(f"  Base Fertility: {soil.base_fertility:.1f}")
print(f"  Water Retention: {soil.water_retention:.1f}")
print(f"  Drainage: {soil.drainage:.1f}")
print(f"  Nutrient Depletion Rate: {soil.nutrient_depletion:.1f}")
print(f"  Irrigation Benefit: {soil.irrigation_benefit:.1f}x")

# Simulate building farms
print("\n" + "-"*60)
print("BUILDING FARMS".center(60))
print("-"*60)
game.farms = 3
game.farming_level = 2
print(f"\n✓ Built 3 farms with farming level 2")

# Show production for multiple seasons
print("\n" + "-"*60)
print("SEASONAL PRODUCTION".center(60))
print("-"*60)

for i in range(4):
    food_before = game.resources['food']
    game.advance_turn()
    food_after = game.resources['food']
    from game_engine.geography import get_current_season
    season = get_current_season(game.turn)
    print(f"{season.name:10s}: {food_after - food_before:+5d} food")

# Discover irrigation
print("\n" + "-"*60)
print("IRRIGATION RESEARCH".center(60))
print("-"*60)
game.discover_technology('irrigation')
print("\n✓ Irrigation technology discovered!")
print(f"  Irrigation status: {'✓ Active' if game.has_irrigation else '✗ Inactive'}")

# Show improved production
print("\n" + "-"*60)
print("PRODUCTION WITH IRRIGATION".center(60))
print("-"*60)

for i in range(4):
    food_before = game.resources['food']
    game.advance_turn()
    food_after = game.resources['food']
    from game_engine.geography import get_current_season
    season = get_current_season(game.turn)
    print(f"{season.name:10s}: {food_after - food_before:+5d} food (irrigated)")

# Show final status
print("\n" + "="*60)
print("FINAL STATUS".center(60))
print("="*60)
ui.display_game_status()

print("\n" + "="*60)
print("✓ SOIL SYSTEM FULLY OPERATIONAL".center(60))
print("="*60)
print("""
The soil system now affects your agriculture:
  • Different terrains have different soil types
  • Soil fertility varies from 0.7 to 1.9
  • Irrigation technology boosts production
  • Seasons affect farming output
  • Farming level increases efficiency
""")
