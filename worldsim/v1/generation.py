from dataclasses import dataclass
from math import floor

from .ids import content_id
from .tiles import TerrainKey, TileData, TileMap, TilePosition


@dataclass(frozen=True, slots=True)
class TerrainBand:
    maximum_elevation_m: float
    terrain_key: TerrainKey


@dataclass(frozen=True, slots=True)
class GenerationConfig:
    seed: int
    elevation_scale_m: float = 120.0
    frequency: float = 0.025
    octaves: int = 4
    persistence: float = 0.5
    terrain_bands: tuple[TerrainBand, ...] = (
        TerrainBand(-15.0, "deep_water"),
        TerrainBand(0.0, "water"),
        TerrainBand(4.0, "sand"),
        TerrainBand(55.0, "grass"),
        TerrainBand(90.0, "rock"),
        TerrainBand(float("inf"), "snow"),
    )

    def __post_init__(self) -> None:
        if self.elevation_scale_m <= 0.0:
            raise ValueError("elevation_scale_m must be greater than zero")
        if self.frequency <= 0.0:
            raise ValueError("frequency must be greater than zero")
        if self.octaves <= 0:
            raise ValueError("octaves must be greater than zero")
        if not 0.0 < self.persistence <= 1.0:
            raise ValueError("persistence must be between >0.0 and 1.0")
        if not self.terrain_bands:
            raise ValueError("At least one terrain band is required")
        maxima = tuple(band.maximum_elevation_m for band in self.terrain_bands)
        if maxima != tuple(sorted(maxima)):
            raise ValueError("Terrain bands must be sorted by elevation")


class ProceduralGenerator:
    def __init__(self, config: GenerationConfig) -> None:
        self.config = config

    def tile_at(self, position: TilePosition) -> TileData:
        elevation = self.elevation_at(position)
        return TileData(
            terrain_key=self.terrain_for(elevation),
            elevation_m=elevation,
        )

    def elevation_at(self, position: TilePosition) -> float:
        value = self._fractal_noise(position.x, position.z)
        return (value * 2.0 - 1.0) * self.config.elevation_scale_m

    def terrain_for(self, elevation_m: float) -> TerrainKey:
        for band in self.config.terrain_bands:
            if elevation_m <= band.maximum_elevation_m:
                return band.terrain_key
        raise RuntimeError("The final terrain band must cover all elevations")

    def generate_region(
        self,
        tile_map: TileMap,
        *,
        start: TilePosition,
        width: int,
        depth: int,
    ) -> None:
        if width <= 0 or depth <= 0:
            raise ValueError("Generated dimensions must be greater than zero")
        for z in range(start.z, start.z + depth):
            for x in range(start.x, start.x + width):
                position = TilePosition(x, z)
                tile_map.set_tile(position, self.tile_at(position))

    def _fractal_noise(self, x: int, z: int) -> float:
        total = 0.0
        amplitude = 1.0
        amplitude_total = 0.0
        frequency = self.config.frequency
        for octave in range(self.config.octaves):
            total += amplitude * self._value_noise(x * frequency, z * frequency, octave)
            amplitude_total += amplitude
            amplitude *= self.config.persistence
            frequency *= 2.0
        return total / amplitude_total

    def _value_noise(self, x: float, z: float, octave: int) -> float:
        x0 = floor(x)
        z0 = floor(z)
        tx = self._smooth(x - x0)
        tz = self._smooth(z - z0)

        top = self._lerp(
            self._lattice(x0, z0, octave),
            self._lattice(x0 + 1, z0, octave),
            tx,
        )
        bottom = self._lerp(
            self._lattice(x0, z0 + 1, octave),
            self._lattice(x0 + 1, z0 + 1, octave),
            tx,
        )
        return self._lerp(top, bottom, tz)

    def _lattice(self, x: int, z: int, octave: int) -> float:
        value = content_id("terrain-noise", self.config.seed, octave, x, z)
        return value / ((1 << 64) - 1)

    @staticmethod
    def _smooth(value: float) -> float:
        return value * value * (3.0 - 2.0 * value)

    @staticmethod
    def _lerp(start: float, end: float, amount: float) -> float:
        return start + (end - start) * amount
