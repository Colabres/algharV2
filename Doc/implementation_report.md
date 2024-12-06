# **Implementation Report**

**Program Name**: Dungeon Generation System  
**Program Purpose**: The application randomly generates a dungeon made of rooms and corridors and applies the A* pathfinding algorithm to find paths between rooms. It utilizes the Bowyer-Watson algorithm for connecting rooms via Delaunay triangulation and generates a minimum spanning tree (MST) for essential connections between rooms.

## **Program Structure**

The program randomly creates a dungeon with rooms and corridors that are efficiently connected to each other. The main tasks include calculating room placements, connecting rooms, and finding paths between rooms using the A* algorithm. The program operates through a command-line interface and visualizes the generated dungeon graphically.

### **Components**

- **Room Class**: This class represents a room in the dungeon. Rooms can have neighbors, and connections between them are weighted based on their distances.
  
- **Bowyer-Watson Algorithm**: This algorithm is used for generating Delaunay triangulation between rooms, connecting them efficiently.
  
- **MST (Minimum Spanning Tree)**: This algorithm creates the minimum required connections between rooms, ensuring all rooms are connected.

- **A* Pathfinding**: The A* algorithm is used to find the shortest paths between rooms in the dungeon.

- **Dungeon Initialization**: The dungeon size and room placement are initialized, ensuring that rooms do not overlap.

- **Visualization**: The dungeon creation and room connections are visualized using the Matplotlib library.

## **Time Complexity and Performance**

- **Dungeon Creation**: The algorithm for placing and positioning rooms works with a time complexity of **O(n)**, where **n** is the number of rooms. This is fairly efficient but can become less scalable with a significantly large number of rooms.

- **Bowyer-Watson Algorithm**: The Delaunay triangulation creation has a time complexity of **O(n log n)**, where **n** is the number of rooms.

- **MST Algorithm**: The Minimum Spanning Tree algorithm operates with a time complexity of **O(n log n)**, where **n** is the number of rooms. This ensures that rooms are efficiently connected with minimal pathways.

- **A* Pathfinding**: The A* algorithm's time complexity is **O((n + e) log n)**, where **n** is the number of rooms and **e** is the number of connections between rooms. This guarantees an efficient search for paths between rooms.

- **Visualization**: Visualization uses the Matplotlib library and performs efficiently for small to medium-sized dungeons.

## **Usability and Input Validation**

The application operates via a command-line interface for dungeon creation and pathfinding. The user can set the number of rooms and adjust the room sizes.

- **Room Placement and Overlap**: Rooms are placed randomly, but the program ensures that they do not overlap, by checking for space around the rooms.

- **Input Validation**: The program ensures that rooms are not placed too close to each other, and there is enough space between them.

- **Dungeon Visualization**: The generated dungeon and the paths between rooms are visualized using Matplotlib.

## **Limitations and Suggestions for Improvement**

### **Graphical User Interface**
Currently, the application works through the command line, but a graphical user interface (GUI) would improve the user experience, especially for visualizing large dungeons interactively.

### **Additional Features**
- **Room Interiors**: Right now, rooms are just empty spaces. Future development could involve adding internal elements like items or enemies within rooms.
  
- **Room Typing**: The program could categorize rooms (e.g., halls, chambers, or special rooms), which would increase the complexity and diversity of the dungeon.

- **Dungeon Size Restrictions**: It may be useful to set size limits for dungeons to avoid generating excessively large or resource-heavy dungeons.

- **More Input Validation**: It would be beneficial to add more detailed input validation, such as ensuring rooms do not overlap too much or exceed the dungeon boundaries.

### **Code Refactoring**
The application contains some long and complex functions that could benefit from refactoring. Specifically, room placement and connection calculations could be divided into smaller, more manageable components.

### **Acknowledgement**
During this project, the documentation was created in collaboration with ChatGPT by OpenAI.
## **Sources**

- [Delaunay Triangulation (Wikipedia)](https://en.wikipedia.org/wiki/Delaunay_triangulation)
- [Bowyer–Watson algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm)
- [Creating Simple Procedural Dungeon Generation (Tom Stephenson)](https://www.tomstephensondeveloper.co.uk/post/creating-simple-procedural-dungeon-generation)
- [Procedurally Generated Dungeons(VAZGRIZ)](https://vazgriz.com/119/procedurally-generated-dungeons/)
