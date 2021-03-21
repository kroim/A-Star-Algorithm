# A class to denote node/vertex & number of edges for that vertex
class Vertex:

	def __init__(self, vertex):
		self.vertex = vertex
		self.edges = []		# All connected edges of that vertex

	def __repr__(self):
		return str(self.vertex) + ' --> ' + self.edges.__repr__()

# A class for Graph data structure
class Graph:

	def __init__(self):
		self.totalVertices = 0		# A variable for keeping track of number of vertices in graph
		self.list = []		# Our adjacency list for storing vertices & their respective edges

	# A function to add vertex in the graph
	def addVertex(self, v):
		self.list.append(Vertex(v))
		self.totalVertices += 1

	# A function to add edge in a specific vertex
	def addEdge(self, v, e):
		# For that vertex, adding that specific edge
		for l in self.list:
			if l.vertex == v:
				l.edges.append(e)

	# A function to print graph
	def __repr__(self):
		return self.list.__repr__()

if __name__ == '__main__':

	# Reading matrix from file
	file = open('input.txt', 'r')
	matrix = []

	# Reading each number from each row from file & adding it to the matrix
	for row in file:
		r = []
		row = row.strip().split()
		for num in row:
			r.append(num)
		matrix.append(r)

	# creating a graph structure using our Graph class
	graph = Graph()

	# Now a '0' denote a vertex, keeping all required vertices in the graph in form of 'A', 'B', ... 'a', 'b'
	#node = 65

	# Replacing '0' with vertex num & adding vertices in the graph from matrix read from the file
	for i in range(0, len(matrix)):
		for j in range(0, len(matrix[i])):
			#if matrix[i][j] == '0' or matrix[i][j] == '3' or matrix[i][j] == '2':
			if matrix[i][j] == '0':
				#matrix[i][j] = chr(node)
				matrix[i][j]  = ((i, j))
				# Also adding vertex in the graph
				#graph.addVertex(matrix[i][j])
				graph.addVertex((i, j))
				#node += 1
				#if node == 91:		# Since Capital Alphabets has 26 letters, then start from lowercase letters
					#node = 97

	# Additionally printing matrix in 'A', 'B' form
	print('Matrix')
	for i in matrix:
		print(i)

	print('------------------------------------')
	print('***** GRAPH *****')

	# Now Adding All Edges of all vertices in the graph with specification of which vertex it is connected with..!
	for r in range(0, len(matrix)):
		for c in range(0, len(matrix[r])):

				# A value in matrix would only be vertex if it is not a wall or '2' or '3'
				v = matrix[r][c]

				if v != '1' and v != '2' and v != '3':
				#if v != '1':
					# Now determining edges for that vertex
					# Checking for left, right, up & down

					# LEFT
					if c > 0:
						cell = matrix[r][c-1]
						if cell != '1' and cell != '2' and cell != '3':
							graph.addEdge(v, matrix[r][c-1])

					# RIGHT
					if c < len(matrix[c])-1:
						cell = matrix[r][c+1]
						if cell != '1' and cell != '2' and cell != '3':
							graph.addEdge(v, matrix[r][c+1])

					# UP
					if r > 0:
						cell = matrix[r-1][c]
						if cell != '1' and cell != '2' and cell != '3':
							graph.addEdge(v, matrix[r-1][c])

					# DOWN
					if r < len(matrix[r])-1:
						cell = matrix[r+1][c]
						if cell != '1' and cell != '2' and cell != '3':
							graph.addEdge(v, matrix[r+1][c])
	# printing graph
	print(graph)