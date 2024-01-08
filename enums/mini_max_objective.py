from enum import Enum

class MiniMaxObjective(Enum):
    """
    Enum definfing the different Objectives that a player can have.  
    """
    # State: 1 means the player wants to win the game -- maximize the score
    MAX = 1

    # State: -1 means the player wants to minimize the game --  minimize the score
    MIN = -1


