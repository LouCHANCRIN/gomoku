import numpy as np
import random
import get_lines

def is_array_equal(arr, seq):
    for arri, seqi in zip(arr, seq):
        if arri != seqi:
            return False
    return True

def get_new_threats(board, row_index, col_index, maximizing_player):
    lr_diags, rl_diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    score = 0
    score += check_line(lr_diags, row_index, maximizing_player)
    score += check_line(rl_diags, row_index, maximizing_player)
    score += check_line(rows, col_index, maximizing_player)
    score += check_line(columns, row_index, maximizing_player)

    return score

def check_side(side, player):
    # Number of consecutive pawn placed directly next to the one played
    consecutive = 0
    # Number of enemy consecutive pawn placed directly next to the one played
    consecutive_enemy = 0
    # Number of consecutive pawn separated by one zero from the consecutive ones
    additional = 0
    # Is there an empty space at the end of the last serie of pawn
    empty_space = False
    # Eating enemy
    eating_enemy = False
    # Open eating move
    open_eating_move = False

    is_consecutive = True
    check_eating_enemy = True
    check_open_eating_move = True
    is_after_one_zero = False
    for i in range(0, min(len(side), 5)):
        if is_consecutive:
            if side[i] == player:
                consecutive += 1
            else:
                is_consecutive = False

        if check_eating_enemy or check_open_eating_move:
            if side[i] == player * -1 and consecutive_enemy < 2:
                consecutive_enemy += 1
            elif side[i] == player and consecutive_enemy == 2:
                # Return eating_move
                return 0, 0, False, True, False
            elif side[i] == 0 and consecutive_enemy == 2:
                # Return open_eating_move
                return 0, 0, False, False, True
            else:
                check_eating_enemy = False
                check_open_eating_move = False

        if side[i] == 0:
            if is_after_one_zero:
                break
        else:
            is_after_one_zero = True
        
        if is_after_one_zero:
            if side[i] == player:
                additional += 1
        
    return consecutive, additional, empty_space, eating_enemy, open_eating_move

def check_line(line, starting_index, maximizing_player):
    if maximizing_player:
        player = 1
    else:
        player = -1
    
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:,]
    l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move = check_side(left, player)
    r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move = check_side(right, player)
    # print(check_consecutive(left, player))
    # print(line)
    # print(left, right)
    # print(l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move)
    # print(r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move)
    # print()
    score = 0
    if l_consecutive + r_consecutive == 4:
        # Win
        return 100_000_000
    
    if l_consecutive + r_consecutive == 3 and l_empty_space and r_empty_space:
        # 4 in a row with an open room on each side
        score += 10_000_000

    if l_consecutive + r_consecutive == 3:
        score += 100_000

    if l_consecutive + r_consecutive == 2:
        score += 1_000
    
    if l_consecutive + r_consecutive == 1:
        score += 10

    return score
