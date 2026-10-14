from typing import List, Dict, Optional
from replit import clear

greyline = "\33[2m" + "-"*32 + "\33[0m"

def sortdlist(dlist: List[Dict], bykeys: List[str]):
	k = {}
	for item in dlist:
		path = k
		for key in bykeys:
			if item[key] not in path:
				path[item[key]] = [] if key == bykeys[-1] else {}
			path = path[item[key]]
		path.append(dlist.index(item))
	new = []
	def finalize(path, i = 1):
		for key in sorted(path.keys()):
			if i == len(bykeys):
				_temp = map(lambda _idx: dlist[_idx], path[key])
				new.extend(_temp)
			else:
				finalize(path[key], i + 1)
	finalize(k)
	return new

def checkinput(key: str or type, prompt: str):
	__types = tuple(personal_data[key]) if type(key) == str else tuple([key])
	_inp = input(prompt)
	if not isinstance(_inp, __types):
		for __t in __types:
			try: return __t(_inp)
			except: pass
	if not isinstance(_inp, __types):
		print("\33[0m", end="")
		return checkinput(key, prompt)
	return _inp

def getprio() -> List[str]:
	_kyz = [*keys]
	_kys = []
	print()
	while len(_kyz) > 1:
		_prompt0 = f"""Sort {amount} people by {listkeys(_kyz)}? \n\t>>> """
		_prompt1 = f"""Then by {listkeys(_kyz)}? \n\t>>> """
		_prompt = _prompt0 if len(_kyz) == len(keys) else _prompt1
		k = input(_prompt).lower().replace(" ","-")
		i = _kyz.index(k) if k in _kyz else 0
		_kys.append(_kyz.pop(i))
		print()
	_kys += _kyz
	del _kyz
	clear()
	return _kys

def listkeys(keys: List[str], sep = ", ", end = "", gfx = None) -> str:
	_s = ""
	sep = ", " if len(keys) > 1 else " "
	for i in keys:
		if i == keys[-1] and len(keys) > 1:
			_s += "\10\10 or "
		_s += f"""\33[3m{i.replace("-"," ").title()}\33[0m{gfx or ""}{end if i == keys[-1] else sep}"""
	return _s

def sortingby():
	print("\33[2mSorting by", listkeys(prio, gfx="\33[2m").replace(" or ", " then "), end = "\33[0m\n\n")

def getpeople():
	_temp = []
	for i in range(amount):
		print("\33[2mPerson", i+1, "/", amount)
		print(greyline)
		_per = {}
		for k in keys:
			_l = (abs(18-len(k)) + 1) * " " + "\33[1m\33[3m"
			_per[k] = checkinput(k, k.replace("-"," ").title() + ":" + _l)
			print("\33[0m", end="")
		_temp.append(_per)
		print(greyline)
		print()
	return _temp

def showpeople(ppl: List[Dict], title: Optional[str] = None):
	if title:
		print("\33[96m"+title+"\33[0m")
		print()
	for i in ppl:
		print(greyline)
		for k in keys:
			_l = (abs(18-len(k)) + 1) * " "
			print(k.replace("-"," ").title() + ":" + _l + i[k])
	print(greyline)
	print()
	print()
	print()


personal_data: Dict[str, List[type]] = {
	"name": [str],
	"age": [int, float],
	"cats-seen": [int]
}
keys: List[str] = list(personal_data.keys())
amount: int = checkinput(int, "How many people to compare? ")
clear()
clear()
people: List[Dict] = getpeople()
prio: List[str] = getprio()
sorted: List[Dict] = sortdlist(people, prio)
showpeople(people, "Unsorted list:")
sortingby()
showpeople(sorted, "Sorted list:")