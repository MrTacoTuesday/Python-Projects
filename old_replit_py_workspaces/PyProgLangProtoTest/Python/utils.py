def inp(prompt: str, default: int) -> int:
	i = input(prompt)
	if not i: 
		print("\t(Defaulted to", default, "\10)")
	return int(i or default)


def format(i: int, d: int = 3) -> str:
	return str(int(100 * i * 10**d) / 10**d) + "%"

from random import randint, sample
def randlist(min: int, max: int, count: int)->list:
	lst = []
	for i in range(count): 
		lst.append(randint(min, max))
	return lst

def randsample(min: int, max: int, count: int)->list:
	lst = []
	for i in range(min,max+1): lst.append(i)
	return sample(lst, count)

import sys
def unprint():
	sys.stdout.write("\033[F")
	sys.stdout.write("\033[K")

import time
def dotdotdot(prompt: str, delay: float = 0.5, dots: int = 3):
	m = {"dots": 0}
	def increment(finished: bool = False):
		#if m["dots"] == 0: print()
		dc = m["dots"] % dots + 1
		print("\r" + prompt + "."*dc + " "*(dots-dc), end="")
		m["dots"] = dc
		if finished: print()
		time.sleep(delay)
	return increment

from threading import Thread
def load():
	a = dotdotdot("Loading", 0.385, 4)
	loading = True
	def _l(): 
		while loading: 
			a(not loading)
	thread = Thread(target=_l)
	thread.start()
	loading = input() and False
	del thread
	unprint()