# tests/test_core_algorithms.py
import pytest
from src.core_algorithms import Point, Triangle, Node  

# Sample data for testing
coords = [(1, 2), (3, 4), (5, 6), (7, 8)]
graph = [(Point(1, 2), Point(3, 4)), (Point(3, 4), Point(5, 6))]
dungeon_map = {(x, y): 0 for x in range(5) for y in range(5)}


# Test Node class
def test_node_initialization():
    node = Node(1, 2, 3, None)
    assert node.x == 1
    assert node.y == 2
    assert node.g == 3
    assert node.camefrom is None

def test_node_set_total_cost():
    node = Node(1, 2, 3, None)
    node.set_total_cost((4, 5))  # Set total cost to (4, 5)
    assert node.h == 6  # h = abs(1-4) + abs(2-5) = 3 + 3 = 6
    assert node.f == 9  # f = g + h = 3 + 6 = 9

def test_node_comparison():
    node1 = Node(1, 2, 3, None)
    node2 = Node(1, 2, 4, node1)
    node3 = Node(1, 3, 3, node1)
    
    assert node1 == node2  # Same x, y values
    assert node1 != node3  # Different y values
    assert node1 < node3   # node1 has smaller y value than node3

def test_node_hashing():
    node1 = Node(1, 2, 3, None)
    node2 = Node(1, 2, 4, node1)
    node_set = {node1, node2}
    
    assert len(node_set) == 1  # Both nodes are considered equal, so only one entry in the set

def test_node_repr():
    # Create a Node instance
    node = Node(5, 10, 3, None)
    
    # Check the string representation of the node
    assert repr(node) == "Node (5, 10)"

    # Test with different values
    node2 = Node(3, 7, 3, None)
    assert repr(node2) == "Node (3, 7)"

# Test Point class
def test_point_initialization():
    point = Point(1, 2)
    assert point.x == 1
    assert point.y == 2
    assert point.name == "1,2"
    assert point.neighbors == []

def test_point_add_neighbor():
    point1 = Point(1, 2)
    point2 = Point(3, 4)
    point1.addNeighbor(point2)

    # Test if neighbor is added
    assert len(point1.neighbors) == 1
    assert point1.neighbors[0][0] == point2  # Check the neighbor
    assert point1.neighbors[0][1] == 4  # The weight is |1-3| + |2-4| = 4

    # Test adding the same neighbor again 
    point1.addNeighbor(point2)
    assert len(point1.neighbors) == 1  # No duplicate

def test_point_comparison():
    point1 = Point(1, 2)
    point2 = Point(1, 2)
    point3 = Point(2, 3)    

    assert point1 < point3   # point1 has smaller x value than point3

# Test Triangle class
def test_triangle_initialization():
    point1 = Point(1, 2)
    point2 = Point(3, 4)
    point3 = Point(5, 6)
    triangle = Triangle(point1, point2, point3)

    # Check that the triangle is initialized with the correct points
    assert triangle.points == [point1, point2, point3]
    assert len(triangle.edges) == 3

def test_triangle_circumcircle_contains():
    point1 = Point(30, 10)
    point2 = Point(50, 40)
    point3 = Point(10, 40)
    triangle = Triangle(point1, point2, point3)
    point_inside = Point(30, 30)
    point_outside = Point(60, 70)
    
    # Test if a point is inside the circumcircle
    assert triangle.circumcircle_contains(point_inside) is True
    assert triangle.circumcircle_contains(point_outside) is False

def test_triangle_repr():
    point1 = Point(30, 10)
    point2 = Point(50, 40)
    point3 = Point(10, 40)
    triangle = Triangle(point1, point2, point3)
    
    # Check the string representation of the node
    assert repr(triangle) == f"Triangle({point1}, {point2}, {point3})"










