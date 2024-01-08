from typing import NamedTuple

class GridLocation(NamedTuple):
    """
    Represents a location within a TicTacToe grid.

    Attributes:
    - row (int): The row index of the location.
    - column (int): The column index of the location.
    """
    row: int
    column: int
    
    def __str__(self) -> str:
        return f"({self.row}, {self.column})"
