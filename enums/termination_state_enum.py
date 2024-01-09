from enum import Enum

class TerminationStateEnum(Enum):
    """
    Enum defining the different TerminationStates of a TicTacToe game.
    """
    PlayerOneWon = -1
    Tie = 0
    PlayerTwoWon = 1