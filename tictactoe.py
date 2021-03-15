"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_counter = 0
    O_counter = 0

    for row in board:
        for cell in row:
            if cell == X:
                X_counter += 1
            if cell == O:
                O_counter += 1
    
    if X_counter <= O_counter: # X goes first on an empty board
        return X
    else:
        return O
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_moves.add((i, j))
    
    return possible_moves
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # make deep copy of board to not modify original board
    resulting_board = copy.deepcopy(board) # + possible move

    # unpack tuple
    i, j = action

    if resulting_board[i][j] != EMPTY:
        raise Exception('Invalid move')
    else:
        resulting_board[i][j] = player(resulting_board)
    
    return resulting_board

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 8 possible winning permutations
    winning_configs = [[(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)], # rows
                       [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)], # columns
                       [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]] # diagonals

    for permutation in winning_configs:
        consecutive_X = 0
        consecutive_O = 0
        for i, j in permutation:
            if board[i][j] == X:
                consecutive_X += 1
                if consecutive_X == 3:
                    return X
            elif board[i][j] == O:
                consecutive_O += 1
                if consecutive_O == 3:
                    return O
    # no winner
    return None

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not actions(board):
        return True
    else:
        return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # alpha and beta are initially -inf and +inf, respectively
    alpha = -math.inf
    beta = math.inf

    # X is maximizing player
    if player(board) == X:
        value = -math.inf
        for action in actions(board):
            new_value = alphabeta(result(board,action), alpha, beta, O)
            alpha = max(new_value, value)
            if new_value > value:
                value = new_value
                best_move = action
    else:
        value = math.inf
        for action in actions(board):
            new_value = alphabeta(result(board, action), alpha, beta, X)
            beta = min(new_value, value)
            if new_value <= value:
                value = new_value
                best_move = action
    
    return best_move

    # raise NotImplementedError

# code adopted from wikipedia's pseudocode (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
def alphabeta(board, alpha, beta, player):
    if terminal(board):
        return utility(board)

    # X is maximizing player
    if player == X:
        value = -math.inf
        for action in actions(board):
            value = max(value, alphabeta(result(board, action), alpha, beta, O))
            alpha = max(alpha, value)
            if alpha > beta:
                break
        return value
    else:
        value = math.inf
        for action in actions(board):
            value = min(value, alphabeta(result(board,action), alpha, beta, X))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value