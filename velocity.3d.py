import sys, random
import pyglet as p
p.options['debug_gl'] = False
from pyglet.window import key

screen = p.window.Window(850, 850)
keyboard = key.KeyStateHandler()
screen.push_handlers(keyboard)
screen.set_exclusive_mouse(True)

def update(dt):
	if keyboard[key.Q]: sys.exit('You got %s points' % (g.points,))
	if g.mode == 'start':
		if keyboard[key.SPACE]:
			g.play()
		return
	if g.gatesmissed > g.maxgatesmissed: g.die(g.points)
	for l in g.pos:
		l.x-=2
	for l in g.v:
		l.x-=2
	for l in g.a:
		l.x-=2
	for gt in g.gates:
		gt.scale *= g.spritescaledelta
		xdiff = (gt.right - gt.left)
		ydiff = (gt.top - gt.bottom)
		gt.top -= ydiff * g.scaledelta
		gt.bottom += ydiff * g.scaledelta
		gt.right -= xdiff * g.scaledelta
		gt.left += xdiff * g.scaledelta
		gt.x = gt.left + gt.x_percent * xdiff
		gt.y = gt.bottom + gt.y_percent * ydiff
		gt.opacity = constrain(g.opacitydelta+gt.opacity, 0, 255)
		if gt.scale < 1 and gt.image is g.sbgate:
			if g.me.y - g.radius > gt.y and g.me.y + g.radius < gt.y + gt.height:
				if g.me.x - g.radius > gt.x and g.me.x + g.radius < gt.x + gt.width:
					gt.image=g.sggate
					g.points += 1
				else:
					gt.image=g.srgate
					g.gatesmissed += 1
			else:
				gt.image=g.srgate
				g.gatesmissed += 1

	bufpos = g.bufpos
	bufnext = bufpos + 1
	bufnext = bufnext % g.bufsize
	bufprev = bufpos - 1
	if bufprev == -1:
		bufprev = g.bufsize -1

	g.x_pbuf[bufpos] = g.mousex_pos
	g.y_pbuf[bufpos] = g.mousey_pos
	g.pos.append(p.sprite.Sprite(img=g.pl, x=g.left, y=g.y_pbuf[bufpos], batch=g.lines))
	g.x_pdbuf[bufpos] = g.mousex_pos - g.x_pbuf[bufprev]
	g.y_pdbuf[bufpos] = g.mousey_pos - g.y_pbuf[bufprev]
	g.x_vbuf[bufpos] = sum(g.x_pdbuf) / g.bufsize + g.center_x
	g.y_vbuf[bufpos] = sum(g.y_pdbuf) / g.bufsize + g.center_y
	g.v.append(p.sprite.Sprite(img=g.vl, x=g.left, y=g.y_vbuf[bufpos], batch=g.lines))
	g.x_vdbuf[bufpos] = 4 * (g.x_vbuf[bufpos] - g.x_vbuf[bufprev]) # straight acceleration isn't responsive enough
	g.y_vdbuf[bufpos] = 4 * (g.y_vbuf[bufpos] - g.y_vbuf[bufprev]) # straight acceleration isn't responsive enough
	g.x_abuf[bufpos] = sum(g.x_vdbuf) / g.bufsize + g.height / 2
	g.y_abuf[bufpos] = sum(g.y_vdbuf) / g.bufsize + g.height / 2
	g.a.append(p.sprite.Sprite(img=g.al, x=g.left, y=g.y_abuf[bufpos], batch=g.lines))
	if g.level == 1:
		g.me.x = g.mousex_pos
		g.me.y = g.mousey_pos
	elif g.level == 2:
		g.me.x = g.x_vbuf[bufpos]
		g.me.y = g.y_vbuf[bufpos]
	elif g.level == 3:
		g.me.x = g.x_abuf[bufpos]
		g.me.y = g.y_abuf[bufpos]


	g.me.x = constrain(g.me.x, g.left+g.radius, g.right-g.radius)
	g.me.y = constrain(g.me.y, g.bottom+g.radius, g.top-g.radius)

	g.bufpos = bufnext

	if random.random()*3 + g.lastgate > 4.5:
		gate = p.sprite.Sprite(img=g.sbgate, x=int(random.randint(1, g.width-(g.sbgate.width*3))),y=int(random.randint(1, g.height-(g.sbgate.height*3))))
		#gate = p.sprite.Sprite(img=sbgate, x=1,y=width-(sbgate.width*3))
		gate.scale = 3
		gate.opacity = 32
		gate.x_percent = (gate.x/g.width)
		gate.y_percent = (gate.y/g.height)
		gate.left, gate.right, gate.top, gate.bottom=1,g.width-1,g.height-1,1
		g.gates.append(gate)
		g.lastgate = 0
		g.levelcnt += 1
	else:
		g.lastgate += dt
	for gt in range(len(g.gates)-1,-1,-1):
		if g.gates[gt].scale < 0.5:
			del(g.gates[gt])
	for i in range(len(g.pos)-1,0,-1):
		if g.pos[i].x < 0:
			del(g.pos[i])
	for i in range(len(g.v)-1,0,-1):
		if g.v[i].x < 0:
			del(g.v[i])
	for i in range(len(g.a)-1,0,-1):
		if g.a[i].x < 0:
			del(g.a[i])

	if g.levelcnt == 10:
		for gt in g.gates:
			gt.image = g.sigate
		g.level = 2
		g.lastgate -= 2
		g.levelcnt += 1
	elif g.levelcnt == 20:
		for gt in g.gates:
			gt.image = g.sigate
		g.level = 3
		g.lastgate -= 2
		g.levelcnt += 1
	g.status.text = 'Level: %s, Points: %s, Pos: %s, Missed: %s' % (g.level, g.points, g.me.y, g.gatesmissed)

@screen.event
def on_draw():
	screen.clear()
	if g.mode == 'start':
		p.gl.glPolygonMode(p.gl.GL_FRONT_AND_BACK, p.gl.GL_FILL);
		g.startmsg.draw()
	elif g.mode == 'play':
		for gt in g.gates:
			p.graphics.draw(4, p.gl.GL_POLYGON,
				('v2f', (gt.left, gt.top, gt.right, gt.top, gt.right, gt.bottom, gt.left, gt.bottom)))
		p.graphics.draw(16, p.gl.GL_LINES,
			('v2f', (0,0, g.ileft, g.ibottom,
				0, g.height, g.ileft, g.itop,
				g.width, g.height, g.iright, g.itop,
				g.width, 0, g.iright, g.ibottom,
				0, g.center_y, g.ileft, g.center_y,
				g.center_x, g.height, g.center_x, g.itop,
				g.width, g.center_y, g.iright, g.center_y,
				g.center_x, 0, g.center_x, g.ibottom)))
		p.gl.glPolygonMode(p.gl.GL_FRONT_AND_BACK, p.gl.GL_FILL);
		g.lines.draw()
		for gt in [x for x in g.gates if x.scale < 1]:
			gt.draw()
		g.me.draw()
		for gt in [x for x in g.gates if x.scale >= 1]:
			gt.draw()
		g.status.draw()
		p.gl.glPolygonMode(p.gl.GL_FRONT_AND_BACK, p.gl.GL_LINE);
		p.graphics.draw(4, p.gl.GL_POLYGON,
			('v2f', (g.left, g.top, g.right, g.top, g.right, g.bottom, g.left, g.bottom)),
			('c3B', (254, 254, 0, 254, 254, 0, 254, 254, 0, 254, 254, 0)))

@screen.event
def on_mouse_motion(x, y, dx, dy):
	global mousey_pos, mousex_pos
	if g.mode == 'play':
		g.mousey_pos += dy
		g.mousex_pos += dx

@screen.event
def on_mouse_press(x, y, btn, mods):
	g.play()

def constrain(val, minv, maxv):
	if val < minv:
		return minv
	elif val>maxv:
		return maxv
	else:
		return val

class Game():
	def __init__(self):
		p.resource.path = ['res']
		p.resource.reindex()
		self.mode = 'start'
		self.circ = p.resource.image('circ.png')
		self.center_image(self.circ)
		self.sggate = p.resource.image('sggate.png')
		#center_image(sggate)
		self.srgate = p.resource.image('srgate.png')
		#center_image(srgate)
		self.sbgate = p.resource.image('sbgate.png')
		#center_image(sbgate)
		self.sigate = p.resource.image('sigate.png')
		#center_image(sbgate)

		self.pl = p.resource.image('pl.png')
		self.vl = p.resource.image('vl.png')
		self.al = p.resource.image('al.png')

		self.width, self.height = screen.width, screen.height
		self.center_x, self.center_y = self.width//2, self.height//2
		msg = 'Click or press space to start'
		self.startmsg = p.text.Label(msg, font_size=self.width//30, width=int(self.width*.9), align='center', x=self.center_x, y=self.center_y, anchor_x='center', multiline=True)
		self.spritescaledelta = 1-(self.width / self.sggate.width / 1000) #This constant needs to change in inverse relation
		self.scaledelta = self.spritescaledelta * .00421 # to this one
		self.opacitydelta = 2
		self.radius = 10
		self.maxgatesmissed = 5
		self.lastgate = 0
		self.status = p.text.Label('', x=self.center_x, y=self.radius, anchor_x='center')
		self.left = self.width/850*283
		self.ileft = self.left+self.sggate.width/1.3
		self.right = self.left + self.width/850*288
		self.iright = self.right-self.sggate.width/1.3
		self.bottom = self.width/850*283
		self.ibottom = self.bottom+self.sggate.width/1.3
		self.top = self.bottom + self.width/850*288
		self.itop = self.top-self.sggate.width/1.3
		self.me = p.sprite.Sprite(img=self.circ, x=self.center_x,y=self.center_y)
		self.lines = p.graphics.Batch()

	def play(self):
		self.mousey_pos = self.center_y
		self.mousex_pos = self.center_x
		self.level = 1
		self.levelcnt = 0
		self.points = 0
		self.gatesmissed = 0
		self.bufsize = bufsize = 10
		self.x_pbuf = [self.center_x] * bufsize
		self.x_pdbuf = [0] * bufsize
		self.x_vbuf = [0] * bufsize
		self.x_vdbuf = [0] * bufsize
		self.x_abuf = [0] * bufsize
		self.y_pbuf = [self.center_y] * bufsize
		self.y_pdbuf = [0] * bufsize
		self.y_vbuf = [0] * bufsize
		self.y_vdbuf = [0] * bufsize
		self.y_abuf = [0] * bufsize
		self.bufpos = 0
		self.gates = []
		self.a = []
		self.v = []
		self.pos = []
		self.mode = 'play'

	def die(self, prevpoints):
		msg = 'Game Over\nYou got %s points\n\nClick or press space to start a new game or press \'q\' to quit.' % (prevpoints,)
		self.startmsg.text = msg
		self.startmsg.y = int(self.center_y * 1.2)
		self.mode = 'start'


	def center_image(self,image):
		"""Sets an image's anchor point to its center"""
		image.anchor_x = image.width // 2
		image.anchor_y = image.height // 2





if __name__ == '__main__':
	g = Game()
	p.clock.schedule_interval(update, 1/60.0)
	p.app.run()