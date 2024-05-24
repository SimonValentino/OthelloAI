from enum import Enum
import pygame


class Piece(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def oppositePiece(piece):
        if (piece == Piece.WHITE):
            return Piece.BLACK
        elif (piece == Piece.BLACK):
            return Piece.WHITE
        else:
            raise Exception("Invalid piece color to get opposite of")


class GameType(Enum):
    PVP = 1
    PVA = 2
    AVP = 3
    AVA = 4


class OthelloState:

    def __init__(self, numCols=8, numRows=8, squareWidth=50, squareBuffer=3):
        self.numCols = numCols
        self.numRows = numRows
        self.squareWidth = squareWidth
        self.squareBuffer = squareBuffer
        self.nextMove = Piece.BLACK
        self.board = [[Piece.EMPTY for i in range(
            numCols)] for i in range(numRows)]
        self.board[numRows//2][numRows//2] = Piece.BLACK
        self.board[numRows//2 - 1][numRows//2 - 1] = Piece.BLACK
        self.board[numRows//2 - 1][numRows//2] = Piece.WHITE
        self.board[numRows//2][numRows//2 - 1] = Piece.WHITE
        self.firstDraw = True

    # draws the board
    # (you almost certainly not need this method;
    # it is only public so that it can be reached by
    # methods in Othello.py)
    # parameters:
    # surface -- a pygame surface object

    def draw(self, surface):

        for i in range(self.numCols):
            for j in range(self.numRows):
                self.__drawSquare(surface, self.board[i][j], i, j)

        if (self.firstDraw):
            for i in range(self.numCols):
                pygame.draw.line(surface, (175, 175, 175),
                                 (i * self.squareWidth, 0), (i *
                                                             self.squareWidth, surface.get_height() - 1),
                                 width=self.squareBuffer)

            for i in range(self.numRows):
                pygame.draw.line(surface, (175, 175, 175),
                                 (0, i * self.squareWidth), (surface.get_width() -
                                                             1, i * self.squareWidth),
                                 width=self.squareBuffer)

            self.firstDraw = False

    def __drawSquare(self, surface, piece, col, row):

        rect = (col * self.squareWidth + self.squareBuffer,
                row * self.squareWidth + self.squareBuffer,
                self.squareWidth - (2 * self.squareBuffer),
                self.squareWidth - (2 * self.squareBuffer))

        pygame.draw.rect(surface, (36, 163, 57), rect)

        if (piece == Piece.BLACK):
            pygame.draw.ellipse(surface, (0, 0, 0), rect)

        if (piece == Piece.WHITE):
            pygame.draw.ellipse(surface, (255, 255, 255), rect)

    # places a piece on the board of the color
    # specified by self.nextMove
    # parameters:
    # x -- x coordinate of move to make
    # y -- y coordinate of move to make

    def placePiece(self, x, y):

        if (not self.isValidMove(x, y, self.nextMove)):
            raise Exception("Invalid move!")
        else:
            self.board[x][y] = self.nextMove
            self.__flipPieces(x, y)

        self.__advanceMove()

    def __isSandwich(self, piece, x, y, xInc, yInc):

        x += xInc
        y += yInc

        hasFilling = False
        hasOtherEnd = False

        while (x >= 0 and x < self.numCols and
               y >= 0 and y < self.numRows):

            if (self.board[x][y] != piece and
               self.board[x][y] != Piece.EMPTY):
                hasFilling = True

            elif (self.board[x][y] == Piece.EMPTY):
                return False

            elif (self.board[x][y] == piece):
                hasOtherEnd = True
                break

            x += xInc
            y += yInc

        return hasFilling and hasOtherEnd

    def __flipSandwich(self, piece, x, y, xInc, yInc):

        oppositePiece = Piece.oppositePiece(piece)

        x += xInc
        y += yInc

        while (x >= 0 and x < self.numCols and
               y >= 0 and y < self.numRows):

            if (self.board[x][y] != piece and
               self.board[x][y] != Piece.EMPTY):
                self.board[x][y] = piece

            else:
                break

            x += xInc
            y += yInc

    def __flipPieces(self, x, y, verbose=True):

        # horizontal left
        if (self.__isSandwich(self.nextMove, x, y, -1, 0)):
            print("1")
            self.__flipSandwich(self.nextMove, x, y, -1, 0)

        # horizontal right
        if (self.__isSandwich(self.nextMove, x, y, 1, 0)):
            print("2")
            self.__flipSandwich(self.nextMove, x, y, 1, 0)

        # vertical up
        if (self.__isSandwich(self.nextMove, x, y, 0, 1)):
            print("3")
            self.__flipSandwich(self.nextMove, x, y, 0, 1)

        # vertical down
        if (self.__isSandwich(self.nextMove, x, y, 0, -1)):
            print("4")
            self.__flipSandwich(self.nextMove, x, y, 0, -1)

        # diagonal NW
        if (self.__isSandwich(self.nextMove, x, y, -1, -1)):
            print("5")
            self.__flipSandwich(self.nextMove, x, y, -1, -1)

        # diagonal SW
        if (self.__isSandwich(self.nextMove, x, y, -1, 1)):
            print("6")
            self.__flipSandwich(self.nextMove, x, y, -1, 1)

        # diagonal NE
        if (self.__isSandwich(self.nextMove, x, y, 1, -1)):
            print("7")
            self.__flipSandwich(self.nextMove, x, y, 1, -1)

        # diagonal SE
        if (self.__isSandwich(self.nextMove, x, y, 1, 1)):
            print("7")
            self.__flipSandwich(self.nextMove, x, y, 1, 1)

    def __advanceMove(self):
        if (self.nextMove == Piece.WHITE):
            self.nextMove = Piece.BLACK
        else:
            self.nextMove = Piece.WHITE

    # determines whether a piece of color specified by self.nextMove
    # can be legally placed in any location on the board
    def existsNextMove(self):

        for i in range(self.numCols):
            for j in range(self.numRows):
                if (self.isValidMove(i, j, self.nextMove)):
                    return True

        else:
            return False

    # determines if a move of a certain color would be valid
    # in a particular location on the board
    # parameters:
    # x -- x coordinate of move to make
    # y -- y coordinate of move to make
    # piece -- color of piece to make
    # verbose -- (this was just to help debugging. Leaving it in because
    # lord knows I'll need it again.)
    def isValidMove(self, x, y, piece, verbose=False):

        if (self.board[x][y] != Piece.EMPTY):
            return False

        if (verbose):
            print("Chechink valid move:")
            print(f"\t{self.__isSandwich(self.nextMove, x, y, -1, 0)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, 1, 0)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, 0, -1)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, 0, 1)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, -1, -1)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, -1, 1)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, 1, -1)}\n" +
                  f"\t{self.__isSandwich(self.nextMove, x, y, 1, 1)}\n")

        return (self.__isSandwich(self.nextMove, x, y, -1, 0) or
                self.__isSandwich(self.nextMove, x, y, 1, 0) or
                self.__isSandwich(self.nextMove, x, y, 0, 1) or
                self.__isSandwich(self.nextMove, x, y, 0, -1) or
                self.__isSandwich(self.nextMove, x, y, -1, -1) or
                self.__isSandwich(self.nextMove, x, y, -1, 1) or
                self.__isSandwich(self.nextMove, x, y, 1, -1) or
                self.__isSandwich(self.nextMove, x, y, 1, 1))

    # counts the number of pieces of each color currently on the board.
    # returns:
    # A 2-tuple of counts in the format (blacks, whites)

    def pieceCounts(self):
        black = 0
        white = 0

        for i in range(self.numCols):
            for j in range(self.numRows):
                if (self.board[i][j] == Piece.WHITE):
                    white += 1
                elif (self.board[i][j] == Piece.BLACK):
                    black += 1

        return (black, white)
