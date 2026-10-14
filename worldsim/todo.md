# TODO

## Next playable slice

- [ ] Choose the first viewer backend after a small rendering benchmark.
- [ ] Open a window and implement camera pan, zoom, and resize handling.
- [ ] Render one generated region with isometric terrain sprites.
- [ ] Cull chunks and tiles outside the camera viewport.
- [ ] Implement elevation-aware terrain and object draw ordering.
- [ ] Convert mouse coordinates into candidate tiles and perform diamond hit
      testing with elevation correction.
- [ ] Add tile and placed-object inspection overlays.
- [ ] Add pause, single-hour step, and simulation-speed controls.
- [ ] Add realm painter GUI for drag-and-drop placement of units and objects
- [ ] Add realm configurator GUI for live experimentation with world generation
      settings in-viewer

## Tile map and assets

- [ ] Decide the production chunk size after measuring generation and rendering.
- [ ] Add chunk load/unload hooks and a bounded in-memory chunk cache.
- [ ] Add asset loading, validation, placeholders, and decoded-image caching.
- [ ] Define initial terrain assets: deep water, water, sand, grass, rock, snow.
- [ ] Add terrain transitions or autotiling between neighboring terrain types.
- [ ] Add tile serialization with a schema version.
- [ ] Replace object lookup scans with spatial indexes if profiling requires it.
- [ ] Define rules for bridges, floors, roofs, underground objects, and stacked
      objects at different altitudes.

## Procedural generation

- [ ] Add moisture and temperature noise fields.
- [ ] Select biomes using elevation, moisture, latitude, and temperature.
- [ ] Add coast shaping, rivers, lakes, erosion, and drainage.
- [ ] Place vegetation, stone, ore, wildlife habitat, and fertile soil.
- [ ] Generate spawn regions with accessible water, food, and buildable land.
- [ ] Add deterministic generation tests and seed snapshots.

## Simulation integration

- [ ] Add agents and structures to world registries.
- [ ] Add pathfinding with terrain and structure movement costs.
- [ ] Add occupancy rules for agents versus placed objects.
- [ ] Add resource harvesting and depletion.
- [ ] Add construction progress, condition, damage, and repair.
- [ ] Add realm claims without storing realm ownership directly on every tile.
- [ ] Define active simulation levels for visible, nearby, and distant regions.

## Language system

- [ ] Import the curated Gekapiso data into `v1` registries.
- [ ] Add constructions that realize propositions as word sequences.
- [ ] Add per-agent vocabulary and language proficiency.
- [ ] Implement the first request-for-water conversation.
- [ ] Resume language learning and historical evolution after the viewer slice.

## Engineering

- [ ] Add a project configuration and automated test runner.
- [ ] Add static type checking as a repeatable command.
- [ ] Add formatting and linting configuration.
- [ ] Add save-file migrations and compatibility tests.
- [ ] Profile memory per generated tile, chunk, and placed object.
