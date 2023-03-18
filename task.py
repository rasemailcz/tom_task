import csv
from collections import defaultdict

import cv2
import numpy as np


# This class represents a directed graph using adjacency list representation
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph

    # function to add an edge to graph
    def add_edge(self, u, v):
        self.graph[u].append(v)

    # A function used by DFS
    def dfs_core(self, v, visited, scc):
        # Mark the current node as visited and print it
        visited[v] = True
        scc.append(v)
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.dfs_core(i, visited, scc)

    def fill_order(self, v, visited, stack):
        # Mark the current node as visited
        visited[v] = True
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.fill_order(i, visited, stack)
        stack.append(v)

    # TODO: Function that returns reverse (or transpose) of this graph
    def get_transpose(self):
        raise RuntimeError("NOT IMPLEMENTED")

    # The main function that finds and prints all strongly connected components
    def get_strongly_connected_components(self):
        stack = []
        # TODO: Mark all the vertices as not visited (For first DFS)
        visited = None

        # Fill vertices in stack according to their finishing times
        for i in range(self.V):
            if not visited[i]:
                self.fill_order(i, visited, stack)

        # Create a reversed graph
        gr = self.get_transpose()

        # TODO: Mark all the vertices as not visited (For second DFS)
        visited = None

        # Now process all vertices in order defined by Stack
        # TODO: Get the length of the largest SCC in graph!
        while stack:
            i = stack.pop()
            if not visited[i]:
                scc = []
                gr.dfs_core(i, visited, scc)


def prepare_graph(scc_data_path):
    vertices_number = 0
    vertex_tuples = []
    with open(scc_data_path, 'r') as file:
        for row in csv.reader(file, delimiter=" "):
            u, v = [int(n) for n in row[:2]]
            vertex_tuples.append([u, v])
            if u > vertices_number:
                vertices_number = u
    g = Graph(vertices_number)
    for u, v in vertex_tuples:
        if v >= vertices_number:
            continue
        g.add_edge(u, v)

    return g


if __name__ == '__main__':
    scc_data_path = 'data/graph_data.txt'

    # PART 1: Implement missing parts of the
    #           Kosaraju's algorithm for detection of strongly-connected components (SCC) in graph
    #           and compute the size of the largest SCC

    graph = prepare_graph(scc_data_path)
    graph.get_strongly_connected_components()

    # PART 2: decode the professor's image with the size of the largest SCC as the SEED
    SEED = 0
    np.random.seed(SEED)

    image = np.load('coded_image.npz')
    image = image - np.random.normal(0, 1, size=image.shape)

    image_decoded = image * 127.5 + 127.5
    image_decoded = image_decoded.astype(np.uint8)

    lines_num = 0  # at what time was the electrifier run?

    cv2.imwrite('partially_decoded_image.png', image_decoded)
    coded_mesage = image_decoded[:lines_num, :, 0]
    image_decoded = image_decoded[lines_num:]

    print([chr(c) for c in coded_mesage.reshape(-1)])
    cv2.imwrite('decoded_image.png', image_decoded)
