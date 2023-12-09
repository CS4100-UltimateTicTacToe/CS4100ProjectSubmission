import numpy as np
#from tictactoe import getPossibleMoves, playGame, checkWin
from copy import deepcopy
import random
from node import Node
from tqdm import tqdm

class MONTE_CARLO:
    def __init__(self, name, root_node, root_board_state, possible_moves, root_total_simulations=0) -> None:
        # name is the "O" or "X" the monte carlor player is using, but I havn't use it yet
        self.name = name
        self.root = Node(cur=root_node, children=[], board_state=deepcopy(root_board_state), max_child=len(possible_moves))
        # an important element to keep track of where we are
        self.cur_node = self.root
        self.turn = "X"
        self.total_simulation = root_total_simulations

    def magic(self, iteration):
        print("start the monte carlo search tree algorithm!")

        for _ in tqdm(range(iteration)):

            self.total_simulation += 1

            # selected node could be the root itself (at the 1st iteration) or its children's children's children...
            selected_node, skip = self.select(self.root)
            # child_node is either the selected node itself or one of its children
            child_node = self.expand(selected_node)
            # we simulate the game based on the child_node
            result = self.simulate(child_node, skip)
            # based on the result, we update the uct of node
            # this will go all way back to root
            self.backpropagate(child_node, result)

        # now we are ready to choose the direct children for root node based on uct value
        uct_list = [child.uct for child in self.root.children]
        best_child = [child for child in self.root.children if child.uct == max(uct_list)]
        best_move = random.choice(best_child)

        return best_move.cur

    def getName(self):
        return self.name

    # select should always begin from the root
    def select(self, node):
        """
        Select a child node with the highest UCT value.
        """
        # The selection function continues down the tree based on UCT scores until it reaches a leaf node.
        # only keep dive down when it has all the children
        while len(node.children) == node.max_child:
            # handle the case when the algo reaches the terminal state
            if node.max_child == 0:
                skip=True
                return node, skip
                break
            uct_list = [child.uct for child in node.children]
            children = [child for child in node.children if child.uct == max(uct_list)]
            node = random.choice(children)
        skip = False

        return node, skip

    def expand(self, node):
        """
        Add a new child node from the unvisited moves.
        """
        # Assuming we have a function that generates possible moves from the current state
        possible_moves = self.get_possible_moves(node.board_state)

        if len(possible_moves) > 0:

            # remove the children that already exists
            for exist_child in node.children:
                possible_moves.remove(exist_child.cur)

            # randomly select a possible move
            new_move = random.choice(possible_moves)
            # get new board for new child node, it is like adding a new move to a board
            new_board_state = self.get_new_state(deepcopy(node.board_state), new_move, node.cur)
            
            node.add_child(new_move, new_board_state)

            return node.children[-1]
        else:
            return node


    def simulate(self, child_node, skip):
        """
        Simulate a random game starting from the given node until a result is determined.
        """
        if not skip:
            current_state = deepcopy(child_node.board_state)

            while not self.is_game_over(current_state):
                current_state.playGame(monte_carlo_on=True)

            return self.get_result(current_state)
        else:
            # handle the terminal state
            return self.get_result(child_node.board_state)

    def backpropagate(self, node, result):
        """
        Backpropagate the simulation result up the tree, updating node statistics.
        """
        
        while node is not None:
            node.visit += 1
            if result == "X":
                node.win += 1
            elif result == "O":
                node.lose += 1
            else:
                node.draw += 1


            # Update the UCT value
            node.uct = self.calculate_uct(node.win, node.visit, self.total_simulation)
            node = node.parent

    def get_new_state(self, cur_board_state, child_node, cur_point):
        """
        given a node, get the next state!
        You can imagine you play first on an empty board, and hand it to a machine, machine take one random possible move
        and wants to simulate the rest!
        """

        if cur_point == None:
            self.turn = "X"
        elif cur_board_state.board[cur_point] == "O":
            self.turn = "X"
        elif cur_board_state.board[cur_point] == "X":
            self.turn = "O"
        cur_board_state.board[child_node] = self.turn
        new_board_state = deepcopy(cur_board_state)

        return new_board_state

    def get_possible_moves(self, board_state):
        # Returns the list of possible moves from the current board state
        return board_state.getPossibleMoves()

    def is_game_over(self, board_state):
        # Determines if the game is over and returns a boolean
        return board_state.checkWin != 0

    def get_result(self, board_state):
        # Analyzes the board state to determine the result ('Win', 'Loss', or 'Draw')
        return board_state.checkWin()

    def calculate_uct(self, wins, visits, total_simulations, c_param=1.41):
        # Calculates the UCT value using the provided formula
        if visits == 0:
            return float('inf')
        return (wins / visits) + c_param * (np.log(total_simulations) / visits) ** 0.5
