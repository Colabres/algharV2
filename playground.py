import numpy as np
import matplotlib.pyplot as plt
import random
import heapq 
import math

#class to create a Node for A*
class Node:
    def __init__(self,x,y,g,camefrom):
        self.x = x
        self.y = y
        self.g = g
        self.h = None
        self.f = None
        self.camefrom = camefrom
    
    def set_total_cost(self,coords):
        self.h = abs(self.x - coords[0]) + abs(self.y - coords[1])
        self.f = self.g+self.h
    
    def __lt__(self, other):        
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"Node ({self.x}, {self.y})"
    

def a_star(graph,dungeonMap):    
    def get_neighbors(current):
        neighbors = []
        neighborOffset = [(-1,0),(1,0),(0,-1),(0,1)]
        for neighbor in neighborOffset:
            
            neighbor_coords = (neighbor[0]+current.x,neighbor[1]+current.y)
            # if not (0 <= neighbor_coords[0] < len(dungeonMap) and 0 <= neighbor_coords[1] < len(dungeonMap[0])):
            #     continue  
            neighbor_g_cost = current.g
            if dungeonMap[neighbor_coords] == 1:
                print("cheking 1")
                for check_coords in [(-1,0),(1,0),(0,-1),(0,1)]:

                    if dungeonMap[(neighbor_coords[0]+check_coords[0],neighbor_coords[1]+check_coords[1])] == 3:
                        print("denger")
                        neighbor_g_cost+=100
                neighbor_g_cost+=10
            elif dungeonMap[neighbor_coords] == 3:
                break
            elif dungeonMap[neighbor_coords] == 2:
                neighbor_g_cost+=0
            else:
                neighbor_g_cost+=1

            neighbors.append(Node(neighbor_coords[0],neighbor_coords[1],neighbor_g_cost,current))

        return neighbors

        

                    

        
    for edge in graph:
        
        print(f"This is the edge : {edge}")
        visited = set()
        open_list = [] 
        start = Node(edge[0].y+1,edge[0].x+1,0,None)
        print(f"this is the start {start}")
        goal = (edge[1].y+1,edge[1].x+1)
        start.set_total_cost(goal)
        heapq.heappush(open_list, (start.f, start))
        path = []
        print("goal is ")
        print(goal)
        while not path and open_list:
            #print(open_list)
            current = heapq.heappop(open_list)[1]
            if current in visited:
                continue
            
            visited.add(current)

            if (current.x,current.y) == goal:

                
                while current.camefrom:
                    path.append(current)
                    current = current.camefrom             
                
                print(f"This is the path {path}")
            
            neighbors = get_neighbors(current)
            for neighbor in neighbors:
                neighbor.set_total_cost(goal)
                heapq.heappush(open_list,(neighbor.f, neighbor))

        for node in path:
            dungeonMap[(node.x,node.y)] = 2

room_count = 2         
dungeonMap = np.zeros((25,40), dtype=int)
rooms = []

dungeon_width = 40
dungeon_height = 25
fail = 0
buff = 3
extra = 0



def place_room(x,y):    
    room_width = 5
    room_height = 5
   
    

        
    
    rooms.append((x,y))
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


place_room(20,15)
place_room(20,5)
a_star([(Node(20,15,0,None),Node(20,5,0,None))],dungeonMap)
plt.figure(figsize=(8, 8))
plt.imshow(dungeonMap, cmap='gray', origin='upper', interpolation='nearest')
plt.colorbar(label="Dungeon Map Values")
plt.title("Dungeon Map")
plt.show()