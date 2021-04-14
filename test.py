import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

graph = nx.Graph()
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)

graph.add_edge(1, 2, weight=1)
graph.add_edge(2, 3, weight=5)
graph.add_edge(3, 1, weight=7)

print(graph.nodes)
print(graph.edges[1, 3]['weight'])
