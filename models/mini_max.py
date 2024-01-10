from typing import Generic, Callable, List, Tuple, Optional
from models.node import Node
from shared.types import T, U
from shared.exceptions.general import InvalidInstanceError
from enums.termination_state_enum import TerminationStateEnum
from models.grid_location import GridLocation

class MiniMax(Generic[T, U]):
    """
    Generic implementation of the MiniMax algorithm for adversarial decision-making in games.
    
    Attributes:
        _initial_node (Node[T, U]): The starting node representing the initial game state.
        _terminal (Callable[[T], bool]): Function to check if a state is terminal.
        _utility (Callable[[T], Optional[TerminationStateEnum]]): Evaluates utility of a terminal state.
        _actions (Callable[[T], List[U]]): Generates possible actions from a state.
        _result (Callable[[T, U], T]): Determines the resulting state from an action.

    Methods:
        start_mini_max: Begins the MiniMax algorithm, returning the best move and its value.
        _mini_max: Recursively calculates the node value, considering the player type.
        _validate_node: Validates node integrity.
        _is_better_score: Compares scores based on player type.
    """

    def __init__(
        self, 
        initial_node: Node[T, U], 
        terminal: Callable[[T], bool], 
        utility: Callable[[T], Optional[TerminationStateEnum]], 
        actions: Callable[[T], List[U]], 
        result: Callable[[T, U], T]
    ) -> None:
        self._validate_initial_node(node=initial_node)
        self._initial_node: Node[T, U] = initial_node
        self._terminal: Callable[[T], bool] = terminal
        self._utility: Callable[[T], Optional[TerminationStateEnum]]  = utility
        self._actions: Callable[[T], List[U]] = actions
        self._result: Callable[[T, U], T] = result

    def _validate_initial_node(self, node: Node[T, U]) -> None:
        """
        Validates the initial node to ensure it's an instance of the Node class.

        Args:
            node (Node[T, U]): The node to be validated.

        Raises:
            InvalidInstanceError: If the node is not an instance of the Node class.
        """
        if not isinstance(node, Node):
            raise InvalidInstanceError(instance=node, expected_type=Node)

    def start_mini_max(self, maximizing_player: Optional[bool] = True) -> Tuple[float, Optional[Node[T, U]]]:
        """
        Initiates the MiniMax algorithm and returns the best move along with its value.

        Args:
            maximizing_player (Optional[bool]): Flag to determine if the current layer is maximizing or not. Defaults to True.

        Returns:
            Tuple[float, Optional[Node[T, U]]]: The score of the best move and the corresponding node.
        """
        return self._mini_max(node=self._initial_node, maximizing_player=maximizing_player)

    def _mini_max(self, node: Node[T, U], maximizing_player: bool = True) -> Tuple[float, Optional[Node[T, U]]]:
        """
        Recursively calculates the MiniMax value of a node.

        Args:
            node (Node[T, U]): The current node in the MiniMax algorithm.
            maximizing_player (bool): A flag indicating if the current evaluation is for a maximizing player.

        Returns:
            Tuple[float, Optional[Node[T, U]]]: The best score achievable from the current node, and the corresponding best node.
        """
        self._validate_node(node)

        # Check if the current state is terminal and return its utility value, if so.
        if self._terminal(node.state):
            utility: TerminationStateEnum = self._utility(node.state)
            return utility.value if utility else 0, node

        # Initialize the best score based on whether the current player is maximizing or minimizing.
        best_score: float = float('-inf') if maximizing_player else float('inf')

        # Initialize the best node to track the optimal move for the current player.
        best_node: Optional[Node[T, U]] = None

        for action in self._actions(node.state):
            new_state: T = self._result(node.state, action)
            new_node: Node[T, U] = Node(state=new_state, parent=node, action=action)

            # Recursively call _mini_max for the next layer with the opposite player objective.
            score, _ = self._mini_max(new_node, not maximizing_player)

            # Update the best score and node if the current score is better based on the player's objective.
            if self._is_better_score(score, best_score, maximizing_player):
                best_score, best_node = score, new_node

        return best_score, best_node

    def _validate_node(self, node: Node[T, U]) -> None:
        """
        Validates the integrity of a node's attributes.

        Args:
            node (Node[T, U]): The node to be validated.

        Raises:
            InvalidInstanceError: If the node or its components do not meet the required type specifications.
        """
        if not isinstance(node, Node) or (node.parent and not isinstance(node.parent, Node)):
            raise InvalidInstanceError(instance=node, expected_type=Node)
        if node.state.__class__.__name__ != "Game":
            raise InvalidInstanceError(instance=node.state, expected_type="Game")
        if node.action and not isinstance(node.action, GridLocation):
            raise InvalidInstanceError(instance=node.action, expected_type=GridLocation)

    def _is_better_score(self, score: float, best_score: float, maximizing_player: bool) -> bool:
        """
        Compares two scores to determine if the current score is better based on the player type.

        Args:
            score (float): The current score to evaluate.
            best_score (float): The best score recorded so far.
            maximizing_player (bool): Indicates whether the current player is maximizing or minimizing.

        Returns:
            bool: True if the current score is better than the best score for the player type, False otherwise.

        Raises:
            ValueError: If any of the arguments are None.
        """
        if score is None or best_score is None or maximizing_player is None:
            raise ValueError("None arguments are not allowed in _is_better_score.")

        return (score > best_score) if maximizing_player else (score < best_score)
