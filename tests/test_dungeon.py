import numpy as np
import pytest
import random
from src.dungeon import Dungeon, initialize_dungeon  

def test_dungeon_initialization():
    # Test dungeon creation with a 20x20 map
    width = 20
    height = 20
    max_room_size = 5
    min_room_size = 3
    buffer = 1  # Buffer space around rooms to prevent overlap
    extra_corridors = 2 
    
    # Create the dungeon
    dungeon = Dungeon(max_room_size, min_room_size, height, width, buffer, extra_corridors)
    
    # Ensure the dungeon map has the correct dimensions
    assert dungeon.map.shape == (height, width), f"Expected map size of ({height,width})"
    assert dungeon.max_room_size == max_room_size, f"Expected ({max_room_size})"
    assert dungeon.min_room_size == min_room_size, f"Expected ({min_room_size})"
    assert dungeon.buffer == buffer, f"Expected ({buffer})"
    assert dungeon.extra_corredors == extra_corridors, f"Expected ({extra_corridors})"


#testing position validator
def test_dungeon_isValidPos_valid():
    dungeon = Dungeon(5,3,20,20,1,2)    
    assert dungeon.isValidPos(15, 15, 3, 3) is True

#testing position validator
def test_dungeon_isValidPos_invalid():
    dungeon = Dungeon(5,3,20,20,1,2)
    dungeon.map[(5,5)] = 3
    assert dungeon.isValidPos(5, 5, 3, 3) is False


#testing room placement function
def test_place_room():
    dungeon = Dungeon(5,3,20,20,1,2)    
    # Place a room and verify the map is updated
    assert dungeon.place_room() is True
    assert len(dungeon.rooms) == 1  
    room_x, room_y = dungeon.rooms[0]
    room_width = dungeon.max_room_size  
    room_height = dungeon.max_room_size
    assert np.any(dungeon.map[room_y : room_y + room_height, room_x : room_x + room_width] > 0)

#edge case for room placement failier
def test_place_room_fail():
    dungeon = Dungeon(5,3,7,7,1,2)
    dungeon.place_room()
    assert dungeon.place_room() == False

#testing dungeon inti function
def test_initialize_dungeon():
    
    width = 10
    height = 10
    room_count = 1
    min_room_size = 3
    max_room_size = 6
    extra_corridors = 0
    buffer = 1
    
    dungeon_map, graph = initialize_dungeon(width, height, room_count, min_room_size, max_room_size, extra_corridors, buffer)
    
    assert dungeon_map is not None
    assert graph is not None


    