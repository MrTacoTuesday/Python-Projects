
from collections.abc import Mapping

from grid import Pos


place = {
    "border": [(-1, -1), (-1, 1), (1, 1), (1, -1)],
    "entrypoints": [(1, 0), (-1, 0), (0, 1), (0, -1)],
    "localization": "place.town_square",
    "events": [],
    "places": [
        {
            "border": [(-1, -1), (-1, -0.5), (-0.5, -0.5), (-0.5, -1)],
            "entrypoints": [(1, 0), (-1, 0), (0, 1), (0, -1)],
            "localization": "place.town_park",
            "events": [],
            "places": []
        }
    ]
}

print(place["border"])

class Place:

    def __init__(self, map, localization: str = "place.unknown"):
        self.map = map #: LevelMap
        self.localization = localization
        self.events = [] #: List[Event]
        self.places: Mapping[Pos, Place] = {}
        