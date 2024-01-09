from typing import Optional, Tuple
from tkinter import Button, Tk, Frame, Label
from models.game import Game
from models.grid_location import GridLocation
from models.node import Node
from shared.constants import ROWS, COLUMNS, FONT
from enums.termination_state_enum import TerminationStateEnum
from shared.exceptions.exception import InvalidGridLocationError

class TicTacToeWithGUI:
    def __init__(self, game: Game, play_with_adversarial_search: Optional[bool] = False):
        self._game = game
        self._play_with_adversarial_search = play_with_adversarial_search
        self.setup_gui(title="Tic Tac Toe")
        self._window.mainloop()

    def setup_gui(self, title: str) -> None:
        """Sets up the GUI for the Tic Tac Toe game."""
        self._window = Tk()
        self._window.title(title)

        self._label = Label(self._window, text=f"Player {self._game.player.identifier} ({self._game.player.symbol}) is next.", font=(FONT, 40))
        self._label.pack(side="top")

        reset_button = Button(self._window, text="Restart", font=(FONT, 20),
                              command=self.restart_game_and_update_label)
        reset_button.pack(side="top")

        self._frame = Frame(self._window)
        self._frame.pack()

        self._buttons = [[self._create_button(GridLocation(row=row, column=column)) for column in range(COLUMNS)] 
                         for row in range(ROWS)]

    def _create_button(self, gl: GridLocation) -> Button:
        """Creates a button for the Tic Tac Toe grid."""
        row, column = gl.row, gl.column
        button = Button(self._frame, text="", font=(FONT, 40), width=5, height=2,
                        command=lambda: self.next_turn(GridLocation(row, column), recursive=False))
        button.grid(row=row, column=column)
        return button

    def next_turn(self, gl: GridLocation, recursive: Optional[bool] = False) -> None:
        """Processes the next turn in the game based on the player's action."""
        if not isinstance(gl, GridLocation):
            raise InvalidGridLocationError(gl=gl)

        if self._game.termination_state:
            self._label.config(text="The game has ended.")
            return

        if not self._game._board.check_valid_move(gl=gl):
            self._label.config(text="Not a valid move.")
            return

        self._game.next_turn(gl=gl)
        self._update_ui(gl=gl)

        if self._game.termination_state is None and self._play_with_adversarial_search and not recursive:
            adversarial_move: Tuple[int, Node[Game, GridLocation]] = self._game.adversarial_move(make_move=False)
            _, node = adversarial_move
            self.next_turn(gl=node.action, recursive=True)


    def _update_ui(self, gl: GridLocation) -> None:
        """Updates the UI elements based on the current game state."""
        if not isinstance(gl, GridLocation):
            raise InvalidGridLocationError(gl=gl)

        row, col = gl.row, gl.column
        self._buttons[row][col]["text"] = self._game.player.symbol
        termination_state = self._game.termination_state

        if termination_state:
            if termination_state in [TerminationStateEnum.PlayerOneWon, TerminationStateEnum.PlayerTwoWon]:
                self._label.config(text=f"Player {self._game.player.identifier} has won")
            else:
                self._label.config(text="It is a tie")
        else:
            self._label.config(text=f"Player {self._game.player.identifier} ({self._game.player.symbol}) is next.")

    def restart_game_and_update_label(self) -> None:
        """Restarts the game and updates the label to reflect the new game state."""
        self._game.new_game()
        self._empty_buttons()
        self._label.config(text=f"Player {self._game.player.identifier} is next.")

    def _empty_buttons(self) -> None:
        """Clears all buttons on the board."""
        for row_buttons in self._buttons:
            for button in row_buttons:
                button["text"] = ""
