import os
import time
import numpy as np

from game import ABGame

if __name__ == '__main__':
    white = 0
    black = 0
    drawn = 0
    for i in range(5):
        game = ABGame()
        step = 0
        while True:
            if step == 0:
                side = 'black'
            else:
                side = ['white', 'black'][(step - 1) // 2 % 2]
            val = game.start(1, side)
            if game.best_move is None:
                game.take(*np.random.randint(0, 19, size=2), side)
            else:
                game.take(*game.best_move, side)
            if game.no_move and step != 0:
                drawn += 1
                break
            os.system('cls')
            print(game)
            step += 1
            if game.judge() == 'white':
                white += 1
                break
            elif game.judge() == 'black':
                black += 1
                break
    print('white:', white)
    print('black:', black)
    print('drawn:', drawn)