import terrain
import drawing
import shapes
import pyglet
import vector
import math
import obj

SQRT2 = 1.414213562373095

class App(pyglet.window.Window):
    
    def __init__(self):
        super(App, self).__init__(caption="Quadtrees", width=512, height=512)
        self.set_mouse_visible(False)        
        self.set_location(0, 900-self.height)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)        

        self.paused = True
        self.operation = None

        self.terrain = terrain.TerrainTree(0, 0, 512, max_level=8)        
        self.player = obj.GameObject(self.terrain.root.rect.width//2, self.terrain.root.rect.height//2)
        self.brush = shapes.Circle(0, 0, 128)
        self.highlight = None

        self.play()
                
    def play(self):
        if self.paused:
            pyglet.clock.schedule_interval(self.update, 1.0/60)
            self.paused = False
                
    def pause(self):
        if not self.paused:
            pyglet.clock.unschedule(self.update)
            self.paused = True
                
    def do_operation(self, dt):
        try:
            self.highlight = self.operation.next()
        except StopIteration:
            self.operation = None
            pyglet.clock.unschedule(self.do_operation)

    def update(self, dt):
        self.player.input(self.keys)
        
        for q in self.terrain.collide_circle(self.player.shape):
            """
            Finds all nodes currently in contact with the player.
            """
            
            halfquad = q.rect.width // 2
            quad_center = vector.Vec2d(q.rect.x + halfquad, q.rect.y + halfquad)
            penetration = quad_center - self.player.pos
            rest = vector.Vec2d()
            rest_dist = 0
            
            if abs(penetration.x) > abs(penetration.y):            
                rest_dist = abs(penetration.x) - abs(self.player.shape.radius + halfquad) 
                if penetration.x < 0: 
                    rest.x = -rest_dist
                else:
                    rest.x = rest_dist

            elif abs(penetration.x) < abs(penetration.y):
                rest_dist = abs(penetration.y) - abs(self.player.shape.radius + halfquad) 
                if penetration.y < 0:
                    rest.y = -rest_dist
                else:
                    rest.y = rest_dist

            else:                
                # diagonal collision            
                rest_dist = abs(penetration.magnitude - (self.player.shape.radius + halfquad * SQRT2))
                rest = penetration.normal * -rest_dist
                print 'CORNER CASE', rest
                
            self.player.pos += rest
            self.player.last_pos = self.player.pos
            
        self.player.integrate(dt*dt)    
        
    def on_draw(self):
        self.clear()
        self.terrain.draw(highlight = self.highlight)
        drawing.circle(self.player.shape.x, self.player.shape.y, self.player.shape.radius, num=8)
        drawing.circle(self.brush.x, self.brush.y, self.brush.radius, num=32)
            
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.BRACKETLEFT:
            self.brush.radius = max(16, self.brush.radius // 2)
        elif symbol == pyglet.window.key.BRACKETRIGHT:
            self.brush.radius = min(512, self.brush.radius * 2)
        elif symbol == pyglet.window.key.R:
            self.terrain.clear()
            self.play()
        elif symbol == pyglet.window.key.SPACE:
            self.operation = self.terrain.detect_slopes()
            pyglet.clock.schedule_interval(self.do_operation, 1.0/60)            
        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()    
        
    def on_mouse_motion(self, x, y, dx, dy):
        if self.operation: return
        self.brush.x = x
        self.brush.y = y
        self.highlight = self.terrain.collide_point(x, y)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.operation: return
        if button == pyglet.window.mouse.LEFT:
            self.terrain.modify_quads_around_point(self.brush, state=True)            
        elif button == pyglet.window.mouse.RIGHT:
            self.terrain.modify_quads_around_point(self.brush, state=False)
                
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        self.on_mouse_press(x, y, button, modifiers)
        
    def run(self):
        pyglet.app.run()
                

if __name__ == '__main__':
    
    app = App()
    app.run()
    