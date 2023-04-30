import numpy as np
from tabulate import tabulate

class TIN_Edges:

	def __init__(self, tin_vertices, tin_triangles):
		self.tin_vertices  = tin_vertices
		self.tin_triangles = tin_triangles

	def sort_tri_indexes( self, i1, i2 ):
		si1 = min(i1, i2)
		si2 = max(i1, i2)
		return (si1, si2)

	def identify_edges(self):
		n_vertices = len(self.tin_vertices) 
		tri_edge_map = np.zeros( shape=(n_vertices, n_vertices), dtype=np.int8 )

		for tri in self.tin_triangles:
			edge1 = self.sort_tri_indexes(tri[0], tri[1])
			edge2 = self.sort_tri_indexes(tri[1], tri[2])
			edge3 = self.sort_tri_indexes(tri[2], tri[0])

			tri_edge_map[edge1[0], edge1[1]] += 1
			tri_edge_map[edge2[0], edge2[1]] += 1
			tri_edge_map[edge3[0], edge3[1]] += 1

		headers = ["col 1", "col 2", "col 3"]
		table = tabulate(tri_edge_map, tablefmt="fancy_grid")
		print(table)

		edge_vertices = np.transpose( np.nonzero( tri_edge_map == 1 ) )
		# print(edge_vertices)

		sorted_edges = self.sort_edges( edge_vertices, tri_edge_map )
		print(sorted_edges)
		return edge_vertices

	def sort_edges(self, edge_vertices, tri_edge_map, close = False):
		sorted_edges = [ edge_vertices[0][0] ]
		index_map = {
			edge_vertices[0][0]: True
		}

		for edge in edge_vertices:
			next_vertex = None
			row = tri_edge_map[ sorted_edges[-1], : ]
			col = tri_edge_map[ :, sorted_edges[-1] ]

			for i in range(len(row)):
				if row[i] == 1 and i not in index_map:
					next_vertex = i
					sorted_edges.append( i )
					index_map[ i ] = True
					break

			if next_vertex != None:
				continue

			for i in range(len(col)):
				if col[i] == 1 and i not in index_map:
					next_vertex = i
					sorted_edges.append( i )
					index_map[ i ] = True
					break

		if close:
			sorted_edges.append( sorted_edges[0] )

		return sorted_edges

if __name__ == '__main__':

	tin_vertices = [
		[0, 0, 100],
    	[30, 30, 100],
    	[30, 0, 100],
    	[0, 30, 100],
    ]
	tin_triangles = [ 
		[0,1,2],
		[1,0,3],
	]
	te = TIN_Edges( tin_vertices, tin_triangles )

	edges = te.identify_edges()
		