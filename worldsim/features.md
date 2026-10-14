# Features

## Implemented foundation

- Persistent UUID identity and deterministic content fingerprints.
- Generic ID-keyed registries with value iteration and keyed lookup.
- Atlas registries for languages, realms, and semantic concepts.
- Language phonemes, words, lexical senses, provenance, and loan behavior.
- Language-independent propositions and communicative intents.
- Chunked square tile map with negative-coordinate support.
- Shared terrain definitions using portable asset keys.
- Per-tile elevation, water, moisture, fertility, and placed-object references.
- Structure/resource/object definitions with multi-tile footprints.
- Terrain tag, elevation, slope, altitude, and vertical collision checks.
- Object placement and removal with quantity and condition state.
- Deterministic seeded fractal value-noise terrain generation.
- Isometric projection and inverse projection math.
- One-hour world clock advancement.

## Intended simulation features

- Biological agents with metabolism, respiration, digestion, immunity, sleep,
  health, aging, reproduction, needs, and wants.
- Jobs, production chains, inventories, trade, prices, households, and wealth.
- Directed relationships, memories, beliefs, skills, personality, and utility AI.
- Settlements, realms, cultures, migration, conflict, and diplomacy.
- Per-agent language knowledge, communication, misunderstanding, learning,
  dialect formation, borrowing, and language evolution.
- Weather, seasons, hydrology, vegetation growth, farming, and renewable and
  finite resource deposits.
- Construction, ownership, multi-level structures, roads, bridges, and paths.
- Save/load, deterministic replay, simulation inspection, and debugging tools.

## Viewer direction

The planned viewer presents the square simulation grid as diagonal isometric
diamonds. Terrain and simulation logic do not depend on a graphics framework.
The rendering adapter will handle:

- camera pan and zoom;
- visible-chunk selection;
- elevation-aware draw ordering;
- terrain and object sprite caching;
- tile and object picking;
- overlays for resources, ownership, jobs, paths, and agent state;
- pause, speed control, and inspection panels.
