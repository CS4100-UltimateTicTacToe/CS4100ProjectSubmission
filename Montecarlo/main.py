from tictactoe import TicTacToe
from TTTPlayer import TTTPlayer
from ultTTT import ultTTT
from ultTTTplayer import ultTTTplayer

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np

# begin here, just set up the web element, if you don't care, scroll down to where I test monte carlo
def check_rows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return None

def check_diagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return None

def check_win(board):
    # Check rows and columns
    for new_board in [board, np.transpose(board)]:
        result = check_rows(new_board)
        if result:
            return result
    # Check diagonals
    return check_diagonals(board)

def create_small_board_layout(small_board, winner=None):
    if winner:
        # If there's a winner, return a large "X" or "O"
        return html.Div(winner, style={'width': '90px', 'height': '90px', 'fontSize': '4em', 'textAlign': 'center', 'border': '1px solid black'})
    else:
        # Otherwise, return the standard 3x3 grid
        return html.Table(
            # Each row in the small board
            [html.Tr([
                html.Td(
                    small_board[i][j] if small_board[i][j] != " " else html.Div(' ', style={'minWidth': '30px', 'minHeight': '30px'}),
                    style={'width': '30px', 'height': '30px', 'border': '1px solid black', 'textAlign': 'center'}
                ) for j in range(3)
            ]) for i in range(3)],
            style={'borderCollapse': 'collapse', 'display': 'inline-block', 'margin': '2px'}
        )

def create_ultimate_board_layout(boards):
    if boards.shape == (3, 3, 3, 3):
        ultimate_board_layout = []
        for row_of_boards in boards:
            row_layout = []
            for small_board in row_of_boards:
                # Check if we have a winner for the small board
                winner = None
                # Generate the layout for the small board
                cell_layout = create_small_board_layout(small_board, winner=winner)
                row_layout.append(cell_layout)
            # Append the row of small boards to the ultimate board layout
            ultimate_board_layout.append(html.Div(row_layout, style={'display': 'flex', 'justifyContent': 'center'}))
        return html.Div(ultimate_board_layout, style={'textAlign': 'center'})
    else:
        result_layout = []
        for i in range(3):
            row_layout = []
            for j in range(3):
                # Create a cell for each result
                cell = html.Div(boards[i][j], style={
                    'width': '90px', 'height': '90px', 'fontSize': '4em',
                    'textAlign': 'center', 'border': '1px solid black', 'display': 'inline-block'
                })
                row_layout.append(cell)
            result_layout.append(html.Div(row_layout, style={'display': 'flex', 'justifyContent': 'center'}))
        return html.Div(result_layout, style={'textAlign': 'center'})


def eval(num_games):
    """
    evaluating the monte carlo win rate, draw rate and lose rate based on input number of games
    """
    
    p1_win = 0
    p2_win = 0
    draw = 0

    for game in range(num_games):
        player1 = ultTTTplayer("player 1", "O")
        player2 = ultTTTplayer("player 2", "X", monte_carlo=True)
        UltTTT = ultTTT(player1, player2)
        UltTTT.playGame()

        winner = UltTTT.getUltWinner()

        if winner == 0:
            draw += 1
        elif winner.name == "player 1":
            p1_win += 1
        elif winner.name == "player 2":
            p2_win += 1

        print(f'game: {game}')

    p1_win_rate = round(p1_win / num_games * 100, 3)
    p2_win_rate = round(p2_win / num_games * 100, 3)

    print(f"Player 1 win {p1_win_rate} percent over {num_games} games")
    print(f"Player 2 win {p2_win_rate} percent over {num_games} games")


#RUN FOR ULTIMATE
if __name__ == "__main__":
    eval(100)

    # if you just want to see one round, please comment the eval and uncomment the thing below 

#     player1 = ultTTTplayer("player 1", "O")
#     player2 = ultTTTplayer("player 2", "X", monte_carlo=True)

#     ultTTT = ultTTT(player1, player2)
#     ultTTT.playGame()

#     records = ultTTT.board_record

#     results = ultTTT.result_board

#     records = np.array(records)

    # uncommented below if you want to see the visualization

#     app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#     # Initialize an empty 3x3x3 board
#     initial_boards = np.full((3, 3, 3, 3), " ")

#     app.layout = html.Div([
#     html.H1("Ultimate Tic-Tac-Toe Board"),
#     dcc.Store(id='board-state', data=initial_boards.tolist()),  # Store to hold board state
#     dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Update every second
#     html.Div(id='ultimate-tic-tac-toe-board')
# ])



#     @app.callback(
#     Output('board-state', 'data'),
#     Input('interval-component', 'n_intervals')
# )
#     def update_board_state(n_intervals):
#         #print(f"Interval: {n_intervals}")
#         index = n_intervals % len(records) 
#         board = records[index]  # Get the current board from the records
#         #print(f"Board at index {index}: {board}")

#         if n_intervals + 1 > len(records):
#             return results.tolist()
#         else:
#             return board.tolist()  

#     @app.callback(
#     Output('ultimate-tic-tac-toe-board', 'children'),
#     Input('board-state', 'data')
# )
#     def update_ultimate_board_layout(current_board_state):
#         # Convert the current board state back to a 4D NumPy array
#         boards = np.array(current_board_state, dtype=object)
#         # Generate the board layout using the current board state
#         board_layout = create_ultimate_board_layout(boards)
#         return board_layout

#     app.run_server(debug=True)



# below is the part for regular tictactoe, if you interested in how monte carlo works on it, comment the "main" function above and uncomment below code

# #RUN FOR REGULAR
# you will want to see how the algorithm works for regular tictaetoe by using this
#if __name__ == "__main__":
#    player1 = TTTPlayer("player 1", "O")
#    player2 = TTTPlayer("player 2", "X", monte_carlo=True)
#    ttt = TicTacToe(player1, player2, True)
#    ttt.playGame()

    #visual.run_visual()

    # p1_win = 0
    # p2_win = 0
    # draw = 0
    # num_game = 100

    # for game in range(num_game):
    #     player1 = TTTPlayer("player 1", "O")
    #     player2 = TTTPlayer("player 2", "X", monte_carlo=True)
    #     ttt = TicTacToe(player1, player2, True)
    #     ttt.playGame()

    #     winner = ttt.getWinner()
    #     if winner == 0:
    #         draw += 1
    #     elif winner.name == "player 1":
    #         p1_win += 1
    #     elif winner.name == "player 2":
    #         p2_win += 1
    #     #visual.run_visual()

    # p1_win_rate = round(p1_win / num_game * 100, 3)
    # p2_win_rate = round(p2_win / num_game * 100, 3)

    # print(f"Player 1 win {p1_win_rate} percent over {num_game} games")
    # print(f"Player 2 win {p2_win_rate} percent over {num_game} games")







