from UltimateTicTacToe import TicTacToe
from TTTPlayer import *
from TTTPlayer import RandomPlayer
from TTTPlayer import PruningPlayer
from tqdm import tqdm

if __name__ == "__main__":
    p1_win = 0
    p2_win = 0
    draw = 0
    num_game = 100

    for i in tqdm(range(num_game), desc="Processing"):
        player1 = PruningPlayer("Player1", "O", 2)
        player2 = RandomPlayer("Player2", "X")
        ttt = TicTacToe(player1, player2) 
        ttt.playGame()
        winner = ttt.checkTotalWin()
        
        if winner == 1:
            p1_win += 1
        elif winner == -1:
            p2_win += 1
        else:
            draw += 1

    p1_win_rate = round(p1_win / num_game * 100, 3)
    p2_win_rate = round(p2_win / num_game * 100, 3)
    draw_rate = round(draw / num_game * 100, 3)

    print(f"Player 1 win {p1_win_rate} percent over {num_game} games")
    print(f"Player 2 win {p2_win_rate} percent over {num_game} games")
    print(f"Over {num_game} games, {draw_rate} percent was a draw")