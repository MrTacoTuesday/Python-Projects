from math import floor

if __name__ == '__main__':
    from hasher import Hasher
else:
    from .hasher import Hasher

class perlin:

    def __init__(self, seed: int) -> None:
        self._hasher = Hasher(seed, 'reset')

    @property
    def seed(self) -> int:
        return self._hasher.seed

    def random(self, *dims: int) -> float:
        return float(self._hasher.combine(*dims).digest())
    
    @classmethod
    def inflate(cls, x: float) -> float:
        return (3 - 2 * x) * x * x

    @classmethod
    def gradient_1d(cls, min: float, max: float, percent: float) -> float:
        return min + (max - min) * cls.inflate(percent)

    def perlin(self, *dims: float) -> float:
        floored = tuple(floor(x) for x in dims)
        deltas = tuple(dims[i]-floored[i] for i in range(len(dims)))
        constants = tuple(
            self.random(
                *(
                    floored[j] + (1 if (i % (2<<j) >= (1<<j)) else 0) 
                    for j in range(len(floored))
                ) # 000, 100, 010, 110, 001, 101, 011, 111 for 3D
            ) for i in range(1<<len(dims))
        )
        for delta in deltas:
            # merges neighbors as gradients     
            #     :   r(x  , y  ) r(x+1, y  ) -> gx(y  )
            #     :   r(x  , y+1) r(x+1, y+1) -> gx(y+1)
            # so next round we can do the same  
            #     :   gx(y  )     gx(y+1)     -> gxy()
            constants = tuple(self.gradient_1d(constants[i<<1], constants[(i<<1)+1], delta) for i in range(len(constants)>>1))
        assert len(constants) == 1
        return constants[0]

    def octaves(self, *dims: float, octaves: int, persistance: float, lacunarity: float):
        value = 0
        amplitude = 2
        weight = 0

        for _ in range(octaves):
            value += amplitude * (self.perlin(*dims)-0.5)
            weight += amplitude
            amplitude *= persistance
            dims=tuple(x*lacunarity for x in dims)

        return value/weight + 0.5


    """
    x  , y  , z
    x+1, y  , z
    x  , y+1, z
    x+1, y+1, z
    x  , y  , z+1
    x+1, y  , z+1
    x  , y+1, z+1
    x+1, y+1, z+1

    dims = ['x','y','z']
    for i in range(2**len(dims)):
        for dim in range(len(dims)):
            print(dims[dim] + ('+1 ' if (i % (2<<dim) >= (1<<dim)) else '   '), end='')
        print()
    """


