import sys, random
from math import sqrt
import pyglet as p
from pyglet.window import key
screen = p.window.Window()
keyboard = key.KeyStateHandler()
screen.push_handlers(keyboard)

def update(dt):
	global aliendir, counter, movedistance, lastbul
	if (counter > movedistance):
		counter = -movedistance
	if (counter >= -1 and counter <= 1) or (counter == movedistance) or (counter == -movedistance):
		aliendir = 'down'
	elif counter < 0:
		aliendir = 'left'
	else:
		aliendir = 'right'
	counter += 1

	delbullets = []
	delinvaders = []

	for inv in invaders:
		if aliendir == 'down':
			inv.y -= 4
		elif aliendir == 'left':
			inv.x -= 2
		elif aliendir == 'right':
			inv.x += 2
		if inv.y < radius:
			sys.exit('Failure? Oh no!')

	if keyboard[key.J]: me.x -= 2
	if keyboard[key.L]: me.x += 2
	if keyboard[key.I]: me.y += 2
	if keyboard[key.K]: me.y -= 2
	if keyboard[key.SPACE] and lastbul>.1:
		bullets.append(p.sprite.Sprite(img=bcirc, x=me.x,y=me.y+radius))
		lastbul = 0
	else:
		lastbul += dt
	if keyboard[key.Q]: sys.exit('Bye bye!')


	if random.randint(0,20) == 0:
		invaders.append(p.sprite.Sprite(img=icirc, x=random.randint(radius*3, width-(radius*3)),y=height))

	for b in range(len(bullets)):
		bul = bullets[b]
		bul.y += 2

		for i in range(len(invaders)):
			inv = invaders[i]
			if sqrt(abs(bul.x - inv.x)**2 + abs(bul.y - inv.y)**2) <= radius:
				if i not in delinvaders: delinvaders.append(i)
				if b not in delbullets: delbullets.append(b)

	list.sort(delinvaders)
	list.sort(delbullets)
	for i in delinvaders[::-1]:
		del(invaders[i])
	for b in delbullets[::-1]:
		del(bullets[b])


@screen.event
def on_draw():
	screen.clear()
	me.draw()
	for inv in invaders:
		inv.draw()
	for b in range(len(bullets)):
		bul = bullets[b]
		bul.draw()

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

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

p.resource.path = ['res']
p.resource.reindex()
circ = p.resource.image('circ.png')
center_image(circ)
icirc = p.resource.image('icirc.png')
center_image(icirc)
bcirc = p.resource.image('bcirc.png')
center_image(bcirc)

aliendir = 1

size = width, height = 600, 400
radius = 10
movedistance = radius * 2
me = p.sprite.Sprite(img=circ, x=width/2,y=height/2)
invaders = []
bullets = []
counter = 0
lastbul = 0

if __name__ == '__main__':
	p.clock.schedule_interval(update, 1/60.0)
	p.app.run()