# Import required library
import turtle

class PongGame:
	def __init__(self):
		self.sc = PongGame.__screen()
		self.p1 = PongGame.__paddle()
		self.p2 = PongGame.__paddle()
		self.ball = PongGame.__ball()
		self.scoreboard = PongGame.__scoreDisplay()
		self.p1score = 0
		self.p2score = 0
		self.winningscore = 10
	def __screen():
		scr = turtle.Screen()
		scr.title("Pong game")
		scr.bgcolor("white")
		scr.setup(width=1000, height=600)
		return scr
	def __paddle():
		p = turtle.Turtle()
		p.speed(0)
		p.shape("square")
		p.color("black")
		p.shapesize(stretch_wid=6, stretch_len=2)
		p.penup()
		p.goto(-400, 0)
		return p
	def __ball():
		b = turtle.Turtle()
		b.speed(40)
		b.shape("circle")
		b.color("blue")
		b.penup()
		b.goto(0, 0)
		b.dx = -5
		b.dy = 0
		return b
	def __scoreDisplay():
		d = turtle.Turtle()
		d.speed(0)
		d.color("blue")
		d.penup()
		d.hideturtle()
		d.goto(0,260)
		PongGame.__updateScore(d,0,0)
		return d
	def __updateScore(d: turtle.Turtle, p1, p2):
		d.clear()
		d.write(f"P1: {p1}		P2: {p2}",
			False,"center",("Courier",24,"normal"))
	def __updatescore(self):
		PongGame.__updateScore(self.scoreboard,self.p1score,self.p2score)
	def movep1(self, dir = "up"):
		y = self.p1.ycor()
		y += 20 * 1 if dir == "up" else -1
		self.p1.sety(y)
	def movep2(self, dir = "up"):
		y = self.p2.ycor()
		y += 20 * 1 if dir == "up" else -1
		self.p2.sety(y)
	def __updateball(self):
		# Move ball with constant speed
		self.ball.setx(self.ball.xcor()+self.ball.dx)
		self.ball.sety(self.ball.ycor()+self.ball.dy)
		# Check for wall collision, flip direction if true
		if self.ball.ycor() > 280:
			self.ball.sety(280)
			self.ball.dy *= -1
		if self.ball.ycor() < -280:
			self.ball.sety(-280)
			self.ball.dy *= -1
		if self.ball.xcor() > 500:
			self.ball.goto(0,0) # back to the middle
			self.ball.dy *= -1
			self.p1score += 1 # Got past p2, +1 pt
			self.__updatescore()
		if self.ball.xcor() < -500:
			self.ball.goto(0,0) # back to the middle
			self.ball.dy *= -1
			self.p2score += 1 # Got past p1, +1 pt
			self.__updatescore()
		# Check for paddle collision
		if (self.ball.xcor() > 360 and self.ball.xcor() < 370) and (self.ball.ycor() < self.p2.ycor()+40 and self.ball.ycor() > self.p2.ycor()-40):
			self.ball.setx(360)
			self.ball.dx *= -1
		if (self.ball.xcor() < -360 and self.ball.xcor() > -370) and (self.ball.ycor() < self.p2.ycor()+40 and self.ball.ycor() > self.p2.ycor()-40):
			self.ball.setx(-360)
			self.ball.dx *= -1
	def run(self):
		self.sc.listen()
		while self.p1score != self.winningscore and self.p2score != self.winningscore:
			self.sc.update()
			self.__updateball()
	def p1keys(self, keys: (str,str)):
		(upkey,downkey) = keys
		self.sc.onkeypress(self.movep1("up"),upkey)
		self.sc.onkeypress(self.movep1("down"),downkey)
	def p2keys(self, keys: (str,str)):
		(upkey,downkey) = keys
		self.sc.onkeypress(self.movep2("up"),upkey)
		self.sc.onkeypress(self.movep2("down"),downkey)
	def setwinscore(self,i):
		self.winningscore = i
game = PongGame()
game.p1keys(("w","s"))
game.p2keys(("Up","Down"))
game.run()
