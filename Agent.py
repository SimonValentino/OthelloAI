from OthelloState import Piece, OthelloState

INF = float('inf')
MAX_DEPTH = 5

DISK_SCORE = 10
CHAIN_BONUS = 15
STRONG_CHAIN_BONUS = 100

POINT_MATRIX = [
    [500, -10, 10, 10, 10, 10, -10, 500],
    [-10, -25, 1, 1, 1, 1, -25, -10],
    [10, 1, 5, 5, 5, 5, 1, 10],
    [10, 1, 5, 0, 0, 5, 1, 10],
    [10, 1, 5, 0, 0, 5, 1, 10],
    [10, 1, 5, 5, 5, 5, 1, 10],
    [-10, -25, 1, 1, 1, 1, -25, -10],
    [500, -10, 10, 10, 10, 10, -10, 500],
]

CORNERS = [
    (0, 0), (0, 7), (7, 0), (7, 7)
]

CORNER_ADJACENCIES = [
    [(0, 1), (1, 0)],
    [(0, 6), (1, 7)],
    [(6, 0), (7, 1)],
    [(6, 7), (7, 6)]
]


class Agent:
    def __init__(self):
        return

    def heuristic(self, state):
        board = state.board
        color = state.nextMove
        opp_color = Piece.oppositePiece(color)

        score = 0

        for i in range(state.numRows):
            for j in range(state.numCols):
                if (i, j) not in CORNER_ADJACENCIES:
                    piece = board[i][j]

                    if piece == color:
                        score += POINT_MATRIX[i][j]
                        score += DISK_SCORE
                    elif piece == opp_color:
                        score -= POINT_MATRIX[i][j]
                        score -= DISK_SCORE

        edges = [(0, col) for col in range(state.numCols - 1, -1, -1)] + \
                [(row, 0) for row in range(1, state.numRows)] + \
                [(state.numRows - 1, col) for col in range(1, state.numCols)] + \
                [(row, state.numCols - 1)
                 for row in range(state.numRows - 2, 0, -1)]
        color_chains = []
        opp_color_chains = []
        chain = []
        prev_color = Piece.EMPTY
        for edge in edges:
            x, y = edge
            curr_color = board[x][y]
            if curr_color != prev_color:
                if curr_color == color:
                    opp_color_chains.append(chain)
                elif curr_color == opp_color:
                    color_chains.append(chain)
                chain.clear()

            chain.append(edge)
            prev_color = curr_color

        for chain in color_chains:
            has_corner = False
            for corner in CORNERS:
                if corner in chain:
                    has_corner = True

            if has_corner:
                score += len(chain) - 1 * STRONG_CHAIN_BONUS
            else:
                score += len(chain) - 1 * CHAIN_BONUS

        return score

    def getNextMove(self, state):
        best_score = -INF
        best_move = None

        for move in self.generate_possible_moves(state):
            new_state = self.apply_move(state, move)
            score = self.minimax(new_state, MAX_DEPTH - 1, False)
            if score > best_score:
                best_score = score
                best_move = move

        print(f"Best Score: {best_score}")
        print(f"Best Move: {best_move}")

        return best_move

    def minimax(self, state, depth, is_maximizing):
        if depth == 0 or not state.existsNextMove():
            return self.heuristic(state)

        if is_maximizing:
            max_eval = -INF
            for move in self.generate_possible_moves(state):
                new_state = self.apply_move(state, move)
                eval = self.minimax(new_state, depth - 1, False)
                max_eval = max(max_eval, eval)

            return max_eval
        else:
            min_eval = INF
            for move in self.generate_possible_moves(state):
                new_state = self.apply_move(state, move)
                eval = self.minimax(new_state, depth - 1, True)
                min_eval = min(min_eval, eval)

            return min_eval

    def generate_possible_moves(self, state):
        moves = []
        for i in range(state.numRows):
            for j in range(state.numCols):
                if state.isValidMove(i, j, state.nextMove):
                    moves.append((i, j))

        return moves

    def apply_move(self, state, move):
        new_state = OthelloState()
        new_state.board = [row[:] for row in state.board]
        new_state.nextMove = state.nextMove
        new_state.placePiece(move[0], move[1])
        new_state._OthelloState__advanceMove()

        return new_state
