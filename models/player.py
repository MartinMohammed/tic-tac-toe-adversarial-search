from typing import NamedTuple
from enums.player_enum import PlayerEnum

class Player(NamedTuple):
    """
    Represents a player in the game, encapsulating their identifier and symbol.

    This named tuple is used to associate a player with their unique identifier and symbol used in the game.
    The 'identifier' is an instance of PlayerEnum, indicating whether the player is PLAYER_1 or PLAYER_2. 
    The 'symbol' is a string representing the symbol assigned to the player, typically used on the game board.

    Attributes:
        identifier (PlayerEnum): The unique identifier of the player, distinguishing between the players in the game.
        symbol (str): The symbol assigned to the player for use in the game, which is an element of BoardSymbolsType.
    """
    identifier: PlayerEnum
    symbol: str
