from models.tic_tac_toe import TicTacToe
from gui.window import construct_window_and_game
from tkinter import Tk


# Initialize the TicTacToe game instance
# Need to make adversarial move manually, because otherwise the UI does not reflect the change.
game1: TicTacToe = TicTacToe(
    initial_player="x", play_with_adversarial_search=False, quiet=True
)
game1.start()

window_with_game: Tk = construct_window_and_game(game=game1)
window_with_game.mainloop()
