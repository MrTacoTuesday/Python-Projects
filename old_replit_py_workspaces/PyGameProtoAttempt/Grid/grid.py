from typing import Dict

from Grid.cell import Cell
from Grid.types import Position


class Grid:
    def __init__(self) -> None:
        self.data: Dict[Position, Cell] = {}

    def get(self, pos: Position) -> Cell | None:
        return self.data[pos]

    def set(self, cell: Cell, pos: Position) -> None:
        self.data[pos] = cell