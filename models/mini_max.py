from typing import Generic, Callable, List, Tuple, Optional
from models.node import Node
from shared.types import T, U
from shared.exceptions.general import InvalidInstanceError
from enums.termination_state_enum import TerminationStateEnum
from models.grid_location import GridLocation


class MiniMax(Generic[T, U]):
    """
    Generic implementation of the MiniMax algorithm for adversarial decision-making in games.

    The MiniMax algorithm calculates the optimal move in a game by considering all possible
    future move sequences and choosing the one that maximizes the utility (for the maximizing player)
    or minimizes the utility (for the minimizing player).

    Attributes:
        _initial_node (Node[T, U]): The starting node representing the initial state of the game.
        _terminal (Callable[[T], bool]): Function to determine if a given state is terminal (end of game).
        _utility (Callable[[T], int]): Function to evaluate the utility value of a terminal state.
        _actions (Callable[[T], List[U]]): Function to generate a list of possible actions from a given state.
        _result (Callable[[T, U], T]): Function to determine the resulting state from an action.

    Methods:
        start_mini_max: Initiates the MiniMax algorithm and returns the best move and its value.
        max_value: Recursive function to calculate the maximum value of a node.
        min_value: Recursive function to calculate the minimum value of a node.
        _get_score: Determines the numerical score based on the termination state.

    Raises:
        InvalidInstanceError: If provided nodes, states, actions, or termination states are of incorrect types.
    """

    def __init__(
        self,
        initial_node: Node[T, U],
        terminal: Callable[[T], bool],
        utility: Callable[[T], int],
        actions: Callable[[T], List[U]],
        result: Callable[[T, U], T],
    ) -> None:
        if not isinstance(initial_node, Node):
            raise InvalidInstanceError(instance=initial_node, expected_type=Node)

        # Additional type checks for Node components can be added here if necessary

        self._initial_node: Node[T, U] = initial_node
        self._terminal: Callable[[T], bool] = terminal
        self._utility: Callable[[T], int] = utility
        self._actions: Callable[[T], List[U]] = actions
        self._result: Callable[[T, U], T] = result

    def start_mini_max(self) -> Tuple[int, Node[T, U]]:
        # Initiate recursion based on the initial objective
        return self.max_value(self._initial_node)

    def max_value(self, node: Node[T, U]) -> Tuple[int, Node[T, U]]:
        """
        Calculates the maximum value for a given node by evaluating potential actions
        and choosing the one leading to the state with the highest minimum value.
        """

        # Type checking using the class name as a string
        if node.parent is not None and not isinstance(node.parent, Node):
            raise InvalidInstanceError(instance=node.parent, expected_type=Node)

        if node.state.__class__.__name__ != "Game":
            raise InvalidInstanceError(instance=node.state, expected_type="Game")

        if node.action is not None and not isinstance(node.action, GridLocation):
            raise InvalidInstanceError(instance=node.action, expected_type=GridLocation)

        # If state is terminal, then it's score will not be None.
        if self._terminal(node.state):
            score: int = self._get_score(self._utility(node.state))
            return (score, node)

        v, max_node = float("-inf"), None
        output: List[Tuple(int, U)] = []
        for action in self._actions(node.state):
            new_state: T = self._result(node.state, action)
            new_node: Node[T, U] = Node(state=new_state, parent=node, action=action)
            new_state_min_value, _ = self.min_value(new_node)
            output.append((new_state_min_value, new_node.action))
            if new_state_min_value > v:
                v, max_node = new_state_min_value, new_node
        print(output)
        return (v, max_node)

    def min_value(self, node: Node[T, U]) -> Tuple[int, Node[T, U]]:
        """
        Calculates the minimum value for a given node by evaluating potential actions
        and choosing the one leading to the state with the lowest maximum value.
        """
        if not isinstance(node, Node):
            raise InvalidInstanceError(instance=node, expected_type=Node)

        # Type checking using the class name as a string
        if node.parent is not None and not isinstance(node.parent, Node):
            raise InvalidInstanceError(instance=node.parent, expected_type=Node)
        if node.state.__class__.__name__ != "Game":
            raise InvalidInstanceError(instance=node.state, expected_type="Game")

        if not isinstance(node.action, GridLocation):
            raise InvalidInstanceError(instance=node.action, expected_type=GridLocation)

        # If state is terminal, then it's score will not be None.
        if self._terminal(node.state):
            score: int = self._get_score(self._utility(node.state))
            return (score, node)

        v, min_node = float("inf"), None
        for action in self._actions(node.state):
            new_state: T = self._result(node.state, action)
            new_node: Node[T, U] = Node(state=new_state, parent=node, action=action)
            new_state_max_value, _ = self.max_value(new_node)
            if new_state_max_value < v:
                v, min_node = new_state_max_value, new_node
        return (v, min_node)

    def _get_score(
        self, termination_state: Optional[TerminationStateEnum]
    ) -> Optional[int]:
        """
        Determines the score from a termination state. If the game is ongoing, indicated by None,
        the score is also None. Otherwise, it returns the value associated with the termination state.
        """
        if termination_state is not None and not isinstance(
            termination_state, TerminationStateEnum
        ):
            raise InvalidInstanceError(
                instance=termination_state, expected_type=TerminationStateEnum
            )
        return None if termination_state is None else termination_state.value
