from .regression import Regression


class LinReg(Regression):

    def finalize(self):
        self.a = self.summary.a
        self.b = self.summary.b
        self.r = self.summary.r

    def __call__(self, x: float) -> float:
        return self.summary.a + self.summary.b * x

    def __repr__(self) -> str:
        return (
            f"{self.title}:" +
            f"\ny = {self.a:.4f} + {self.b:.4f} * x" +
            f"\n\tr = {self.r:.4f}" +
            f"\n\tr² = {self.r2:.4f}" + "\n"
        )