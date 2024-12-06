import heapq

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

class Point:
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
        return f"Point {self.name}"
    
    def __lt__(self, other):        
        return (self.x, self.y) < (other.x, other.y)


#class to make a triangle object of 3 nodes
# i use this class for bowyer_watson algoritm    
class Triangle:
    def __init__(self,p1,p2,p3):
        self.points=[p1,p2,p3]
        self.edges = [(p1,p2), (p2,p3), (p3,p1)]

    #using matrix det to identify if the given room inside the triangle.
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
    

# bowyer_watson algoritm
# This is one of the core algoritm of my project that uses matrix calculations 
# to imply tecnic known as Delaunay triangulation to connect the rooms the best way.
def bowyer_watson(coords):
    #creating a pont objects out of tuples
    points = []
    for point in coords:
        points.append(Point(point[0],point[1]))        


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

    triangles = [triangle for triangle in triangles if all(vert not in super_triangle.points for vert in triangle.points)]

    return triangles, points

#making graph out of Delaunay triangulation   
def triangulate(triangles):
    #using Delaunay triangulation to add neighbors to rooms that are to be connected
    for triangle in triangles:
        triangle.points[0].addNeighbor(triangle.points[1])
        triangle.points[0].addNeighbor(triangle.points[2])
        triangle.points[1].addNeighbor(triangle.points[0])
        triangle.points[1].addNeighbor(triangle.points[2])
        triangle.points[2].addNeighbor(triangle.points[0])
        triangle.points[2].addNeighbor(triangle.points[1])
        #x_values = [triangle.points[0].x, triangle.points[1].x, triangle.points[2].x, triangle.points[0].x]
        #y_values = [triangle.points[0].y, triangle.points[1].y, triangle.points[2].y, triangle.points[0].y]

# This is another core algoritm that takes a graph and removes the unnesesary edges keeping only the most eficient ones but making sure that evry room is reacheble.    
def mst(points):
    new_graph = []
    visited = set()
    min_heap = []
    if len(points) < 2:
        return []
    def add_edge(point):        
        visited.add(point)
        for neighbor in point.neighbors:
            if neighbor not in visited:
                heapq.heappush(min_heap,(neighbor[1],point,neighbor[0]))
    add_edge(points[0])

    while min_heap:
        weight, from_room, to_room = heapq.heappop(min_heap)

        if to_room in visited:
            continue

        new_graph.append((from_room,to_room,weight))
        add_edge(to_room)
    
    return new_graph          

# A* algorithm is a path finder that i use to draw the actual coridors in the most efficient way connecting predeterment rooms.
def a_star(graph,dungeonMap):
    print(graph)
    #helper function that creates new nodes surounding the current node and calculating a g cost that A* needs to function.    
    def get_neighbors(current):
        neighbors = []
        neighborOffset = [(-1,0),(1,0),(0,-1),(0,1)]
        for neighbor in neighborOffset:
            
            neighbor_coords = (neighbor[0]+current.x,neighbor[1]+current.y)
            if not (0 <= neighbor_coords[0] < len(dungeonMap) and 0 <= neighbor_coords[1] < len(dungeonMap[0])):
                continue  
            neighbor_g_cost = current.g
            if dungeonMap[neighbor_coords] == 1:
                for check_coords in [(-1,0),(1,0),(0,-1),(0,1)]:
                    if dungeonMap[(neighbor_coords[0]+check_coords[0],neighbor_coords[1]+check_coords[1])] == 3:
                        neighbor_g_cost+=1000
                neighbor_g_cost+=100
            elif dungeonMap[neighbor_coords] == 3:
                break
            elif dungeonMap[neighbor_coords] == 2:
                neighbor_g_cost+=20
            else:
                if neighbor[0]==0:
                    neighbor_g_cost+=30
                else:
                    neighbor_g_cost+=25
            neighbors.append(Node(neighbor_coords[0],neighbor_coords[1],neighbor_g_cost,current))
        return neighbors
        

    for edge in graph:

        visited = set()
        open_list = [] 
        start = Node(edge[0].y+1,edge[0].x+1,0,None)

        goal = (edge[1].y+1,edge[1].x+1)
        start.set_total_cost(goal)
        heapq.heappush(open_list, (start.f, start))
        path = []

        while not path and open_list:
            current = heapq.heappop(open_list)[1]
            if current in visited:
                continue
            
            visited.add(current)

            if (current.x,current.y) == goal:
                while current.camefrom:
                    path.append(current)
                    current = current.camefrom             
            
            neighbors = get_neighbors(current)
            for neighbor in neighbors:
                neighbor.set_total_cost(goal)
                heapq.heappush(open_list,(neighbor.f, neighbor))

        for node in path:
            dungeonMap[(node.x,node.y)] = 2

