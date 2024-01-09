from typing import List, Optional
from custom_types.board_symbols_type import BoardSymbolsType
from models.player import Player

def get_player_symbols(players: List[Player]) -> BoardSymbolsType:
    """
    Extracts and returns the symbols of each player in the provided list.

    This function iterates over a list of Player objects and compiles a list of their symbols.
    It's useful for retrieving a collection of all player symbols in the game, typically for display,
    comparison, or game logic purposes.

    Parameters:
        players (List[Player]): A list of Player objects from which symbols are to be extracted.

    Returns:
        BoardSymbolsType: A list containing the symbol of each player in the order they appear in the input list.
    """
    return [player.symbol for player in players]

def get_player_by_symbol(symbol: str, players: List[Player]) -> Optional[Player]:
    """
    Retrieves the player associated with the given symbol.

    Iterates over the list of players and returns the player whose symbol matches the given symbol. 
    If no matching player is found, returns None.

    Parameters:
        symbol (str): The symbol to match against the players' symbols.
        players (List[Player]): The list of players to search through.

    Returns:
        Optional[Player]: The player with the matching symbol, or None if no match is found.
    """
    for player in players:
        if player.symbol == symbol:
            return player
    
