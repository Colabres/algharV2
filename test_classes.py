import pytest
from main import Point, Triangle  # Assuming your classes are in the main.py file

# Test the Point class
def testPoint():
    p = Point(3, 4)
    assert p.x == 3, "Point's x-coordinate should be 3"
    assert p.y == 4, "Point's y-coordinate should be 4"

def test_point_repr():
    p = Point(3, 4)
    assert repr(p) == "Point(3, 4)", "The string representation of the point is incorrect"

# Test the Triangle class
def testTriangle():
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(0, 1)
    
    triangle = Triangle(p1, p2, p3)
    
    # Check that the triangle has exactly 3 points
    assert len(triangle.points) == 3, "Triangle should have exactly 3 points"
    
    # Check that the points in the triangle are correct
    assert triangle.points[0] == p1, "First point should be p1"
    assert triangle.points[1] == p2, "Second point should be p2"
    assert triangle.points[2] == p3, "Third point should be p3"

def testEdges():
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(0, 1)
    
    triangle = Triangle(p1, p2, p3)
    
    # Check the edges are correct
    expected_edges = [(p1, p2), (p2, p3), (p3, p1)]
    assert triangle.edges == expected_edges, "Edges of the triangle are incorrect"