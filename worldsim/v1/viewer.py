from dataclasses import dataclass

from .tiles import GridPosition, TilePosition


@dataclass(frozen=True, slots=True)
class ScreenPosition:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class IsometricProjection:
    tile_width_px: float = 64.0
    tile_height_px: float = 32.0
    elevation_px_per_m: float = 1.0
    origin: ScreenPosition = ScreenPosition(0.0, 0.0)

    def __post_init__(self) -> None:
        if self.tile_width_px <= 0.0 or self.tile_height_px <= 0.0:
            raise ValueError("Tile dimensions must be greater than zero")
        if self.elevation_px_per_m < 0.0:
            raise ValueError("elevation_px_per_m cannot be negative")

    def project(self, position: GridPosition) -> ScreenPosition:
        half_width = self.tile_width_px / 2.0
        half_height = self.tile_height_px / 2.0
        return ScreenPosition(
            x=self.origin.x + (position.world_x - position.world_z) * half_width,
            y=(
                self.origin.y
                + (position.world_x + position.world_z) * half_height
                - position.elevation_m * self.elevation_px_per_m
            ),
        )

    def tile_center(
        self, tile: TilePosition, elevation_m: float = 0.0
    ) -> ScreenPosition:
        return self.project(
            GridPosition(tile=tile, elevation_m=elevation_m)
        )

    def unproject(
        self, screen: ScreenPosition, *, elevation_m: float = 0.0
    ) -> tuple[float, float]:
        """Return continuous world x/z for a known elevation plane."""
        dx = (screen.x - self.origin.x) / (self.tile_width_px / 2.0)
        dy = (
            screen.y
            - self.origin.y
            + elevation_m * self.elevation_px_per_m
        ) / (self.tile_height_px / 2.0)
        return (dx + dy) / 2.0, (dy - dx) / 2.0
