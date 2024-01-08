from typing import Generic, Optional
from shared.types import T, U

class Node(Generic[T, U]):
    """
    Represents a node in a partially directed graph where nodes can have children,
    but not all nodes necessarily have a parent.
    """

    def __init__(self, state: T, parent: Optional["Node[T, U]"], action: Optional[U],  cost: float = 0.0, heuristic: float = 0.0):
        """
        Initializes a node in the graph with the given state, optional parent node,
        cost, and heuristic.

        Parameters:
        - state: The state associated with the node.
        - parent: The optional parent node (if exists) from which this node is derived.
        - action: The action taken to transition from the parent state to the current state.
                For Tic Tac Toe, this could be a tuple (row, column) indicating the move's position.
        """
        self.state: T = state
        self.parent: Optional["Node[T, U]"] = parent
        self.action: U = action