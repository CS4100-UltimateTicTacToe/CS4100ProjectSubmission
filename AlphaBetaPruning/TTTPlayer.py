import random
import numpy as np
from node import Node
from abpruning import ab_step

# A basic player which implements fully random behaviour
class TTTPlayer(object):
    def __init__(self, name, letter) -> None:
        self.name = name
        self.letter = letter

    def getName(self):
        return self.name
    
    def takeTurn(self, board, possibleMoves):
        pass

    def result(didWin):
        pass
    
class RandomPlayer(TTTPlayer):
    def __init__(self, name, letter) -> None:
        super().__init__(name, letter)
    
    def takeTurn(self, root_node, board, possibleMoves, subgrid):
        if (len(possibleMoves) < 1):
            print(board)
            raise ValueError("No possible moves")
        return random.choice(possibleMoves)

#Player that moves using Alpha-Beta Pruning
class PruningPlayer(TTTPlayer):
    def __init__(self, name, letter, depth) -> None:
        super().__init__(name, letter)
        self.depth = depth

    def takeTurn(self, board, root_node, possibleMoves, subgrid):
        node = Node(board, heuristic=0, nextSubGrid=subgrid, children=[], move_by_parent=None)
        ab_move = ab_step(node, self.letter, possibleMoves, subgrid, self.depth)
        return ab_move