import sys, random
from math import sqrt
import pyglet as p
from pyglet.window import key
screen = p.window.Window()
keyboard = key.KeyStateHandler()
screen.push_handlers(keyboard)
screen.set_exclusive_mouse(True)

def update(dt):
	global lastgate
	if keyboard[key.Q]: sys.exit('Bye bye!')
	for g in gates:
		g.x-=2
		if g.x < width/2 and g.image is bgate:
			if abs(me.y - g.y) < (g.height/2 - radius):
				g.image=ggate
			else:
				g.image=rgate
	if level == 1:
		me.y = mouse_pos[1]
		me.y = constrain(me.y, radius, height-radius)


	if random.random()*3 + lastgate > 4:
		gates.append(p.sprite.Sprite(img=bgate, x=width,y=int(random.randint(bgate.height, height-bgate.height))))
		lastgate = 0
	else:
		lastgate += dt
	for g in range(len(gates)-1,0,-1):
		if gates[g].x < 0:
			del(gates[g])

@screen.event
def on_draw():
	screen.clear()
	me.draw()
	for g in gates:
		g.draw()


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

@screen.event
def on_mouse_motion(x, y, dx, dy):
	global mouse_pos
	mouse_pos[1] += dy

p.resource.path = ['res']
p.resource.reindex()
circ = p.resource.image('circ.png')
center_image(circ)
ggate = p.resource.image('ggate.png')
center_image(ggate)
rgate = p.resource.image('rgate.png')
center_image(rgate)
bgate = p.resource.image('bgate.png')
center_image(bgate)

size = width, height = 640, 480
radius = 10
mouse_pos = [0, 0]
level = 1
lastgate = 0

def constrain(val, minv, maxv):
	if val < minv:
		return minv
	elif val>maxv:
		return maxv
	else:
		return val

me = p.sprite.Sprite(img=circ, x=width/2,y=height/2)
gates = []

if __name__ == '__main__':
	p.clock.schedule_interval(update, 1/60.0)
	p.app.run()