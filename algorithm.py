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
    def __init__(self, maze_array, start, end):
        self.maze_array = maze_array
        self.weight = 1
        self.start_node = Node
        self.end_node = Node
        self.graph = nx.Graph()
        self.create_graph(start, end)

    def create_graph(self, start, end):
        graph = nx.Graph()
        for r_index, row in enumerate(self.maze_array):
            for c_index, col in enumerate(row):
                item_index = r_index * len(row) + c_index
                # add nodes to graph
                graph.add_node(item_index, pos=(r_index, c_index), data=col)
                if col == start:
                    self.start_node = item_index
                if col == end:
                    self.end_node = item_index
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


class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def _equals(self, item):
        return self.pos == item.pos


class Algorithm:
    def __init__(self, graph, start_node, end_node):
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.search()

    def return_path(self):
        pass

    def search(self):
        graph = self.graph
        print(graph.nodes[self.start_node])
        print(graph.nodes[self.end_node])


if __name__ == '__main__':
    M = Maze('input1.txt')
    G = Graph(M.data, '3', '2')
    A = Algorithm(G.graph, G.start_node, G.end_node)
