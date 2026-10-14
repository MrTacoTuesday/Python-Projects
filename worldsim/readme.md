# WorldSim

WorldSim is an agent-based world simulation built around an hourly simulation
tick. Its intended scope includes terrain, settlements, economics, biological
needs, jobs, relationships, culture, language, and long-term social change.

The current `v1` package is an experimental foundation. Its APIs may change as
the first playable viewer and simulation loop are developed.

## Current architecture

The simulation uses a square logical grid rendered through an isometric
(diagonal) projection. Keeping projection separate from grid topology makes
pathfinding, neighborhood queries, procedural generation, and save files
independent of the eventual rendering library.

```text
World
├── Atlas
│   ├── languages
│   ├── realms
│   └── semantic concepts
└── TileMap
    ├── shared terrain definitions
    ├── shared object definitions
    ├── lazily created tile chunks
    └── placed structures/resources/objects
```

Important modules:

- `v1/assets.py`: portable asset keys and path resolution at the viewer edge.
- `v1/tiles.py`: coordinates, chunks, terrain, tile state, and object placement.
- `v1/generation.py`: deterministic seeded terrain generation.
- `v1/viewer.py`: isometric world-to-screen projection math.
- `v1/world.py`: the world, atlas, and realm containers.
- `v1/language.py`: phonology, words, senses, and language borrowing.
- `v1/semantics.py`: concepts, propositions, and communicative intent.

## Assets

Simulation objects store asset names such as `grass` or `oak_tree`, never
machine-specific file paths. `AssetCatalog` resolves those names for a viewer:

```python
from pathlib import Path
from worldsim.v1 import AssetCatalog

assets = AssetCatalog(Path("assets"))
grass_image = assets.tile_path("grass")
# assets/tiles/grass.png
```

Image loading and caching belong in the viewer. Reading an ordinary tile never
performs hidden filesystem access.

## Generating a small map

```python
from worldsim.v1 import (
    GenerationConfig,
    ProceduralGenerator,
    TerrainBand,
    TerrainDefinition,
    TileMap,
    TilePosition,
    TileTag,
)

tile_map = TileMap()
tile_map.register_terrain(
    TerrainDefinition(
        key="grass",
        asset_key="grass",
        tags=frozenset({TileTag.LAND, TileTag.SOIL, TileTag.BUILDABLE}),
    )
)

# A real generator configuration must provide bands whose terrain keys have
# all been registered on the tile map.
generator = ProceduralGenerator(
    GenerationConfig(
        seed=42,
        terrain_bands=(TerrainBand(float("inf"), "grass"),),
    )
)
generator.generate_region(
    tile_map,
    start=TilePosition(0, 0),
    width=32,
    depth=32,
)
```

## Position and elevation

`TilePosition` identifies an integer grid cell. `GridPosition` adds normalized
horizontal offsets and an elevation in meters. Movement normalizes across tile
boundaries automatically through `GridPosition.moved()`.

Terrain elevation is stored in `TileData`. An object's `altitude_m` is its
height above the local terrain. The isometric projection combines world
position and elevation into screen coordinates.

## Placed objects

Structures, natural resources, vegetation, and decorations use a shared
placement model. An `ObjectDefinition` describes:

- its asset and object kind;
- its multi-tile footprint;
- permitted placement layers;
- required and forbidden terrain tags;
- ground elevation and slope limits;
- altitude range, height, and collision behavior.

`PlacedObject` contains mutable instance state such as quantity and condition.
This permits mines, trees, crops, buildings, bridges, and airborne objects to
share placement infrastructure while developing specialized systems later.

## Compatibility

`worldsim.abstract.abstract_4` re-exports the `worldsim.v1` API for earlier
experiments. New code should import from `worldsim.v1`.
