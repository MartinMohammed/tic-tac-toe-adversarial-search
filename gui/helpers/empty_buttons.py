from typing import List


def empty_buttons(buttons: List[List]) -> None:
    """
    Clears the text from all buttons on the TicTacToe board.

    Args:
        buttons (List[List]): A 2D list of button widgets representing the game board.
    """
    for row in buttons:
        for button in row:
            button["text"] = ""
