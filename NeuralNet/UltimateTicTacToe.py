import numpy as np
from TTTPlayer import RandomPlayer
from typing import Final
import copy
import multiprocessing as mp
import tqdm

moveMap = []
for k in range(9):
    for i in range(3):
        for j in range(3):
            moveMap.append((k,i,j))

def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0

def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

def checkWin(board):
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)

def getPossibleMoves(board, subGridID):
    possibleMoves = []
    if subGridID is None:
        for k in range(9):
            for i in range(3):
                for j in range(3):
                    possibleMoves.append((k, i, j))
        return possibleMoves
    else:
        for i in range(3):
            for j in range(3):
                if board[subGridID,i,j] == 0:
                    possibleMoves.append((subGridID,i,j))
        if len(possibleMoves) > 0:
            return possibleMoves
        else:
            return getPossibleMoves(board, None)

def converGridToText(board):
    out = np.full((9,3,3), "~")
    for k in range(9):
        for i in range(3):
            for j in range(3):
                if board[k,i,j] == 0:
                    out[k,i,j] = " "
                elif board[k,i,j] < 0:
                    out[k,i,j] = "X"
                elif board[k,i,j] > 0:
                    out[k,i,j] = "O"
                else:
                    raise RuntimeError("Invalid symbol")
    return out

def prettyPrintBoard(board):
    tempBoard = converGridToText(board)
    row1 = np.hstack((tempBoard[0,:,:],tempBoard[1,:,:],tempBoard[2,:,:]))
    row2 = np.hstack((tempBoard[3,:,:],tempBoard[4,:,:],tempBoard[5,:,:]))
    row3 = np.hstack((tempBoard[6,:,:],tempBoard[7,:,:],tempBoard[8,:,:]))
    out = np.vstack((row1, row2, row3))
    print(out.__repr__())

def simulateMove(board, move, iterations, nextSubGrid):
    player = 1 if np.count_nonzero(board) % 2 == 0 else -1
    wins = 0
    draws = 0
    board[move] = player
    for _ in range(iterations):
        game = TicTacToe(RandomPlayer("Player1"), RandomPlayer("Player2"), copy.deepcopy(board), nextSubGrid)
        winner = game.playGame()
        if len(winner) == 2:
            draws += 1
        elif winner[0].getName() == "Player1":
            wins += 1
    losses = iterations - (wins + draws)
    return wins / iterations, draws / iterations, losses / iterations

def evaluateMove(args):
    board = args[0]
    move = args[1]
    possibleMoves = args[2]
    iterations = args[3]
    if move not in possibleMoves:
        return 0
    else:
        nextSubGrid = move[1] * 3 + move[2]
        w, d, l = simulateMove(board, move, iterations, nextSubGrid)
        #print(f"{w} : {d} : {l}")
        return w

def findBestMove(board, nextSubGrid, iterations):
    possibleMoves = getPossibleMoves(board, nextSubGrid)
    args = []
    for move in moveMap:
        args.append([board, move, possibleMoves, iterations])
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(evaluateMove, args)
    return moveMap[np.argmax(result)]

def generateBoards(num):
    boards = []
    while len(boards) < num:
        game = TicTacToe(RandomPlayer(""), RandomPlayer(""))
        game.playGame()
        states = game.getMoveHistory()
        boards += states
    if len(boards) == num:
        return boards
    else:
        return boards[:num - 1]

class TicTacToe:
    def __init__(self, player1, player2, board=None, nextSubGrid=None):

        if board is None:
            self.board = np.zeros(shape=(9,3,3), dtype=np.int8)
        else:
            self.board = board
        
        self.stateHistory = []

        self.playerO = player1
        self.playerX = player2

        self.turnNum = np.count_nonzero(self.board)
        self.nextSubGrid = nextSubGrid

    def __repr__(self):
        tempBoard = converGridToText(self.board)
        row1 = np.hstack((tempBoard[0,:,:],tempBoard[1,:,:],tempBoard[2,:,:]))
        row2 = np.hstack((tempBoard[3,:,:],tempBoard[4,:,:],tempBoard[5,:,:]))
        row3 = np.hstack((tempBoard[6,:,:],tempBoard[7,:,:],tempBoard[8,:,:]))
        out = np.vstack((row1, row2, row3))
        return out.__repr__()
    
    def getTotalGrid(self):
        totalGrid = np.zeros(shape=(3,3), dtype=np.int8)
        for i in range(9):
            subGrid = self.board[i,:,:]
            y = int(i / 3)
            x = (i - 3*y)
            totalGrid[y,x] = checkWin(subGrid)
        return totalGrid

    def checkTotalWin(self):
        totalGrid = self.getTotalGrid()
        winner = checkWin(totalGrid)
        return winner
    
    def checkTotalDraw(self):
        return 0.0 not in self.board

    def getMoveHistory(self):
        return self.stateHistory

    def playGame(self):
        while self.checkTotalWin() == 0 and not self.checkTotalDraw():
            self.stateHistory.append((copy.deepcopy(self.board), copy.deepcopy(self.nextSubGrid)))
            if self.turnNum % 2 == 0:
                player = self.playerO
                otherPlayer = self.playerX
                playerNum = np.int8(1)
            else:
                player = self.playerX
                otherPlayer = self.playerO
                playerNum = np.int8(-1)
            
            possibleMoves = getPossibleMoves(self.board, self.nextSubGrid)
            move = player.takeTurn(copy.deepcopy(self.board) * playerNum, possibleMoves, self.nextSubGrid)

            if move not in possibleMoves:
                print("Wrong move buddy B)")
                return [otherPlayer] # invalid move, you lose
            else:
                self.board[move] = playerNum

            self.nextSubGrid = move[1] * 3 + move[2]
            assert(self.nextSubGrid > -1 and self.nextSubGrid < 9)

            self.turnNum += 1
        if self.checkTotalWin() != 0:
            winner = self.checkTotalWin()
            winningPlayer = [self.playerO] if winner == 1 else [self.playerX]
            return winningPlayer
        else:
            return [self.playerO, self.playerX]
            
def rotateSubGrid(subGrid):
    assert(subGrid.shape == (3,3))
    rotated_grid = np.transpose(subGrid)[::-1, :]
    return rotated_grid

def rotations(board, subgrid, move):
    output = np.zeros(shape=(9,3,3))
    output[0] = rotateSubGrid(board[2])
    output[1] = rotateSubGrid(board[5])
    output[2] = rotateSubGrid(board[8])
    output[3] = rotateSubGrid(board[1])
    output[4] = rotateSubGrid(board[4])
    output[5] = rotateSubGrid(board[7])
    output[6] = rotateSubGrid(board[0])
    output[7] = rotateSubGrid(board[3])
    output[8] = rotateSubGrid(board[6])
    return output



if __name__ == "__main__":
    print(f"CPU Cores Detected: {mp.cpu_count()}")
    boards = generateBoards(1000)
    rotations(boards[9][0], 0, 0)
"""     bestMoves = []
    data = []
    subgrids = []
    counter = 0
    for board, subGrid in tqdm.tqdm(boards):
        if counter % 5 == 0 and counter > 0:
            boardData = np.stack(data)
            moveData = np.asarray(bestMoves)
            subGridData = np.asarray(subgrids)
            np.save("boards", boardData)
            np.save("moves", moveData)
            np.save("subgrids", subgrids)
        move = findBestMove(board, subGrid, 1000)
        data.append(board)
        bestMoves.append(move)
        subgrids.append(subGrid)
        counter += 1
    boardData = np.stack(data)
    moveData = np.asarray(bestMoves)
    subGridData = np.asarray(subgrids)
    np.save("boards", boardData)
    np.save("moves", moveData)
    np.save("subgrids", subgrids) """
    