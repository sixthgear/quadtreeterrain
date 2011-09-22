import pyglet
import math

def circle(x, y, radius, num=12):
    data = []
    for a in range(0, 360, 360//num):
        data.append(x + math.cos(math.radians(a)) * radius)
        data.append(y + math.sin(math.radians(a)) * radius)        
    pyglet.gl.glColor4f(1, 1, 1, 1)
    pyglet.graphics.draw(len(data)//2, pyglet.gl.GL_LINE_LOOP, ('v2f', data))
