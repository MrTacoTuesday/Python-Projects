from pygame import Color, init
from pygame.display import get_surface, set_mode, set_caption
from pygame.draw import circle
from pygame.math import Vector2
from pygame.sprite import Sprite  #, spritecollide

init()
DISPLAYSURF = set_mode((400, 300))
set_caption('Test')
DISPLAYSURF.fill(Color("white"))

class Ball(Sprite):

    def __init__(self, pos: Vector2, radius: int, color: Color, velocity: Vector2):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.rect = circle(get_surface(), color, (pos.x, pos.y), radius)
        self.rect.move(pos.x, pos.y)

    def set_pos(self, x: float, y: float):
        self.pos.update(x, y)

    def update(self, timedelta: float):
        pass

    def draw(self):
        self.rect.move(self.pos.x, self.pos.y)
        #self.rect