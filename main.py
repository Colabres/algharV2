import numpy as np
import matplotlib.pyplot as plt
import random

room_count = 20         
dungeonMap = np.zeros((50,80), dtype=int)
#dungeonMap[1][10] = 2 
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
print(fail)
plt.imshow(dungeonMap, cmap='gray', vmin=0, vmax=2)
plt.show()