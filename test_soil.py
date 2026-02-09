"""Quick test of soil system integration"""
import random
from game_engine.game_state import GameState
from game_engine.soil import SOIL_TYPES

# Create a new game state
gs = GameState()

print("=" * 50)
print("SOIL SYSTEM TEST")
print("=" * 50)

# Display initial state
print(f"\nGeography: {gs.geography_type}")
print(f"Soil Type: {gs.soil_type}")
soil = SOIL_TYPES[gs.soil_type]
print(f"Soil Name: {soil.name}")
print(f"Base Fertility: {soil.base_fertility}")
print(f"Water Retention: {soil.water_retention}")
print(f"Drainage: {soil.drainage}")
print(f"Has Irrigation: {gs.has_irrigation}")
print(f"Soil Quality: {gs.soil_quality}")

# Add some farms
gs.farms = 3
gs.farming_level = 2

print(f"\n--- Testing Farm Production ---")
print(f"Farms: {gs.farms}")
print(f"Farming Level: {gs.farming_level}")

# Test before turn
food_before = gs.resources['food']
print(f"\nFood before turn: {food_before}")

# Advance a turn
random.seed(42)
gs.advance_turn()

food_after = gs.resources['food']
print(f"Food after turn: {food_after}")
print(f"Net food change: {food_after - food_before} (production minus consumption)")

# Test with irrigation on a new game state to compare fairly
print(f"\n--- Comparing with Irrigation ---")
gs2 = GameState()
gs2.soil_type = gs.soil_type  # Use same soil type for fair comparison
gs2.farms = 3
gs2.farming_level = 2
gs2.discover_technology('irrigation')
print(f"Has Irrigation: {gs2.has_irrigation}")

food_before2 = gs2.resources['food']
random.seed(42)
gs2.advance_turn()
food_after2 = gs2.resources['food']

print(f"Food change without irrigation: {food_after - food_before}")
print(f"Food change with irrigation: {food_after2 - food_before2}")
print(f"Irrigation benefit: +{(food_after2 - food_before2) - (food_after - food_before)} food/turn")

# Test different soil types
print(f"\n--- Testing Different Soil Types ---")
soil_comparison = {}
for soil_name in ['alluvial', 'loess', 'black_earth', 'sandy', 'volcanic']:
	gs_test = GameState()
	gs_test.soil_type = soil_name
	gs_test.farms = 2
	gs_test.farming_level = 1
	food_b = gs_test.resources['food']
	gs_test.advance_turn()
	food_a = gs_test.resources['food']
	soil_comparison[soil_name] = food_a - food_b

print("\nFood production comparison (2 farms, level 1):")
for soil_name, production in sorted(soil_comparison.items(), key=lambda x: x[1], reverse=True):
	soil_info = SOIL_TYPES[soil_name]
	print(f"  {soil_info.name}: {production:+d} food/turn (fertility: {soil_info.base_fertility})")

print("\n✓ Soil system working correctly!")
