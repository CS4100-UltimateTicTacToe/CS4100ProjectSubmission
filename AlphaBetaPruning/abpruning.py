from copy import deepcopy
from node import Node
import numpy as np

def ab_step(node, letter, possibleMoves, subGrid, depth):
    isO = False
    #We must expand all of our option first
    if letter == "O":
        isO = True
        expand(node, isO, possibleMoves, subGrid)
    else:
        expand(node, isO, possibleMoves, subGrid)

    #Then, we must simulate to see what move has the best heuristic
    ## TO DIRECTLY APPLY HEURISTICS -- COMMENT OUT LINE 16
    list, best_heuristic = abpruning(node, depth, float('-inf'), float('inf'), isO, depth, [])
    best_child = 0
    heuristics = []
    children = []
    for child in node.children:
        heuristics.append(child[0].heuristic)
        children.append(child[0])
    ## TO DIRECTLY APPLY HEURISTICS -- UNCOMMENT LINES 24-27
    # if isO == True:
    #     best_child = children[np.argmax(heuristics)]
    # if isO == False:
    #     best_child = children[np.argmin(heuristics)]


    #Return the move taken to get to the child with the best heuristic
    for child in list:
        if child[1] == best_heuristic:
            best_child = child[0]
    return best_child.move_by_parent

# PSEUDOCODE SOURCE: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#See_also
def abpruning(node, depth, alpha, beta, maximizingPlayer, original_depth, keep_children):
    if depth == 0: 
        return node.heuristic
   
    if maximizingPlayer:
        # the heuristic value starts off as negative infinity
        value = float('-inf')
        #iteratively traverse tree, and return the maximum score
        for child in node.children:
            child_subGrid = get_sub_grid(child[0].board, child[0].move_by_parent)
            child_moves = getPossibleMoves(child[0].board, child_subGrid)
            expand(child[0], True, child_moves, child_subGrid)
            value = max(value, (abpruning(child[0], depth - 1, alpha, beta, False, original_depth, keep_children)))
            #if maximum score is less than beta, this child is usless for computation
            if value > beta:
                break
            alpha = max(value, alpha)
        if depth == original_depth - 1:
            keep_children.append((node, value))
        # node.heuristic = value
        if depth == original_depth:
            return keep_children, value
        return value
    else:
        # the heuristic value starts off as negative infinity
        value = float('inf')

        #iteratively traverse tree, and return the maximum score
        for child in node.children:
            child_subGrid = get_sub_grid(child[0].board, child[0].move_by_parent)
            child_moves = getPossibleMoves(child[0].board, child_subGrid)
            expand(child[0], False, child_moves, child_subGrid)
            #if maximum score is less than beta, this child is usless for computation
            value = min(value, (abpruning(child[0], depth - 1, alpha, beta, True, original_depth, keep_children)))
            if value < alpha:
                break
            beta = min(value, alpha)
        if depth == original_depth - 1:
            keep_children.append((node, value))
        # node.heuristic = value
        if depth == original_depth:
            return keep_children, value
        return value
##END OF INFLUENCE FROM SOURCE CITED ABOVE

def expand(node, maximizingPlayer, possibleMoves, subGrid):
    #add these nodes as the children of the current node
    create_children(node, possibleMoves, maximizingPlayer, deepcopy(node.board), subGrid)

#Create this node's children
def create_children(node, possibleMoves, maximizingPlayer, board, subGrid):
    # iterate through the entirety of possibleMoves to make
    # getting the current node's children possible
    for i in range(len(possibleMoves)):
        move = possibleMoves[i]
        if maximizingPlayer:
            child_board = deepcopy(board) #we need a deep copy so that we do not change the original board
            child_board[move] = 1
            heuristic = get_heuristic(node, move, maximizingPlayer, board, subGrid)
            child = Node(board, heuristic, subGrid, [], move) ##FINISH IMPLEMENTING HEURISTIC
            node.children.append((child, child.heuristic))
        else:
            child_board = deepcopy(board) #we need a deep copy so that we do not change the original board
            child_board[move] = -1
            heuristic = get_heuristic(node, move, maximizingPlayer, board, subGrid)
            child = Node(board, heuristic, subGrid, [], move) ##FINISH IMPLEMENTING HEURISTIC
            node.children.append((child, child.heuristic))

# iterate through the entirety of possibleMoves to make
def get_heuristic(node, move, maximizingPlayer, board, subGrid):
    if maximizingPlayer:
        heuristic = get_heuristic_helper(node, move, maximizingPlayer, board, subGrid, 1)
    else:
        heuristic = get_heuristic_helper(node, move, maximizingPlayer, board, subGrid, -1)
    return heuristic

#SOME FUNCITIONS ARE COPIED FROM ULTIMATETICTACTOE -- EXCEPT THEY RETURN HEURISTICS
def checkRows(board, points, get_pts):
    for row in board:
        if len(set(row)) == 1:
            if get_pts:
                return points
            else:
                return row[0]
    return 0

def checkDiagonals(board, points, get_pts):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        if get_pts:
            return points
        else:
            return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        if get_pts:
            return points
        else:
            return board[0][len(board)-1]
    return 0

def checkWin(board, points, get_pts):
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard, points, get_pts)
        if result:
            return result
    return checkDiagonals(board, points, get_pts)

def getTotalGrid(board):
    totalGrid = np.zeros(shape=(3,3), dtype=np.int8)
    for i in range(9):
        subGrid = board[i,:,:]
        y = int(i / 3)
        x = (i - 3*y)
        totalGrid[y,x] = checkWin(subGrid, 0, False)
    return totalGrid

#this method checks if the move leads to a two in a row/diagonal
#with a potential of winning
def checkTwo(board, points, sign):
    for newBoard in [board, np.transpose(board)]:
        result = checkTwoInRow(newBoard, points, sign)
        if result:
            return result
    return checkTwoInDiagonal(board, points, sign)

#check if the move leads to a two in a row
def checkTwoInRow(board, points, sign):
    p_num = sign * 1
    op_num = sign * -1
    good_attempts = [[p_num, p_num, 0], [p_num, 0, p_num], [0, p_num, p_num]]
    better_attempts = [[p_num, op_num, op_num], [op_num, p_num, op_num], [op_num, op_num, p_num]]
    bad_attempts = [[p_num, p_num, op_num], [p_num, op_num, p_num], [op_num, p_num, p_num]]
    worse_attempts = [[op_num, op_num, 0], [op_num, 0, op_num], [0, op_num, op_num]]
    for row in board:
        if list(row) in good_attempts:
            return points
        if list(row) in better_attempts:
            return 2 * points
        if list(row) in bad_attempts:
            return -1 * points
        if list(row) in worse_attempts:
            return -2 * points
    return 0

def checkTwoInDiagonal(board, points, sign):
    p_num = sign * 1
    op_num = sign * -1
    good_attempts = [[p_num, p_num, 0], [p_num, 0, p_num], [0, p_num, p_num]]
    better_attempts = [[p_num, op_num, op_num], [op_num, p_num, op_num], [op_num, op_num, p_num]]
    bad_attempts = [[p_num, p_num, op_num], [p_num, op_num, p_num], [op_num, p_num, p_num]]
    worse_attempts = [[op_num, op_num, 0], [op_num, 0, op_num], [0, op_num, op_num]]

    if list([board[i][i] for i in range(len(board))]) in good_attempts:
        return points
    elif list([board[i][i] for i in range(len(board))]) in better_attempts:
        return 2 * points
    elif list([board[i][i] for i in range(len(board))]) in bad_attempts:
        return -1 * points
    elif list([board[i][i] for i in range(len(board))]) in worse_attempts:
        return -2 * points
    if list([board[i][len(board)-i-1] for i in range(len(board))]) in good_attempts:
        return points
    elif list([board[i][len(board)-i-1] for i in range(len(board))]) in better_attempts:
        return 2 * points
    elif list([board[i][len(board)-i-1] for i in range(len(board))]) in bad_attempts:
        return -1 * points
    elif list([board[i][len(board)-i-1] for i in range(len(board))]) in worse_attempts:
        return -2 * points
    return 0

def checkDraw(board):
    return 0.0 not in board

def one_move_left(board):
    count_of_zero =  0
    for i in range(len(board)):
        for k in range(len(board)):
            if board[i][k] == 0:
                count_of_zero += 1
    return count_of_zero

def get_next_subgrid(move):
    """
    Given a move (represented as a tuple (grid, row, column)),
    determine the next subgrid where the opponent must play.
    """
    _, row, col = move
    return row % 3 * 3 + col % 3

def get_heuristic_helper(node, move, maximizingPlayer, board, subGrid, sign):
    heuristic = 0
    test_board = deepcopy(board) #we need a deep copy so that we do not change the original board
    test_board[move] = sign * 1

    #Evaluate if a small grid is won
    totalGrid = np.zeros(shape=(3,3), dtype=np.int8)
    for i in range(9):
        if i != subGrid:
            continue
        sub_board = test_board[i,:,:]
        heuristic += checkWin(sub_board, sign * 100, True)

        #middle spots are more valuable
        if move[1] == sign * 1 and move[2] == sign * 1:
            heuristic += sign * 5

        #Two in a row for small boards are valuable
        heuristic += checkTwo(sub_board, sign * 50, sign * 1)

    #Evaluate if the entire game is won
    total_board = getTotalGrid(test_board)
    val = checkWin(total_board, sign * 1000000, False)
    heuristic += val

    #middle spots are more valuable
    if move[0] == 4:
        heuristic += sign * 10

    #Two in a row for big boards are also valuable
    heuristic += checkTwo(total_board, sign * 300, sign* 1)

    #We want to fulfill a move that increases our likelihood of a getting a good placement
    next_grid = get_next_subgrid(move)
    heuristic += checkWin(test_board[next_grid], sign * 40, True)

    return heuristic

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

#gets the subgrid we are being sent to as a result of the move taken
def get_sub_grid(board, move):
    _, row, col = move
    return (row * 3) + col



