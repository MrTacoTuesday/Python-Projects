from typing import Dict

from Registry.utils import load


class Locale:

    def __init__(self, region: str) -> None:
        self.data = Locale.tryLoad(region)
        self.name = self.getName("loc.name", region)

    @staticmethod 
    def tryLoad(region: str, backup: str = "en_US") -> Dict[str,str]: 
        d = load("./locales/" + region + ".loc")
        if d == {} or d is None:
            d = load("./locales/" + backup + ".loc")
        return d

    def getName(self, marker: str, backup: str | None = None)->str:
        if marker not in self.data:
            return backup or marker
        return self.data[marker]
            