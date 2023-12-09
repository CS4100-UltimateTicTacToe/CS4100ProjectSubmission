import random
from monte_carlo import MONTE_CARLO

# A basic player which implements fully random behaviour
class TTTPlayer:
    def __init__(self, name, letter, monte_carlo=False) -> None:
        self.name = name
        self.letter = letter
        self.mc = monte_carlo

    def getName(self):
        return self.name
    
    #ADDED BY CHRIS
    def getLetter(self):
        return self.letter
    
    def takeTurn(self, possibleMoves, node=None, board=None, monte_carlo_on=False):
        if (len(possibleMoves) < 1):
            raise ValueError("No possible moves")
        if self.mc == True and not monte_carlo_on:
            monte_carlo_mode = MONTE_CARLO(name=self.letter, root_node=node, root_board_state=board, possible_moves=possibleMoves)
            mc_move = monte_carlo_mode.magic(iteration=1000)
            return mc_move
        else:
            return random.choice(possibleMoves)
    

