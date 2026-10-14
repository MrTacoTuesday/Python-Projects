
from Grid.types import Positions
from Registry import LocaleMarker


class CellData:
    def __init__(self,locale: str) -> None:
        self.region: LocaleMarker  = LocaleMarker(locale)
        self.cells: Positions = []