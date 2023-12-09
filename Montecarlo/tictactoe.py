import numpy as np
from TTTPlayer import TTTPlayer
from typing import Final

class TicTacToe:

    xSize: Final[int] = 3
    ySize: Final[int] = 3

    # The board is represented as a 3x3 matrix of ints
    # empty represents an unplayed square
    # 1 or 2 represents playerO and playerX respectively
    # all other values are invalid


    # constructs a TicTacToe game from the given players
    # CHRIS: added a Visual parameter
    def __init__(self, player1, player2, displayTurn):
        self.turnNum = 0
        self.board = np.full((3,3), " ")
        self.playerO = player1
        self.playerX = player2
        self.displayTurn = displayTurn
        # self.visual = visual

    # Returns the string representation of the board
    def __repr__(self) -> str:
        if self.displayTurn:
            return f"Turn: {self.turnNum}\n{self.board.__str__()}\n"
        else:
            return f"{self.board.__str__()}\n"

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
    def getWinner(self) -> TTTPlayer:
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
    def playerTakeTurn(self, player, playerSymbol, node=None, board=None, monte_carlo_on=False):
        possibleMoves = self.getPossibleMoves()
        turn = player.takeTurn(possibleMoves, node, board, monte_carlo_on)
        if turn in possibleMoves:
            self.board[turn] = playerSymbol
            # self.visual.add_to_order(turn, playerSymbol)
            #self.visual.add_to_order(turn, playerSymbol)
        self.turnNum += 1
        print("This is the tictactoe class: " + str(self.board))
        print(self)

        return turn


    # Run a game to completion
    # Prints the board state after each placement
    # Announces the winner at the end
    def playGame(self, monte_carlo_on=False):
        # monte_carlo_on indicates if we are still running the monte carlo or it is real game
        winner = 0
        print(self.board)

        turn_O = None

        while True:
            #turn_O = self.playerTakeTurn(self.playerO, "O")
            turn_X = self.playerTakeTurn(self.playerX, "X", turn_O, self, monte_carlo_on)
            winner = self.getWinner()
            if winner != 0:
                break
            if " " not in self.board and winner == 0:
                print("It's a draw!")
                break
            #turn_X = self.playerTakeTurn(self.playerX, "X", turn_O, self, monte_carlo_on)
            turn_O = self.playerTakeTurn(self.playerO, "O")
            winner = self.getWinner()
            if winner != 0:
                break
            if " " not in self.board and winner == 0:
                print("It's a draw!")
                break
        if winner != 0:
            print(f"'{winner.getName()}' has won!")

    # ADDED BY CHRIS FOR ULTIMATE VERSION
    # Prompts a player to take a turn
    # Checks if the turn is valid
    # If the turn is valid, it will enact the requested placement on the board
    def ultTakeTurn(self, player, playerSymbol, turn):
        self.board[turn] = playerSymbol

    #ADDED BY CHRIS FOR ULTIMATE VERSION
    def checkDraw(self):
        if " " not in self.board:
            return True
        else:
            return False
        
