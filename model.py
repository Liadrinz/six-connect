import numpy as np

from evaluate import evaluate, judge

INFINITY = 0xffffffff

class Model:

    def __init__(self, board=None):
        if board is None:
            self.board = np.zeros([19, 19])
        else:
            self.board = board
        self.best_move = None
        self.side = 'white'
        self.no_move = False
    
    def take(self, x, y, side):
        if side == 'white':
            self.board[x, y] = -1
        else:
            self.board[x, y] = 1

    def untake(self, x, y, side):
        self.board[x, y] = 0
    
    def judge(self):
        return judge(self.board)

    def __str__(self):
        result = ''
        for row in self.board:
            row_result = ''
            for val in row:
                row_result += ' ' * (1 + (val >= 0)) + str(int(val))
            result += row_result + '\n'
        return result
    
    def __repr__(self):
        return self.__str__()

class ABModel(Model):
    
    def __init__(self, board=None):
        super().__init__(board=board)
        self.best_move = None

    def oab(self, depth, a, b, begin=0, top=True):
        if begin == 0:
            side = 'white'
        elif (begin - 1) // 2 % 2 == 0:
            side = 'black'
        else:
            side = 'white'
        # side = 'white' if begin == 0 else 'black'
        val, moves = evaluate(self.board)
        best_move = None
        if depth == 0:
            return val
        if len(moves) > 0:
            self.no_move = False
        else:
            self.no_move = True
            return val
        for move in moves:
            self.take(*move, side)
            if begin == 0:
                v = -self.oab(depth - 1, -b, -a, begin + 1, False)
            elif (begin - 1) // 2 % 2 == 0:
                v = self.oab(depth, a, b, begin + 1, False)
            else:
                v = -self.oab(depth - 1, -b, -a, begin + 1, False)
            self.untake(*move, side)
            if v >= b:
                return b
            if v > a:
                a = v
                best_move = move
        if top and best_move is not None:
            self.best_move = best_move
        return a
        
    def search(self, depth, side):
        # begin = 0 if side == 'black' else 1
        return self.oab(depth, -INFINITY, INFINITY, 0)