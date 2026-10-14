from typing import List, Tuple

from pygame import Surface, display

Pos = Tuple[int, int]
CellBounds = Tuple[Pos, Pos]
RGB = Tuple[int, int, int]


class Grid:

    def __init__(self, cell_width: int, cell_height: int, cell_margin: int,
                 rows: int, columns: int):
        self.cell = (cell_width, cell_height)
        self.margin = cell_margin
        self.rows = rows
        self.columns = columns
        self.cells: List[Cell] = []
        self.surface: Surface
        self.bg_color = (50, 50, 50)
        self.selected_cells: List[int] = []
        self.refresh_size()
        self.init_cells()

    def refresh_size(self):
        self.width = (self.cell[0] + self.margin) * self.rows + self.margin
        self.height = (self.cell[1] + self.margin) * self.columns + self.margin
        self.surface = display.set_mode((self.width, self.height))

    def _cell_bounds(self, row: int, column: int) -> CellBounds:
        start_x = (self.cell[0] + self.margin) * row + self.margin
        start_y = (self.cell[1] + self.margin) * column + self.margin
        end_x = start_x + self.cell[0]
        end_y = start_y + self.cell[1]
        return ((start_x, start_y), (end_x, end_y))

    def cell_id(self, row: int, column: int) -> int:
        return self.columns * row + column

    def get_cell(self, id: int) -> "Cell | None":
        for c in self.cells:
            if c.id == id:
                return c
        return None

    def get_cell_at(self, x: int, y: int) -> "Cell | None":
        for c in self.cells:
            if c.is_in_bounds(x,y):
                return c
        return None

    def has_cell(self, id: int) -> bool:
        return self.get_cell(id) is not None

    def init_cells(self):
        for r in range(self.rows):
            for c in range(self.columns):
                id = self.cell_id(r, c)
                if self.has_cell(id):
                    continue
                bounds = self._cell_bounds(r, c)
                cell = Cell(id, (r, c), bounds, self)
                self.cells.append(cell)

    def draw(self):
        self.surface.fill(self.bg_color)
        for cell in self.cells:
            cell.draw()

    def select_all(self):
        for c in self.cells:
            c.select()
    
    def unselect_all(self):
        for c in self.cells:
            c.unselect()


class Cell:

    def __init__(self, id: int, pos: Pos, bounds: CellBounds, grid: "Grid"):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.color: RGB = (255, 255, 255)
        self.image = None
        self.surface = grid.surface
        self._grid = grid
        self.is_selected = False
        self.update_bounds(bounds)

    def update_bounds(self, bounds: CellBounds):
        self.x_bounds = (bounds[0][0], bounds[1][0])
        self.y_bounds = (bounds[0][1], bounds[1][1])

    def is_in_bounds(self, x: int, y: int) -> bool:
        (x0, x1) = self.x_bounds
        (y0, y1) = self.y_bounds
        return x <= x1 and x >= x0 and y <= y1 and y >= y0

    def recolor(self, rgb: RGB):
        self.color = rgb
        self.draw()

    def select(self):
        if self.is_selected:
            return
        self.is_selected = True
        if self.id not in self._grid.selected_cells:
            self._grid.selected_cells.append(self.id)
        self.draw()

    def unselect(self):
        if not self.is_selected:
            return
        self.is_selected = False
        if self.id in self._grid.selected_cells:
            self._grid.selected_cells.remove(self.id)
        self.draw()

    def toggle_selection(self):
        self.selection(not self.is_selected)

    def selection(self, toggled: bool):
        if toggled:
            self.select()
        else:
            self.unselect()

    def pos(self) -> Pos:
        return (self.x, self.y)

    def pixel_pos(self) -> Pos:
        return (self.x_bounds[0], self.y_bounds[0])

    def get_size(self) -> Tuple[int, int]:
        w = self.x_bounds[1] - self.x_bounds[0]
        h = self.y_bounds[1] - self.y_bounds[0]
        return (w, h)

    def draw(self):
        (x, y) = self.pixel_pos()
        (w, h) = self.get_size()
        
        if self.is_selected:
            self._draw_selection(x, y, w, h)
        else:
            self._draw(x, y, w, h)

    def _draw_selection(self, x: int, y: int, w: int, h: int):
        self.surface.fill((255, 0, 0), [x, y, w, h])
        self.surface.fill(self.color, [x + 2, y + 2, w - 4, h - 4])

    def _draw(self, x: int, y: int, w: int, h: int):
        self.surface.fill(self.color, [x, y, w, h])
