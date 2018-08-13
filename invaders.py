import sys, random
from math import sqrt
import pygame as p

aliendir = 1

def main():
	global aliendir
	p.display.init()

	size = width, height = 600, 400
	radius = 10
	movedistance = radius * 2
	mycolor = (0,0,255)
	aliencolor = (0,255,0)
	bulletcolor = (255,0,0)
	myloc = [int(width/2),int(height-radius)]
	black = (0, 0, 0)
	invaders = []
	bullets = []
	counter = 0
	screen = p.display.set_mode(size)

	while 1:
		for event in p.event.get():
			if event.type == p.QUIT: sys.exit()

		if (counter > movedistance):
			counter = -movedistance
		if (counter >= -1 and counter <= 1) or (counter == movedistance) or (counter == -movedistance):
			aliendir = 'down'
		elif counter < 0:
			aliendir = 'left'
		else:
			aliendir = 'right'
		counter += 1

		keys = p.key.get_pressed()
		if keys[p.K_j]: myloc[0] -= 2
		if keys[p.K_l]: myloc[0] += 2
		if keys[p.K_i]: myloc[1] -= 2
		if keys[p.K_k]: myloc[1] += 2
		if keys[p.K_SPACE]:
			bullets.append(Bullet(myloc[0],myloc[1]-radius,2,bulletcolor))

		if random.randint(0,20) == 0:
			invaders.append(Invader(random.randint(radius*3, width-(radius*3)), -radius, radius, aliencolor))

		screen.fill(black)
		p.draw.circle(screen,mycolor,myloc,radius)

		delbullets = []
		delinvaders = []

		for inv in invaders:
			inv.draw(screen)
			if inv.y > height - radius:
				sys.exit('Failure? Oh no!')
		for b in range(len(bullets)):
			bul = bullets[b]
			bul.draw(screen)
			for i in range(len(invaders)):
				inv = invaders[i]
				if sqrt(abs(bul.x - inv.x)**2 + abs(bul.y - inv.y)**2) <= radius:
					if i not in delinvaders: delinvaders.append(i)
					if b not in delbullets: delbullets.append(b)

		for i in delinvaders[::-1]:
			del(invaders[i])
		for b in delbullets[::-1]:
			del(bullets[i])

		p.display.flip()
		p.time.wait(20)

class Invader:
	def __init__(self, x, y, r, color):
		self.x = x
		self.y = y
		self.r = r
		self.color = color
		
	def draw(self,screen):
		global aliendir
		if aliendir == 'down':
			self.y += 4
		elif aliendir == 'left':
			self.x -= 2
		elif aliendir == 'right':
			self.x += 2

		p.draw.circle(screen,self.color,(self.x,self.y),self.r)

class Bullet:
	def __init__(self, x, y, r, color):
		self.x = x
		self.y = y
		self.r = r
		self.color = color
		
	def draw(self,screen):
		global aliendir
		self.y -= 2

		p.draw.circle(screen,self.color,(self.x,self.y),self.r)


if __name__ == '__main__':
	main()