from typing import Mapping, Tuple

from pygame.surface import Surface

Coordinate = Tuple[int, int]
Pixels = int
Size = Tuple[Pixels, Pixels]


class Level:

    def __init__(self, size: Size, cell_size: Pixels):
        self.map: Mapping[Coordinate, Cell] = {}
        self.scale: float = 1.0
        self.size: Size = size
        self.cell_size: Pixels = cell_size
        

    def cell(self, at: Coordinate) -> "Cell | None":
        return self.map[at]

class Cell():

    def __init__(self, grid_position: Coordinate, level: Level):
        self.grid_position: Coordinate = grid_position
        self.level = level
        self.__size: Pixels = self.level.cell_size
        self.__image: Surface

    @property
    def size(self) -> Pixels:
        return int(self.__size * self.level.scale)
    
    def _refresh_bounds(self, _xy: Coordinate):
        (x0,y0) = _xy
        (x1,y1) = (x0 + self.size, y0 + self.size)
        self.__bounds = ((x0,x1),(y0,y1))