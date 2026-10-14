
### Finding Roots ###
from research_tests_simulations.old_replit_py_workspaces.PyMathDerivationTest.methods import a
#from datetime import datetime as time

'''num = 648
pow = 3

mine = "\33[32m\33[3mMine\33[0m"
pyth = "\33[31m\33[3mPython's\33[0m"

s0 = time.now()
py = num**(1/pow)
s1 = time.now()
print(pyth, "\10: ", py, py**pow)

ppe = 100*abs((num-py**pow)/num)
print(ppe, "% Error")

print()

s2 = time.now()
my = i(num, lambda x: x**pow)
s3 = time.now()
print(mine, "\10: ", my, my**pow)

mpe = 100*abs((num-my**pow)/num)
print(mpe, "% Error")

print()

if not mpe and not ppe:
	print("Both are perfectly accurate")
elif not mpe or not ppe:
	print(pyth if mpe else mine, "is perfectly accurate")
elif mpe == ppe:
	print("Equally accurate")
elif mpe < ppe:
	print(mine, "is", int(ppe/mpe*10)/10, "times more accurate")
else:
	print(pyth, "is", int(mpe/ppe*10)/10, "times more accurate")
print(mine, "is", int((s3-s2)/(s1-s0)*10)/10, "times slower")'''

'''s4 = time.now()
print(s4-s0)'''

# 2x - 250x slower than python's method, usually ~10x (with variable input)
# 7x - 300x slower - usually ~40x (with literal input)
l = lambda x: (x+2)**2
b = a(9, l) # x = -5, 1
print(b)