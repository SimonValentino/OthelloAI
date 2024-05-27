from OthelloState import Piece, OthelloState
import random
import time

INF = float('inf')
DEPTH = 6

COUNT_WEIGHT = 20
CHAIN_WEIGHT = 10
STRONG_CHAIN_WEIGHT = 50
MATRIX_WEIGHT = 100

POINT_MATRIX = [
    [4, -3, 2, 2, 2, 2, -3, 4],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [2, -1, 1, 0, 0, 1, -1, 2],
    [2, -1, 0, 1, 1, 0, -1, 2],
    [2, -1, 0, 1, 1, 0, -1, 2],
    [2, -1, 1, 1, 1, 1, -1, 2],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [4, -3, 2, 2, 2, 2, -3, 4]
]

ADJACENT_CORNERS = [
    (0, 1), (1, 0), (1, 1), (0, 6), (1, 6), (1, 7),
    (6, 0), (6, 1), (7, 1), (6, 6), (6, 7), (7, 6)
]


class Agent:
    def __init__(self):
        return

    def getNextMove(self, state):
        # ALPHA BETA PRUNING
        # best_move, best_value = self.__minimax(state, DEPTH, -INF, INF, True)
        # return best_move
    
        # JUST HEURISTIC
        best = -INF
        best_move = None
        moves = self.__generate_possible_moves(state)
        for move in moves:
            new_state = self.__apply_move(state, move)
            val = self.__heuristic(new_state)
            if val > best:
                best = val
                best_move = move

        return best_move

    def __minimax(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or not state.existsNextMove():
            return None, self.__heuristic(state)

        best_move = None

        moves = self.__generate_possible_moves(state)
        if is_maximizing:
            max_eval = -INF
            for move in moves:
                new_state = self.__apply_move(state, move)
                _, eval = self.__minimax(
                    new_state, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = INF
            for move in moves:
                new_state = self.__apply_move(state, move)
                _, eval = self.__minimax(
                    new_state, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def __heuristic(self, state, verbose=False):
        my_color = state.nextMove
        opp_color = Piece.oppositePiece(my_color)
        board = state.board

        # MATRIX and COUNT
        my_matrix = 0
        opp_matrix = 0
        my_count = 0
        opp_count = 0

        for i in range(len(POINT_MATRIX)):
            for j in range(len(POINT_MATRIX[0])):
                if board[i][j] == my_color:
                    my_matrix += POINT_MATRIX[i][j]
                    my_count += 1
                elif board[i][j] == opp_color:
                    opp_matrix += POINT_MATRIX[i][j]
                    opp_count += 1

        matrix = my_matrix - opp_matrix
        count = my_count - opp_count

        # Adjusting the values of adjacent corner squares
        corners = [(0, 0), (0, state.numCols - 1), (state.numRows -
                                                    1, 0), (state.numRows - 1, state.numCols - 1)]
        for x, y in corners:
            if board[x][y] == Piece.EMPTY:
                for dx, dy in [(0, 1), (1, 0), (1, 1), (0, -1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]:
                    adj_x, adj_y = x + dx, y + dy
                    if 0 <= adj_x < state.numRows and 0 <= adj_y < state.numCols:
                        if board[adj_x][adj_y] == my_color:
                            matrix -= POINT_MATRIX[adj_x][adj_y]
                        elif board[adj_x][adj_y] == opp_color:
                            matrix += POINT_MATRIX[adj_x][adj_y]

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
            has_corner = any(corner in chain for corner in corners)
            if has_corner:
                my_strong_chain += len(chain) - 1
            else:
                my_chain += len(chain) - 1

        for chain in opp_chains:
            has_corner = any(corner in chain for corner in corners)
            if has_corner:
                opp_strong_chain += len(chain) - 1
            else:
                opp_chain += len(chain) - 1

        chain = my_chain - opp_chain
        strong_chain = my_strong_chain - opp_strong_chain

        score = matrix * MATRIX_WEIGHT + \
            count * COUNT_WEIGHT + \
            chain * CHAIN_WEIGHT + \
            strong_chain * STRONG_CHAIN_WEIGHT

        if verbose:
            print(my_color, "COUNT:", my_count)
            print(opp_color, "COUNT:", opp_count)
            print(my_color, "CHAIN:", my_chain)
            print(opp_color, "CHAIN:", opp_chain)
            print(my_color, "STRONG CHAIN:", my_strong_chain)
            print(opp_color, "STRONG CHAIN:", opp_strong_chain)
            print(my_color, "MATRIX:", my_matrix)
            print(opp_color, "MATRIX:", opp_matrix)
            print("SCORE:", score)

        return score

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
