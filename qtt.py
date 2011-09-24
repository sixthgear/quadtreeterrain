import pyglet

pyglet.resource.path = ['data']
pyglet.resource.reindex()

import collections
import drawing
import math
import obj
import shapes
import terrain
import vector

SQRT2 = 1.414213562373095

class App(pyglet.window.Window):
    
    def __init__(self):
        super(App, self).__init__(caption="Quadtrees", width=512, height=512)
        self.set_mouse_visible(False)        
        # self.set_location(0, 900-self.height)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)        

        self.paused = True
        self.operation = None

        self.terrain = terrain.TerrainTree(0, 0, 512, max_level=5)
        self.player = obj.GameObject(self.terrain.root.rect.width//2, self.terrain.root.rect.height//2)
        self.brush = shapes.Circle(0, 0, 128)
        self.brush_type = 1
        self.highlight = collections.deque()
        self.highlight_cursor = None
        
        self.render_mode = 0

        self.debug_label = pyglet.text.Label(
            text='LABEL', 
            font_size=18, x=self.width-20, y=self.height-20,
            anchor_x='right', anchor_y='top',
            color=(255,255,255,255)
        )
                
        self.play()
                
    def play(self):
        if self.paused:
            pyglet.clock.schedule_interval(self.update, 1.0/60)
            pyglet.clock.schedule_interval(self.relax_highlight, 0.25)
            self.paused = False
                
    def relax_highlight(self, dt):
        if len(self.highlight):
            self.highlight.popleft()
        
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
        self.player.integrate(dt*dt)    
        
        for q in self.terrain.collide_circle(self.player.shape):
            """
            Finds all nodes currently in contact with the player.
            """
            halfquad = q.rect.width // 2
            quad_center = vector.Vec2d(q.rect.x + halfquad, q.rect.y + halfquad)
            delta = quad_center - self.player.pos
            rest = vector.Vec2d()
            rest_dist = 0
            
            if abs(delta.x) > abs(delta.y):
                rest_dist = abs(delta.x) - (self.player.shape.radius + halfquad)
                if delta.x < 0: 
                    rest.x = -rest_dist
                else:
                    rest.x = rest_dist
            
            elif abs(delta.x) < abs(delta.y):
                rest_dist = abs(delta.y) - (self.player.shape.radius + halfquad)
                if delta.y < 0:
                    rest.y = -rest_dist
                else:
                    rest.y = rest_dist
            
            else:                
                # diagonal collision                
                rest_dist = delta.magnitude - (self.player.shape.radius + halfquad * SQRT2)
                rest = delta.normal * -rest_dist
                print 'CORNER CASE', rest                
                # self.pause()
                return
                
            if q not in self.highlight:
                self.highlight.append(q)
            self.player.pos += rest
            self.player.shape.x = self.player.pos.x
            self.player.shape.y = self.player.pos.y
            
            # n = len(self.terrain.collide_circle(self.player.shape))
            # if n: print n        
        
    def on_draw(self):
        self.clear()
        h = list(self.highlight)
        if self.highlight_cursor:
            h.append(self.highlight_cursor)
        self.terrain.draw(highlight=h, mode=self.render_mode)
        drawing.circle(self.player.shape.x, self.player.shape.y, self.player.shape.radius, num=8)
        drawing.circle(self.brush.x, self.brush.y, self.brush.radius, num=32)
        # self.debug_label.draw()
            
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.BRACKETLEFT:
            self.brush.radius = max(16, self.brush.radius // 2)
        elif symbol == pyglet.window.key.BRACKETRIGHT:
            self.brush.radius = min(512, self.brush.radius * 2)
        elif symbol == pyglet.window.key._1:
            self.brush_type = 0
        elif symbol == pyglet.window.key._2:
            self.brush_type = 1
        elif symbol == pyglet.window.key._3:
            self.brush_type = 2            
        elif symbol == pyglet.window.key._4:
            self.brush_type = 3                        
        elif symbol == pyglet.window.key.R:
            self.terrain.clear()
            self.play()
        elif symbol == pyglet.window.key.G:
            self.render_mode = abs(self.render_mode - 1)            
        elif symbol == pyglet.window.key.SPACE:
            # self.play()
            # self.operation = self.terrain.detect_slopes()
            # pyglet.clock.schedule_interval(self.do_operation, 1.0/60)            
            pass
        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()    
        
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.brush_type = (self.brush_type + scroll_y) % 4
                
    def on_mouse_motion(self, x, y, dx, dy):
        if self.operation: return
        self.brush.x = x
        self.brush.y = y
                
        # node = self.highlight
        self.highlight_cursor = self.terrain.collide_point(self.brush.x, self.brush.y)
        # if not node:
        #     return
        #         

        # self.debug_label.text = 'x: %d  x2: %d  y: %d  y2: %d' % (x,x2,y,y2)
        # self.debug_label.text = 'xbot: %d  xtop: %d  yleft: %d  yright: %d' % (x_entry_bottom_sq, x_entry_top_sq, y_entry_left_sq, y_entry_right_sq)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.operation: return
        if button == pyglet.window.mouse.LEFT:
            self.terrain.modify_quads_around_point(self.brush, type=self.brush_type)
        elif button == pyglet.window.mouse.RIGHT:
            self.terrain.modify_slope(node=self.highlight_cursor)
                
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        self.on_mouse_press(x, y, button, modifiers)
        
    def run(self):
        pyglet.app.run()
                

if __name__ == '__main__':
    
    app = App()
    app.run()
    