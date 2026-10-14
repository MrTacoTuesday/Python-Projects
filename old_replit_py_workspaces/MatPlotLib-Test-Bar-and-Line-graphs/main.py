import matplotlib.pyplot as mpl

def line(x, y, xl = "X", yl = "Y", title = "", file = "line.png"):
	mpl.clf()
	mpl.plot(x, y)
	mpl.xlabel(xl)
	mpl.ylabel(yl)
	mpl.title(title)
	mpl.savefig(file)
	mpl.clf()

def bar(x, y, xl = "X", yl = "Y", title = "", file = "bar.png"):
	mpl.clf()
	mpl.bar(x, y)
	mpl.xlabel(xl)
	mpl.ylabel(yl)
	mpl.title(title)
	mpl.savefig(file)
	mpl.clf()

bar(
	["Wednesday","Thursday","Friday","Saturday"],
	[6,5,4,2],
	xl = "Day",
	yl = "Amount of Fruit & Vegetable Servings",
	title = "Fruit and Vegetable Consumption"
)