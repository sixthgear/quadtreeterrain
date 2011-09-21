class Point(object):
    __slots__ = ['x', 'y']
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
class AABB(object):
    __slots__ = ['x', 'y', 'width', 'height']
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
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