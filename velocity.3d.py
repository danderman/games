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
	bufnext = bufnext % bufsize
	bufprev = bufpos - 1
	if bufprev == -1:
		bufprev = bufsize -1

	x_pbuf[bufpos] = mousex_pos
	y_pbuf[bufpos] = mousey_pos
	pos.append(p.sprite.Sprite(img=pl, x=width//2-radius, y=y_pbuf[bufpos], batch=lines))
	x_pdbuf[bufpos] = mousex_pos - x_pbuf[bufprev]
	y_pdbuf[bufpos] = mousey_pos - y_pbuf[bufprev]
	x_vbuf[bufpos] = sum(x_pdbuf) / bufsize + height / 2
	y_vbuf[bufpos] = sum(y_pdbuf) / bufsize + height / 2
	v.append(p.sprite.Sprite(img=vl, x=width//2-radius, y=y_vbuf[bufpos], batch=lines))
	x_vdbuf[bufpos] = 3 * (x_vbuf[bufpos] - x_vbuf[bufprev]) # straight acceleration isn't responsive enough
	y_vdbuf[bufpos] = 3 * (y_vbuf[bufpos] - y_vbuf[bufprev]) # straight acceleration isn't responsive enough
	x_abuf[bufpos] = sum(x_vdbuf) / bufsize + height / 2
	y_abuf[bufpos] = sum(y_vdbuf) / bufsize + height / 2
	a.append(p.sprite.Sprite(img=al, x=width//2-radius, y=y_abuf[bufpos], batch=lines))
	if level == 1:
		me.x = mousex_pos
		me.y = mousey_pos
	elif level == 2:
		me.x = x_vbuf[bufpos]
		me.y = y_vbuf[bufpos]
	elif level == 3:
		me.x = x_abuf[bufpos]
		me.y = y_abuf[bufpos]


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
	global mousey_pos, mousex_pos
	mousey_pos += dy
	mousex_pos += dx

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
mousey_pos = height//2
mousex_pos = width//2
level = 1
levelcnt = 0
points = 0
lastgate = 0
bufsize = 10
x_pbuf = [height/2] * bufsize
x_pdbuf = [0] * bufsize
x_vbuf = [0] * bufsize
x_vdbuf = [0] * bufsize
x_abuf = [0] * bufsize
y_pbuf = [height/2] * bufsize
y_pdbuf = [0] * bufsize
y_vbuf = [0] * bufsize
y_vdbuf = [0] * bufsize
y_abuf = [0] * bufsize
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