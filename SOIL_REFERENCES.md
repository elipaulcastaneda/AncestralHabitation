# Soil calibration references

This project uses normalized soil stats (fertility, water retention, drainage, depletion) derived
from real-world soil properties. Values are scaled to game-friendly ranges while preserving
relative differences described in the sources below.

## References
- Soil texture and water-holding capacity are linked: fine-textured soils (more clay/silt) generally
  retain more water; sandy soils have lower water retention and faster drainage.
  https://en.wikipedia.org/wiki/Soil_texture
- Chernozem (black earth) has high humus content and is very fertile with strong moisture storage.
  Humus is reported around 4% to 16% in chernozem.
  https://en.wikipedia.org/wiki/Chernozem
- Andosols (volcanic soils) can be highly fertile and support intensive cropping in many regions.
  https://en.wikipedia.org/wiki/Andosol
- Laterite forms under intense leaching in wet tropics and is less fertile without amendments,
  though it can respond well to management.
  https://en.wikipedia.org/wiki/Laterite
- Peat soils are organic and water-retentive due to persistent wet conditions.
  https://en.wikipedia.org/wiki/Peat
- Alluvial deposits are young river sediments; in floodplains they are often productive for agriculture.
  https://en.wikipedia.org/wiki/Alluvium

## How the game scales real-world concepts
- Base fertility is normalized so that very fertile soils (chernozem, volcanic) are above 1.0
  and low-fertility soils (sandy, laterite, mountain) are below 1.0.
- Water retention and drainage values follow texture-driven behavior:
  clay/peat higher retention, sand higher drainage, loess and alluvial near balanced.
- Nutrient depletion is higher in soils prone to leaching/erosion (laterite, sandy, mountain).
- Irrigation benefit is higher for water-limited soils (sandy, mountain) and lower where
  waterlogging risk is higher (peat, clay).

These scalings aim to stay faithful to the qualitative ranges from the sources while keeping
turn-by-turn gameplay stable.
