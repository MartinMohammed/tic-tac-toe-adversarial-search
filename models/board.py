from __future__ import annotations
from typing import List

from models.grid_location import GridLocation
from custom_types.grid_type import GridType
from models.player import Player
from shared.constants import COLUMNS, ROWS


class Board:
    """
    Represents a grid board used in games like Tic Tac Toe, typically 3x3 in size.

    The Board class is responsible for managing the placement of symbols within a grid, ensuring
    that each move is made to an unoccupied location. It tracks the moves made and the current state
    of the play grid. The Board itself does not determine the outcome of the game; such logic is managed
    externally, typically by a game controller.

    Parameters:
        initial_grid (GridType): The initial state of the game grid.

    Raises:
        ValueError: If the provided initial grid is not 3x3 in size.

    Attributes:
        _rows (int): The number of rows in the grid.
        _columns (int): The number of columns in the grid.
        _grid (GridType): The current state of the game grid.
        _maximum_plays (int): The total number of plays possible on the board.
        _plays (int): The number of plays that have been made on the board.
    """

    def __init__(self, initial_grid: GridType) -> None:
        if len(initial_grid) != ROWS or len(initial_grid[0]) != COLUMNS:
            raise ValueError("The board must be 3 rows by 3 columns in size.")
        self._rows: int = ROWS
        self._columns: int = COLUMNS
        self._grid: GridType = initial_grid
        self._maximum_plays: int = self._rows * self._columns
        self._plays: int = self._maximum_plays - len(self.actions())

    @property
    def grid(self) -> GridType:
        """
        Retrieves the current game board.

        Returns:
            np.ndarray: The current state of the game board as a numpy array.
        """
        return self._grid

    @property
    def plays(self) -> int:
        """
        Retrieves the number of plays made on the board.

        Returns:
            int: The number of plays that have been made on the board.
        """
        return self._plays

    def mark(self, gl: GridLocation, player: Player) -> Board:
        """
        Marks a position on the board with the specified player's symbol and returns the updated board state.

        This method first checks if the move is valid (i.e., within bounds and unoccupied). If valid, it updates the game grid
        at the specified grid location with the symbol of the player's enum, increments the count of plays, and returns the
        current instance of the Board reflecting the updated state. If the move is invalid, a warning is printed, and the
        current state of the board is returned without any changes.

        Parameters:
            gl (GridLocation): The grid location to mark.
            player (PlayerEnum): The player making the mark.

        Returns:
            Board: The current instance of the Board with the updated state after marking the specified location.
        """
        if not self.check_valid_move(gl=gl):
            print(f"This move {gl} is not allowed")
            return self

        # Increase the number of plays.
        self._plays += 1

        row, column = gl.row, gl.column
        self._grid[row][column] = player.symbol
        return self

    def show_board(self) -> None:
        """
        Prints the current state of the game board to the console.

        This method provides a simple way to visually inspect the current state of the game board by printing it.
        """
        print(self)

    def actions(self) -> List[GridLocation]:
        """
        Generates a list of possible grid locations that can be selected from the current board given its state.

        This method scans the entire grid and returns a list of all unoccupied (not blocked) grid locations.
        These locations represent the potential moves a player can make. If the number of plays equals the maximum
        possible plays, it returns an empty list indicating no further actions are possible.

        Returns:
            List[GridLocation]: A list of GridLocation objects representing all possible moves.
        """
        return [
            GridLocation(row, column)
            for column in range(self._columns)
            for row in range(self._rows)
            if not self._is_blocked(GridLocation(row=row, column=column))
        ]

    def terminal(self) -> bool:
        """Determines whether a game has terminated or not."""

    def result(self, action: GridLocation) -> Board:
        """
        Creates a deep copy of the current Board instance, performs the specified action on the copy,
        and returns the resulting board. This is useful for evaluating the consequences of a move without
        altering the current state of the board.

        Parameters:
            action (GridLocation): The grid location where the move is to be made.

        Returns:
            Board: A new Board instance reflecting the state after performing the action.
        """
        return self._copy_board().mark(action)

    def reset_board(self) -> Board:
        """
        Resets the game board to its initial state and returns the reset board.

        This method clears all marks from the players on the board and resets the count of plays to zero,
        effectively restarting the board for a new game. It then returns the current instance of the Board,
        now in its reset state. This approach allows for method chaining or immediate reuse of the board.

        Returns:
            Board: The current instance of the Board, reset to its initial state.

        Postconditions:
            - All grid elements are reset to their initial state.
            - The number of plays is reset to zero.
        """
        self._empty_spaces()
        self._plays = 0
        return self

    def _copy_board(self) -> Board:
        """
        Creates a deep copy of the current Board instance.

        Returns:
            Board: A new Board instance with a grid that is a deep copy of the current board's grid.
        """
        return Board(initial_grid=self._copy_grid())

    def _empty_spaces(self) -> None:
        """
        Clears all occupied spaces on the game board.

        This method resets each cell in the game grid to an empty state, preparing the board for a new game or for
        state evaluation purposes.
        """
        self._grid = [["" for _ in range(self._columns)] for _ in range(self._rows)]

    def check_valid_move(self, gl: GridLocation) -> bool:
        """
        Checks whether a proposed move is valid. A move is valid if it is within board boundaries and the target field is unoccupied.

        Args:
            gl (GridLocation): The grid location of the proposed move.

        Returns:
            bool: True if the move is valid (within boundaries and unoccupied), False otherwise.
        """
        if self._check_out_of_boundary(gl) or self._is_blocked(gl):
            return False
        return True

    def _check_out_of_boundary(self, gl: GridLocation) -> bool:
        """
        Checks if the specified grid location is out of the game board's boundaries.

        Args:
            gl (GridLocation): The grid location to check.

        Returns:
            bool: True if the location is out of bounds, False otherwise.
        """
        row, column = gl.row, gl.column
        return not (0 <= row <= 2 and 0 <= column <= 2)

    def _is_blocked(self, gl: GridLocation) -> bool:
        """
        Determines if the specified grid location is already occupied.

        Args:
            gl (GridLocation): The grid location to check.

        Returns:
            bool: True if the location is occupied, False if it is free.
        """
        assert not self._check_out_of_boundary(
            gl
        ), f"The specified GridLocation is out of bounds: {gl}"
        row, column = gl.row, gl.column
        return self._grid[row][column] != ""

    def _copy_board(self) -> Board:
        """
        Creates a deep copy of the current Board instance.

        This method generates a new Board instance using a deep copy of the current board's grid.
        The new Board instance will have the same grid state as the current one but will be completely independent.
        Any changes made to the new Board will not affect this one. This can be useful for creating hypothetical
        scenarios or for backtracking algorithms where you need to explore different board states without affecting
        the original board.

        Returns:
            Board: A new Board instance with a grid that is a deep copy of the current board's grid.
        """
        return Board(initial_grid=self.copy_grid())

    def __str__(self) -> str:
        """
        Provides a string representation of the game board, useful for debugging and logging. Empty cells are represented by a dot.

        Returns:
            str: The string representation of the game board, showing the current state of each cell.
        """
        return "\n".join(
            [" ".join([cell if cell else "." for cell in row]) for row in self._grid]
        )
