import itertools
import operator

square = [[ 8,  5, 13, 13, 29, 15, 23, 30],
          [17 ,22, 30,  3, 13, 25,  2, 14],
          [10, 15, 18, 28,  2, 18, 27,  6],
          [ 0, 31,  1, 11, 22,  7, 16, 20],
          [12, 17, 24, 26,  3, 24, 25,  5],
          [27, 31,  8, 11, 19,  4, 12, 21],
          [21, 20, 28,  4,  9, 26,  7, 14],
          [ 1,  6,  9, 19, 29, 10, 16,  0]]

class Board:
     def __init__(self):
         self.board = square
         self.pos = (0, 0)
         self.size = 8
         self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

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
         pass