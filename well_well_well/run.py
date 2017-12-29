#!/usr/bin/env python3

import itertools
import operator
import numpy as np
import math
import string
import networkx as nx
import matplotlib.pyplot as plt

square = [[ 1,  5, 27, 22, 28, 40, 14],
          [39, 13, 17, 30, 41, 12,  2],
          [32, 35, 24, 25, 19, 47, 34],
          [16, 33, 10, 42,  7, 44, 18],
          [ 3,  8, 45, 37,  4, 21, 20],
          [15, 46, 38,  6, 26, 48, 49],
          [ 9, 23, 31, 29, 11, 36, 43]]
N_COLS = len(square[0])
N_ROWS = len(square)
#data = np.matrix(square

class Well:
    def __init__(self):
        self.time = 0
        self.fr = 1 #flow rate
        self.G = nx.DiGraph()
        self.init_node = (0, 0)
        # set up nodes
        for r in range(N_ROWS):
            for c in range(N_COLS):
                self.G.add_node((r, c), depth=square[r][c])

        # vertical edges
        for r in range(N_ROWS - 1):
            for c in range(N_COLS):
                delta = self.G.nodes[(r + 1, c)]["depth"] - self.G.nodes[(r, c)]["depth"]
                if delta > 0:
                    self.G.add_edge((r, c), (r + 1, c), borders=1, capacity=delta)
                else:
                    self.G.add_edge((r + 1, c), (r, c), borders=1, capacity=-delta)

        # horizontal edges
        for r in range(N_ROWS):
            for c in range(N_COLS - 1):
                delta = self.G.nodes[(r, c + 1)]["depth"] - self.G.nodes[(r, c)]["depth"]
                if delta > 0:
                    self.G.add_edge((r, c), (r, c + 1), borders=1, capacity=delta)
                else:
                    self.G.add_edge((r, c + 1), (r, c), borders=1, capacity=-delta)

    def isSink(self, node):
        # check if node has successors
        for _ in self.G.successors(node):
            return False
        maxFlow = nx.maximum_flow(self.G, self.init_node, node)
        if maxFlow > 0:
            return True
        else:
            return False

    def mergeNodes(self, host, child):
        child_only = []
        both = []
        for _ in self.G.successors(child):
            raise RuntimeError("YOU FAIL")
        for n in self.G.predecessors(child):
            child_only.append(n)
        child_only.remove(host)
        for n in self.G.predecessors(host):
            pass
#plt.subplot(121)
#nx.draw_spectral(G, with_labels=True, font_weight='bold')
#plt.show()