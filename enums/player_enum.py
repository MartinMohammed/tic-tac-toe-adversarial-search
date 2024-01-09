from enum import Enum


class PlayerEnum(Enum):
    """
    Enum for differentiating between players in a game or application.

    This enum is used to assign unique identifiers to players, facilitating the distinction between them in
    game logic, scoring, turns, or any other functionality where it is necessary to differentiate between players.

    Attributes:
        PLAYER_1 (int): Represents the first player, assigned the identifier 1.
        PLAYER_2 (int): Represents the second player, assigned the identifier 2.
    """

    PLAYER_1 = 1
    PLAYER_2 = 2
