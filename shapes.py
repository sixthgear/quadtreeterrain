class Point(object):
    __slots__ = ['x', 'y']
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
        
class AABB(object):
    __slots__ = ['x', 'y', 'width', 'height']
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
    
    @property
    def x2(self): return self.x + self.width
    
    @property
    def y2(self): return self.y + self.height
    
    @property
    def corners(self):
        return [
            self.x, self.y,
            self.x, self.y + self.height,
            self.x + self.width, self.y + self.height,
            self.x + self.width, self.y,            
        ]
                        
class Circle(object):
    __slots__ = ['x', 'y', 'radius']
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius