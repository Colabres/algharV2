import pytest
import numpy as np
from src.core_algorithms import Point, Triangle, Node, bowyer_watson, triangulate, mst, a_star

def test_bowyer_watson():
    coords = [
        (0, 0), 
        (1, 0), 
        (0, 1), 
        (1, 1), 
        (0.5, 0.5),  # Point inside the convex hull
    ]
    
    # Call the Bowyer-Watson algorithm
    triangles, points = bowyer_watson(coords)
    
    # Assert that the number of triangles is as expected
    assert len(triangles) > 0
    
    
    for triangle in triangles:
        for point in points:
            # Ensure no point lies inside the circumcircle of any triangle.
            assert triangle.circumcircle_contains(point) is False
    
    
    for triangle in triangles:
        assert all(isinstance(p, Point) for p in triangle.points)

def test_triangulate():
    # Create Points
    p1 = Point(3, 1)
    p2 = Point(5, 4)
    p3 = Point(1, 4)
    p4 = Point(7, 1)

    # Create Triangles (each triangle formed by three points)
    triangle1 = Triangle(p1, p2, p3)
    triangle2 = Triangle(p1, p4, p2)
    
    # Create a list of triangles for the triangulate function
    triangles = [triangle1, triangle2]
    
    # Run the triangulate function
    triangulate(triangles)    
       
    # Test the neighbors
    # Point p1 should have neighbors p2 and p3 (from triangle1)
    assert any(neighbor == p2 for neighbor, _ in p1.neighbors)
    assert any(neighbor == p3 for neighbor, _ in p1.neighbors)
    
    # Point p2 should have neighbors p1, p3, and p4
    assert any(neighbor == p1 for neighbor, _ in p2.neighbors)
    assert any(neighbor == p3 for neighbor, _ in p2.neighbors)
    assert any(neighbor == p4 for neighbor, _ in p2.neighbors)

    # Point p3 should have neighbors p1, p2
    assert any(neighbor == p1 for neighbor, _ in p3.neighbors)
    assert any(neighbor == p2 for neighbor, _ in p3.neighbors)
  

    # Point p4 should have neighbors p2 and p1 (from triangle2)
    assert any(neighbor == p2 for neighbor, _ in p4.neighbors)
    assert any(neighbor == p1 for neighbor, _ in p4.neighbors)
    
        
    # Check if the number of neighbors is correct
    assert len(p1.neighbors) == 3  # p1 has two neighbors: p2, p3
    assert len(p2.neighbors) == 3  # p2 has three neighbors: p1, p3, p4
    assert len(p3.neighbors) == 2  # p3 has three neighbors: p1, p2, p4
    assert len(p4.neighbors) == 2  # p4 has two neighbors: p2, p3

# Pytest tests for the MST function
def test_mst_basic():
    # Create points
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(0, 1)
    p4 = Point(1, 1)

    # Add neighbors
    p1.addNeighbor(p2)
    p1.addNeighbor(p3)
    p2.addNeighbor(p1)
    p2.addNeighbor(p4)
    p3.addNeighbor(p1)
    p3.addNeighbor(p4)
    p4.addNeighbor(p2)
    p4.addNeighbor(p3)

    points = [p1, p2, p3, p4]

    # Call the mst function
    mst_result = mst(points)
 
    # Assert that the result is a list of tuples (from_point, to_point, weight)
    assert len(mst_result) == 3  # There should be 3 edges in the MST

    # Ensure the MST contains the expected edges
    expected_edges = [
        (p1, p3, 1),  # Edge between (0,0) and (0,1) with weight 1
        (p1, p2, 1),  # Edge between (0,0) and (1,0) with weight 1
        (p3, p4, 1),  # Edge between (0,1) and (1,0) with weight 1
    ]
    
    for edge in expected_edges:
        assert edge in mst_result

def test_mst_no_points():
    # Test with no points, the result should be an empty list
    points = []
    mst_result = mst(points)
    assert mst_result == []

def test_mst_one_point():
    # Test with one point, no edges should be added
    p1 = Point(0, 0)
    points = [p1]
    mst_result = mst(points)
    assert mst_result == []

# Test the A* pathfinding algorithm
def test_a_star():
    # Example dungeon map (0 = empty, 1 = wall, 2 = path, 3 = obstacle)
    dungeon_map = np.zeros((8,8), dtype=int)
    dungeon_map[(5,4)] = 3
    dungeon_map[(6,4)] = 1
    dungeon_map[(5,5)] = 1
    dungeon_map[(5,6)] = 2
    dungeon_map[(5,7)] = 2
    dungeon_map[(7,4)] = 3
    graph = [(Point(0,0), Point(4,5), 15)]
    
    # Call the A* function
    a_star(graph, dungeon_map)
    
    # Check if the path is correct    
    assert dungeon_map[1, 2].item() == 2  # Start
    assert dungeon_map[1, 3].item() == 2 
    assert dungeon_map[1, 4].item() == 2 
    assert dungeon_map[2, 4].item() == 2
    assert dungeon_map[2, 5].item() == 2
    assert dungeon_map[3, 5].item() == 2
    assert dungeon_map[4, 5].item() == 2
    assert dungeon_map[4, 6].item() == 2
    assert dungeon_map[5, 6].item() == 2
    assert dungeon_map[6, 6].item() == 2
    assert dungeon_map[5, 6].item() == 2  # Goal    



