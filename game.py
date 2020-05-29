import numpy as np

from evaluate import evaluate, judge

INFINITY = 0xffffffff

class Game:

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
        if side == 'white':
            self.board[x, y] = 0
        else:
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

class ABGame(Game):
    
    def __init__(self, board=None):
        super().__init__(board=board)
        self.best_move = None

    def oab(self, depth, a, b, begin=0, top=True):
        side = 'white' if begin else 'black'
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
            v = -self.oab(depth - 1, -b, -a, 1-begin, False)
            self.untake(*move, side)
            if v >= b:
                return b
            if v > a:
                a = v
                best_move = move
        if top and best_move is not None:
            self.best_move = best_move
        return a
        
    def start(self, depth, side):
        begin = 0 if side == 'black' else 1
        return self.oab(depth, -INFINITY, INFINITY, begin)
    
    def min(self, depth, a, b):
        val, moves = evaluate(self.board)
        self.no_move = (len(moves) == 0)
        if depth <= 0:
            return val
        for move in moves:
            self.take(*move, 'white')
            if self.side == 'white':
                self.best_move = move
            val = self.max(depth - 1, b, a)
            self.untake(*move, 'white')
            if val < b:
                return b
            if val < a:
                a = val
        return a


    def max(self, depth, a, b):
        val, moves = evaluate(self.board)
        self.no_move = (len(moves) == 0)
        if depth <= 0:
            return val
        for move in moves:
            self.take(*move, 'black')
            if self.side == 'black':
                self.best_move = move
            val = self.min(depth - 1, b, a)
            self.untake(*move, 'black')
            if val > b:
                return b
            if val > a:
                a = val
        return a

