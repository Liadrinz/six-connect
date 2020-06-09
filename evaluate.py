import re
import numpy as np
from scipy import signal

p = 1
q = 0.8
N = 9

def F(x):
    nonzero = np.array(x != 0, dtype=np.int)
    ev = p * (N ** np.abs(x + 0.1)) * (x + 0.1 / np.abs(x + 0.1))
    return nonzero * ev

def evaluate(matrix):
    h_connects = F(signal.convolve2d(matrix, q * np.ones([1, 6]), mode='same'))
    v_connects = F(signal.convolve2d(matrix, q * np.ones([6, 1]), mode='same'))
    d_connects = F(signal.convolve2d(matrix, q * np.eye(6), mode='same'))
    r_connects = F(signal.convolve2d(matrix, q * np.rot90(np.eye(6)), mode='same'))
    a_mat = h_connects + v_connects + d_connects + r_connects
    legal_moves = np.array(a_mat != 0, dtype=np.int) * np.array(matrix == 0, dtype=np.int)
    return np.sum(a_mat), np.array(np.where(legal_moves != 0)).T

def judge(matrix):
    h_connects = signal.convolve2d(matrix, np.ones([1, 6]), mode='same')
    v_connects = signal.convolve2d(matrix, np.ones([6, 1]), mode='same')
    d_connects = signal.convolve2d(matrix, np.eye(6), mode='same')
    r_connects = signal.convolve2d(matrix, np.rot90(np.eye(6)), mode='same')
    if (h_connects >= 6).any() or (v_connects >= 6).any() or (d_connects >= 6).any() or (r_connects >= 6).any():
        return 'black'
    if (h_connects <= -6).any() or (v_connects <= -6).any() or (d_connects <= -6).any() or (r_connects <= -6).any():
        return 'white'
    return None

import time

if __name__ == '__main__':
    board = np.zeros([19, 19])
    board[:6, :6] = np.eye(6)
    board[0, 13:18] = [1 for _ in range(5)]
    board[13:19, 0] = [1 for _ in range(6)]
    score = evaluate(board)
    print(score)
    # count = get_score(0, 0, 5, [0, 0, 0, 1, 1, 1, 1, -1, -1, 0, 0])
    # print(count)