import itertools
import operator
import numpy as np
import math
import string

square = [[ 8,  5, 13, 13, 29, 15, 23, 30],
          [17 ,22, 30,  3, 13, 25,  2, 14],
          [10, 15, 18, 28,  2, 18, 27,  6],
          [ 0, 31,  1, 11, 22,  7, 16, 20],
          [12, 17, 24, 26,  3, 24, 25,  5],
          [27, 31,  8, 11, 19,  4, 12, 21],
          [21, 20, 28,  4,  9, 26,  7, 14],
          [ 1,  6,  9, 19, 29, 10, 16,  0]]
MAX_MOVES = 40
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
START = (7, 0)
FINISH = (0, 7)
data = np.matrix(square)

def isSquare(number):
    if number < 1:
        return False
    return math.sqrt(number) - int(math.sqrt(number)) == 0

def getValidMoves(pos):
    moves = []
    for m in MOVES:
        step = 0
        while True:
            step += 1
            move = tuple(i * step for i in m)
            new_pos = tuple(map(operator.add, pos, move))
            if new_pos[0] < 0 or new_pos[0] >= data.shape[0] or new_pos[1] < 0 or new_pos[1] >= data.shape[1]:
                break
            moves.append(new_pos)
    return moves

def parseMove(startDecrement, frm, to):
    fieldSum = data[frm] + data[to] - 2*startDecrement
    decrement = 5
    if fieldSum > 0 and isSquare(fieldSum):
        decrement = 1
    return data[to] - startDecrement, decrement

def makeMoveLookup():
    lut = {}
    for r in range(data.shape[0]):
        for c in range(data.shape[1]):
            lut[(r, c)] = getValidMoves((r, c))
    return lut

def makeFieldList(npArray):
    fields = []
    for r in range(npArray.shape[0]):
        for c in range(npArray.shape[1]):
            fields.append((r,c))
    return fields

def prettyMove(rawMove, shape):
    alphabet = list(string.ascii_lowercase)
    letter = alphabet[rawMove[1]]
    return letter + str(shape[0] - rawMove[0])

class Node:
    def __init__(self):
        self.parents = []
        self.children = []
        self.score = 0
        self.bestParent = None

lut = makeMoveLookup()
fl = makeFieldList(data)
#print(lut)
#print(fl)

graph = {}
graph[0] = {}
graph[0][START] = Node()
for n in range(1, MAX_MOVES):
    graph[n] = {}
    for m in fl:
        graph[n][m] = Node()


initalMoves = lut[(0, 0)]
for m in initalMoves:
    score, decrement = parseMove(0, START, m)
    node = graph[decrement][m]
    node.parents.append((0, START))
    node.score += score
    node.bestParent = (0, START)
    graph[0][START].children.append((decrement, m))

for n in range(1, MAX_MOVES):
    for f in fl:
        from_node = graph[n][f]
        if len(from_node.parents) > 0:
            moves = lut[f]
            for m in moves:
                score, dec = parseMove(n, f, m)
                if n + dec < MAX_MOVES:
                    #print("Move: " + str(m))
                    #print("Decrement " + str(n+dec))
                    #print(graph[n + dec])
                    #print("Key " + str(m) + " in dict: " + str(bool(m in graph[n + dec])))
                    from_node.children.append((n + dec, m))
                    to_node = graph[n + dec][m]
                    to_node.parents.append((n, f))
                    if to_node.score < from_node.score + score:
                        to_node.score = from_node.score + score
                        to_node.bestParent = ((n, f))

results = {}
for i in range(1, MAX_MOVES):
    print("Score at decrement " + str(i) + ": " + str(graph[i][FINISH].score))
    results[i] = graph[i][FINISH].score
best_decrement = -1
highscore = -1
for k, v in results.items():
    if v > highscore:
        highscore = v
        best_decrement = k
parent = (best_decrement, FINISH)

winningMoves = []
while parent != None:
    #print("Dec: " + str(parent[0]) + " at " + str(parent[1]))
    winningMoves.append(parent[1])
    #prev_score = graph[parent[0]][parent[1]].score
    parent = graph[parent[0]][parent[1]].bestParent
    #print("Delta score: " + str(-graph[parent[0]][parent[1]].score + prev_score))



class Board:
     def __init__(self):
         self.board = np.matrix(square)
         self.pos = START
         self.size = 8
         self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
         self.score = 0
         self.nMoves = 0

     def getMoves(self):
         moves = []
         for m in self.moves:
             step = 0
             pos = self.pos
             while True:
                 step += 1
                 move = tuple(i * step for i in m)
                 new_pos = tuple(map(operator.add, self.pos, move))
                 if new_pos[0] < 0 or new_pos[0] >= self.size or new_pos[1] < 0 or new_pos[1] >= self.size:
                     break
                 moves.append(new_pos)
         return moves

     def move(self, to):
         if to[0] < 0 or to[0] >= self.size or to[1] < 0 or to[1] >= self.size:
             raise ValueError("move target out of bounds")

         stepSum = self.getAt(self.pos) + self.getAt(to)
         self.score += self.getAt(to)
         if (isSquare(stepSum)):
             self.board -= 1
         else:
             self.board -= 5

         self.pos = to

     def getAt(self, pos):
         return self.board[pos]

b = Board()
print("-- Breakdown --")
print("Score: 0")
winningMoves.reverse()
for m in winningMoves[1:]:
    b.move(m)
    print("After moving to " + prettyMove(m, data.shape) + ": " + str(b.score))