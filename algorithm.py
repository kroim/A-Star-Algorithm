import networkx as nx


class Maze:
    def __init__(self, file):
        self.file = file
        self.data = []
        self.create_maze_array()

    def create_maze_array(self):
        file = open(self.file, 'r')
        maze_array = []
        for line in file:
            line = line.strip()
            items = line.split(" ")
            maze_array.append(items)
        self.data = maze_array


class Graph:
    def __init__(self, maze_array):
        self.maze_array = maze_array
        self.weight = 1
        self.graph = nx.Graph()
        self.create_graph()

    def create_graph(self):
        graph = nx.Graph()
        for r_index, row in enumerate(self.maze_array):
            for c_index, col in enumerate(row):
                item_index = r_index * len(row) + c_index
                # add nodes to graph
                graph.add_node(item_index, pos=(r_index, c_index), data=col)
                # add edges to graph
                if col == '1':
                    continue
                if r_index == 1 and c_index == 0:
                    continue
                _up = r_index - 1
                _left = c_index - 1
                if _up > 0 and self.maze_array[_up][c_index] != '1':
                    _up_index = _up * len(row) + c_index
                    graph.add_edge(_up_index, item_index, weight=self.weight)
                if _left > 0 and self.maze_array[r_index][_left] != '1':
                    _left_index = r_index * len(row) + _left
                    graph.add_edge(_left_index, item_index, weight=self.weight)
        self.graph = graph


class Algorithm:
    def __init__(self, graph):
        self.graph = graph


if __name__ == '__main__':
    M = Maze('input1.txt')
    G = Graph(M.data)
    A = Algorithm(G.graph)
