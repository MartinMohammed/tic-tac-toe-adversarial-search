from typing import List
from models.game import Game
from shared.constants import BOARD_SYMBOLS
from models.player import Player
from gui.window import TicTacToeWithGUI


players: List[Player] = [Player(identifier=1, symbol=BOARD_SYMBOLS[0]), Player(identifier=2, symbol=BOARD_SYMBOLS[1])]

# Initialize the TicTacToe game instance
# Need to make adversarial move manually, because otherwise the UI does not reflect the change.
game1: Game = Game(
    initial_player=players[0],
    players=players,
    play_with_adversarial_search=False,
    quiet=False,
)
TicTacToeWithGUI(game=game1, play_with_adversarial_search=True)
