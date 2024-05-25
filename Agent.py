from OthelloState import Piece, OthelloState
import random
import time

INF = float('inf')
MAX_DEPTH = 10

COUNT_WEIGHT = 10
MOBILITY_WEIGHT = 30
CHAIN_BONUS = 300
STRONG_CHAIN_BONUS = 3000
POINT_MATRIX = [
    [10000, -700,  100,  60,  60,  100, -700, 10000],
    [-700, -1000,  -45, -50, -50,  -45, -1000, -700],
    [100,  -45,   3,    1,   1,    3,   -45,  100],
    [60,   -50,   1,    2,   2,    1,   -50,   60],
    [60,   -50,   1,    2,   2,    1,   -50,   60],
    [100,  -45,   3,    1,   1,    3,   -45,  100],
    [-700, -1000,  -45, -50, -50,  -45, -1000, -700],
    [10000, -700,  100,  60,  60,  100, -700, 10000]
]


class Agent:
    def __init__(self):
        return

    def getNextMove(self, state):
        score, move = self.__minimax(state, MAX_DEPTH, -INF, INF, True)
        print(score)
        return move

    def __minimax(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or not state.existsNextMove():
            return self.__heuristic(state), None

        if is_maximizing:
            val = -INF
            moves = self.__generate_possible_moves(state)

            for move in moves:
                new_state = self.__apply_move(state, move)

                temp = self.__minimax(
                    new_state, depth - 1, alpha, beta, False)[0]
                if temp > val:
                    val = temp
                    best_move = move

                if val >= beta:
                    break

                alpha = max(alpha, val)

        else:
            val = INF
            moves = self.__generate_possible_moves(state)

            for move in moves:
                new_state = self.__apply_move(state, move)

                temp = self.__minimax(
                    new_state, depth - 1, alpha, beta, True)[0]

                if temp < val:
                    val = temp
                    best_move = move

                if val <= alpha:
                    break

                beta = min(beta, val)

        return val, best_move

    def __heuristic(self, state):
        color = state.nextMove

        my_points = 0
        opp_points = 0

        my_count = 0
        opp_count = 0

        for i in range(state.numRows):
            for j in range(state.numCols):
                piece = state.board[i][j]
                if piece == color:
                    my_points += POINT_MATRIX[i][j]
                    my_count += 1
                elif piece == Piece.oppositePiece(color):
                    opp_points += POINT_MATRIX[i][j]
                    opp_count += 1

        edges = [(0, col) for col in range(state.numCols)] + \
                [(state.numRows - 1, col) for col in range(state.numCols)] + \
                [(row, 0) for row in range(1, state.numRows - 1)] + \
                [(row, state.numCols - 1)
                 for row in range(1, state.numRows - 1)]

        my_chain_score = 0
        opp_chain_score = 0

        my_chains = []
        opp_chains = []
        chain = []
        prev_piece = Piece.EMPTY

        for edge in edges:
            x, y = edge
            curr_piece = state.board[x][y]
            if curr_piece != prev_piece:
                if prev_piece == color:
                    my_chains.append(chain)
                elif prev_piece == Piece.oppositePiece(color):
                    opp_chains.append(chain)

                chain = []

            chain.append(edge)
            prev_piece = curr_piece

        if prev_piece == color:
            my_chains.append(chain)
        elif prev_piece == Piece.oppositePiece(color):
            opp_chains.append(chain)

        corners = [(0, 0),
                   (0, state.numCols - 1),
                   (state.numRows - 1, 0),
                   (state.numRows - 1,
                    state.numCols - 1)]

        for chain in my_chains:
            has_corner = any(corner in chain for corner in corners)
            if has_corner:
                my_chain_score += (len(chain) - 1) * STRONG_CHAIN_BONUS
            else:
                my_chain_score += (len(chain) - 1) * CHAIN_BONUS

        for chain in opp_chains:
            has_corner = any(corner in chain for corner in corners)
            if has_corner:
                opp_chain_score += (len(chain) - 1) * STRONG_CHAIN_BONUS
            else:
                opp_chain_score += (len(chain) - 1) * CHAIN_BONUS

        my_moves = len(self.__generate_possible_moves(state))

        point_score = my_points - opp_points
        count_score = my_count - opp_count
        chain_score = my_chain_score - opp_chain_score
        mobility_score = MOBILITY_WEIGHT * my_moves

        return count_score + mobility_score + point_score + chain_score

    def __generate_possible_moves(self, state):
        moves = []
        for i in range(state.numRows):
            for j in range(state.numCols):
                if state.isValidMove(i, j, state.nextMove):
                    moves.append((i, j))

        return moves

    def __apply_move(self, state, move):
        new_state = OthelloState()
        new_state.board = [row[:] for row in state.board]
        new_state.nextMove = state.nextMove
        new_state.placePiece(move[0], move[1])
        new_state.nextMove = Piece.oppositePiece(new_state.nextMove)

        return new_state
