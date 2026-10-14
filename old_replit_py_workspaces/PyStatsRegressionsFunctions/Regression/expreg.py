from math import exp, log

from .regression import Regression


class ExpReg(Regression):

    def __init__(self, x, y = None):
        _y = y if y else x.splitXY()[1]
        super().__init__(x, _y.modifiedX(lambda x: log(x)))
        self.x, self.y = x.xList, y.xList if y else x.yList

    def finalize(self):
        self.a = exp(self.summary.a)
        self.b = exp(self.summary.b)

    def __call__(self, x: float) -> float:
        return self.a * self.b ** x

    def __repr__(self) -> str:
        return (
            f"{self.title}:" +
            f"\ny = {self.a:.4f}({self.b:.4f})^x" +
            f"\n\tr² = {self.r2:.4f}" + "\n"
        )