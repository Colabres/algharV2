from src.visualization import visualize_dungeon

from src.dungeon import initialize_dungeon

dungeonMap,graph = initialize_dungeon(80,50,20,5,6,5,3)
visualize_dungeon(dungeonMap,graph)
