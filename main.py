import numpy as np
import matplotlib.pyplot as plt
import random
import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
class Triangle:
    def __init__(self,p1,p2,p3):
        self.points=[p1,p2,p3]
        self.edges = [(p1,p2), (p2,p3), (p3,p1)]

    def circumcircle_contains(self,point):
        ax, ay = self.points[0].x, self.points[0].y
        bx, by = self.points[1].x, self.points[1].y
        cx, cy = self.points[2].x, self.points[2].y
        dx, dy = point.x, point.y

        a = ax - dx
        b = ay - dy
        c = (ax**2 + ay**2) - (dx**2 + dy**2)
        d = bx - dx
        e = by - dy
        f = (bx**2 + by**2) - (dx**2 + dy**2)
        g = cx - dx
        h = cy - dy
        i = (cx**2 + cy**2) - (dx**2 + dy**2)

        det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

        return det > 0
    
    def __repr__(self):
        return f"Triangle({self.points[0]}, {self.points[1]}, {self.points[2]})"

def bowyer_watson(points):

    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    delta_x = max_x - min_x
    delta_y = max_y - min_y

    max_delta = max(delta_x,delta_y)

    super_triangle = Triangle(Point(min_x - 10 * max_delta, min_y - max_delta),
                              Point(min_x + 10 * max_delta, min_y - max_delta),
                              Point(max_x, min_y + 10 * max_delta))

    triangles = [super_triangle]

    for point in points:
        bad_triangles = []
        for triangle in triangles:
            if triangle.circumcircle_contains(point):
                bad_triangles.append(triangle)
        polygon = []
        for triangle in bad_triangles:
            for edge in triangle.edges:
                is_shared = any(
                    edge == other_edge or edge[::-1] == other_edge 
                    for other_triangle in bad_triangles if other_triangle != triangle 
                    for other_edge in other_triangle.edges)             
                if not is_shared:
                    polygon.append(edge)

        triangles = [triangle for triangle in triangles if triangle not in bad_triangles]

        for edge in polygon:
            new_triangle = Triangle(edge[0],edge[1],point)
            triangles.append(new_triangle)

    triangles = [triangle for triangle in triangles if all(vert not in super_triangle.points for vert in triangle.points)]

    return triangles

room_count = 20         
dungeonMap = np.zeros((50,80), dtype=int)
points = []
min_room_size = 5
max_room_size = 9
dungeon_width = 80
dungeon_height = 50
fail = 0
buff = 3
def isValidPos(x,y,width,height):
    global fail
    x_start = x - buff
    y_start = y - buff
    x_end = x + width + buff
    y_end = y + height + buff


    
    for i in range(y_start, y_end):
        for j in range(x_start, x_end):
            if dungeonMap[i, j] != 0:                
                fail+=1    
                return False
    return True

def place_room():    
    room_width = random.randint(min_room_size, max_room_size)
    room_height = random.randint(min_room_size, max_room_size)
    #print(room_width," - ",room_height)
    for _ in range(100):  
        x = random.randint(buff, dungeon_width - room_width - buff)
        y = random.randint(buff, dungeon_height - room_height - buff)

        
        if isValidPos(x, y, room_width, room_height):
            points.append(Point(x,y))
            for i in range(y, y + room_height):
                for j in range(x, x + room_width):
                    if i == y or i == y + room_height - 1 or j == x or j== x + room_width - 1:
                        dungeonMap[i, j] = 1
                    else:
                        dungeonMap[i, j] = 2
            return True  
    return False  


placed_rooms = 0

while placed_rooms < room_count:
    if place_room():
        placed_rooms += 1
triangles=bowyer_watson(points)
print(triangles)
plt.imshow(dungeonMap, cmap='gray', vmin=0, vmax=2)
for triangle in triangles:
    x_values = [triangle.points[0].x, triangle.points[1].x, triangle.points[2].x, triangle.points[0].x]
    y_values = [triangle.points[0].y, triangle.points[1].y, triangle.points[2].y, triangle.points[0].y]
    plt.plot(x_values, y_values, color='blue', linestyle='-', linewidth=1)
plt.show()