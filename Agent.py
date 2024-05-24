from OthelloState import Piece

NUM_ROWS = 8
NUM_COLS = 8

DISK_SCORE = 10
CHAIN_BONUS = 15
STRONG_CHAIN_BONUS = 30

POINT_MATRIX = [
    [100, -10, 10, 10, 10, 10, -10, 100],
    [-10, -25, 1, 1, 1, 1, -25, -10],
    [10, 1, 5, 5, 5, 5, 1, 10],
    [10, 1, 5, 0, 0, 5, 1, 10],
    [10, 1, 5, 0, 0, 5, 1, 10],
    [10, 1, 5, 5, 5, 5, 1, 10],
    [-10, -25, 1, 1, 1, 1, -25, -10],
    [100, -10, 10, 10, 10, 10, -10, 100],
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

    # this constructor should not take any parameters
    # You can change the body of the constructor
    # if you want/need to
    def __init__(self):
        return

    def heuristic(board, color):
        opp_color = Piece.BLACK if color == Piece.WHITE else Piece.BLACK

        score = 0

        # Point matrix and num disks
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if (i, j) not in CORNER_ADJACENCIES:
                    piece = board[i][j]

                    if piece == color:
                        score += POINT_MATRIX[i][j]
                        score += DISK_SCORE
                    elif piece == opp_color:
                        score -= POINT_MATRIX[i][j]
                        score -= DISK_SCORE

        edges = [(0, col) for col in range(NUM_COLS - 1, -1, -1)] + \
                [(row, 0) for row in range(1, NUM_ROWS)] + \
                [(NUM_ROWS - 1, col) for col in range(1, NUM_COLS)] + \
                [(row, NUM_COLS - 1) for row in range(NUM_ROWS - 2, 0, -1)]
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

    # this method's header should not change
    # This is the main method you'll be implementing
    # it should return the number of the column where
    # the next move will be made.
    # This method can only take 5 seconds or less to run
    # Any more and the game will immediately end
    # and the other player will win by default

    def getNextMove(self, gameState):
        return (0, 0)
