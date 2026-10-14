from game import game


class Cond:

	def __init__(self,
	             target: str,
	             *lookup: str,
	             mode: str,
	             value: int,
	             once: bool = False):
		self.target = target
		self.lookup = list(lookup)
		self.mode = mode
		self.value = value
		self.once = once
		self.success = False

	def test(self) -> bool:
		if self.once and self.success: return True
		if hasattr(game, self.target):
			rel = getattr(game, self.target, None)
			for i in self.lookup:
				rel = getattr(rel, i, None)
			if self.mode == "is":
				self.success = rel == self.value
			elif self.mode == "lt":
				self.success = rel < self.value
			elif self.mode == "gt":
				self.success = rel > self.value
			elif self.mode == "lte":
				self.success = rel <= self.value
			elif self.mode == "gte":
				self.success = rel >= self.value
			elif self.mode == "custom":
				self.success = self.value(rel)
			else:
				return False
			return self.success
		return False


# a = Cond("player", "level", mode="is", value=32, once=True)
# Cond("player", "level", mode="lte", value = 12)
