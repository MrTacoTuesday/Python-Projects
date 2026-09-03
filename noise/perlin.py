from math import floor

if __name__ == "__main__":
    from noise.hashrandom import SeededHashRandomizer, HasherMode
else:
    from .hashrandom import SeededHashRandomizer, HasherMode


class perlin:

    def __init__(self, seed: int) -> None:
        self._hasher = SeededHashRandomizer(seed, HasherMode.reset)

    @property
    def seed(self) -> int:
        return self._hasher.seed

    def random(self, *dims: int) -> float:
        return float(self._hasher.combine(*dims).digest())

    @classmethod
    def inflate(cls, x: float) -> float:
        return (3 - 2 * x) * x * x

    @classmethod
    def gradient_1d(
        cls, left_bound: float, right_bound: float, percent: float
    ) -> float:
        return left_bound + (right_bound - left_bound) * cls.inflate(percent)

    def perlin_1d(self, x: float) -> float:
        fx = floor(x)
        dx = x - fx
        cx = self.random(fx), self.random(fx + 1)
        return self.gradient_1d(cx[0], cx[1], dx)

    def perlin_2d(self, x: float, y: float) -> float:
        fx, fy = floor(x), floor(y)
        dx, dy = x - fx, y - fy
        cxy = self.random(fx, fy), self.random(fx + 1, fy)
        cxY = self.random(fx, fy + 1), self.random(fx + 1, fy + 1)
        return self.gradient_1d(
            left_bound=self.gradient_1d(cxy[0], cxy[1], dx),
            right_bound=self.gradient_1d(cxY[0], cxY[1], dx),
            percent=dy,
        )

    def perlin(self, *dims: float) -> float:
        floored = tuple(floor(x) for x in dims)
        deltas = tuple(dims[i] - floored[i] for i in range(len(dims)))
        constants = tuple(
            self.random(
                *(
                    floored[j] + (1 if (i % (2 << j) >= (1 << j)) else 0)
                    for j in range(len(floored))
                )  # (000, 100, 010, 110, 001, 101, 011, 111) for 3D
            )
            for i in range(1 << len(dims))
        )
        for delta in deltas:
            # merges neighbors as gradients
            #     :   r(x  , y  ) r(x+1, y  ) -> gx(y  )
            #     :   r(x  , y+1) r(x+1, y+1) -> gx(y+1)
            # so next round we can do the same
            #     :   gx(y  )     gx(y+1)     -> gxy()
            constants = tuple(
                self.gradient_1d(constants[i << 1], constants[(i << 1) + 1], delta)
                for i in range(len(constants) >> 1)
            )
        assert len(constants) == 1
        return constants[0]

    def octaves(
        self, *dims: float, octaves: int, persistance: float, lacunarity: float
    ) -> float:
        value = 0
        amplitude = 2
        weight = 0

        #optimize to hardcoded versions
        match len(dims):
            case 1:
                func = self.perlin_1d
            case 2:
                func = self.perlin_2d
            case _:
                func = self.perlin

        for _ in range(octaves):
            value += amplitude * (func(*dims) - 0.5)
            weight += amplitude
            amplitude *= persistance
            dims = tuple(dim * lacunarity for dim in dims)

        return value / weight + 0.5

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
