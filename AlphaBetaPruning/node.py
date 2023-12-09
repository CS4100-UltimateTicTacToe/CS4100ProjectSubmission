class Node():
    def __init__(self, board, heuristic, nextSubGrid, children, move_by_parent):
        self.board = board
        self.heuristic = heuristic
        self.nextSubGrid = nextSubGrid
        self.children = children
        self.move_by_parent = move_by_parent