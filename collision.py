import vector
import shapes

SQRT2 = 1.414213562373095

### detection

def point_within_circle(point, circle):    
    return (circle.x - point.x) ** 2 + (circle.y - point.y) ** 2 <= circle.radius ** 2

def rect_within_circle(rect, circle):
    return point_within_circle(shapes.Point(rect.x, rect.y), circle) and \
        point_within_circle(shapes.Point(rect.x + rect.width, rect.y), circle) and \
        point_within_circle(shapes.Point(rect.x + rect.width, rect.y + rect.height), circle) and \
        point_within_circle(shapes.Point(rect.x, rect.y + rect.height), circle)
                
def rect_vs_circle(rect, circle):    
    circle_dist = shapes.Point()
    circle_dist.x = abs(circle.x - rect.x - rect.width / 2)
    circle_dist.y = abs(circle.y - rect.y - rect.height / 2)
    if (circle_dist.x >= (rect.width / 2 + circle.radius)): return False
    if (circle_dist.y >= (rect.height / 2 + circle.radius)): return False
    if (circle_dist.x < (rect.width / 2)): return True
    if (circle_dist.y < (rect.height / 2)): return True
    corner_dist_sq = (circle_dist.x - rect.width/2) ** 2 + (circle_dist.y - rect.height/2) ** 2
    return (corner_dist_sq < (circle.radius ** 2))
    
# def rect_within_rect(rect_in, rect_out):    
#     if rect_in.x < rect_out.x: return False
#     if rect_in.y < rect_out.y: return False
#     if rect_in.x + rect_in.width > rect_out.x + rect_out.width: return False
#     if rect_in.y + rect_in.height > rect_out.y + rect_out.height: return False
#     return True

#### response

def resp_circle_vs_full(circle, node):
    """
    Finds all nodes currently in contact with the player.
    """
    halfquad = node.rect.width // 2
    quad_center = vector.Vec2d(node.rect.x + halfquad, node.rect.y + halfquad)
    delta = quad_center - vector.Vec2d(circle.x, circle.y)
    rest = vector.Vec2d()
    rest_dist = 0

    if abs(delta.x) > abs(delta.y):
        rest_dist = abs(delta.x) - (circle.radius + halfquad)
        if delta.x < 0: 
            rest.x = -rest_dist
        else:
            rest.x = rest_dist

    elif abs(delta.x) < abs(delta.y):
        rest_dist = abs(delta.y) - (circle.radius + halfquad)
        if delta.y < 0:
            rest.y = -rest_dist
        else:
            rest.y = rest_dist

    else:                
        # diagonal collision                
        rest_dist = delta.magnitude - (circle.radius + halfquad * SQRT2)
        rest = delta.normal * -rest_dist
        print 'CORNER CASE', rest
            
    return rest

    # n = len(self.terrain.collide_circle(self.player.shape))
    # if n: print n