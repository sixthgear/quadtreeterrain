import shapes
import pyglet
import vector

class GameObject(object):
    
    def __init__(self, x, y):
        self.shape = shapes.Circle(0,0,8)
        self.pos = vector.Vec2d(x, y)
        self.lastpos = vector.Vec2d(x, y)
        self.thruster = vector.Vec2d(0, 0)
        self.power = 5000
        self.dampening = 0.6
        
    def integrate(self, dt2):
        """
        Verlet integration.
        """
        accumulated_force = self.thruster        
        p = self.pos
        self.pos = self.pos * (1.0 + self.dampening) - self.lastpos * self.dampening + accumulated_force * dt2
        self.lastpos = p
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y
        
    def input(self, keys):
        self.thruster = vector.Vec2d(0,0)
        if keys[pyglet.window.key.A]:
            self.thruster.x = -1
        elif keys[pyglet.window.key.D]:
            self.thruster.x = 1
        if keys[pyglet.window.key.W]:
            self.thruster.y = 1
        elif keys[pyglet.window.key.S]:
            self.thruster.y = -1
        self.thruster.normalize()
        self.thruster *= self.power
