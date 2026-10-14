from random import randint
from functools import reduce


class v2:

	def __init__(self, *shift: int, mul: int = None):
		if not (shift and len(shift) and mul): s = v2.new()
		self.shiftlen = len(list(shift)) or s.shiftlen
		self.shift = tuple(shift) or s.shift
		self.mul = mul or s.mul

	def new(shifts: int = None, shiftdeg: int = None, muldeg: int = None):
		sl = shifts or randint(2, 10)
		sc = 2**(shiftdeg or 12) - 1
		mc = 2**(muldeg or 5)
		lst = []
		for i in range(0, sl):
			lst.append(randint(0, sc))
		return v2(*lst, mul=randint(1, mc))

	def encrypt(self, message: str) -> bytes:
		#Unicode values range: [0,55296) 235**2+70 = 55295
		lst = []
		for i in range(0, len(message)):
			c = ord(message[i])
			c += self.shift[i % self.shiftlen]
			c *= self.mul
			lst.append(c // 55296)
			lst.append(c % 55296)
		return reduce(lambda x, y: x + chr(y), lst, "").encode("utf-8")

	def decrypt(self, encryption: bytes) -> str:
		lst = []
		encryption = encryption.decode("utf-8")
		for i in range(0, len(encryption), 2):
			c = ord(encryption[i]) * 55296 + ord(encryption[i + 1])
			c //= self.mul
			c -= self.shift[(i // 2) % self.shiftlen]
			lst.append(c)
		return reduce(lambda x, y: x + chr(y), lst, "")

	def __repr__(self):
		return repr(self.shift).replace(")", ", mul = " + str(self.mul) + ")")


def test(key: v2, message: str):
	print("Key: ", key)
	print("Secret Message: \"", message, "\"", sep="")
	print()

	secret = key.encrypt(message)

	print("Ciphertext: \n", secret, sep="\n")
	print()
	print()

	recieved = key.decrypt(secret)

	print("Deciphered Message: \"", recieved, "\"", sep="")


def trydecrypt(key: v2, msg: bytes):
	try:
		print(key.decrypt(msg))
	except:
		print("Error: Invalid Key For Phrase")