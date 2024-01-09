from typing import Any, Optional
from shared.constants import COLUMNS, ROWS
from custom_types.grid_type import GridType


def create_grid(
    fill: Optional[Any] = "",
    fill_by: Optional[GridType] = None,
    rows: int = ROWS,
    columns: int = COLUMNS,
) -> GridType:
    """
    Creates a grid (a 2D list) of specified dimensions, filled with a given value or pattern.

    This function generates a grid (two-dimensional list) where each cell is initialized with
    either a specified 'fill' value or values from 'fill_by' if provided. The dimensions of 
    the grid are determined by the 'rows' and 'columns' parameters. It's useful for initializing 
    the state of a game board or any other grid-based data structure.

    Parameters:
        fill (Any, optional): The value used to fill the grid cells. Defaults to an empty string.
        fill_by (GridType, optional): A 2D list to use as a pattern for filling the grid. 
                                      If provided, it overrides 'fill'.
        rows (int, optional): The number of rows in the grid. Defaults to ROWS.
        columns (int, optional): The number of columns in the grid. Defaults to COLUMNS.

    Returns:
        GridType: A grid (list of lists) with each cell set to the specified 'fill' value or 
                  patterned after 'fill_by'.
    """

    if fill_by is not None:
        # Assert the dimensions of the grid: 
        if len(fill_by) != rows or len(fill_by[0]) != columns:
            raise ValueError("The specified dimensions of rows and columns does not match the shape of the provided `fill_by` object.")
        return [[fill_by[row][column] for column in range(columns)] for row in range(rows)]

    return [[fill for _ in range(columns)] for _ in range(rows)]
