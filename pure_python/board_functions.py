import numpy as np
import numba as nb
from numba import njit

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def init_board(size):
    board = np.zeros((size, size), dtype=np.int64)
    return board

@njit("UniTuple(boolean, 2)(int64[:,:], int64[:], int64, int64, int64)", fastmath=True)
def check_eating_enemy(board, position, step_x, step_y, player):
    # TODO: check if enemy can win by eating or break the serie
    left = [position[0] - step_x, position[1] - step_y]
    right = [position[0] + step_x, position[1] + step_y]
    enemy = player * -1

    eating_left = False
    eating_right = False

    consecutive_enemy = 0
    for i in range(0, 3):
        if left[0] >= 0 and left[1] >= 0 and left[0] <= 18 and left[1] <= 18:
            if board[left[0]][left[1]] == player and consecutive_enemy == 2:
                board[left[0] + step_x][left[1] + step_y] = 0
                board[left[0] + 2 * step_x][left[1] + 2 * step_y] = 0
                eating_left = True
                break
            elif board[left[0]][left[1]] == enemy:
                consecutive_enemy += 1
            else:
                break
        left[0] -= step_x
        left[1] -= step_y

    consecutive_enemy = 0
    for i in range(0, 3):
        if right[0] >= 0 and right[1] >= 0 and right[0] <= 18 and right[1] <= 18:
            if board[right[0]][right[1]] == player and consecutive_enemy == 2:
                board[right[0] - step_x][right[1] - step_y] = 0
                board[right[0] - 2 * step_x][right[1] - 2 * step_y] = 0
                eating_right = True
                break
            elif board[right[0]][right[1]] == enemy:
                consecutive_enemy += 1
            else:
                break
        right[0] += step_x
        right[1] += step_y
    return eating_left, eating_right

def update_board(board, eating_left, eating_right, position, step_x, step_y):
    if eating_left:
        board[position[0] - step_x][position[1] - step_y] = 0
        board[position[0] - 2 * step_x][position[1] - 2 * step_y] = 0
    
    if eating_right:
        board[position[0] + step_x][position[1] + step_y] = 0
        board[position[0] + 2 * step_x][position[1] + 2 * step_y] = 0
    
    return board

def place_stone(board, position, player):
    board[position[0]][position[1]] = player
    total_eat = 0
    # Check lr diag
    eating_left, eating_right = check_eating_enemy(board, position, -1, -1, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, -1, -1)
    
    # Check rl diag
    eating_left, eating_right = check_eating_enemy(board, position, 1, 1, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, 1, 1)
    
    # Check row diag
    print("\n\nCHECK ROW")
    print(position)
    eating_left, eating_right = check_eating_enemy(board, position, 0, 1, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, 0, 1)
    print("END CHECK ROW\n\n")
    
    # Check col diag
    eating_left, eating_right = check_eating_enemy(board, position, 1, 0, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, 1, 0)

    return board, total_eat

def add_stone(board, player, position, captured_stones):
    board[position[0]][position[1]] = player
    for stone in captured_stones:
        board[stone[0]][stone[1]] = 0
    return board

def remove_stone(board, player, position, captured_stones):
    board[position[0]][position[1]] = 0
    for stone in captured_stones:
        board[stone[0]][stone[1]] = -player
    return board

def print_board(board, last_move=None):
    row_len, col_len = board.shape
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    
    print("  0 1 2 3 4 5 6 7 8 9 A B C D E F G H I")
    for i in range(0, row_len):
        line = f'{index[i]} '
        for j in range(0, col_len):
            if board[i][j] == 1:
                if type(last_move) == np.ndarray and i == last_move[0] and j == last_move[1]:
                    line += f'{bcolors.FAIL}N{bcolors.ENDC} '
                else:
                    line += f'{bcolors.OKBLUE}N{bcolors.ENDC} '
            elif board[i][j] == -1:
                if type(last_move) == np.ndarray and i == last_move[0] and j == last_move[1]:
                    line += f'{bcolors.FAIL}B{bcolors.ENDC} '
                else:
                    line += f'{bcolors.OKGREEN}B{bcolors.ENDC} '
            else:
                line += '- '
        print(line)
    print()