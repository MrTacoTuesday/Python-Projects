
class Game:
	def __init__(self):
		pass
	def set(self, id: str, value):
		setattr(self, id, value)

game = Game()
game.set("player", 376000)