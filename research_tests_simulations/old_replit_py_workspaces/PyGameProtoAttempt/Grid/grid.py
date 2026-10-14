from typing import Dict

from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Grid.cell import Cell
from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Grid.types import Position


class Grid:
    def __init__(self) -> None:
        self.data: Dict[Position, Cell] = {}

    def get(self, pos: Position) -> Cell | None:
        return self.data[pos]

    def set(self, cell: Cell, pos: Position) -> None:
        self.data[pos] = cell