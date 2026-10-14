from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto
from math import floor
from typing import TypeAlias, overload
from uuid import uuid4

from .assets import AssetKey, validate_asset_key
from .ids import IDSet, ObjectID
from .registry import Registry


TerrainKey: TypeAlias = str
ObjectDefinitionKey: TypeAlias = str


class TileTag(StrEnum):
    LAND = auto()
    WATER = auto()
    SOIL = auto()
    ROCK = auto()
    BUILDABLE = auto()
    FARMABLE = auto()


class ObjectKind(StrEnum):
    STRUCTURE = auto()
    RESOURCE = auto()
    VEGETATION = auto()
    DECORATION = auto()


class PlacementLayer(StrEnum):
    UNDERGROUND = auto()
    SURFACE = auto()
    STRUCTURE = auto()
    CANOPY = auto()
    AIR = auto()


@dataclass(frozen=True, slots=True, order=True)
class TilePosition:
    x: int = 0
    z: int = 0

    def offset(self, dx: int = 0, dz: int = 0) -> TilePosition:
        return TilePosition(self.x + dx, self.z + dz)

    def neighbors(self, *, include_diagonals: bool = True) -> tuple[TilePosition, ...]:
        cardinal = (
            self.offset(dx=-1),
            self.offset(dx=1),
            self.offset(dz=-1),
            self.offset(dz=1),
        )
        if not include_diagonals:
            return cardinal
        return cardinal + (
            self.offset(-1, -1),
            self.offset(-1, 1),
            self.offset(1, -1),
            self.offset(1, 1),
        )

    def __add__(self, offset: TileOffset) -> TilePosition:
        return self.offset(offset.dx,offset.dz)

    @overload
    def __sub__(self, other: TilePosition) -> TileOffset: ...

    @overload
    def __sub__(self, other: TileOffset) -> TilePosition: ...

    def __sub__(self, other: TilePosition | TileOffset) -> TileOffset | TilePosition:
        if isinstance(other, TilePosition):
            return TileOffset(self.x-other.x,self.z-other.z)
        return self.offset(-other.dx, -other.dz)


@dataclass(frozen=True, slots=True)
class TileOffset:
    dx: int = 0
    dz: int = 0

    def __neg__(self) -> TileOffset:
        return TileOffset(-self.dx, -self.dz)

    def __mul__(self, other: int) -> TileOffset:
        return TileOffset(self.dx*other,self.dz*other)

    def __floordiv__(self, other: int) -> TileOffset:
        return TileOffset(self.dx//other, self.dz//other)


@dataclass(frozen=True, slots=True)
class GridPosition:
    tile: TilePosition = field(default_factory=TilePosition)
    x_offset: float = 0.5
    z_offset: float = 0.5
    elevation_m: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.x_offset < 1.0:
            raise ValueError("x_offset must be between 0.0 and <1.0")
        if not 0.0 <= self.z_offset < 1.0:
            raise ValueError("z_offset must be between 0.0 and <1.0")

    @classmethod
    def from_world(
        cls, world_x: float, world_z: float, elevation_m: float = 0.0
    ) -> GridPosition:
        tile_x = floor(world_x)
        tile_z = floor(world_z)
        return cls(
            tile=TilePosition(tile_x, tile_z),
            x_offset=world_x - tile_x,
            z_offset=world_z - tile_z,
            elevation_m=elevation_m,
        )

    @property
    def world_x(self) -> float:
        return self.tile.x + self.x_offset

    @property
    def world_z(self) -> float:
        return self.tile.z + self.z_offset

    def moved(self, dx: float = 0.0, dz: float = 0.0, dy: float = 0.0) -> GridPosition:
        return GridPosition.from_world(
            self.world_x + dx,
            self.world_z + dz,
            self.elevation_m + dy,
        )


@dataclass(frozen=True, slots=True)
class TerrainDefinition:
    key: TerrainKey
    asset_key: AssetKey
    tags: frozenset[TileTag] = field(default_factory=frozenset)
    movement_cost: float = 1.0

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("Terrain key cannot be empty")
        validate_asset_key(self.asset_key)
        if self.movement_cost <= 0.0:
            raise ValueError("movement_cost must be greater than zero")


@dataclass(frozen=True, slots=True)
class TileData:
    terrain_key: TerrainKey
    elevation_m: float = 0.0


@dataclass(slots=True)
class TileState:
    water_depth_m: float = 0.0
    soil_moisture: float = 0.0
    fertility: float = 1.0
    object_ids: IDSet[ObjectID] = field(default_factory=IDSet[ObjectID])

    def __post_init__(self) -> None:
        if self.water_depth_m < 0.0:
            raise ValueError("water_depth_m cannot be negative")
        if not 0.0 <= self.soil_moisture <= 1.0:
            raise ValueError("soil_moisture must be between 0.0 and 1.0")
        if not 0.0 <= self.fertility <= 1.0:
            raise ValueError("fertility must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class ObjectDefinition:
    key: ObjectDefinitionKey
    kind: ObjectKind
    asset_key: AssetKey
    footprint: tuple[TileOffset, ...] = (TileOffset(),)
    allowed_layers: frozenset[PlacementLayer] = field(
        default_factory=lambda: frozenset({PlacementLayer.SURFACE})
    )
    required_tile_tags: frozenset[TileTag] = field(default_factory=frozenset)
    forbidden_tile_tags: frozenset[TileTag] = field(default_factory=frozenset)
    min_ground_elevation_m: float | None = None
    max_ground_elevation_m: float | None = None
    min_altitude_m: float = 0.0
    max_altitude_m: float = 0.0
    height_m: float = 1.0
    max_footprint_slope_m: float = 0.0
    blocks_placement: bool = True

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("Object definition key cannot be empty")
        validate_asset_key(self.asset_key)
        if not self.footprint:
            raise ValueError("Object footprint cannot be empty")
        if not self.allowed_layers:
            raise ValueError("Object must allow at least one placement layer")
        if self.min_altitude_m > self.max_altitude_m:
            raise ValueError("min_altitude_m cannot exceed max_altitude_m")
        if self.height_m < 0.0:
            raise ValueError("height_m cannot be negative")
        if self.max_footprint_slope_m < 0.0:
            raise ValueError("max_footprint_slope_m cannot be negative")

    def permits(
        self,
        terrain: TerrainDefinition,
        ground_elevation_m: float,
        altitude_m: float,
        layer: PlacementLayer,
    ) -> bool:
        if layer not in self.allowed_layers:
            return False
        if not self.required_tile_tags <= terrain.tags:
            return False
        if self.forbidden_tile_tags & terrain.tags:
            return False
        if (
            self.min_ground_elevation_m is not None
            and ground_elevation_m < self.min_ground_elevation_m
        ):
            return False
        if (
            self.max_ground_elevation_m is not None
            and ground_elevation_m > self.max_ground_elevation_m
        ):
            return False
        return self.min_altitude_m <= altitude_m <= self.max_altitude_m


@dataclass(slots=True)
class PlacedObject:
    definition_key: ObjectDefinitionKey
    anchor: TilePosition
    altitude_m: float = 0.0
    layer: PlacementLayer = PlacementLayer.SURFACE
    quantity: float | None = None
    condition: float = 1.0
    id: ObjectID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.quantity is not None and self.quantity < 0.0:
            raise ValueError("quantity cannot be negative")
        if not 0.0 <= self.condition <= 1.0:
            raise ValueError("condition must be between 0.0 and 1.0")


class PlacementError(ValueError):
    pass


@dataclass(frozen=True, slots=True, order=True)
class ChunkPosition:
    x: int
    z: int


@dataclass(slots=True)
class TileChunk:
    position: ChunkPosition
    size: int
    tiles: list[TileData | None] = field(init=False)
    states: list[TileState | None] = field(init=False)

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise ValueError("Chunk size must be greater than zero")
        cell_count = self.size * self.size
        self.tiles = [None] * cell_count
        self.states = [None] * cell_count

    def _index(self, local_x: int, local_z: int) -> int:
        if not 0 <= local_x < self.size or not 0 <= local_z < self.size:
            raise IndexError((local_x, local_z))
        return local_z * self.size + local_x

    def set(self, local_x: int, local_z: int, tile: TileData) -> None:
        index = self._index(local_x, local_z)
        self.tiles[index] = tile
        if self.states[index] is None:
            self.states[index] = TileState()

    def data(self, local_x: int, local_z: int) -> TileData | None:
        return self.tiles[self._index(local_x, local_z)]

    def state(self, local_x: int, local_z: int) -> TileState | None:
        return self.states[self._index(local_x, local_z)]


@dataclass(slots=True)
class TileMap:
    chunk_size: int = 32
    terrains: dict[TerrainKey, TerrainDefinition] = field(default_factory=dict)
    object_definitions: dict[ObjectDefinitionKey, ObjectDefinition] = field(
        default_factory=dict
    )
    objects: Registry[PlacedObject] = field(default_factory=Registry[PlacedObject])
    chunks: dict[ChunkPosition, TileChunk] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

    def register_terrain(self, terrain: TerrainDefinition) -> TerrainDefinition:
        existing = self.terrains.get(terrain.key)
        if existing is not None and existing != terrain:
            raise ValueError(f"Terrain key already registered: {terrain.key}")
        self.terrains[terrain.key] = terrain
        return terrain

    def register_object_definition(
        self, definition: ObjectDefinition
    ) -> ObjectDefinition:
        existing = self.object_definitions.get(definition.key)
        if existing is not None and existing != definition:
            raise ValueError(
                f"Object definition key already registered: {definition.key}"
            )
        self.object_definitions[definition.key] = definition
        return definition

    def set_tile(self, position: TilePosition, tile: TileData) -> None:
        if tile.terrain_key not in self.terrains:
            raise ValueError(f"Unknown terrain: {tile.terrain_key}")
        chunk, local_x, local_z = self._chunk_cell(position, create=True) # type: ignore
        chunk.set(local_x, local_z, tile)

    def tile_data(self, position: TilePosition) -> TileData | None:
        result = self._chunk_cell(position, create=False)
        if result is None:
            return None
        chunk, local_x, local_z = result
        return chunk.data(local_x, local_z)

    def tile_state(self, position: TilePosition) -> TileState | None:
        result = self._chunk_cell(position, create=False)
        if result is None:
            return None
        chunk, local_x, local_z = result
        return chunk.state(local_x, local_z)

    def terrain_at(self, position: TilePosition) -> TerrainDefinition | None:
        tile = self.tile_data(position)
        return None if tile is None else self.terrains[tile.terrain_key]

    def place_object(
        self,
        definition_key: ObjectDefinitionKey,
        anchor: TilePosition,
        *,
        altitude_m: float = 0.0,
        layer: PlacementLayer = PlacementLayer.SURFACE,
        quantity: float | None = None,
    ) -> PlacedObject:
        try:
            definition = self.object_definitions[definition_key]
        except KeyError as error:
            raise PlacementError(f"Unknown object definition: {definition_key}") from error

        footprint = tuple(
            anchor.offset(offset.dx, offset.dz) for offset in definition.footprint
        )
        elevations: list[float] = []
        for position in footprint:
            tile = self.tile_data(position)
            terrain = self.terrain_at(position)
            if tile is None or terrain is None:
                raise PlacementError(f"Missing tile at {position}")
            if not definition.permits(
                terrain, tile.elevation_m, altitude_m, layer
            ):
                raise PlacementError(
                    f"{definition_key!r} is incompatible with tile {position}"
                )
            elevations.append(tile.elevation_m)

        if max(elevations) - min(elevations) > definition.max_footprint_slope_m:
            raise PlacementError(
                f"{definition_key!r} exceeds its maximum footprint slope"
            )

        self._check_object_collisions(definition, footprint, altitude_m)
        placed = PlacedObject(
            definition_key=definition_key,
            anchor=anchor,
            altitude_m=altitude_m,
            layer=layer,
            quantity=quantity,
        )
        self.objects.register(placed)
        for position in footprint:
            state = self.tile_state(position)
            if state is None:
                raise RuntimeError(f"Tile state missing at {position}")
            state.object_ids.add(placed.id)
        return placed

    def remove_object(self, item_or_id: PlacedObject | ObjectID) -> PlacedObject:
        placed = self.objects.remove(item_or_id)
        definition = self.object_definitions[placed.definition_key]
        for offset in definition.footprint:
            state = self.tile_state(placed.anchor.offset(offset.dx, offset.dz))
            if state is not None:
                state.object_ids.discard(placed.id)
        return placed

    def _check_object_collisions(
        self,
        definition: ObjectDefinition,
        footprint: tuple[TilePosition, ...],
        altitude_m: float,
    ) -> None:
        if not definition.blocks_placement:
            return
        candidate_top = altitude_m + definition.height_m
        checked: set[ObjectID] = set()
        for position in footprint:
            state = self.tile_state(position)
            if state is None:
                continue
            for object_id in state.object_ids:
                if object_id in checked:
                    continue
                checked.add(object_id)
                existing = self.objects[object_id]
                existing_definition = self.object_definitions[existing.definition_key]
                if not existing_definition.blocks_placement:
                    continue
                existing_top = existing.altitude_m + existing_definition.height_m
                overlaps = (
                    altitude_m < existing_top
                    and existing.altitude_m < candidate_top
                )
                if overlaps:
                    raise PlacementError(
                        f"Placement collides with object {existing.id}"
                    )

    def _chunk_cell(
        self, position: TilePosition, *, create: bool
    ) -> tuple[TileChunk, int, int] | None:
        chunk_x, local_x = divmod(position.x, self.chunk_size)
        chunk_z, local_z = divmod(position.z, self.chunk_size)
        chunk_position = ChunkPosition(chunk_x, chunk_z)
        chunk = self.chunks.get(chunk_position)
        if chunk is None:
            if not create:
                return None
            chunk = TileChunk(chunk_position, self.chunk_size)
            self.chunks[chunk_position] = chunk
        return chunk, local_x, local_z
