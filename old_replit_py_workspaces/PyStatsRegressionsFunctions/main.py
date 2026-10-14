from math import exp
from random import randint
from Application.data_parse import data_from_xy
from Application.math_fx import func_x

from Regression.expreg import ExpReg
from Regression.linreg import LinReg
from Regression.logreg import LogReg
from Regression.quadreg import QuadReg
from Stat.data import Data
from Stat.iv import IV
from Stat.table import Table

D6 = IV([1, 2, 3, 4, 5, 6])
D20 = IV(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
Coin = IV([1, 2])
D4 = IV([1, 2, 3, 4])



"""lindat = [1.0,2,3,4,5,6,7,8,9]
mldat = [1.0,1.4,2.5,3.2,4.7,7.8,11.1,16.9,22.6]
_ = Data(lindat, mldat)
_.title = "Investment Growth Data"
_.summaryType = None
print(_)

reg = ExpReg(_)

print(reg)
print(reg.resid())"""


"""DC = ((D6.repeated(3) * Coin + D20) / D6).truncatedX()
DC.title = "Points Earned vs Frequency"
print(DC)
print(DC.random(10))

reg = QuadReg(DC.cumulated())
reg.title = "Points Earned vs Cumulative Relative Frequency"
print(reg)"""


"""def a(x):
    return 6*x**2 + 0.5*x + 1 + randint(-100,100)

#1000000
q = Table.fill(47, a, type="TwoVar", title="Model Data")
print(q.TwoVar)
reg = QuadReg(q)
print(reg)"""


"""q = Table.fill(
    666, 
    lambda x: 22*x**2 - 47*x + 7 + randint(-666,666), 
    type="TwoVar", 
    title="Model Data"
)
print(q.TwoVar)
print(QuadReg(q))"""


##print(data_from_xy())
f = func_x("sqrt(((x-2)**2 + (x-1)**2 + (x)**2 + (x+1)**2 + (x+2)**2)/5)")
for x in range(12):
    print(f(x))