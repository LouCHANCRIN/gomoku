import numpy as np

from src.utils import timeit


@timeit
def minimax(state, alpha, beta, depth, is_maximiser):
    if depth == 0 or state.is_finished():
        return evaluation_state(state, state.color.swap())

    if is_maximiser:
        max_eval = np.int8.min
        for move in state.get_best_moves(is_maximiser):
            evaluation = minimax(
                state.next(move), alpha, beta, depth - 1, not is_maximiser
            )
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            return max_eval
    else:
        min_eval = np.int8.max
        for move in state.get_best_moves(not is_maximiser):
            evaluation = minimax(state.next(move), alpha, beta, depth - 1, is_maximiser)
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            return max_eval
