from shared.constants import COLUMNS, ROWS
from typing import Any, Optional
from custom_types.grid_type import GridType


def create_grid(
    fill: Optional[Any] = "",
    rows: Optional[int] = ROWS,
    columns: Optional[int] = COLUMNS,
) -> GridType:
    """
    Creates a grid (a 2D list) of specified dimensions, filled with a given value.

    This function generates a grid (two-dimensional list) where each cell is initialized with
    the specified 'fill' value. The dimensions of the grid are determined by the 'rows' and
    'columns' parameters. This is useful for initializing the state of a game board or any
    other grid-based data structure.

    Parameters:
        fill (Any, optional): The value used to fill the grid cells. Defaults to an empty string.
        rows (int, optional): The number of rows in the grid. Defaults to ROWS.
        columns (int, optional): The number of columns in the grid. Defaults to COLUMNS.

    Returns:
        GridType: A grid (list of lists) with each cell set to the specified 'fill' value.
    """
    return [[fill for _ in range(columns)] for _ in range(rows)]
