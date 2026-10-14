from math import log

from .regression import Regression


class LogReg(Regression):

    def __init__(self, x, y = None):
        super().__init__(x.modifiedX(lambda x: log(x)), y)
        self.x, self.y = x.xList, y.xList if y else x.yList

    def finalize(self):
        self.a = self.summary.a
        self.b = self.summary.b

    def __call__(self, x: float) -> float:
        return self.a + self.b * log(x)

    def __repr__(self) -> str:
        return (
            f"{self.title}:" +
            f"\ny = {self.a:.4f} + {self.b:.4f} ln x" +
            f"\n\tr² = {self.r2:.4f}" + "\n"
        )