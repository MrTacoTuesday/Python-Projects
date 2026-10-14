from functools import reduce
from replit import clear as _cls
from time import sleep
#import credits ## Fancy intro (shown in the video)

Temps = ["Farenheit", "Celsius", "Kelvin"]
Temp = Temps[0]


def clear():
	_cls()
	print('''


 				\33[1;35mTemperature Statistics\33[0m
	 
''')
	print("----"*15)


def temp(_temp) -> str:
	if _temp is None:
		_temp = "?"
	elif isinstance(_temp, (int, float)):
		_temp = round(float(_temp), 1)
	return str(_temp) + "°" + Temp[0]


def avg(args: list) -> float:
	args = map(float, filter(lambda i: i is not None, args))
	args = list(args)
	if len(args) > 1:
		avg = reduce(float.__add__, args) / len(args)
	else:
		avg = args[0]
	return avg


def median(args: list) -> float:
	args = map(float, filter(lambda i: i is not None, args))
	args = list(sorted(args))
	if len(args) % 2 == 0:
		_i = len(args) // 2
		return avg(args[_i:_i + 1])
	return args[len(args) // 2]

def maximum(args: list) -> float:
	args = list(sorted(filter(lambda i: i is not None, args)))
	if not len(args):
		return None
	return args[-1]

def minimum(args: list) -> float:
	args = list(sorted(filter(lambda i: i is not None, args)))
	if not len(args):
		return None
	return args[0]
	

def stddev(args: list, _avg: float = None) -> float:
	args = list(filter(lambda i: i is not None, args))
	if not len(args): return None
	if _avg is None: _avg = avg(args)
	_ret = 0
	for xn in args:
		_ret += (xn - _avg)**2
	_ret /= len(args)
	return _ret**0.5


def statistics(place: "Place") -> list:
	return [
	 	("Average Temp", avg(place.__lows__ + place.__highs__)),
		("Lowest Temp", minimum(place.__lows__)),
	 	("Median Temp", median(place.__lows__ + place.__highs__)),
		("Highest Temp", maximum(place.__highs__)),
		("Lowest High", minimum(place.__highs__)),
	 	("Highest Low", maximum(place.__lows__)),
		("Standard Dev.", stddev(place.__highs__ + place.__lows__)),
	]


class Day:

	def __init__(self, _high: int = None, _low: int = None):
		if _high is None and _low is None:
			raise ValueError("high and low cannot both be None")
		high = max(_high, _low)
		low = min(_high, _low)
		self.high = high
		self.low = low
		if high and low:
			self.avg: float = (high + low) / 2
		else:
			self.avg = high if high is not None else low

	def __repr__(self):
		return temp(self.avg)

	def long(self) -> str:
		return f"{self} \33[2m(↑{temp(self.high)} ↓{temp(self.low)})\33[0m"

	def input(number: int = None) -> "Day":
		if number:
			print("Day", number)
		h = input(f"""High for the day ({temp("")}): """)
		l = input(f"""Low for the day ({temp("")}): """)
		return Day(None if h == "" else int(h), None if l == "" else int(l))


class Place:

	def __init__(self, name: str, data: list):
		self.name = name
		self.data = data
		self.__highs__ = list(map(lambda i: i.high, self.data))
		self.__lows__ = list(map(lambda i: i.low, self.data))

	def title(self) -> str:
		return f"{self.name}'{'s' if self.name[-1] != 's' else ''} {len(self.data)}-day temperature"

	def long(self) -> str:
		return f"{self.title()} data:\n{self.days()}"

	def stats(self):
		#clear()
		print(self.long())
		print()
		print(self.title(), "statistics:")
		for stat in statistics(self):
			space = abs(13 - len(stat[0]))
			print(f"{stat[0]}  {space*' '}- ", temp(stat[1]))

	def days(self) -> str:
		_a = map(lambda i: f"Day #{self.data.index(i)+1}: \t{i.long()}", self.data)
		return reduce(lambda a, b: f"{a}\n{b}", _a)

	def input() -> "Place":
		name = input("What place do you have data for? ")
		days = []
		for i in range(int(input("How many days to record? ") or 1) or 1):
			print()
			days.append(Day.input(i + 1))
		print()
		return Place(name, days)


def example():
	Place("Evans, Georgia", [
		 Day(76, 56),
		 Day(80, 63),
		 Day(83, 60),
		 Day(74, 60),
		 Day(70, 51),
		 Day(70, 52),
		 Day(75, 50),
		 Day(71, 48),
		 Day(77, 55),
		 Day(75, 54),
	]).stats()
	sleep(4)


def run():
	Place.input().stats()


clear()
while True:
	_inp = input("\33[33m\33[0m ")
	if _inp == "exit": break
	elif _inp == "exit()": break
	elif not _inp: continue
	else:
		try:
			_ret = eval(_inp)
			if _ret is not None: 
				print(f"\n\33[1;2m{_ret}\33[0m")
		except Exception as e:
			raise e
			try:
				_ret = exec(_inp)
				if _ret is not None: 
					print(f"\n\33[1;2m{_ret}\33[0m")
			except:
				print(f"\n\t\33[2;31mUnknown Input: \33[36m`{_inp}`\33[0m")
	print()

#credits.out() ## Fancy outro (shown in the video)