import numpy as np
from ultTTTplayer import ultTTTplayer
from tictactoe import TicTacToe
from typing import Final
from copy import deepcopy

class ultTTT:

    xSize: Final[int] = 3
    ySize: Final[int] = 3

    # The board is represented as a 3x3 matrix of tictactoe boards
    # 1 or 2 represents playerO and playerX respectively
    def __init__(self, player1, player2):
        self.turnNum = 0
        self.playerO = player1
        self.playerX = player2
        # self.visual = visual
        self.board = [[TicTacToe(self.playerO, self.playerX, False) for j in range(3)] for i in range(3)]
        self.boardRep = np.full((3,3), " ")
        self.previousMove = [-1, -1]
        self.previousTurn = []
        #some small boards will be won before the full game is over
        self.forbiddenBoards = []
        self.board_record = []
        self.result_board = None

    # Returns the string representation of the board
    def __repr__(self) -> str:
        return f"Turn: {self.turnNum}\n{self.board.__str__()}\n"

    # Returns a list of tuples representing the possible moves to play
    # i.e. the list of unplayed squares on the grid 
    # based on the direction chosen by the previous player
    def getPossibleMoves(self):
        possibleMoves = []

        #If the this is not the first move or the board correspondant to the previous play
        #is already done being played, make the possible moves all possible moves 
        if self.previousMove[0] == -1 or [self.previousMove[0], self.previousMove[1]] in self.forbiddenBoards:
            for i in range(self.ySize):
                for j in range(self.xSize):
                    if [i, j] not in self.forbiddenBoards:
                        possibleMoves.append((i,j, self.board[i][j].getPossibleMoves()))
        #After the first turn, the next player must take
        #a turn on the board correspondant to the position
        #of the turn taken by the last player's move
        else:
            possibleMoves = [self.previousMove[0], self.previousMove[1], self.board[self.previousMove[0]][self.previousMove[1]].getPossibleMoves()]
        
        # print("These are the possible moves " + str(possibleMoves))
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
    def checkUltWin(self):
        for newBoard in [self.boardRep, np.transpose(self.boardRep)]:
            result = self.checkRows(newBoard)
            if result:
                return result
        return self.checkDiagonals(self.boardRep)

    # Returns the winning Player object
    # If nobody has won yet, returns 0
    def getUltWinner(self) -> ultTTTplayer:
        result = self.checkUltWin()
        if result == " " or result == 0 or result == "D":
            return 0
        elif result == "X":
            return self.playerX
        elif result == "O":
            return self.playerO
        else:
            print(self, flush=True)
            raise ValueError(f"Invalid value in grid: {result}")

    #Evaluate if a game on a smaller board has just been won,
    #If so, count this as a mark on the larger board
    def getSmallBoardWinner(self):
        result = self.board[self.previousTurn[0]][self.previousTurn[1]].getWinner()
        # print("this is the result " + str(result))
        # print("This is the previous move: " + str(self.previousMove))
        # print("This is the previous turn: " + str(self.previousTurn[0]) + " and " + str(self.previousTurn[1]))
        # print("this is the analyzed board: \n" + str(self.board[self.previousTurn[0]][self.previousTurn[1]]))
        #if the result is not 0, then there has been a small board win
        #Update this on the board representation
        if result != 0:
            print("win recorded")
            self.boardRep[self.previousTurn[0]][self.previousTurn[1]] = result.getLetter()
            self.forbiddenBoards.append([self.previousTurn[0], self.previousTurn[1]])
            print(self.boardRep)
        elif result == 0 and self.board[self.previousTurn[0]][self.previousTurn[1]].checkDraw():
            print("draw recorded")
            self.boardRep[self.previousTurn[0]][self.previousTurn[1]] = "D"
            self.forbiddenBoards.append([self.previousTurn[0], self.previousTurn[1]])
            print(self.boardRep)


    # Prompts a player to take a turn
    # Checks if the turn is valid
    # If the turn is valid, it will enact the requested placement on the board
    def playerTakeTurn(self, player, playerSymbol, node=None, board=None, monte_carlo_on=False):
        possibleMoves = self.getPossibleMoves()
        turn = player.takeTurn(possibleMoves, node, board, monte_carlo_on)
        self.board[turn[0]][turn[1]].ultTakeTurn(player, playerSymbol, turn[2])
        self.turnNum += 1
        # print("This is the turn: " + str(turn))
        self.previousMove = turn[2]
        self.previousTurn = turn
        #print(f"previous move: {turn[2]}")
        #print(f'Previoys turn', turn)
        if not monte_carlo_on:
            print(self)
            print(self.boardRep)

        return turn 

    # Run a game to completion
    # Prints the board state after each placement
    # Announces the winner at the end
    def playGame(self, monte_carlo_on=False):
        winner = 0
        turn_O = None

        while True:
            # you can switch turn_O and turn_X to make monte carlo first or second
            # just comment the one there and uncomment the other one

            #turn_O = self.playerTakeTurn(self.playerO, "O", monte_carlo_on=monte_carlo_on)
            turn_X = self.playerTakeTurn(self.playerX, "X", turn_O, self, monte_carlo_on)
            if not monte_carlo_on:
                self.board_record.append(self.prepocess())
  
            #track if there has been a win on one of the subboards
            self.getSmallBoardWinner()
            winner = self.getUltWinner()
            if winner != 0:
                break
            if " " not in self.boardRep and winner == 0:
                print("It's a draw!")
                break
            #turn_X = self.playerTakeTurn(self.playerX, "X", turn_O, self, monte_carlo_on)
            turn_O = self.playerTakeTurn(self.playerO, "O", turn_X, self, monte_carlo_on)
            if not monte_carlo_on:
                self.board_record.append(self.prepocess())
            #track if there has been a win on one of the subboards
            self.getSmallBoardWinner()
            winner = self.getUltWinner()
            if winner != 0:
                break
            if " " not in self.boardRep and winner == 0:
                print("It's a draw!")
                break

        self.result_board = self.boardRep

        if winner != 0:
            print(f"'{winner.getName()}' has won!")

    def prepocess(self):
        output = deepcopy(self.board)

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                output[i][j] = deepcopy(output[i][j]).board
                if output[i][j].shape != (3,3):
                    print("error")

        return output