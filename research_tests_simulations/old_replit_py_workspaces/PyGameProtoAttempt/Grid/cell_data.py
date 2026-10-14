
from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Grid.types import Positions
from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Registry import LocaleMarker


class CellData:
    def __init__(self,locale: str) -> None:
        self.region: LocaleMarker  = LocaleMarker(locale)
        self.cells: Positions = []