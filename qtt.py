import collision
import shapes
import pyglet
import math
import random

class TerrainNode(object):
    """
    Quadtree that represents terrain
    """
        
    def __init__(self, x, y, size): # , vl=None
                            
        self.rect = shapes.AABB(x, y, size, size)
        self.enabled = False
        self.children = []
                    
    def point_in(self, x, y):
        if not self.children: 
            return self
        else:
            tx, ty = (0, 0)
            if x >= self.rect.x + self.rect.width / 2: tx = 1
            if y >= self.rect.y + self.rect.height / 2: ty = 1
            idx = ty*2 + tx
            return self.children[idx].point_in(x, y)
                        
    def combine(self):
        self.children = []
                
    def subdivide(self):
                    
        size = self.rect.width // 2
        self.children = [
            TerrainNode(self.rect.x, self.rect.y, size), # vl=self.vl
            TerrainNode(self.rect.x + size, self.rect.y, size), # vl=self.vl
            TerrainNode(self.rect.x, self.rect.y + size, size), # vl=self.vl
            TerrainNode(self.rect.x + size, self.rect.y + size, size), # vl=self.vl
        ]
        for c in self.children:
            c.enabled = self.enabled
        
    def modify_quads_around_point(self, brush, state=False):
        """
        This is the main terrain deformation routine.
        """
        
        if self.enabled == state and not self.children: 
            return
                        
        if collision.rect_within_circle(self.rect, brush):            
            self.combine()
            self.enabled = state
            
        elif collision.rect_vs_circle(self.rect, brush):
            
            if not self.children and self.rect.width >= 8:
                # todo: stop subdividing if the cirlce just skims a node
                self.subdivide()
               
            for c in self.children:
                c.modify_quads_around_point(brush, state)
                
        if self.children:
            if self.children[0] == self.children[1] == self.children[2] == self.children[3]:
                self.enabled = self.children[0].enabled
                self.combine()
                                            
    def draw(self, highlight=None, root=True):

        vdata1 = [] # background
        vdata2 = [] # foreground
        
        if self.children: 
            for c in self.children:
                v1, v2 = c.draw(highlight, root=False)
                vdata1 += v1
                vdata2 += v2
        else:            
            if not self.enabled:
                vdata1 = self.rect.corners
            else:
                vdata2 = self.rect.corners                
                     
        if root:
            pyglet.gl.glColor3f(0.2,0.2,0.2)
            pyglet.gl.glPolygonMode (pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_FILL)
            pyglet.graphics.draw(len(vdata2)//2, pyglet.gl.GL_QUADS, ('v2f', vdata2))            
            pyglet.gl.glPolygonMode (pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_LINE)
            pyglet.gl.glColor3f(0.2,0.2,0.2)
            pyglet.graphics.draw(len(vdata1)//2, pyglet.gl.GL_QUADS, ('v2f', vdata1))
            pyglet.gl.glColor3f(1,1,1)
            pyglet.graphics.draw(len(vdata2)//2, pyglet.gl.GL_QUADS, ('v2f', vdata2))
            if highlight:
                pyglet.gl.glColor3f(1,0.5,0.5)
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', highlight.rect.corners))                        
            
        else:
            return vdata1, vdata2

class App(pyglet.window.Window):
    
    def __init__(self):
        super(App, self).__init__(caption="Quadtrees", width=800, height=800)
        self.set_mouse_visible(False)        
        self.brush = shapes.Circle(0, 0, 128)
        self.terrain = TerrainNode(0, 0, 800)        
        self.highlight = None
        # pyglet.clock.schedule_interval(self.update, 1.0/30)
        
    def circle(self, x, y, radius, num=12):    
        data = []
        for a in range(0, 360, 360//num):
            data.append(x + math.cos(math.radians(a)) * radius)
            data.append(y + math.sin(math.radians(a)) * radius)        
        pyglet.gl.glColor4f(1, 1, 1, 1)
        pyglet.graphics.draw(len(data)//2, pyglet.gl.GL_LINE_LOOP, ('v2f', data))

    def update(self, dt):
        pass
        
    def on_draw(self):
        self.clear()
        self.terrain.draw(highlight = self.highlight)
        self.circle(self.brush.x, self.brush.y, self.brush.radius, num=32)
            
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.BRACKETLEFT:
            self.brush.radius = max(16, self.brush.radius // 2)
        elif symbol == pyglet.window.key.BRACKETRIGHT:
            self.brush.radius = min(512, self.brush.radius * 2)
        elif symbol == pyglet.window.key.R:
            self.terrain.children = []
            self.terrain.enabled = False
        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()    
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.brush.x = x
        self.brush.y = y
        self.highlight = self.terrain.point_in(x, y)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.terrain.modify_quads_around_point(self.brush, state=True)
        elif button == pyglet.window.mouse.RIGHT:
            self.terrain.modify_quads_around_point(self.brush, state=False)
                
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        self.on_mouse_press(x, y, button, modifiers)
        
    def run(self):
        pyglet.clock.set_fps_limit(24)        
        pyglet.app.run()
                

if __name__ == '__main__':
    
    app = App()
    app.run()
    