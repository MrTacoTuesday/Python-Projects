from parser import poly_input
from wmath import poly
from time import sleep

COLOR = "\033[033m\ueea7\ueea7\ueea7\033[0m"


def test(a: poly = None, b: poly = None, display: str = "Test") -> poly:
	print("\33[34m"+display+"\33[0m:")
	if a: print("Dividend " + COLOR, a)
	else: a = poly_input("Dividend " + COLOR + " ", True)
	if b: print("Divisor " + COLOR, b)
	else: b = poly_input("Divisor " + COLOR + " ", True)
	print("Quotient " + COLOR, a // b)
	print("Remainder " + COLOR, a % b)

a = poly(1, 5, 10, 10, 5, 1)
b = poly(1, 4, 4, 1)

test(a, b, "Example")
sleep(1.2)
print("\n")
test(display="Your Turn")
sleep(1.2)
print("\n\33[31mWant to try more?\033[0m")
sleep(1.3)
print("Just type\33[0m in \33[35mtest()\33[0m!")
sleep(1.2)
print()

import wmath, wpoly, parser
while True:
	i = input(COLOR + " \33[35m")
	print(f"\33[F{COLOR} \33[35m{i}\33[0m")
	if i == "": continue
	print()
	if i.lower() == "exit": 
		print("Exiting.")
		break
	e = eval(i)
	if e is not None: print(e)
	print()

