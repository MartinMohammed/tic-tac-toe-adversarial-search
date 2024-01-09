from typing import Generic, Callable, List, Tuple, Union
from models.node import Node
from shared.types import T, U
from enums.mini_max_objective_enum import MiniMaxObjectiveEnum
from enums.termination_state_enum import TerminationStateEnum

class MiniMax(Generic[T, U]):
    """
    Implementation of the MiniMax algorithm.

    Attributes:
    - _initial_node: The starting node of the game, encapsulating the initial state.
    - _mini_max_objective: Determines whether the goal is to maximize or minimize. 
                        By default we can assume it's initial value is MAX as root of indirect recursion.
    - _terminal: A function to check if a game state is terminal (end of game).
    - _utility: A function to evaluate the utility of a game state.
    - _actions: A function to generate possible actions from a given state.
    - _result: A function to determine the resulting state from an action.
    - _next_node: The recommended next node (state and action) based on MiniMax.

    Methods:
    - max_value: Calculates the maximum value of a node.
    - min_value: Calculates the minimum value of a node.
    - _get_score: Determines the score from a termination state.
    """

    def __init__(self, initial_node: Node[T, U],
                 terminal: Callable[[T], bool], utility: Callable[[T], float], 
                 actions: Callable[[T], List[U]], result: Callable[[T, U], T],
                 initial_objective: MiniMaxObjectiveEnum = MiniMaxObjectiveEnum.MAX) -> None:
        assert all([initial_node is not None, initial_objective is not None, 
                    terminal is not None, actions is not None, result is not None]), \
               "All parameters must be provided."
        self._initial_node: Node[T, U] = initial_node
        self._mini_max_objective: MiniMaxObjectiveEnum = initial_objective
        self._terminal: Callable[[T], bool] = terminal
        self._utility: Callable[[T], int] = utility
        self._actions: Callable[[T], List[U]] = actions
        self._result: Callable[[T, U], T] = result

    @property
    def mini_max_objective(self) -> MiniMaxObjectiveEnum:
        """
        Returns the current MiniMaxObjectiveEnum.
        """
        return self._mini_max_objective

    @mini_max_objective.setter
    def mini_max_objective(self, new_objective: MiniMaxObjectiveEnum):
        """
        Sets the new MiniMaxObjectiveEnum.
        """
        self._mini_max_objective = new_objective

    def start_mini_max(self) -> Tuple[int, Node[T, U]]:        
        # Initiate recursion based on the initial objective
        if self._mini_max_objective == MiniMaxObjectiveEnum.MAX:
            self._next_node: Tuple[int, Node[T, U]] = self.max_value(self._initial_node)
        else:
            self._next_node: Tuple[int, Node[T, U]] = self.min_value(self._initial_node)
        # Return the result. 
        return self._next_node
        
    def max_value(self, node: Node[T, U]) -> Tuple[int, Node[T, U]]:
        """
        Calculates the maximum value for a given node by evaluating potential actions 
        and choosing the one leading to the state with the highest minimum value.
        """

        # If state is terminal, then it's score will not be None.
        if self._terminal(node.state):
            score: int = self._get_score(self._utility(node.state))
            return (score, node)

        v, max_node = float('-inf'), None
        for action in self._actions(node.state):
            new_state = self._result(node.state, action)
            new_node = Node(state=new_state, parent=node, action=action)

            new_state_min_value, _ = self.min_value(new_node)
            if new_state_min_value > v:
                v, max_node = new_state_min_value, new_node
        return (v, max_node)

    def min_value(self, node: Node[T, U]) -> Tuple[int, Node[T, U]]:
        """
        Calculates the minimum value for a given node by evaluating potential actions 
        and choosing the one leading to the state with the lowest maximum value.
        """

        # If state is terminal, then it's score will not be None.
        if self._terminal(node.state):
            score: int = self._get_score(self._utility(node.state))
            return (score, node)

        v, min_node = float('inf'), None
        for action in self._actions(node.state):
            new_state = self._result(node.state, action)
            new_node = Node(state=new_state, parent=node, action=action)

            new_state_max_value, _ = self.max_value(new_node)
            if new_state_max_value < v:
                v, min_node = new_state_max_value, new_node
        return (v, min_node)

    def _get_score(self, termination_state: Union[None, TerminationStateEnum]) -> Union[None, int]:
        """
        Determines the score from a termination state. If the game is ongoing, indicated by None,
        the score is also None. Otherwise, it returns the value associated with the termination state.
        """
        return None if termination_state is None else termination_state.value
    