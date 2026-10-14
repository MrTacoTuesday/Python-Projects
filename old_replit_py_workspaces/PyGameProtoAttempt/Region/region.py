from typing import Any, Dict, Tuple, Type

from Registry.locale_marker import LocaleMarker


class Region:
    def __init__(self, locale: str) -> None:
        self.name = LocaleMarker(locale)
        #self.attributes: List[RegionAttribute] = []



class RegionAttributeType:
    def __init__(self, id: str, data_type: Dict[str, Type]) -> None:
        self.id = id
        self.data_type = data_type

    def setup_data(self, data: Dict[str, Any])->Dict[str, Any]:
        d: Dict[str, Any] = {}
        for i in self.data_type:
            T: Type = self.data_type[i]
            d[i] = data[i] if i in data and isinstance(data[i], T) else None
        return d

    @staticmethod
    def get_range(data) -> Tuple[Any, Any]:
        min: Any = data["min"] if "min" in data else None
        max: Any = data["max"] if "max" in data else None
        return (min, max)

    @staticmethod
    def get_value(data) -> Any:
        value: Any = data["value"] if "value" in data else None
        return value

    @staticmethod
    def get_ranged_data(data) -> Tuple[Any, Any]:
        min: Any = data["min"] if "min" in data else None
        max: Any = data["max"] if "max" in data else None
        return (min, max)


class RegionAttributeTypes:
    PlantGrowth = RegionAttributeType("plant-growth-chance", {
        "value": float, "min": float, "max": float})
            

class RegionAttribute:
    def __init__(self, type: RegionAttributeType, data: Dict[str, Any]) -> None:
        self.type = type
        self.data = type.setup_data(data)


RegionAttribute(RegionAttributeTypes.PlantGrowth, {"min": 0.33, "max": 5.4})

_ = {
    "beach": {
        "attributes": [
            {
                "plant-growth-chance": {
                    "min": 0.33, "max": 5.4
                },
                "tile-decay-chance": {
                    "min": 0.1, "max": 0.2
                },
            }
        ]
    }
}

_ = {
    "plants": {
        "illium": {
            "locale": "tile.plant.illium",
            "distribution": {
                "type": "cluster",
                "amount": 3
            },
            "regions": {
                "beach": {
                    "min-chance": 36.4,
                    "max-chance": 80.8
                },
                "forest": {
                    "min-chance": 77.0,
                    "max-chance": 97.8
                }
            }
        }
    }
}

_ = {
    "Pos(0,0)": {
        "tile": {
            "locale": "tile.sand",
            "texture": "tiles/sand",
            "sound" : "tiles/sand",
            "object": {
                "locale": "object.grass",
                "texture": "objects/grass",
                "sound": "objects/grass"
            },
            "": ""
        },
        "region": {
            "locale": "region.desert",
            "sound": "regions/desert"
        }
    }
}