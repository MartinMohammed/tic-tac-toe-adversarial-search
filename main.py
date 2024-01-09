from typing import List
from models.game import Game
from gui.window import construct_window_and_game
from tkinter import Tk
from shared.constants import BOARD_SYMBOLS
from models.player import Player


players: List[Player] = [Player(1, BOARD_SYMBOLS[0]), Player(2, BOARD_SYMBOLS[1])]

# Initialize the TicTacToe game instance
# Need to make adversarial move manually, because otherwise the UI does not reflect the change.
game1: Game = Game(
    initial_player=players[0],
    players=players,
    play_with_adversarial_search=False,
    quiet=False,
)
game1.start()

window_with_game: Tk = construct_window_and_game(
    game=game1, play_with_adversarial_search=True
)
window_with_game.mainloop()
