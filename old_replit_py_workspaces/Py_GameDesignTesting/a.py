import pygame
pygame.init()
SCREEN = pygame.display.set_mode((300, 300))

move_map = {pygame.K_w: pygame.math.Vector2( 0, -1),
            pygame.K_s: pygame.math.Vector2( 0,  1),
            pygame.K_a: pygame.math.Vector2(-1,  0),
            pygame.K_d: pygame.math.Vector2( 1,  0)}

class Actor(pygame.sprite.Sprite):
    def __init__(self, group, color, pos, size=(30, 30)):
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        pygame.sprite.Sprite.__init__(self, group)

class Bullet(Actor):
    def __init__(self, *args):
        Actor.__init__(self, *args)
        self.speed = 10

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if not SCREEN.get_rect().colliderect(self.rect):
            self.kill()

class Player(Actor):
    def __init__(self, *args):
        self._layer = 4
        Actor.__init__(self, *args)
        self.speed = 4
        self.timeout = 0

    def update(self):
        p = pygame.key.get_pressed()
        move_vector = pygame.math.Vector2(0, 0)
        for v in [move_map[key] for key in move_map if p[key]]:
            move_vector += v
        if move_vector:
            self.rect.move_ip(*move_vector.normalize() * self.speed)
            self.rect.clamp_ip(SCREEN.get_rect())

        if self.timeout :
            self.timeout -= 1
        if p[pygame.K_SPACE] and not self.timeout:
            Bullet(self.groups()[0], (130, 200, 77), self.rect.center, (10, 3))
            self.timeout = 5


class Background(pygame.sprite.Sprite):
    def __init__(self, number, *args):
        self.image = pygame.image.load('textures/stone_tile.png').convert()
        self.rect = self.image.get_rect()
        self._layer = -10
        pygame.sprite.Sprite.__init__(self, *args)
        self.moved = 0
        self.number = number
        self.rect.x = self.rect.width * self.number

    def update(self):
        self.rect.move_ip(-1, 0)
        self.moved += 1

        if self.moved >= self.rect.width:
            self.rect.x = self.rect.width * self.number
            self.moved = 0

group = pygame.sprite.LayeredUpdates()
Player(group, (255, 255, 255), (100, 100))
Background(0, group)
Background(1, group)

clock = pygame.time.Clock()
run = True
while run:
    for e in pygame.event.get():
        if e.type ==pygame.QUIT:
            run = False
    SCREEN.fill((0,0,0))
    group.update()
    group.draw(SCREEN)
    pygame.display.flip()
    clock.tick(60)