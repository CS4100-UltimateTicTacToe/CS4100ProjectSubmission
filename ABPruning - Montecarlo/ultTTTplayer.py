import random
from ult_monte_carlo import ULT_MONTE_CARLO

# A basic player which implements fully random behaviour
class ultTTTplayer:
    def __init__(self, name, letter, monte_carlo=False) -> None:
        self.name = name
        self.letter = letter
        self.mc = monte_carlo

    def getName(self):
        return self.name

    def getLetter(self):
        return self.letter
    
    def takeTurn(self, possibleMoves, node=None, board=None, monte_carlo_on=False):
        if (len(possibleMoves) < 1):
            raise ValueError("No possible moves")
        
        #A list of possible moves contains the board's positions and 
        #it's list of possible moves.
        #if there is more than one board of action to take, this (usually) means
        #that this is the first play
        if isinstance(possibleMoves[0], tuple):
            randomSet = random.choice(possibleMoves)
        else:
            randomSet = possibleMoves

        if self.mc == True and not monte_carlo_on:
            # the board should be a ultTTT instance
            # the node should be a 3-dimension coordinates now! [int, int, (int, int)]
            # and it (node) should be the turn made by the other player...

            monte_carlo_mode = ULT_MONTE_CARLO(name=self.name, root_node=node, root_board_state=board, possible_moves=randomSet)
            mc_move = monte_carlo_mode.magic(iteration=1000)

            return mc_move
        
        else:
            #print("This is the possible moves:",  possibleMoves)
            #This returns a random choice of action
            #print("This is the randomSet " + str(randomSet))
            randomTurn = random.choice(randomSet[2])

            #returns board dimensions and the a random spot to play
            return [randomSet[0], randomSet[1], randomTurn]

    

