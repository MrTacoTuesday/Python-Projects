from research_tests_simulations.old_replit_py_workspaces.PyStatsRegressionsFunctions.Stat.data import Data
from research_tests_simulations.old_replit_py_workspaces.PyStatsRegressionsFunctions.Stat.summary2 import Summary2


class Regression:

    def __init__(self, x: Data, y: Data | None = None):
        self.x, self.y = x.xList, y.xList if y else x.yList
        self.summary = Summary2(self.x, self.y)
        self.title = self.__class__.__name__
        self.finalize()

    def finalize(self):
        pass

    def inverted(self) -> "Regression":
        _new = self
        _new.x, _new.y = _new.y, _new.x
        _new.summary = Summary2(_new.x, _new.y)
        _new.title = "Inverted " + _new.title 
        _new.finalize()
        return _new

    def __call__(self, x: float) -> float:
        return NotImplemented

    def predict(self, x: float) -> float:
        return self(x)

    def __repr__(self) -> str:
        return NotImplemented

    def resid(self) -> Data:
        resid = Data({x: y - self(x) for x, y in zip(self.x, self.y, strict=True)})
        resid.title = "Residuals"
        resid.summaryType = "TwoVar"
        return resid

    @property
    def r2(self) -> float:
        return 1 - (
            sum((y - self(x))**2 for x, y in zip(self.x, self.y, strict=True)) / 
            self.summary.varianceY
        )
