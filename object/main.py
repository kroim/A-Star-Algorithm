# constructs a triangulation on the polygon world and forms a graph of the paths

import cv2
import descartes
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import triangle as tr
from environment import scenario
from shapely.ops import unary_union
from simulation import plot_endpoints
from AStarAlgorithm import AStarAlgorithm

xlen = 100
ylen = 50
size = (ylen, xlen)
G = nx.Graph()

###########################################################################
# POLYGON WORLD
###########################################################################
polygons, start, goal = scenario('polyworld', size)

# combine overlapping polygons
polygons = unary_union(polygons)
start = list(start)
goal = list(goal)

fig, ax = plt.subplots(1, 1)

for poly in polygons:
    ax.add_patch(descartes.PolygonPatch(poly, fc='blue', alpha=0.5))

plot_endpoints(ax, start, goal)

fig.set_facecolor('white')
fig.set_edgecolor('white')
plt.axis('on')

plt.show()

fig.savefig('plot.png')
img = cv2.imread('plot.png')

holes = np.empty((len(polygons), 2), dtype=int)
corners = np.empty((100, 2), dtype=int)
f = 0
for k in range(len(polygons)):
    # store holes in array
    point = polygons[k].centroid
    holes[k] = [point.x, point.y]

    # add each verticy in an array and dictionary
    vertices = list(polygons[k].exterior.coords)
    vertices = np.array(tuple(tuple(map(int, x)) for x in vertices))
    for j in range(len(vertices) - 1):
        c = vertices[j]
        corners[f] = c
        f += 1

# add corners of environment boundaries
corners[f] = [0, 0]
f += 1
corners[f] = [xlen, 0]
f += 1
corners[f] = [xlen, ylen]
f += 1
corners[f] = [0, ylen]
f += 1

corners = corners[0:f, :]

# store segments in array
segments = np.empty((100, 2), dtype=int)
g = 0
for h in range(len(polygons)):
    vertices = list(polygons[h].exterior.coords)
    vertices = np.array(tuple(tuple(map(int, x)) for x in vertices))
    for n in range(len(vertices) - 1):
        c = [vertices[n][0], vertices[n][1]]
        c2 = [vertices[n + 1][0], vertices[n + 1][1]]
        ind1 = corners.tolist().index(c)
        ind2 = corners.tolist().index(c2)
        segments[g] = [ind1, ind2]
        g += 1

# add walls of environment
segments[g] = [f - 4, f - 3]
g += 1
segments[g] = [f - 3, f - 2]
g += 1
segments[g] = [f - 2, f - 1]
g += 1
segments[g] = [f - 1, f - 4]
g += 1
segments = segments[0:g, :]

# Create Dictionary
poly = {'holes': holes,
        'vertices': corners,
        'segments': segments}

t = tr.triangulate(poly, 'pc')
# tr.compare(plt, poly, t)
plt.axis('on')
tr.plot(plt.axes(), **t)

plt.xlim(0, 100)
plt.ylim(0, 50)

triList = t['triangles']
corners = t['vertices']
nodes = {}
triGraph = {}

# # find and plot centers of triangles (remember nodes closest to start and goal )
startNodeIndex = 0
sVal = xlen
goalNodeIndex = 0
gVal = xlen

for q in range(len(triList)):
    # coordinate of the vertices
    vert1 = corners[triList[q][0]]
    vert2 = corners[triList[q][1]]
    vert3 = corners[triList[q][2]]
    # calculate centroid
    x = np.uint8((vert1[0] + vert2[0] + vert3[0]) / 3)
    y = np.uint8((vert1[1] + vert2[1] + vert3[1]) / 3)
    # store in a node dictionary
    nodes[q] = [x, y]
    # find closest nodes to start and end
    temp = np.linalg.norm(np.array([goal[1], goal[0]]) - np.array([x, y]))
    if temp < gVal:
        gVal = temp
        goalNodeIndex = q
    temp = np.linalg.norm(np.array(start) - np.array([x, y]))
    if temp < sVal:
        sVal = temp
        startNodeIndex = q

# if any of the previous nodes share 2 verticies
# add them to the dictionary
for d in range(len(nodes)):
    vert1 = triList[d][0]
    vert2 = triList[d][1]
    vert3 = triList[d][2]
    for b in range(len(nodes)):
        verta = triList[b][0]
        vertb = triList[b][1]
        vertc = triList[b][2]
        count = 0
        if np.any([verta == vert1, verta == vert2, verta == vert3]):
            count += 1
        if np.any([vertb == vert1, vertb == vert2, vertb == vert3]):
            count += 1
        if np.any([vertc == vert1, vertc == vert2, vertc == vert3]):
            count += 1

        if count == 2:
            if d in triGraph:
                triGraph[d] = [*triGraph[d], b]
                G.add_node(d)
            else:
                triGraph[d] = [b]
                G.add_node(d)

# add start and end points
nodes[len(nodes)] = list(start)
nodes[len(nodes)] = list([goal[1], goal[0]])
triGraph[len(triGraph)] = [startNodeIndex]
G.add_node(startNodeIndex)
triGraph[len(triGraph)] = [goalNodeIndex]
G.add_node(goalNodeIndex)

# plot nodes and edges of graph
for u in triGraph:
    uCoords = nodes[u]
    for v in range(len(triGraph[u])):
        vCoords = nodes[triGraph[u][v]]
        plt.plot([nodes[u][0], nodes[triGraph[u][v]][0]], [nodes[u][1], nodes[triGraph[u][v]][1]], 'bo-')
        wt = np.linalg.norm(np.array(uCoords) - np.array(vCoords))
        G.add_edge(triGraph[u][v], u, weight=wt)

# add start and end point markers
plt.plot(start[0], start[1], 'ro', markersize=12)
plt.plot(goal[1], goal[0], 'ro', markersize=12)
plt.show()
plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
AStarAlgorithm(G, nodes)
