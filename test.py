import os
import time
import numpy as np

from model import ABModel

if __name__ == '__main__':
    white = 0
    black = 0
    drawn = 0
    for i in range(5):
        model = ABModel()
        step = 0
        while True:
            if step == 0:
                side = 'black'
            else:
                side = ['white', 'black'][(step - 1) // 2 % 2]
            val = model.search(1, side)
            if model.best_move is None:
                model.take(*np.random.randint(0, 19, size=2), side)
            else:
                model.take(*model.best_move, side)
            if model.no_move and step != 0:
                drawn += 1
                break
            os.system('cls')
            print(model)
            step += 1
            if model.judge() == 'white':
                white += 1
                break
            elif model.judge() == 'black':
                black += 1
                break
    print('white:', white)
    print('black:', black)
    print('drawn:', drawn)