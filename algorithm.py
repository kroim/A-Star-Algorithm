import networkx as nx


class Maze:
    def __init__(self, file):
        self.file = file
        self.data = []
        self.create_maze_array()

    def create_maze_array(self):
        file = open('input.txt', 'r')
        maze_array = []
        for line in file:
            line = line.strip()
            items = line.split(" ")
            maze_array.append(items)
        self.data = maze_array


if __name__ == '__main__':
    M = Maze('input (1).txt')
    print(M.data)
