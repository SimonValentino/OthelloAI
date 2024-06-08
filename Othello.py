import pygame
import time
from datetime import datetime
from sys import platform
import os
from OthelloLog import OthelloLog
from OthelloState import OthelloState
from OthelloState import Piece
from OthelloState import GameType
from Agent import Agent
from SpareAgent import SpareAgent
from copy import deepcopy


NUM_ROWS = 8
NUM_COLS = 8
SQUARE_WIDTH = 80
SQUARE_BUFFER = 3

BACKGROUND_COLOR = (36, 163, 57)

# measured in ms
MAX_MOVE_TIME = 5000


def main():
    pygame.init()

    gameType = GameType.AVA  # Set the game type to Agent vs Agent
    num_games = 100
    black_wins = 0
    white_wins = 0

    for game_number in range(num_games):
        log = OthelloLog(gameType)
        agentA = Agent()
        agentB = SpareAgent()

        screen = pygame.display.set_mode((SQUARE_WIDTH * NUM_COLS,
                                          SQUARE_WIDTH * NUM_ROWS))

        state = OthelloState(numCols=NUM_COLS, numRows=NUM_ROWS,
                             squareWidth=SQUARE_WIDTH, squareBuffer=SQUARE_BUFFER)
        state.draw(screen)
        pygame.display.update()

        running = True
        gameOver = False
        curPlayer = agentA
        while running:
            while not gameOver:
                if isinstance(curPlayer, (Agent, SpareAgent)):
                    stateCopy = deepcopy(state)
                    startTime = round(time.time() * 1000)
                    move = curPlayer.getNextMove(stateCopy)
                    endTime = round(time.time() * 1000)

                    if endTime - startTime > MAX_MOVE_TIME:
                        if state.nextMove == Piece.RED:
                            log.winner = Piece.YELLOW
                            white_wins += 1
                        else:
                            log.winner = Piece.RED
                            black_wins += 1

                        log.endCondition = "Timeout"
                        running = False
                        gameOver = True

                    else:
                        try:
                            log.addMove(move)
                            state.placePiece(move[0], move[1])

                        except:
                            log.endCondition = "Placement Error"
                            running = False
                            gameOver = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                state.draw(screen)
                pygame.display.update()

                if curPlayer == agentA:
                    curPlayer = agentB
                else:
                    curPlayer = agentA

                if not state.existsNextMove():
                    gameOver = True
                    scores = state.pieceCounts()
                    log.black = scores[0]
                    log.white = scores[1]
                    log.endCondition = "Game finish"
                    if scores[0] > scores[1]:
                        log.winner = "Black"
                        black_wins += 1
                    elif scores[1] > scores[0]:
                        log.winner = "White"
                        white_wins += 1
                    else:
                        log.winner = "Tie"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        writeLogToOS(log, game_number)
        pygame.quit()  # Close the game window after each game
        pygame.init()  # Reinitialize pygame for the next game

    print(f"Black wins: {black_wins}")
    print(f"White wins: {white_wins}")


def writeLogToOS(log, game_number):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":", "-")

    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file_path = f"logs/{game_number}_{time_str}.log" if platform != "win32" else f"logs\\{game_number}_{time_str}.log"
    with open(log_file_path, "w") as logFile:
        logFile.write(str(log))


if __name__ == "__main__":
    main()
