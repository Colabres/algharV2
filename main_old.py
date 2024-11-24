import numpy as np
import random
from modules.visualization import visualize_dungeon
from modules.core_algorithms import bowyer_watson, mst, a_star
from modules.dungeon import initialize_dungeon

# class for room
# this class and the node class i very related basicly thay just a point in the map but since i needed different 
# fitures i didnt want to put it all to make over large single class
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

   
#base setup for new dungeon
#this is a base setup that is adjusteble if a biger or smaller dungeon is needed 
room_count = 20         
dungeonMap = np.zeros((50,80), dtype=int)
rooms = []
min_room_size = 5
max_room_size = 9
dungeon_width = 80
dungeon_height = 50
buff = 3
extra = 5

#making sure that rooms dont overlap
def isValidPos(x,y,width,height):
    
    x_start = x - buff
    y_start = y - buff
    x_end = x + width + buff
    y_end = y + height + buff

    for i in range(y_start, y_end):
        for j in range(x_start, x_end):
            if dungeonMap[i, j] != 0:                    
                return False
    return True

#function to place room.
def place_room():    
    room_width = random.randint(min_room_size, max_room_size)
    room_height = random.randint(min_room_size, max_room_size)
    
    for _ in range(100):  
        x = random.randint(buff, dungeon_width - room_width - buff)
        y = random.randint(buff, dungeon_height - room_height - buff)
        
        if isValidPos(x, y, room_width, room_height):
            rooms.append(Room(x,y))
            for i in range(y, y + room_height):
                for j in range(x, x + room_width):
                    if i == y or i == y + room_height - 1 or j == x or j== x + room_width - 1:
                        if ((i == y and j == x) or               # Top-left corner
                            (i == y and j == x + room_width - 1) or  # Top-right corner
                            (i == y + room_height - 1 and j == x) or  # Bottom-left corner
                            (i == y + room_height - 1 and j == x + room_width - 1)):  # Bottom-right corner
                            dungeonMap[i, j] = 3
                        else:
                            dungeonMap[i, j] = 1
                    else:
                        dungeonMap[i, j] = 2
            return True  
    return False  


#placing rooms one by one making sure thay do not overlap and have a wide enought area in between
placed_rooms = 0
while placed_rooms < room_count:
    if place_room():
        placed_rooms += 1
triangles=bowyer_watson(rooms)


#using Delaunay triangulation to add neighbors to rooms that are to be connected
for triangle in triangles:

    triangle.points[0].addNeighbor(triangle.points[1])
    triangle.points[0].addNeighbor(triangle.points[2])
    triangle.points[1].addNeighbor(triangle.points[0])
    triangle.points[1].addNeighbor(triangle.points[2])
    triangle.points[2].addNeighbor(triangle.points[0])
    triangle.points[2].addNeighbor(triangle.points[1])
    x_values = [triangle.points[0].x, triangle.points[1].x, triangle.points[2].x, triangle.points[0].x]
    y_values = [triangle.points[0].y, triangle.points[1].y, triangle.points[2].y, triangle.points[0].y]
    #plt.plot(x_values, y_values, color='blue', linestyle='-', linewidth=1)

#making a graph of minimum requerd connections
graph = mst(rooms)

while extra > 0:
    room = random.choice(rooms)
    neighbor = random.choice(room.neighbors)
    edge = (room,neighbor[0],neighbor[1])
    if edge not in graph:
        extra-=1
        graph.append(edge)

# for room1, room2, _ in graph:
#     plt.plot([room1.x, room2.x], [room1.y, room2.y], 'blue', lw=1)
initialize_dungeon()

a_star(graph,dungeonMap)

visualize_dungeon(dungeonMap,graph)