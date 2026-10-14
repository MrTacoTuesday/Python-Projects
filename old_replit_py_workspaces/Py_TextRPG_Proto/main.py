#import TBRPG

"""# Item Effect: +20% VIT
player.vitality.add_modifier(
    AttributeModifier(uuid4(), AttributeModifierType.MULT_BASE, 0.2))

# Class Effect: x2 VIT
player.vitality.add_modifier(
    AttributeModifier(uuid4(), AttributeModifierType.MULT_TOTAL, 2))"""


"""from uuid import uuid4

from ATTRIBUTE.attribute_map import AttributeMap
from ENTITY.player import Player

player = Player(uuid4(), AttributeMap())
player.set_name("Azalys Othem")

print(uuid4())"""


"""from ENTITY.gender import Gender
from ENTITY.race_instance import RaceInstance
from ENTITY.race_variants import RaceVariants
from ENTITY.races import Races
from RESOURCES.locale import Locale

Locale.set_locale("en_US")

print(Gender.Male.get_name())
print(Gender.Female.get_name())
print(Races.Elf.get_name())

print(RaceInstance(RaceVariants.TribalHuman, Gender.Male).get_name())"""

"""while True:
    cmd = input(" > ")
    
    if cmd == "exit":
        break
    
    print(en_US.get(cmd))"""

from random import randint

def p(r: int, n: int) -> int:
    w = 0
    for _ in range(n):
        if randint(1, r) == 1:
            w += 1
    return w

def p_freq(r: int, n: int, sims: int = 10) -> dict[int, int]:
    print(f"Simulating event on a population of {n} over {sims} trials")
    print(f"Chance of event occuring: {1 / r}")
    d = {}
    for i in range(sims):
        if i in (sims // 4, sims // 2, sims // 4 * 3):
            print(f"{i/sims*100:.0f}% of trials completed")
        _p = p(r,n)
        if _p not in d:
            d[_p] = 1
        else:
            d[_p] += 1
    print(f"100% of trials completed")
    for k in sorted(d.keys()):
        print(f"{k}: {d[k]}")
    return d

#p_freq(6, 30, sims=256)
