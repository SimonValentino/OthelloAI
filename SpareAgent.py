from OthelloState import OthelloState
from OthelloState import Piece
from OthelloState import GameType
from copy import deepcopy
import time
import random
# from Othello import OthelloState


class SpareAgent:

    # this constructor should not take any parameters
    # You can change the body of the constructor
    # if you want/need to
    def __init__(self):
        return

    def gameEval(self, state):
        score = 0
        gBoard = state.board
        empty = Piece.EMPTY
        black = Piece.BLACK
        white = Piece.WHITE
        bCount = 0
        wCount = 0
        for col in gBoard:
            for slot in col:
                if (slot == black):
                    bCount += 1
                elif (slot == white):
                    wCount += 1
        if (not state.existsNextMove()):
            if bCount > wCount:
                return 9999
            elif bCount < wCount:
                return -9999
            else:
                return 0

        if (bCount + wCount > 58):
            for col in gBoard:
                for slot in col:
                    if (slot == black):
                        score += 2
                    elif (score == white):
                        score -= 2

        edge = len(gBoard)-1
        corners = [gBoard[0][0], gBoard[edge][0],
                   gBoard[0][edge], gBoard[edge][edge]]
        aroundCorners = [[gBoard[1][0], gBoard[1][1], gBoard[0][1]],
                         [gBoard[edge-1][0], gBoard[edge-1][1], gBoard[edge][1]],
                         [gBoard[0][edge-1], gBoard[1][edge-1], gBoard[1][edge]],
                         [gBoard[edge][edge-1], gBoard[edge-1][edge-1], gBoard[edge-1][edge]]]
        # 1 means corner owned by black, -1 means corner owned by white. 0 means corner is empty
        cornerData = [0, 0, 0, 0]
        for corner in corners:
            if corner == black:
                cornerData[corners.index(corner)] = 1
                score += (8-(bCount+wCount)/11)
            elif corner == white:
                cornerData[corners.index(corner)] = -1
                score -= (8-(bCount+wCount)/11)
        for neighbors in aroundCorners:
            penalize = True
            if (cornerData[aroundCorners.index(neighbors)] != 0):
                penalize = False
            for slot in neighbors:
                if slot == black and penalize == True:
                    score -= (3-(bCount+wCount)/22)
                elif slot == white and penalize == True:
                    score += (3-(bCount+wCount)/22)

        centerBox = [[gBoard[2][2], gBoard[3][2], gBoard[4][2], gBoard[5][2]],
                     [gBoard[2][3], gBoard[3][3], gBoard[4][3], gBoard[5][3]],
                     [gBoard[2][4], gBoard[3][4], gBoard[4][4], gBoard[5][4]],
                     [gBoard[2][5], gBoard[3][5], gBoard[4][5], gBoard[5][5]]]

        for row in centerBox:
            for slot in row:
                if slot == black:
                    score += 0.2
                elif slot == white:
                    score -= 0.2

        if (gBoard[0][0] != empty):
            for i in range(1, edge-1):
                if (gBoard[i][0] == empty):
                    break
                else:
                    if (gBoard[0][0] == black):
                        score += 0.8
                    else:
                        score -= 0.8
            for i in range(1, edge-1):
                if (gBoard[0][i] == empty):
                    break
                else:
                    if (gBoard[0][0] == black):
                        score += 0.8
                    else:
                        score -= 0.8

        if (gBoard[edge][0] != empty):
            for i in range(edge-1, 0, -1):
                if (gBoard[i][0] == empty):
                    break
                else:
                    if (gBoard[edge][0] == black):
                        score += 0.8
                    else:
                        score -= 0.8
            for i in range(1, edge):
                if (gBoard[edge][i] == empty):
                    break
                else:
                    if (gBoard[edge][0] == black):
                        score += 0.8
                    else:
                        score -= 0.8

        if (gBoard[0][edge] != empty):
            for i in range(edge-1, 0, -1):
                if (gBoard[i][0] == empty):
                    break
                else:
                    if (gBoard[0][edge] == black):
                        score += 0.8
                    else:
                        score -= 0.8
            for i in range(1, edge):
                if (gBoard[i][edge] == empty):
                    break
                else:
                    if (gBoard[0][edge] == black):
                        score += 0.8
                    else:
                        score -= 0.8

        if (gBoard[edge][edge] != empty):
            for i in range(edge-1, 0, -1):
                if (gBoard[i][edge] == empty):
                    break
                else:
                    if (gBoard[edge][edge] == black):
                        score += 0.8
                    else:
                        score -= 0.8
            for i in range(edge-1, 0, -1):
                if (gBoard[edge][i] == empty):
                    break
                else:
                    if (gBoard[edge][edge] == black):
                        score += 0.8
                    else:
                        score -= 0.8
        perimeter = [gBoard[1][0], gBoard[2][0], gBoard[3][0], gBoard[4][0], gBoard[5][0], gBoard[6][0],
                     gBoard[0][1], gBoard[0][2], gBoard[0][3], gBoard[0][4], gBoard[0][5], gBoard[0][6],
                     gBoard[1][7], gBoard[2][7], gBoard[3][7], gBoard[4][7], gBoard[5][7], gBoard[6][7],
                     gBoard[7][1], gBoard[7][2], gBoard[7][3], gBoard[7][4], gBoard[7][5], gBoard[7][6]]
        for slot in perimeter:
            if slot == black:
                score += 0.4
            elif slot == white:
                score -= 0.4
        return score

    def legalMoves(self, state):
        moves = []
        for i in range(8):
            for j in range(8):
                if state.isValidMove(i, j, state.nextMove):
                    moves.append((i, j))
        return moves

    def minimax(self, state, depth, maximizingPlayer):
        if depth == 0 or not state.existsNextMove():
            return self.gameEval(state), None

        possibleMoves = self.legalMoves(state)
        bestMove = None

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in possibleMoves:
                future = deepcopy(state)
                future.placePiece(move[0], move[1])
                eval, _ = self.minimax(future, depth - 1, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
            return maxEval, bestMove
        else:
            minEval = float('inf')
            for move in possibleMoves:
                future = deepcopy(state)
                future.placePiece(move[0], move[1])
                eval, _ = self.minimax(future, depth - 1, True)
                if eval < minEval:
                    minEval = eval
                    bestMove = move
            return minEval, bestMove

    # this method's header should not change
    # This is the main method you'll be implementing
    # it should return the number of the column where
    # the next move will be made.
    # This method can only take 5 seconds or less to run
    # Any more and the game will immediately end
    # and the other player will win by default
    def getNextMove(self, state):
        moves = self.legalMoves(state)
        return random.choice(moves)
        
        time.sleep(0)
        depth = 4
        # pass in the color of your opponent
        _, bestMove = self.minimax(state, depth, state.nextMove == Piece.BLACK)
        return bestMove