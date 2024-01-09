from typing import List, Union
from models.tic_tac_toe import TicTacToe
from models.grid_location import GridLocation
from enums.termination_state_enum import TerminationStateEnum


def next_turn(
    game: TicTacToe,
    gl: GridLocation,
    buttons: List[List],
    label,
    play_with_adversarial_search=True,
) -> None:
    """
    Processes a player's turn in the TicTacToe game.

    Args:
        game (TicTacToe): The game instance.
        gl (GridLocation): The grid location where the player chooses to make a move.
        buttons (List[List]): A 2D list of button widgets representing the game board.
        label: The label widget to display game status messages.
    """
    row, column = gl.row, gl.column
    if game.termination_state is not None:
        label.config(text="The game has ended.")
        return

    buttons[row][column]["text"] = game.player
    game.next_turn(GridLocation(row, column))
    termination_state: Union[None, TerminationState] = game.termination_state

    if termination_state is None:
        label.config(text=f"{game.player} is next.")
        if game.identify_player(game.player) == 2 and play_with_adversarial_search:
            score, next_node = game.adversarial_move(make_move=False)
            action: GridLocation = next_node.action
            print(score, action)
            # Avoid infinite loop, no adversarial move next.
            next_turn(
                game=game,
                gl=action,
                buttons=buttons,
                label=label,
                play_with_adversarial_search=False,
            )

    elif termination_state in [
        TerminationStateEnum.PlayerTwoWon,
        TerminationStateEnum.PlayerOneWon,
    ]:
        label.config(text=f"{game.player} has won")
    else:
        label.config(text="It is a tie")
