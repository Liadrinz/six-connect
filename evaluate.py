import numpy as np
from scipy import signal

def F(x):
    return 10 ** x * np.array(x != 0, dtype=np.int)

def evaluate(matrix):
    h_connects = F(signal.convolve2d(matrix, np.ones([1, 6]), mode='same'))
    v_connects = F(signal.convolve2d(matrix, np.ones([6, 1]), mode='same'))
    d_connects = F(signal.convolve2d(matrix, np.eye(6), mode='same'))
    a_mat = h_connects + v_connects + d_connects
    legal_moves = np.array(a_mat != 0, dtype=np.int) * np.array(matrix == 0, dtype=np.int)
    return np.sum(a_mat), np.array(np.where(legal_moves != 0)).T

def judge(matrix):
    h_connects = signal.convolve2d(matrix, np.ones([1, 6]), mode='same')
    v_connects = signal.convolve2d(matrix, np.ones([6, 1]), mode='same')
    d_connects = signal.convolve2d(matrix, np.eye(6), mode='same')
    if (h_connects >= 6).any() or (v_connects >= 6).any() or (d_connects >= 6).any():
        return 'black'
    if (h_connects <= -6).any() or (v_connects <= -6).any() or (d_connects <= -6).any():
        return 'white'
    return None