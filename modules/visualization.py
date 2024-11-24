import matplotlib.pyplot as plt

#using numpy to actually draw a visualisation of a new generated dungeon
def visualize_dungeon(dungeon_map, graph):
    print(graph)
    plt.imshow(dungeon_map, cmap='gray', vmin=0, vmax=3)
    for room1, room2, _ in graph:
        plt.plot([room1.x, room2.x], [room1.y, room2.y], 'blue', lw=1)

    plt.title("Dungeon Visualization")
    plt.show()