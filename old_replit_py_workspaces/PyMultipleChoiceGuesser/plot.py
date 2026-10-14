import matplotlib.pyplot as mpl
from datetime import datetime as time


def line(x: list,
         y: list,
         xl: str = "X",
         yl: str = "Y",
         title: str = "",
         filename: str = ""):
	mpl.clf()
	mpl.plot(x, y)
	mpl.xlabel(xl)
	mpl.ylabel(yl)
	mpl.title(title)
	t = time.now().strftime("%Y-%m-%d-%H-%M-%S")
	mpl.savefig(filename + t + ".png")
	mpl.clf()
