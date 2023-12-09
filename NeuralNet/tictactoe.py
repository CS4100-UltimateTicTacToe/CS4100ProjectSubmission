import numpy as np
from TTTPlayer import RandomPlayer
from typing import Final
import copy

class TicTacToe:

    xSize: Final[int] = 3
    ySize: Final[int] = 3

    # The board is represented as a 3x3 matrix of ints
    # empty represents an unplayed square
    # 1 or 2 represents playerO and playerX respectively
    # all other values are invalid


    # constructs a TicTacToe game from the given players
    def __init__(self, player1=RandomPlayer("Player 1"), player2=RandomPlayer("Player 2")):
        self.debug = False
        self.states = []
        self.turnNum = 0
        self.board = np.full((3,3), " ")
        self.playerO = player1
        self.playerX = player2

    def simRandom(self, board):
        self.turnNum = np.count_nonzero(board != " ")
        self.board = board
        self.states = []
        self.playerO = RandomPlayer("O")
        self.playerX = RandomPlayer("X")
        if " " not in self.board:
            if self.checkWin() == 0:
                return [self.playerO, self.playerX]
            else:
                return [self.getWinner()]
        else:
            return self.playGame()
    
    def getStates(self):
        return self.states

    def setDebug(self, flag):
        self.debug = flag
        return self

    # Returns the string representation of the board
    def __repr__(self) -> str:
        return f"Turn: {self.turnNum}\n{self.board.__str__()}\n"

    # Returns a list of tuples representing the possible moves to play
    # i.e. the list of unplayed squares on the grid for basic tictactoe
    def getPossibleMoves(self):
        possibleMoves = []
        for i in range(self.ySize):
            for j in range(self.xSize):
                if self.board[i,j] == " ":
                    possibleMoves.append((i,j))
        return possibleMoves

    # Checks the rows to see if anybody has completed a line
    def checkRows(self, board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return 0

    # Checks the diagonals to see if anybody has completed a line 
    def checkDiagonals(self, board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
            return board[0][len(board)-1]
        return 0

    # checks if somebody has won yet
    # if they have, returns their symbol (e.g. "X" or "O")
    # otherwise, returns 0
    def checkWin(self):
        for newBoard in [self.board, np.transpose(self.board)]:
            result = self.checkRows(newBoard)
            if result:
                return result
        return self.checkDiagonals(self.board)
    
    # Returns the winning Player object
    # If nobody has won yet, returns 0
    def getWinner(self) -> RandomPlayer:
        result = self.checkWin()
        if result == " " or result == 0:
            return 0
        elif result == "X":
            return self.playerX
        elif result == "O":
            return self.playerO
        else:
            print(self, flush=True)
            raise ValueError(f"Invalid value in grid: {result}")
        
    # Prompts a player to take a turn
    # Checks if the turn is valid
    # If the turn is valid, it will enact the requested placement on the board
    def playerTakeTurn(self, player, playerSymbol):
        possibleMoves = self.getPossibleMoves()
        turn = player.takeTurn(self.board, possibleMoves)
        self.turnNum += 1
        if turn in possibleMoves:
            self.board[turn] = playerSymbol
            if self.debug:
                print(self)
            return True
        else:
            if self.debug:
                print(self)
            return False
        


    # Run a game to completion
    # Prints the board state after each placement
    # Announces the winner at the end
    def playGame(self):
        winner = 0
        if self.debug:
            print(self)
        while(True):
            player = self.playerO if self.turnNum % 2 == 0 else self.playerX
            otherPlayer = self.playerO if self.turnNum % 2 != 0 else self.playerX
            playerSymb = "O" if self.turnNum % 2 == 0 else "X"
            res = self.playerTakeTurn(player, playerSymb)
            if not res:
                winner = otherPlayer
                break
            winner = self.getWinner()
            if winner != 0:
                break
            if " " not in self.board and winner == 0:
                if self.debug:
                    print("It's a draw!")
                break
            self.states.append(copy.deepcopy(self.board))

        if winner != 0:
            if self.debug:
                print(f"'{winner.getName()}' has won!")
            return [winner]
        else:
            return [self.playerO, self.playerX]