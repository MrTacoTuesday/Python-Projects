#import levelwalk


from typing import Any, Tuple

from pygame import Surface, display, transform
from pygame import init as setup
from pygame.image import load as load_image
from pygame.sprite import Group, Sprite

setup()

scr = display.set_mode((500, 500))
scr.fill((64, 47, 106))

scale = 128

GROUND = transform.scale(load_image("textures/ground.png"), (scale, scale))
TILE = transform.scale(load_image("textures/stone_tile.png"), (scale, scale))

for r in range(-2,6):
    for c in range(-2,6):
        p = (scale*c+44, scale*r+55)
        if r*c < 0:
            scr.blit(GROUND, p)
        else:
            scr.blit(TILE, p)

def draw_cells(r, c, scr, tex_surf):
    for r in range(-1,5):
        for c in range(-1,5):
            scr.blit(tex_surf, (scale*c, scale*r))


#display.toggle_fullscreen()
display.update()

