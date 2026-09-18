from noise.hashrandom import HashRandom
from noise.tests import run_all_tests

#run_all_tests()


rng = HashRandom('Hello, World!!!', size=4)
for _ in range(rng.randint(5,10)):
    print("bool",_,": ",rng.randbool())