from random import randint as r
from utils import inp, format, randsample


def mc(q: int = None,
       c: int = None,
       runs: int = None,
       prints: bool = True) -> int:
	if q is None: q = inp("How many questions >>> ", 10)
	if c is None: c = inp("How many choices >>> ", 4)
	if runs is None: runs = inp("How many re-runs >>> ", 5)
	if prints is not None: print()
	total = 0
	tq = runs * q
	for i in range(runs):
		correct = 0
		for _ in range(q):
			if r(1, c) == 1:
				correct += 1
				total += 1
		if prints: print("Test", i + 1, "\10:\t", correct, "/", q)
	epr = total / tq  # experimental probability
	tpr = 1 / c  # theoretical probability
	pe = abs(1 - c * epr)  # (decimal) percent error
	if prints is not None:
		print()
		print("Average:", total, "/", tq)
		print("Score:", format(epr))
		print("Expected:", format(tpr))
		print("Error:", format(pe))
	return epr


def matching(q: int = None,
             c: int = None,
             runs: int = None,
             prints: bool = True) -> int:
	if q is None: q = inp("How many questions >>> ", 10)
	if c is None: c = inp("How many extra choices >>> ", 2)
	c += q
	if runs is None: runs = inp("How many re-runs >>> ", 5)
	if prints is not None: print()
	total = 0
	tq = runs * q
	for i in range(runs):
		correct = 0
		ans = randsample(1, c, q)
		for a in range(q):
			if a + 1 == ans[a]:
				correct += 1
				total += 1
		if prints: print("Test", i + 1, "\10:\t", correct, "/", q)
	epr = total / tq  # experimental probability
	tpr = 1 / c  # theoretical probability
	pe = abs(1 - c * epr)  # (decimal) percent error
	if prints is not None:
		print()
		print("Average:", total, "/", tq)
		print("Score:", format(epr))
		print("Expected:", format(tpr))
		print("Error:", format(pe))
	return epr

import plot
def matching_xy(qs: int = None,
                ear: int = None,
                tries: int = None,
                plots: bool = False) -> (list, list):
	x, y = [], []
	if qs is None: qs = inp("How many questions >>> ", 10)
	if ear is None: ear = inp("How many extra choices >>> ", 5)
	if tries is None: tries = inp("How many re-runs >>> ", 10000)
	if plots:
		from datetime import datetime as time
		start = time.now()
		print("Starting simulations ...")
	prints = None if plots is None or True else False
	for i in range(ear + 1):
		x.append(int(i))
		y.append(matching(qs, i, tries, prints) * 100)
	if not plots: return (x, y)
	print("\nCompleted", ear + 1, "different simulations with", tries,
	      "tries each in", (time.now() - start).total_seconds(), "seconds.\n\n")
	print("Plot points:")
	for i in range(ear + 1):
		print(str(x[i]) + ": " + str(y[i]))
	print("\n")
	ps = time.now()
	file = (str(qs) + "Qs " + "x" + str(tries) + " Tries x" + str(ear) +
	        " Iterations ")
	xl = "Extra Answers"
	yl = "Average Score Over \0 Runs (%)".replace("\0", str(tries))
	ttl = "\0Q Matching Test: Score vs Extra Answers Count".replace("\0", str(qs))
	print("Starting line graph ...")
	plot.line(x, y, xl, yl, ttl, file)
	print("\nGraph finished in", (time.now() - ps).total_seconds(), "seconds.")
	print("\n\nTotal runtime", (time.now() - start).total_seconds(), "seconds.")
	return (x, y)
