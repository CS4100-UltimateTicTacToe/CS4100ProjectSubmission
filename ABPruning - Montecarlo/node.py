import random

class Node:

    def __init__(self, parent=None, children=[], visit=0, win=0, draw=0, lose=0, uct=0, cur=None, board_state=None, max_child=0, total_simulation=0):
        """
        parent should only be one!
        """

        self.parent = parent
        self.children = children
        self.visit = visit
        self.win = win
        self.draw = draw
        self.lose = lose
        self.uct = uct
        self.cur = cur
        self.board_state = board_state
        self.max_child = max_child
        #self.total_simulation = total_simulation

    def add_child(self, child, board_state):
        """ child should be a play, a coordinate on the board"""
        child_node = Node(parent=self, cur=child, children=[], board_state=board_state, max_child=len(board_state.getPossibleMoves()))
        self.children.append(child_node)

    def ult_add_child(self, child, board_state):
        """ child should be a play, a coordinate on the board"""
        possible_moves = board_state.getPossibleMoves()
        muti=False
        for x in possible_moves:
            if type(x) == tuple:
                muti=True
        if muti:
            possible_moves = random.choice(possible_moves)
        child_node = Node(parent=self, cur=child, children=[], board_state=board_state, max_child=len(possible_moves))
        self.children.append(child_node)
