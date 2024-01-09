from typing import List, Union
from models.game import Game
from models.grid_location import GridLocation
from enums.termination_state_enum import TerminationStateEnum


def next_turn(
    game: Game,
    gl: GridLocation,
    buttons: List[List],
    label,
    play_with_adversarial_search=False,
) -> None:
    """
    Processes a player's turn in the TicTacToe game.

    Args:
        game (TicTacToe): The game instance.
        gl (GridLocation): The grid location where the player chooses to make a move.
        buttons (List[List]): A 2D list of button widgets representing the game board.
        label: The label widget to display game status messages.
    """
    
    if game.termination_state is not None:
        label.config(text="The game has ended.")
        return

    if not game._board.check_valid_move(gl):
        print("Not a valid move.")
        return
    
    row, column = gl.row, gl.column
    buttons[row][column]["text"] = game.player.symbol
    game.next_turn(GridLocation(row, column))
    termination_state: Union[None, TerminationStateEnum] = game.termination_state

    if termination_state is None:
        label.config(
            text=f"Player {game.player.identifier} ({game.player.symbol}) is next."
        )
        if game.player.identifier == 2 and play_with_adversarial_search:
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
        label.config(
            text=f"Player {game.player.identifier} ({game.player.symbol}) has won"
        )
    else:
        label.config(text="It is a tie")
