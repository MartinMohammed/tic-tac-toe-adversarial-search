from typing import List
from gui.helpers.empty_buttons import empty_buttons
from models.game import Game


def restart_game(game: Game, buttons: List[List], label) -> None:
    """
    Restarts the TicTacToe game.

    Args:
        game (TicTacToe): The game instance to restart.
        buttons (List[List]): A 2D list of button widgets representing the game board.
        label: The label widget to display game status messages.
    """
    game.new_game()
    empty_buttons(buttons)
    label.config(text=f"{game.player}'s turn")
