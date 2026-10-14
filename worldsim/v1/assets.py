from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias


AssetKey: TypeAlias = str


def validate_asset_key(key: AssetKey) -> None:
    if not key or "/" in key or "\\" in key:
        raise ValueError(f"Asset keys must be non-empty names, got {key!r}")


@dataclass(frozen=True, slots=True)
class AssetCatalog:
    """Resolves portable asset keys at the viewer/resource boundary."""

    root: Path
    image_extension: str = ".png"

    def tile_path(self, key: AssetKey) -> Path:
        validate_asset_key(key)
        return self.root / "tiles" / f"{key}{self.image_extension}"

    def object_path(self, key: AssetKey) -> Path:
        validate_asset_key(key)
        return self.root / "objects" / f"{key}{self.image_extension}"
