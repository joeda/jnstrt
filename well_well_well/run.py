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
#data = np.matrix(square)
G = nx.DiGraph()

#set up nodes
for r in range(N_ROWS):
    for c in range(N_COLS):
        G.add_node((r, c), depth=square[r][c])

#vertical edges
for r in range(N_ROWS - 1):
    for c in range(N_COLS):
        delta = G.nodes[(r+1,c)]["depth"] - G.nodes[(r, c)]["depth"]
        if delta < 0:
            G.add_edge((r, c), (r+1, c), grad= -delta)
        else:
            G.add_edge((r+1, c), (r, c), grad=delta)

#horizontal edges
for r in range(N_ROWS):
    for c in range(N_COLS - 1):
        delta = G.nodes[(r, c+1)]["depth"] - G.nodes[(r, c)]["depth"]
        if delta < 0:
            G.add_edge((r, c), (r, c+1), grad= -delta)
        else:
            G.add_edge((r, c+1), (r, c), grad=delta)

plt.subplot(121)
nx.draw_spectral(G, with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(G)
plt.show()