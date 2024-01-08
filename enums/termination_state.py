from enum import Enum

class TerminationState(Enum):
    """
    Enum defining the different TerminationStates of a TicTacToe game.
    """
    PlayerTwoWon = -1
    Tie = 0
    PlayerOneWon = 1