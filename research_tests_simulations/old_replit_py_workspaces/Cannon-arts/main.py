from math import radians
from time import sleep

from cannon import Cannon

Royal = Cannon(3.658, 29.94)

print("Cannon Royal Physics (3.658m barrel, 29.94kg shot)")
print()
print()


for angle in (0, 15, 30, 45, 60, 75, 90):

    sleep(3)
    Royal.test(radians(angle))
    print()