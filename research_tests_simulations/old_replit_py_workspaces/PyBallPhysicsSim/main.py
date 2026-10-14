from research_tests_simulations.old_replit_py_workspaces.PyBallPhysicsSim.old_sim import main

main()

"""
import sys
from time import sleep

from pygame import QUIT, quit
from pygame import event as events
from pygame.display import update
from pygame.sprite import Group, spritecollide

from Simulation import Ball, Color, Vector2

print("Hello")

BALLS = Group()


a = Ball(Vector2(100, 100), 10, Color("black"), Vector2(0, 0))
b = Ball(Vector2(120, 109), 10, Color("black"), Vector2(0, 0))

BALLS.add(a, b)

for collision in spritecollide(a, BALLS, False):
    if collision is not a:
        print(collision)


while True:
    for event in events.get():
        if event.type == QUIT:
            RUNNING = False
            quit()
            sys.exit()
    a.set_pos(a.pos.x + 1, a.pos.y + 1)
    b.set_pos(b.pos.x - 2, b.pos.y)
    sleep(1)
    update()
"""