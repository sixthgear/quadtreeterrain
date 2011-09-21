import shapes

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
    if (circle_dist.x > (rect.width / 2 + circle.radius)): return False
    if (circle_dist.y > (rect.height / 2 + circle.radius)): return False
    if (circle_dist.x <= (rect.width / 2)): return True
    if (circle_dist.y <= (rect.height / 2)): return True
    corner_dist_sq = (circle_dist.x - rect.width/2) ** 2 + (circle_dist.y - rect.height/2) ** 2
    return (corner_dist_sq <= (circle.radius ** 2))
    
# def rect_within_rect(rect_in, rect_out):    
#     if rect_in.x < rect_out.x: return False
#     if rect_in.y < rect_out.y: return False
#     if rect_in.x + rect_in.width > rect_out.x + rect_out.width: return False
#     if rect_in.y + rect_in.height > rect_out.y + rect_out.height: return False
#     return True