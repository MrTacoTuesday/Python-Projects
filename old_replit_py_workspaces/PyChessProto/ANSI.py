from enum import Enum
from Utils import iter_str


# With help from::
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
class ANSI(Enum):
	Reset = 0
	Bold = 1
	Faint = 2
	Italic = 3
	Underline = 4
	BlinkSlow = 5
	BlinkFast = 6
	InvertColor = 7
	Conceal = 8
	Strikethrough = 9
	FontDefault = 10
	Font1 = 11
	Font2 = 12
	Font3 = 13
	Font4 = 14
	Font5 = 15
	Font6 = 16
	Font7 = 17
	Font8 = 18
	Font9 = 19
	UnderlineDouble = 21
	NormalIntensity = 22
	ItalicOff = 23
	UnderlineOff = 24
	BlinkOff = 25
	InvertOff = 27
	ConcealOff = 28
	StrikethroughOff = 29
	TextBlack = 30
	TextRed = 31
	TextGreen = 32
	TextYellow = 33
	TextBlue = 34
	TextMagenta = 35
	TextCyan = 36
	TextWhite = 37
	TextColor = (38, [(5, "n"), (2, "r", "g", "b")])
	TextDefault = 39
	BGBlack = 40
	BGRed = 41
	BGGreen = 42
	BGYellow = 43
	BGBlue = 44
	BGMagenta = 45
	BGCyan = 46
	BGWhite = 47
	BGColor = (48, [(5, "n"), (2, "r", "g", "b")])
	BGDefault = 49
	BorderFramed = 51
	BorderEncircled = 52
	Overline = 53
	BorderOff = 54
	OverlineOff = 55
	TextBrightBlack = 90
	TextBrightRed = 91
	TextBrightGreen = 92
	TextBrightYellow = 93
	TextBrightBlue = 94
	TextBrightMagenta = 95
	TextBrightCyan = 96
	TextBrightWhite = 97
	BGBrightBlack = 100
	BGBrightRed = 101
	BGBrightGreen = 102
	BGBrightYellow = 103
	BGBrightBlue = 104
	BGBrightMagenta = 105
	BGBrightCyan = 106
	BGBrightWhite = 107

	def format(self, *args: int) -> str:
		if type(self.value) == int:
			return str(self.value)
		(_id, _args) = self.value
		_build = str(_id)
		_valid = []
		for (__id, *__args) in _args:
			if len(args) == len(__args):
				_build += f":{__id}"
				if __id in range(2, 5): _build += ":"
				for _int in args:
					_build += f":{_int}"
				break
			else:
				_valid.append("(" + iter_str(__args, lambda i: str(i) + ": int") + ")")
		if _build == str(_id):
			_err = f"""Expected arguments to match {iter_str(_valid, str, last=" or ")}; got {tuple(args)} instead"""
			raise ValueError(_err)
		return _build

	def combine(*allOf: "ANSI" or str) -> str:
		_res = ""
		for i in allOf:
			_res += i if type(i) is str else i.format()
			if allOf[-1] is not i:
				_res += ";"
		return _res

	def finalize(val: "ANSI" or str) -> str:
		if type(val) == str:
			if "m" in val or val == "": return val
		else:
			return ANSI.finalize(val.format())
		return f"""\33[{val}m"""

	def wrap(code: "ANSI" or str, txt: str, endcode: "ANSI" or str = "") -> str:
		return ANSI.finalize(code) + txt + ANSI.finalize(endcode)