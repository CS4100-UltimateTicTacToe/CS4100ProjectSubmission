import random
import numpy as np

# A basic player which implements fully random behaviour
class TTTPlayer(object):
    def __init__(self, name) -> None:
        self.name = name

    def getName(self):
        return self.name
    
    def takeTurn(self, board, possibleMoves):
        pass

    def result(didWin):
        pass
    


class RandomPlayer(TTTPlayer):
    def __init__(self, name) -> None:
        super().__init__(name)
    
    def takeTurn(self, board, possibleMoves, subgrid):
        if (len(possibleMoves) < 1):
            print(board)
            raise ValueError("No possible moves")
        return random.choice(possibleMoves)

