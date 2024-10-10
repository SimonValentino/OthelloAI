from OthelloState import Piece, OthelloState
import random
import time
from copy import deepcopy

INF = float('inf')
DEPTH = 5

COUNT_WEIGHT = 100
LATE_GAME_COUNT_WEIGHT = 5000
LATE_GAME = 6
CHAIN_WEIGHT = 400
STRONG_CHAIN_WEIGHT = 1200
MATRIX_WEIGHT = 100

# Point matrix inspired by a paper written by Vaishnavi Sannidhanam and Muthukaruppan Annamalai
# in the Department of Computer Science and Engineering,
# Paul G. Allen Center,
# University of Washington,
# Seattle, WA-98195
POINT_MATRIX = [
    [100, -3, 11, 8, 8, 11, -3, 100],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [100, -3, 11, 8, 8, 11, -3, 100]
]

CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]

ADJACENT_CORNERS = [
    (0, 1), (1, 0), (1, 1), (0, 6), (1, 6), (1, 7),
    (6, 0), (6, 1), (7, 1), (6, 6), (6, 7), (7, 6)
]


class Agent:
    def __init__(self):
        return

    def getNextMove(self, state):
        # Make it always take a corner if it can
        # for x, y in CORNERS:
        #     if state.isValidMove(x, y, state.nextMove):
        #         return (x, y)

        time.sleep(0)
        # MINIMAX
        best_move, best_value = self.__minimax(
            state, state.nextMove, DEPTH, -INF, INF, True)

        return best_move

    def __minimax(self, state, my_color, depth, alpha, beta, is_maximizing):
        if depth == 0 or not state.existsNextMove():
            return None, self.__heuristic(state, my_color)

        best_move = None
        moves = self.__generate_possible_moves(state)
        if is_maximizing:
            max_eval = -INF
            for move in moves:
                new_state = self.__apply_move(state, move)
                eval = self.__minimax(
                    new_state, my_color, depth - 1, alpha, beta, False)[1]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    pass

            return best_move, max_eval
        else:
            min_eval = INF
            for move in moves:
                new_state = self.__apply_move(state, move)
                eval = self.__minimax(
                    new_state, my_color, depth - 1, alpha, beta, True)[1]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    pass

            return best_move, min_eval

    def __heuristic(self, state, my_color):
        opp_color = Piece.oppositePiece(my_color)
        board = state.board

        # MATRIX and COUNT
        my_matrix = 0
        opp_matrix = 0
        my_count = 0
        opp_count = 0

        for i in range(len(POINT_MATRIX)):
            for j in range(len(POINT_MATRIX[0])):
                if board[i][j] not in ADJACENT_CORNERS:
                    if board[i][j] == my_color:
                        my_matrix += POINT_MATRIX[i][j]
                        my_count += 1
                    elif board[i][j] == opp_color:
                        opp_matrix += POINT_MATRIX[i][j]
                        opp_count += 1

        count = my_count - opp_count

        for x, y in CORNERS:
            if board[x][y] == Piece.EMPTY:
                for dx, dy in [(0, 1), (1, 0), (1, 1), (0, -1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]:
                    adj_x, adj_y = x + dx, y + dy
                    if 0 <= adj_x < state.numRows and 0 <= adj_y < state.numCols:
                        if board[adj_x][adj_y] == my_color:
                            my_matrix += POINT_MATRIX[adj_x][adj_y]
                        elif board[adj_x][adj_y] == opp_color:
                            opp_matrix += POINT_MATRIX[adj_x][adj_y]

        matrix = my_matrix - opp_matrix

        # CHAIN and STRONG CHAIN
        edges = [(0, col) for col in range(state.numCols)] + \
                [(state.numRows - 1, col) for col in range(state.numCols)] + \
                [(row, 0) for row in range(1, state.numRows - 1)] + \
                [(row, state.numCols - 1)
                 for row in range(1, state.numRows - 1)]

        my_chain = 0
        opp_chain = 0
        my_strong_chain = 0
        opp_strong_chain = 0

        my_chains = []
        opp_chains = []
        chain = []
        prev = Piece.EMPTY

        for edge in edges:
            x, y = edge
            curr = state.board[x][y]
            if curr != prev:
                if prev == my_color:
                    my_chains.append(chain)
                elif prev == opp_color:
                    opp_chains.append(chain)

                chain = []

            chain.append(edge)
            prev = curr

        if prev == my_color:
            my_chains.append(chain)
        elif prev == opp_color:
            opp_chains.append(chain)

        for chain in my_chains:
            has_corner = any(corner in chain for corner in CORNERS)
            if has_corner:
                my_strong_chain += len(chain) - 1
            else:
                my_chain += len(chain) - 1

        for chain in opp_chains:
            has_corner = any(corner in chain for corner in CORNERS)
            if has_corner:
                opp_strong_chain += len(chain) - 1
            else:
                opp_chain += len(chain) - 1

        chain = my_chain - opp_chain
        strong_chain = my_strong_chain - opp_strong_chain

        board = state.board
        blank_count = 0
        for row in board:
            for piece in row:
                if piece == Piece.EMPTY:
                    blank_count += 1

        count_weight = COUNT_WEIGHT if blank_count > LATE_GAME else LATE_GAME

        score = matrix * MATRIX_WEIGHT + \
            count * count_weight + \
            chain * CHAIN_WEIGHT + \
            strong_chain * STRONG_CHAIN_WEIGHT

        return score

    def __generate_possible_moves(self, state):
        moves = []
        for i in range(state.numRows):
            for j in range(state.numCols):
                if state.isValidMove(i, j, state.nextMove):
                    moves.append((i, j))

        return moves

    def __apply_move(self, state, move):
        new_state = deepcopy(state)
        new_state.placePiece(move[0], move[1])

        return new_state
