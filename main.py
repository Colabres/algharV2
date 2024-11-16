import numpy as np
import matplotlib.pyplot as plt
import random
import heapq 
import math

#class to create a point
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

#class to make a triangle object of 3 rooms    
class Triangle:
    def __init__(self,p1,p2,p3):
        self.rooms=[p1,p2,p3]
        self.edges = [(p1,p2), (p2,p3), (p3,p1)]

    #using matrix det to identify if the given room inside the triangle.
    def circumcircle_contains(self,point):
        ax, ay = self.rooms[0].x, self.rooms[0].y
        bx, by = self.rooms[1].x, self.rooms[1].y
        cx, cy = self.rooms[2].x, self.rooms[2].y
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
        return f"Triangle({self.rooms[0]}, {self.rooms[1]}, {self.rooms[2]})"

#class for node
class Room:
    def __init__(self,x,y):
        self.name = f"{x},{y}"
        self.x = x
        self.y = y
        self.neighbors = []
        
    def addNeighbor(self,neighbor):
        if any(neighbor == n[0] for n in self.neighbors):
            return
        weight = abs(self.x-neighbor.x) + abs(self.y - neighbor.y)
        self.neighbors.append((neighbor,weight))

    def __repr__(self):
        return f"Room {self.name}"
    
    def __lt__(self, other):        
        return (self.x, self.y) < (other.x, other.y)

        
#bowyer_watson algoritm
def bowyer_watson(points):

    #geting min max coordinates for super triangle
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    delta_x = max_x - min_x
    delta_y = max_y - min_y

    max_delta = max(delta_x,delta_y)

    #make a super triangle based on max delta
    super_triangle = Triangle(Point(min_x - 10 * max_delta, min_y - max_delta),
                              Point(min_x + 10 * max_delta, min_y - max_delta),
                              Point(max_x, min_y + 10 * max_delta))

    triangles = [super_triangle]

    #algoritm core.
    # for evry point we check if the point is inside the existing triangles. if it is the triangle is a bad triangle and we make a new triangles. 
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

    triangles = [triangle for triangle in triangles if all(vert not in super_triangle.rooms for vert in triangle.rooms)]

    return triangles

def mst(rooms):
    new_graph = []
    visited = set()
    min_heap = []

    def add_edge(room):
        
        visited.add(room)
        for neighbor in room.neighbors:
            if neighbor not in visited:
                #print("hep")
                print(neighbor[1],room,neighbor[0])
                heapq.heappush(min_heap,(neighbor[1],room,neighbor[0]))
        print("done")
    add_edge(rooms[0])

    while min_heap:
        weight, from_room, to_room = heapq.heappop(min_heap)

        if to_room in visited:
            continue

        new_graph.append((from_room,to_room,weight))
        add_edge(to_room)
    
    return new_graph            

    

#base setup for new dungeon
room_count = 20         
dungeonMap = np.zeros((50,80), dtype=int)
rooms = []
min_room_size = 5
max_room_size = 9
dungeon_width = 80
dungeon_height = 50
fail = 0
buff = 3

#making sure that rooms dont overlap
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

#function to place room.
def place_room():    
    room_width = random.randint(min_room_size, max_room_size)
    room_height = random.randint(min_room_size, max_room_size)
    #print(room_width," - ",room_height)
    for _ in range(100):  
        x = random.randint(buff, dungeon_width - room_width - buff)
        y = random.randint(buff, dungeon_height - room_height - buff)

        
        if isValidPos(x, y, room_width, room_height):
            rooms.append(Room(x,y))
            for i in range(y, y + room_height):
                for j in range(x, x + room_width):
                    if i == y or i == y + room_height - 1 or j == x or j== x + room_width - 1:
                        dungeonMap[i, j] = 1
                    else:
                        dungeonMap[i, j] = 2
            return True  
    return False  


placed_rooms = 0

#placing rooms one by one making sure thay do not overlap and have a wide enought area in between
while placed_rooms < room_count:
    if place_room():
        placed_rooms += 1
triangles=bowyer_watson(rooms)
#print(triangles)
#using numpy to actually draw a visualisation of a new generated dungeon
plt.imshow(dungeonMap, cmap='gray', vmin=0, vmax=2)

for triangle in triangles:
    #print(triangle)
    triangle.rooms[0].addNeighbor(triangle.rooms[1])
    triangle.rooms[0].addNeighbor(triangle.rooms[2])
    triangle.rooms[1].addNeighbor(triangle.rooms[0])
    triangle.rooms[1].addNeighbor(triangle.rooms[2])
    triangle.rooms[2].addNeighbor(triangle.rooms[0])
    triangle.rooms[2].addNeighbor(triangle.rooms[1])
    x_values = [triangle.rooms[0].x, triangle.rooms[1].x, triangle.rooms[2].x, triangle.rooms[0].x]
    y_values = [triangle.rooms[0].y, triangle.rooms[1].y, triangle.rooms[2].y, triangle.rooms[0].y]
    #plt.plot(x_values, y_values, color='blue', linestyle='-', linewidth=1)

graph = mst(rooms)
for room1, room2, _ in graph:
    plt.plot([room1.x, room2.x], [room1.y, room2.y], 'blue', lw=1)
print(graph)
# for room in rooms:
#     print(room)
# print(rooms[0].neighbors)
# print(len(rooms[0].neighbors))
plt.show()