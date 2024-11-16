# Specification Document


This specification document defines the project for the exercise in the "Algorithms and Artificial Intelligence" course, part of the Bachelor's program in Computer Science (TKT) at the University of Helsinki.


## Topic and Impelmentation


In this project, I will implement Procedurally Generated Dungeons tool that generates a random dungeon map. The program will feature at least one substantial algorithm that is not part of the course prerequisites. Specifically, I will implement an algorith for generating a Delaunay triangulation, which will serve as the foundation for creating the dungeon layout and connecting the rooms in a natural way. Delaunay triangulation ensures that no points are inside the circumcircle of any triangle, which helps to generate a map that is both efficient and visually appealing.


## Algorithms

1. **Room GEneration Algorithm**: Creates individual rooms within the dungeon.
2. **Corridor Generation Algorith**: Connects the rooms with corridors.
3. **Delaunay Triangulation Algorithm**: A custom algorithm to generate the dungeon's connectivity and layout based on geometric principles. This algorithm ensures that the generated rooms are well-connected and creates an efficient dungeon layout.

## Project Language

The project documentation will be written in English. The docstring comments in the code will also be in English. Code and variable names will be in English.


## Sources


The following sources will be used in this project:


- [Delaunay Triangulation (Wikipedia)](https://en.wikipedia.org/wiki/Delaunay_triangulation)
- [Bowyer–Watson algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm)
- [Creating Simple Procedural Dungeon Generation (Tom Stephenson)](https://www.tomstephensondeveloper.co.uk/post/creating-simple-procedural-dungeon-generation)
- [Procedurally Generated Dungeons(VAZGRIZ)](https://vazgriz.com/119/procedurally-generated-dungeons/)

