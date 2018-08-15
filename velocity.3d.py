import sys, random
from math import sqrt
import pyglet as p
p.options['debug_gl'] = False
from pyglet.window import key
screen = p.window.Window(900, 900)
keyboard = key.KeyStateHandler()
screen.push_handlers(keyboard)
screen.set_exclusive_mouse(True)

def update(dt):
	global lastgate, bufpos, level, levelcnt, points
	if keyboard[key.Q]: sys.exit('You got %s points' % (points,))
	for g in pos:
		g.x-=2
	for g in v:
		g.x-=2
	for g in a:
		g.x-=2
	for g in gates:
		g.scale -= scaledelta
		g.opacity = constrain(opacitydelta+g.opacity, 0, 255)
		if g.scale < 1 and g.image is sbgate:
			if abs(me.y - g.y) < (g.height/2 - radius):
				if abs(me.x - g.x) < (g.height/2 - radius):
					g.image=sggate
					points += 1
				else:
					g.image=srgate
			else:
				g.image=srgate

	bufnext = bufpos + 1
	bufnext = bufnext % len(pbuf)
	bufprev = bufpos - 1
	if bufprev == -1:
		bufprev = len(pbuf) -1

	pbuf[bufpos] = mouse_pos
	pos.append(p.sprite.Sprite(img=pl, x=width//2-radius, y=pbuf[bufpos], batch=lines))
	pdbuf[bufpos] = mouse_pos - pbuf[bufprev]
	vbuf[bufpos] = sum(pdbuf) / len(pdbuf) + height / 2
	v.append(p.sprite.Sprite(img=vl, x=width//2-radius, y=vbuf[bufpos], batch=lines))
	vdbuf[bufpos] = 3 * (vbuf[bufpos] - vbuf[bufprev]) # straight acceleration isn't responsive enough
	abuf[bufpos] = sum(vdbuf) / len(vdbuf) + height / 2
	a.append(p.sprite.Sprite(img=al, x=width//2-radius, y=abuf[bufpos], batch=lines))
	if level == 1:
		me.y = mouse_pos
	elif level == 2:
		me.y = vbuf[bufpos]
	elif level == 3:
		me.y = abuf[bufpos]


	me.y = constrain(me.y, radius, height-radius)

	bufpos = bufnext

	if random.random()*3 + lastgate > 4:
		gates.append(p.sprite.Sprite(img=sbgate, x=int(random.randint(sbgate.width//2, width-sbgate.width//2)),y=int(random.randint(sbgate.height//2, height-sbgate.height//2))))
		gates[-1].scale = 3
		gates[-1].opacity = 64
		lastgate = 0
		levelcnt += 1
	else:
		lastgate += dt
	for g in range(len(gates)-1,-1,-1):
		if gates[g].scale < 0:
			del(gates[g])
	for g in range(len(pos)-1,0,-1):
		if pos[g].x < 0:
			del(pos[g])
	for g in range(len(v)-1,0,-1):
		if v[g].x < 0:
			del(v[g])
	for g in range(len(a)-1,0,-1):
		if a[g].x < 0:
			del(a[g])
	if levelcnt == 20:
		level = 2
	elif levelcnt == 40: 
		level = 3
	status.text = 'Level: %s, Points: %s, Pos: %s' % (level, points, me.y)

@screen.event
def on_draw():
	p.gl.glPolygonMode(p.gl.GL_FRONT_AND_BACK, p.gl.GL_FILL);
	screen.clear()
	me.draw()
	for g in gates:
		g.draw()
	lines.draw()
	status.draw()
	p.gl.glPolygonMode(p.gl.GL_FRONT_AND_BACK, p.gl.GL_LINE);
	p.graphics.draw(4, p.gl.GL_POLYGON,
    ('v2i', (upper_left_x,upper_left_y, upper_right_x, upper_right_y, lower_right_x,lower_right_y, lower_left_x, lower_left_y)))


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

@screen.event
def on_mouse_motion(x, y, dx, dy):
	global mouse_pos
	mouse_pos += dy

p.resource.path = ['/Users/notme/devel/games/res']
p.resource.reindex()
circ = p.resource.image('circ.png')
center_image(circ)
ggate = p.resource.image('ggate.png')
center_image(ggate)
rgate = p.resource.image('rgate.png')
center_image(rgate)
bgate = p.resource.image('bgate.png')
center_image(bgate)
sggate = p.resource.image('sggate.png')
center_image(sggate)
srgate = p.resource.image('srgate.png')
center_image(srgate)
sbgate = p.resource.image('sbgate.png')
center_image(sbgate)

pl = p.resource.image('pl.png')
vl = p.resource.image('vl.png')
al = p.resource.image('al.png')

size = width, height = screen.width, screen.height
scaledelta = width / sggate.width / 500
opacitydelta = 2
radius = 10
mouse_pos = 0
level = 1
levelcnt = 0
points = 0
lastgate = 0
pbuf = [height/2] * 10
pdbuf = [0] * 10
vbuf = [0] * 10
vdbuf = [0] * 10
abuf = [0] * 10
bufpos = 0
status = p.text.Label('', x=width//2, y=radius, anchor_x='center')
upper_left_x = 50
upper_left_y = 950
upper_right_x = 950
upper_right_y = 950
lower_left_x = 50
lower_left_y = 50
lower_right_x = 950
lower_right_y = 50

def constrain(val, minv, maxv):
	if val < minv:
		return minv
	elif val>maxv:
		return maxv
	else:
		return val

me = p.sprite.Sprite(img=circ, x=width/2,y=height/2)
gates = []
a = []
v = []
pos = []
lines = p.graphics.Batch()


if __name__ == '__main__':
	p.clock.schedule_interval(update, 1/60.0)
	p.app.run()