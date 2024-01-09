from enum import Enum


class MiniMaxObjectiveEnum(Enum):
    """
    Enum defining the strategic objectives of players in a Minimax algorithm context.

    This enum categorizes players as either MAX or MIN within the framework of the Minimax algorithm. The MAX player
    aims to maximize their winning potential, searching for game paths that optimize their chances of success.
    Typically, in AI implementations, the AI (adversarial player) is considered the MAX player. The MIN player,
    on the other hand, seeks to minimize the MAX player's chances of winning.

    When the AI is the MAX player, the MIN player represents the human or non-AI opponent. In this scenario,
    the MIN player is an abstraction of the opponent making the most optimal moves possible at each turn, adhering
    to the Minimax principle. This principle ensures that the AI evaluates all possible moves from a given state,
    choosing the one that leads to the maximum of the minimum values achievable by the opponent, and vice versa for
    the MIN player.

    Attributes:
        MAX (int): Represents the player (typically AI) trying to maximize their winning potential.
        MIN (int): Represents the opponent (human or non-AI) attempting to minimize the MAX player's winning potential.
    """

    MAX = 1
    MIN = -1
