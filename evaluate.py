import re
import numpy as np
from scipy import signal
from values import cost

def sigmoid(X):
    return 1 / (1 + np.exp(-X))

def F(x):
    nonzero = np.array(x != 0, dtype=np.int)
    ev = (9 ** np.abs(x + 0.1)) * (x + 0.1 / np.abs(x + 0.1))
    return nonzero * ev

def valid(x, y):
    return x >= 0 and x < 19 and y >= 0 and y < 19

def repeat_scalar(value, type):
    offset = {'h': 1, 'v': 2, 'd1': 3, 'd2': 4}[type]
    return (value >> offset) % 2 == 1

def repeat(vector, type):
    offset = {'h': 1, 'v': 2, 'd1': 3, 'd2': 4}[type]
    return ((vector >> offset) % 2 == 1).any()

def trim_diagonal(i, j, x0, x1, y0, y1):
    if i - x0 > j - y0:
        x0 += ((i - x0) - (j - y0))
    else:
        y0 += ((j - y0) - (i - x0))
    if x1 - i > y1 - j:
        x1 -= ((x1 - i) - (y1 - j))
    else:
        y1 -= ((y1 - j) - (x1 - i))
    return x0, x1, y0, y1

def evaluate(matrix):
    h_connects = F(signal.convolve2d(matrix, 0.8 * np.ones([1, 6]), mode='same', fillvalue=0))
    v_connects = F(signal.convolve2d(matrix, 0.8 * np.ones([6, 1]), mode='same', fillvalue=0))
    d_connects = F(signal.convolve2d(matrix, 0.8 * np.eye(6), mode='same', fillvalue=0))
    r_connects = F(signal.convolve2d(matrix, 0.8 * np.rot90(np.eye(6)), mode='same', fillvalue=0))
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

def handle_hv(i, j, x0, x1, y0, y1, matrix, original, handle, type):
    airs = []
    offset = 1 if type == 'h' else 2
    if type == 'h':
        mat = matrix[i, y0:y1]
        ori = list(original[i, y0:y1])
        if y0 == 0:
            while len(ori) < 11:
                ori.insert(0, -1)
        if y1 == 19:
            while len(ori) < 11:
                ori.append(-1)
        center = j - y0
    elif type == 'v':
        mat = matrix[x0:x1, j]
        ori = list(original[x0:x1, j])
        if x0 == 0:
            while len(ori) < 11:
                ori.insert(0, -1)
        if x1 == 19:
            while len(ori) < 11:
                ori.append(-1)
        center = i - x0
    if not repeat(mat, type):
        handle([i, j], center, ori)
        mat += (np.array(mat != 0, dtype=np.int) << offset)

def handle_dd(i, j, x0, x1, y0, y1, matrix, original, handle, type):
    offset = 3 if type == 'd1' else 4
    vector = []
    center = 0
    for dx in range(-5, 6):
        x2 = i + dx if type == 'd1' else i - dx
        y2 = j + dx
        if valid(x2, y2):
            if repeat_scalar(matrix[x2, y2], type):
                return
            vector.append(original[x2, y2])
            if dx == 0:
                center = len(vector) - 1
            matrix[x2, y2] += np.array(matrix[x2, y2] != 0, dtype=np.int) << offset
        else:
            vector.append(-1)
    handle([i, j], center, vector)

def traverse(matrix, handle):
    original = np.array(matrix, dtype=np.int)
    matrix = np.array(matrix, dtype=np.int)
    f0 = lambda a : a-5 if a > 5 else 0
    f1 = lambda a : a+6 if a < 13 else 19
    f = lambda i, j : (f0(i), f1(i), f0(j), f1(j))
    for i in range(19):
        for j in range(19):
            if matrix[i, j] != 0:
                x0, x1, y0, y1 = f(i, j)
                handle_hv(i, j, x0, x1, y0, y1, matrix, original, handle, 'h')
                handle_hv(i, j, x0, x1, y0, y1, matrix, original, handle, 'v')
                handle_dd(i, j, x0, x1, y0, y1, matrix, original, handle, 'd1')
                handle_dd(i, j, x0, x1, y0, y1, matrix, original, handle, 'd2')

def get_score(i, j, center, line):
    count = {key: 0 for key in ['C6', 'A5', 'S5', 'A4', 'S4', 'A3', 'S3']}
    left_idx, right_idx = 5, 5
    while right_idx < 10:
        if line[right_idx + 1] != 1:
            break
        right_idx += 1
    while left_idx > 0:
        if line[left_idx - 1] != 1:
            break
        left_idx -= 1
    left_range, right_range = left_idx, right_idx
    while right_range < 10:
        if line[right_range + 1] == -1:
            break
        right_range += 1
    while left_range > 0:
        if line[left_range - 1] == -1:
            break
        left_range -= 1
    
    chess_range = right_range - left_range + 1
    m_range = right_idx - left_idx + 1

    if m_range == 6:
        count['C6'] += 1
    
    if m_range == 5:
        left_empty = right_empty = False
        if line[left_idx - 1] == 0:
            left_empty = True
        if line[right_idx + 1] == 0:
            right_empty = True
        if left_empty and right_empty:
            count['A5'] += 1
        elif left_empty or right_empty:
            count['S5'] += 1
    
    if m_range == 4:
        left_empty = right_empty = False
        left_five = right_five = False
        if line[left_idx - 1] == 0:
            if line[left_idx - 2] == 1:
                count['S5'] += 1
                left_five = True
            left_empty = True
        
        if line[right_idx + 1] == 0:
            if line[right_idx + 2] == 1:
                count['S5'] += 1
                right_five = True
            right_empty = True
        
        if left_five or right_five:
            pass
        elif left_empty and right_empty:
            if chess_range > 5:
                count['A4'] += 1
            else:
                count['S4'] += 1
        elif left_empty or right_empty:
            count['S4'] += 1
    
    if m_range == 3:
        left_empty = right_empty = False
        left_four = right_four = False
        if line[left_idx-1] == 0:
            if line[left_idx-2] == 1:
                if line[left_idx-3] == 0:
                    if line[right_idx+1] == 0:
                        count['A4'] += 1
                    else:
                        count['S4'] += 1
                    left_four = True
                elif line[left_idx-3] == -1:
                    if line[right_idx+1] == 0:
                        count['S4'] += 1
                        left_four = True
            left_empty = True
        
        if line[right_idx+1] == 0:
            if line[right_idx+2] == 1:
                if line[right_idx+3] == 1:
                    count['S5'] += 1
                    right_four = True
                elif line[right_idx+3] == 0:
                    if left_empty:
                        count['A4'] += 1
                    else:
                        count['S4'] += 1
                    right_four = True
                elif left_empty:
                    count['S4'] += 1
                    right_four = True
            right_empty = True
        if left_four or right_four:
            pass
        elif left_empty and right_empty:
            count['A3'] += 1
        elif left_empty or right_empty:
            count['S3'] += 1
    return count

def gen_move(matrix):
    move = np.zeros_like(matrix)
    blank = np.array(matrix == 0, dtype=np.int)
    filled = np.array(np.where(matrix != 0)).T
    around_indices = []
    for item in filled:
        around_indices.extend([item + np.array([0, 1]), item - np.array([0, 1]), item + np.array([1, 0]), item - np.array([1, 0])])
    for index in around_indices:
        if valid(*index) and blank[index[0], index[1]]:
            move[index[0], index[1]] = 1
    return np.array(np.where(move != 0)).T

# def evaluate(matrix):
#     score = 0
#     def handle(pos, center, vector):
#         nonlocal score
#         i, j = pos
#         count = get_score(i, j, center, vector)
#         for key in count:
#             score += count[key] * cost[key]
#     traverse(matrix, handle)
#     return score, gen_move(matrix)


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