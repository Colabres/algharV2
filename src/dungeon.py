import numpy as np
import random
from src.core_algorithms import mst, a_star, bowyer_watson,triangulate


class Dungeon:
    def __init__(self,max_room_size,min_room_size,height,width,buffer,extra_corredors):
        self.map = np.zeros((height,width), dtype=int)
        self.height = height
        self.width = width
        self.buffer = buffer
        self.extra_corredors = extra_corredors
        self.max_room_size = max_room_size
        self.min_room_size = min_room_size
        
        self.rooms = []

    #making sure that rooms dont overlap
    def isValidPos(self,x,y,room_width,room_height):
        x_start = x - self.buffer
        y_start = y - self.buffer
        x_end = x + room_width + self.buffer
        y_end = y + room_height + self.buffer

        for i in range(y_start, y_end):
            for j in range(x_start, x_end):
                if self.map[i, j] != 0:                    
                    return False
        return True      

    #function to place room.
    def place_room(self):    
        room_width = random.randint(self.min_room_size, self.max_room_size)
        room_height = random.randint(self.min_room_size,self.max_room_size)
        
        for _ in range(100):  
            x = random.randint(self.buffer, self.width - room_width - self.buffer)
            y = random.randint(self.buffer, self.height - room_height - self.buffer)
            
            if self.isValidPos(x, y,room_width,room_height):
                self.rooms.append((x,y))
                for i in range(y, y + room_height):
                    for j in range(x, x + room_width):
                        if i == y or i == y + room_height - 1 or j == x or j== x + room_width - 1:
                            if ((i == y and j == x) or               # Top-left corner
                                (i == y and j == x + room_width - 1) or  # Top-right corner
                                (i == y + room_height - 1 and j == x) or  # Bottom-left corner
                                (i == y + room_height - 1 and j == x + room_width - 1)):  # Bottom-right corner
                                self.map[i, j] = 3
                            else:
                                self.map[i, j] = 1
                        else:
                            self.map[i, j] = 2
                return True  
        return False  
    
 

def initialize_dungeon(width,height,room_count,min_room_size,max_room_size,extra_corridors,buffer):
    dungeon = Dungeon(max_room_size,min_room_size,height,width,buffer,extra_corridors) 

    #placing rooms one by one making sure thay do not overlap and have a wide enought area in between
    placed_rooms = 0
    while placed_rooms < room_count:
        if dungeon.place_room():
            placed_rooms += 1

    triangles, points = bowyer_watson(dungeon.rooms)
    triangulate(triangles)
    graph = mst(points)
    a_star(graph,dungeon.map)
    return dungeon.map, graph


