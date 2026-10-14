from pygame import MOUSEBUTTONDOWN, QUIT, quit
from pygame import event as Event
from pygame import init as setup
from pygame.display import flip, set_caption
from pygame.mouse import get_pos as mouse_pos
from pygame.time import Clock

import research_tests_simulations.old_replit_py_workspaces.Py_GameDesignTesting._old.grid as grid

COLOR_RED = (255, 10, 10)
COLOR_GREEN = (10, 255, 10)
COLOR_BLUE = (10, 10, 255)
COLOR_BROWN = (150, 75, 10)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (25, 25, 25)
COLOR_WHITE = (255, 255, 255)

setup()

color_grid = grid.Grid(40,40,8,8,8)
color_grid.init_cells()
for cell in color_grid.cells:
    r = 36 + cell.x * 20
    g = 86 + cell.y * 20
    b = 77 + (cell.x + cell.y)*10
    cell.color = (r % 256, g % 256, b % 256)

set_caption("Level Builder")

done = False
clock = Clock()
while not done:
    for event in Event.get():
        if event.type == QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            mp = mouse_pos()
            print("Mouse : ", mp)
            cell = color_grid.get_cell_at(*mp)
            if cell:
                print("Grid  : ", (cell.x, cell.y))
                #s = cell.is_selected
                color_grid.unselect_all()
                #cell.selection(not s)
                #cell.toggle_selection()
                cell.select()
    color_grid.draw()
    clock.tick(10)
    flip()
quit()