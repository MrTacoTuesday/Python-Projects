import sys
from itertools import combinations
from random import randint
from threading import Thread
from time import sleep

import numpy as np
import pygame
from pygame.locals import QUIT

pygame.init()

RUNNING = False
DOES_TEST_COLLISIONS = False

DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Test')

FRAMES_PER_SECOND = 40
TICKS_PER_SECOND = 20

MODE = "v"
SPAWN_VELOCITY_X = 20
SPAWN_VELOCITY_Y = 20
GRAVITY_X = 0 #0
GRAVITY_Y = -9.81
SURFACE_FRICTION_COEFFICIENT = 0.4


def cls():
    DISPLAYSURF.fill(pygame.Color("white"))


def circle(x, y, radius, color: pygame.Color | None = None):
    color = color or pygame.Color("black")
    pygame.draw.circle(DISPLAYSURF, color, (x, y), radius)


class Ball:

    def __init__(self,
                 radius: float,
                 x: float | None = None,
                 y: float | None = None):
        self.x = 0
        self.y = DISPLAYSURF.get_height()
        self.radius = radius
        self.applied_ax = 0
        self.applied_ay = 0
        self.vx = 0
        self.vy = 0
        self.color = pygame.Color("black")
        self.setxy(x or self.x, y or self.y)

    def setcolor(self, color: pygame.Color):
        self.color = color

    def setvelocity(self, vx: float, vy: float):
        self.vx = vx if abs(vx) > 1e-3 else 0
        self.vy = vy if abs(vy) > 1e-3 else 0

    @property
    def ax(self) -> float:
        return self.applied_ax + GRAVITY_X

    @property
    def ay(self) -> float:
        return self.applied_ay + GRAVITY_Y

    def update(self, time: float):
        t = time * 10  # cs
        self.movedelta(self.vx * t + 0.5 * self.ax * t**2,
                       -self.vy * t - 0.5 * self.ay * t**2)
        self.setvelocity(self.vx + self.ax * t, self.vy + self.ay * t)

    def movedelta(self, dx: float, dy: float):
        self.setxy(self.x + dx, self.y + dy)

    def setxy(self, x: float, y: float):
        width = DISPLAYSURF.get_width()
        height = DISPLAYSURF.get_height()
        r = self.radius
        self.x = max(r, min(width - r, x))
        self.y = max(r, min(height - r, y))
        if self.isonground or self.isonceiling:
            C = 1 - SURFACE_FRICTION_COEFFICIENT
            self.setvelocity(C * self.vx, C * -self.vy)
        if self.isonwall:
            C = 1 - SURFACE_FRICTION_COEFFICIENT
            self.setvelocity(C * -self.vx, C * self.vy)
                

    def applyforce(self, fx: float, fy: float):
        self.applied_ax += fx
        self.applied_ay += fy

    @property
    def mass(self) -> float:
        """
        Mass of ball in grams
        """
        ## 1 g/pixel^2
        return 1 * (self.radius**2 * 3.14159)

    @property
    def isonground(self) -> bool:
        height, r = DISPLAYSURF.get_height(), self.radius
        return self.y == height - r

    @property
    def isonwall(self) -> bool:
        width, r = DISPLAYSURF.get_width(), self.radius
        return self.x == width - r or self.x == r

    @property
    def isonceiling(self) -> bool:
        return self.y == self.radius

    @property
    def isonboundary(self) -> bool:
        return self.isonceiling or self.isonwall or self.isonground

    def iscolliding(self, other: "Ball") -> bool:
        """
        Returns True if the two balls collide
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) < (self.radius + other.radius)**2

    def redraw(self):
        circle(self.x, self.y, self.radius, self.color)


BALLS: list[Ball] = []


def register(ball: Ball) -> Ball:
    BALLS.append(ball)
    return ball

def experiment():
    ball = register(Ball(radius=10, x=0, y=300))
    ball.setcolor(pygame.Color("green"))
    ball.setvelocity(16, 70)


def draw():
    cls()
    for ball in BALLS:
        ball.redraw()
    pygame.display.update()


def drawer():
    global time, RUNNING
    draw()
    while RUNNING:
        t = 1 / FRAMES_PER_SECOND
        sleep(t)
        for ball in BALLS:
            ball.update(t)
        if DOES_TEST_COLLISIONS:
            checkcollisions()
        draw()


def ticker():
    global time, RUNNING
    while RUNNING:
        t = 1 / TICKS_PER_SECOND
        sleep(t)
        checkupdates()


def checkcollisions():

    def update_velocities(b1: Ball, b2: Ball):
        m1, m2 = b1.mass, b2.mass
        M = m1 + m2
        r1, r2 = np.array((b1.x, b1.y)), np.array((b2.x, b2.y))
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = np.array((b1.vx, b1.vy)), np.array((b2.vx, b2.vy))
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        b1.setvelocity(u1[0], u1[1])
        b2.setvelocity(u2[0], u2[1])

    for b1, b2 in combinations(BALLS, 2):
        if b1.iscolliding(b2):
            update_velocities(b1, b2)


def checkupdates():
    global RUNNING, SPAWN_VELOCITY_X, SPAWN_VELOCITY_Y, MODE, GRAVITY_X, GRAVITY_Y, DOES_TEST_COLLISIONS
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                ball = register(Ball(radius=randint(6,18), x=x, y=y))
                ball.setvelocity(
                    randint(-SPAWN_VELOCITY_X * 2, SPAWN_VELOCITY_X * 2),
                    randint(-SPAWN_VELOCITY_Y * 2, SPAWN_VELOCITY_Y * 2))
            elif event.button == 3:
                BALLS.clear()
                experiment()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and MODE == "v":
                SPAWN_VELOCITY_Y += 10
                print("Max spawning Vy:", SPAWN_VELOCITY_Y)
            elif event.key == pygame.K_DOWN and MODE == "v":
                SPAWN_VELOCITY_Y -= 10
                print("Max spawning Vy:", SPAWN_VELOCITY_Y)
            elif event.key == pygame.K_LEFT and MODE == "v":
                SPAWN_VELOCITY_X -= 10
                print("Max spawning Vx:", SPAWN_VELOCITY_X)
            elif event.key == pygame.K_RIGHT and MODE == "v":
                SPAWN_VELOCITY_X += 10
                print("Max spawning Vx:", SPAWN_VELOCITY_X)
            if event.key == pygame.K_UP and MODE == "g":
                GRAVITY_Y += 1e-1
                print("Gravity Y:", GRAVITY_Y)
            elif event.key == pygame.K_DOWN and MODE == "g":
                GRAVITY_Y -= 1e-1
                print("Gravity Y:", GRAVITY_Y)
            elif event.key == pygame.K_LEFT and MODE == "g":
                GRAVITY_X -= 1e-1
                print("Gravity X:", GRAVITY_X)
            elif event.key == pygame.K_RIGHT and MODE == "g":
                GRAVITY_X += 1e-1
                print("Gravity X:", GRAVITY_X)
            elif event.key == pygame.K_MINUS and MODE == "v":
                SPAWN_VELOCITY_X = -SPAWN_VELOCITY_X
                print("Negating Spawning Vx")
            elif event.key in [pygame.K_KP_MINUS, pygame.K_EQUALS] and MODE == "v":
                SPAWN_VELOCITY_Y = -SPAWN_VELOCITY_Y
                print("Negating Spawning Vy")
            elif event.key == pygame.K_MINUS and MODE == "g":
                GRAVITY_X = -GRAVITY_X
                print("Flipping Gravity X:", GRAVITY_X)
            elif event.key in [pygame.K_KP_MINUS, pygame.K_EQUALS] and MODE == "g":
                GRAVITY_Y = -GRAVITY_Y
                print("Flipping Gravity Y:", GRAVITY_Y)
            elif event.key == pygame.K_v:
                MODE = "v"
                print("Mode: Max Spawning Velocity")
            elif event.key == pygame.K_g:
                MODE = "g"
                print("Mode: Ambient Gravity")
            elif event.key == pygame.K_c:
                DOES_TEST_COLLISIONS = not DOES_TEST_COLLISIONS
                print("Collision Testing:", "ON" if DOES_TEST_COLLISIONS else "OFF")
                


DRAWER = Thread(target=drawer)
TICKER = Thread(target=ticker)


def main():
    global RUNNING
    RUNNING = True

    experiment()

    DRAWER.start()
    TICKER.start()