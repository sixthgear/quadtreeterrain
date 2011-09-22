import collections
import collision
import pyglet
import shapes
import math

class TerrainNode(object):
    """
    Quadtree node.
    """
    def __init__(self, x, y, size, enabled=False, level=0):
        self.rect = shapes.AABB(x, y, size, size)    
        self.children = []
        self.enabled = enabled
        self.slope = 0.0
        self.level = level
    
    def combine(self):
        """
        Remove all descendants.
        """
        self.children = []
                
    def subdivide(self):
        """
        Split into four.
        """
        size = self.rect.width // 2
        self.children = [
            TerrainNode(self.rect.x, self.rect.y, size, self.enabled, self.level+1), 
            TerrainNode(self.rect.x + size, self.rect.y, size, self.enabled, self.level+1), 
            TerrainNode(self.rect.x, self.rect.y + size, size, self.enabled, self.level+1), 
            TerrainNode(self.rect.x + size, self.rect.y + size, size, self.enabled, self.level+1), 
        ]

    def simplify(self):
        """
        Check if all children are equivalent and childless. Combine them if so.
        """
        if not self.children: return
            
        if self.children[0].children or \
            self.children[1].children or \
            self.children[2].children or \
            self.children[3].children:
                return
            
        if self.children[0].enabled == \
            self.children[1].enabled == \
            self.children[2].enabled == \
            self.children[3].enabled:
                self.enabled = self.children[0].enabled
                self.combine()
                        
                                            
class TerrainTree(object):
    """
    Quadtree that represents terrain
    """
    
    def __init__(self, x, y, size, min_node_size=None, max_level=None, enabled=False):
        if min_node_size and max_level:
            print "Cannot specify both min_node_size and max_level"
            pyglet.app.exit()
        elif min_node_size:
            self.min_node_size = min_node_size
            self.max_level = size // min_node_size
        elif max_level:
            self.max_level = max_level
            self.min_node_size = size // 2 ** max_level
        else:
            self.min_node_size = 8
            self.max_level = size // self.min_node_size
            
        self.root = TerrainNode(x, y, size, enabled)
    
    def clear(self, state=False):        
        self.root.combine()
        self.root.enabled = state
                        
    def modify_quads_around_point(self, brush, state=False, node=None):
        """
        This is the main terrain deformation routine.
        """
        
        node = node or self.root
             
        if node.enabled == state and not node.children: 
            # rect is already where it needs to be
            return
                        
        if collision.rect_within_circle(node.rect, brush):
            # rect completely within circle
            node.combine()
            node.enabled = state
                        
        elif collision.rect_vs_circle(node.rect, brush):
            # rect partially within circle
            if not node.children and node.level < self.max_level:
                node.subdivide()
            for c in node.children:
                self.modify_quads_around_point(brush, state, node=c)
            node.simplify()

    def collide_point(self, x, y, node=None):
                
        node = node or self.root
            
        if not node.children:
            return node
        else:
            tx, ty = (0, 0)
            if x >= node.rect.x + node.rect.width / 2: tx = 1
            if y >= node.rect.y + node.rect.height / 2: ty = 1
            idx = ty*2 + tx
            return self.collide_point(x, y, node=node.children[idx])

    def collide_circle(self, circle, node=None):
        """
        Collision detection helper that can recursively generate a list of nodes
        """
        node = node or self.root        
        nodes = []
        if collision.rect_vs_circle(node.rect, circle):
            if node.children:
                for c in node.children:
                    nodes += self.collide_circle(circle, node=c)
            elif node.enabled:
                return [node]        
        return nodes
        
                                                    
    def draw(self, highlight=None, node=None):
        """
        Draw all the nodes in the tree.
        """
        node = node or self.root
        node_stack = [node]
        v_background = []
        v_foreground = []
                
        while node_stack:
            node = node_stack.pop()
            if node.children:
                node_stack += node.children
                continue            
            if not node.enabled:
                v_background += node.rect.corners
            else:
                v_foreground += node.rect.corners
        
        # switch to fill mode
        pyglet.gl.glPolygonMode (pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_FILL)
        
        # draw fills for enabled quads
        pyglet.gl.glColor3f(0.2, 0.2, 0.2)
        pyglet.graphics.draw(len(v_foreground)//2, pyglet.gl.GL_QUADS, ('v2f', v_foreground))
    
        # switch to outline mode
        pyglet.gl.glPolygonMode (pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_LINE)
        
        # draw outlines for disabled quads        
        pyglet.gl.glColor3f(0.2,0.2,0.2)
        pyglet.graphics.draw(len(v_background)//2, pyglet.gl.GL_QUADS, ('v2f', v_background))
        
        # draw outlines for enabled quads
        pyglet.gl.glColor3f(1,1,1)
        pyglet.graphics.draw(len(v_foreground)//2, pyglet.gl.GL_QUADS, ('v2f', v_foreground))
        
        # draw outlines for highlighted quad
        if highlight:
            pyglet.gl.glColor3f(1,0.5,0.5)
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', highlight.rect.corners))                        
