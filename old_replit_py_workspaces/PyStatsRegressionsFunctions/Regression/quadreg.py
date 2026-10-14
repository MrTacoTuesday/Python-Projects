from math import log

from .regression import Regression


class QuadReg(Regression):

    def finalize(self):
        n = self.summary.n
        meanX, meanY = self.summary.meanX, self.summary.meanY
        # could be sum(x) **2  instead of sum(x**2)
        meanX2 = self.summary.sumX2 / n 
        Sxx = sum((x - meanX)**2 for x in self.x)
        Sxy = sum(
            (x - meanX) * (y - meanY) 
            for x, y in zip(self.x, self.y, strict=True)
        )
        Sxx2 = sum(
            (x - meanX) * (x**2 - meanX2) 
            for x in self.x
        )
        Sx2x2 = sum(
            (x**2 - meanX2) ** 2
            for x in self.x
        )
        Sx2y = sum(
            (x**2 - meanX2) * (y - meanY)
            for x, y in zip(self.x, self.y, strict=True)
        )
        self.a = (
            (Sx2y * Sxx - Sxy * Sxx2) /
            (Sxx * Sx2x2 - Sxx2 ** 2)
        )
        self.b = (
            (Sxy * Sx2x2 - Sx2y * Sxx2) /
            (Sxx * Sx2x2 - Sxx2 ** 2)
        )
        self.c = (
            meanY - self.b * meanX - self.a * meanX2
        )

    def __call__(self, x: float) -> float:
        return self.a * x**2 + self.b * x + self.c

    def __repr__(self) -> str:
        return (
            f"{self.title}:" +
            f"\ny = {self.a:.4f}x² + {self.b:.4f}x + {self.c:.4f}" +
            f"\n\tr² = {self.r2:.4f}" + "\n"
        )