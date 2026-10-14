"""
Board {
	[Tile: {
 		pos = (r,c)	
   		color: (r,g,b)
 		Piece: {
   			color: (r,g,b)
	  		ontile: Tile
	  		def move(r,c)->bool 
		}?
	} * 64]
}
"""

from enum import Enum


class PieceType(Enum):
	Rook = 0x2656
	Knight = 0x2658
	Bishop = 0x2657
	Queen = 0x2655
	King = 0x2654
	Pawn = 0x2659

	def chr(self, color: "PieceColor") -> str:
		return chr(self.value + (6 if color is PieceColor.Black else 0))


from ANSI import ANSI


class PieceColor(Enum):
	Black = ANSI.TextColor.format(60, 60, 60)
	White = ANSI.TextColor.format(240, 240, 255)

	def colorize(self, type: PieceType) -> str:
		return ANSI.wrap(self.value, type.chr(self), ANSI.TextDefault)


class Piece:

	def __init__(self, type: PieceType, color: PieceColor):
		self.name = color.name + " " + type.name
		self.type = type
		self.color = color
		self._txt_ = color.colorize(type)
		self._tile_ = None
		self._moved_ = False

	def settile(self, tile: "Tile"):
		self._tile_ = tile
		tile._piece_ = self

	@property
	def tile(self) -> "Tile":
		return self._tile_

	@property
	def moved(self) -> bool:
		return self._moved_

	def __repr__(self) -> str:
		return self._txt_


class TileColor(Enum):
	Black = ANSI.BGColor.format(37, 32, 37)
	White = ANSI.BGColor.format(175, 170, 175)

	def _colorize(self, str: str) -> str:
		return ANSI.wrap(self.value, str, ANSI.BGDefault)

	def colorize(self, piece: Piece or None) -> str:
		return self._colorize("  " if piece is None else piece._txt_)

	def pos(col: str, row: int)->"TileColor":
		black = ("abcdefgh".index(col) + row - 1) % 2 == 0
		return TileColor.Black if black else TileColor.White


class Tile:

	COLUMNS = "abcdefgh"
	ROWS = tuple(range(1,8))
	
	def __init__(self, col: str, row: int):
		self.col = col
		self.row = row
		self.color = TileColor.pos(col, row)
		self._piece_: Piece = None

	@property
	def has_piece(self) -> bool:
		return self._piece_ is not None

	def iscell(self, col: str, row: int) -> bool:
		return self.col == col and self.row == row

	def can_place(self, piece: Piece)->bool:
		if not self.has_piece: 
			return True
		if self._piece_.color is piece.color:
			return False

	def __repr__(self) -> str:
		return self.color.colorize(self._piece_)

board = {
	
}
for col in Tile.COLUMNS:
	for row in Tile.ROWS:
		print(col, row, Tile(col, row), "end")

	


print(Piece(PieceType.Knight, PieceColor.Black))
