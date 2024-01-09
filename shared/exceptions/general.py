from models.grid_location import GridLocation
from typing import Any, Optional


class InvalidGridLocationError(ValueError):
    """Exception raised for errors in the input GridLocation."""

    def __init__(
        self,
        gl: Any,
        message: Optional[str] = "The provided GridLocation is not valid.",
    ):
        self.gl: Any = gl
        self.message: str = message
        super().__init__(f"{message} Received: {gl}")


class InvalidSymbolError(TypeError):
    """Exception raised for errors in the input symbol."""

    def __init__(
        self,
        symbol: Any,
        message: Optional[str] = "The provided symbol is not valid. Expected a string.",
    ):
        self.symbol: Any = symbol
        self.message: str = message
        super().__init__(f"{message} Received: {symbol}")


class InvalidMoveError(ValueError):
    """Exception raised for attempting an invalid move in the game."""

    def __init__(
        self,
        gl: GridLocation,
        message: Optional[str] = "The attempted move is not allowed.",
    ):
        self.gl: GridLocation = gl
        self.message: str = message
        super().__init__(f"{message} Grid Location: {gl}")


class InvalidInstanceError(TypeError):
    """Exception raised for errors in the type of a provided instance."""

    def __init__(
        self, instance: type, expected_type: type, message: Optional[str] = None
    ):
        self.instance = instance
        self.expected_type = expected_type
        if message is None:
            type_name: str = expected_type if isinstance(expected_type, str) else expected_type.__name__
            message: str = (
                f"The provided instance is not of type {type_name}."
                f" Received type: {instance.__class__.__name__}"
            )
        super().__init__(message)
