from __future__ import annotations
from typing import Optional, List, Tuple
from models.board import Board
from models.mini_max import MiniMax
from models.node import Node
from models.grid_location import GridLocation
from enums.mini_max_objective_enum import MiniMaxObjectiveEnum
from enums.termination_state_enum import TerminationStateEnum
from models.player import Player
from enums.player_enum import PlayerEnum
from shared.utils.player_utils import get_player_by_symbol
from shared.utils.board_utils import create_grid


class Game:
    """
    Represents a Game game with functionalities to manage the game TerminationState,
    perform moves, and check game status.

    Attributes:
        _play_with_adversarial_search (bool): Whether to play with adversarial search.
        _players (List[str]): List of player symbols.
        _plays (int): Number of plays made in the game.
        _player (str): The current player.
        _initial_player (str): The initial player. Reset to this player if game restarts and no player switch.
        _grid (List[List[str]]): The game board.
        _termination_state (Optional[TerminationState]): The termination of the game if it has ended.
        _mini_max: (MiniMax[TicTacToe, GridLocation]): MiniMax instance for adversarial search.
    """

    def __init__(
        self,
        players: List[Player],
        play_with_adversarial_search: bool = False,
        initial_player: Optional[Player] = None,
        initial_board: Optional[Board] = None,
        **kwargs,
    ) -> None:
        """
        Initializes a new TicTacToe game with optional parameters for players,
        the initial player, and the game grid.

        Args:
            players (Optional[List[str]]): The symbols of the two players.
            initial_player (Optional[str]): The player who starts the game.
            initial_grid (Optional[List[List[str]]]): The initial game state.
        """

        # Handling kwargs
        self._quiet = kwargs.get(
            "quiet", True
        )  # Example of handling a 'quiet' keyword argument

        if len(players) != 2:
            raise ValueError("The number of players must be exactly 2.")
        self._players: List[Player] = players
        if initial_player not in players:
            raise ValueError("The initial player must be one of the players.")

        assert (
            initial_player in players
        ), "The initial player must be part of the provided players."

        if initial_board is not None:
            self._board: Board = initial_board
        else:
            self._board: Board = Board(initial_grid=create_grid(fill=""))

        self._play_with_adversarial_search: bool = play_with_adversarial_search
        self._mini_max: Optional[MiniMax[Game, GridLocation]] = None

        # Needed when restarting the game
        self._initial_player: Player = (
            initial_player if initial_player is not None else players[0]
        )
        self._player: Player = initial_player

        # Get the termination state of the current board:
        self._termination_state: Optional[TerminationStateEnum] = None

        # Cannot be None if game has terminated
        if Game.terminal(self):
            self._termination_state: TerminationStateEnum = (
                self._get_termination_state()
            )

    def start(self) -> None:
        """Add information to the console that the game has started."""
        print("The game begins: ")
        if not self._quiet:
            self.show_game()

    @property
    def player(self) -> Player:
        """
        Gets the current player.

        Returns:
            str: The symbol of the current player.
        """
        return self._player

    @property
    def players(self) -> List[Player]:
        """
        Retrieves the list of player symbols.

        Returns:
            List[Player]: List of player types.
        """
        return self._players

    @property
    def termination_state(self) -> Optional[TerminationStateEnum]:
        """
        Retrieves the current termination state of the game.

        Returns:
            Optional[TerminationState]: Termination State of the game.
        """
        return self._termination_state

    # ----------------- Static methods BECAUSE THEY SHOULD WORK UPON INSTANCES -----------------
    @staticmethod
    def utility(instance: Game) -> Optional[TerminationStateEnum]:
        """
        Determines the utility of the game if it has reached a terminal state.
        """
        return instance.termination_state

    @staticmethod
    def result(instance: Game, gl: GridLocation):
        """
        Predicts the game state resulting from making a move at the specified location.
        """
        copy: Game = instance._copy_game().next_turn(gl)
        return copy

    @staticmethod
    def actions(instance: Game) -> List[GridLocation]:
        """
        Provides a list of all possible legal moves in the current game state.
        """
        return instance._board.actions()

    @staticmethod
    def terminal(instance: Game) -> bool:
        """
        Checks if the game of the instance is terminal.
        """
        return instance.termination_state != None

    # -------------------------------------------------------------
    def next_turn(self, gl: GridLocation) -> Game:
        """
        Processes the next turn in the game at the specified grid location and returns the game instance.

        This method checks if the move at the given location is valid and, if so, makes the move and updates the game state.
        It then checks for a winning or terminal state. If the game has not ended, it switches to the next player. If the
        game has ended, it updates the termination state. The method also handles adversarial moves if applicable.

        After processing the turn, the method returns the current instance of the Game, reflecting any changes made during
        the turn.

        Args:
            gl (GridLocation): The location where the next move is made.

        Returns:
            Game: The current instance of the Game, updated with the changes made during this turn.
        """
        if self._board.check_valid_move(gl=gl):
            # Make the move
            self._board.mark(gl=gl, symbol=self._player.symbol)

            winner: Optional[TerminationStateEnum] = self._get_termination_state()

            # Game has not ended yet.
            if winner is None:
                self._switch_player()
            else:
                # The game terminated.
                self._termination_state = winner

            if not self._quiet:
                self.show_game()

            if (
                self._play_with_adversarial_search
                and self._player.identifier == 2
                and self._termination_state is None
            ):
                self.adversarial_move(make_move=True)
        return self

    def adversarial_move(self, make_move=False) -> Tuple[int, Node[Game, GridLocation]]:
        """
        Executes an adversarial move based on the MiniMax algorithm in the current game state.

        This method initializes a MiniMax instance with the current game state and then
        computes the optimal adversarial move. The move is determined by evaluating the game's
        potential future states and choosing the one that maximizes the chances of winning,
        as per the MiniMax strategy.

        After computing the move, the game state is updated to reflect this choice, and the
        method returns the score associated with the move and the corresponding node in the
        game tree that represents the new state.

        Returns:
            Tuple[int, Node[TicTacToe, GridLocation]]: A tuple containing the score of the
            computed move and the node representing the game state after the move is made.
        """
        self._mini_max: MiniMax[Game, GridLocation] = MiniMax[Game, GridLocation](
            initial_node=Node(state=self, parent=None, action=None),
            initial_objective=MiniMaxObjectiveEnum.MAX,
            terminal=Game.terminal,
            utility=Game.utility,
            result=Game.result,
            actions=Game.actions,
        )

        score, next_node = self._mini_max.start_mini_max()
        if make_move:
            self.next_turn(next_node.action)
        return (score, next_node)

    def new_game(self, change_players: bool = False) -> None:
        """
        Starts a new game, optionally switching the starting player.

        Args:
            change_players (bool): Whether to switch the starting player for the new game.
        """
        self._board.reset_board()
        self._termination_state: Optional[TerminationStateEnum] = None
        self._player: Player = self._initial_player
        if change_players:
            self._switch_player()

        if self._play_with_adversarial_search:
            # A new instace for the minimax object since the current state has been reseted.
            self._mini_max = MiniMax[Game, GridLocation] = MiniMax(
                initial_node=Node(state=self, parent=None, action=None),
                initial_objective=MiniMaxObjectiveEnum.MAX,
                terminal=Game.terminal,
                utility=Game.utility,
                result=Game.result,
                actions=Game.actions,
            )

        if not self._quiet:
            self.show_game()

    def show_game(self) -> None:
        """
        Displays the current state of the game board to the console.
        This includes showing who's turn it is, the winner, or if the game is a tie.
        """
        print("-" * 10)
        print(self)

    def _get_termination_state(self) -> Optional[TerminationStateEnum]:
        """
        Determines the termination state of the current game.

        This method checks the game board for any win conditions (horizontal, vertical, diagonal) and
        determines if the game has ended in a win for either player or a tie. If a winning condition
        is met, it updates the `self._termination_state` with the appropriate state. If no winning condition
        is met and the game is still ongoing, it returns None.

        Postconditions:
            - If a win condition is detected, `self._termination_state` is updated to the corresponding
            termination state (PlayerOneWon or PlayerTwoWon).
            - If a tie condition is detected, `self._termination_state` is updated to Tie.
            - If the game is still ongoing, `self._termination_state` remains unchanged.

        Returns:
            Optional[TerminationStateEnum]: The termination state of the game (win for player one,
            win for player two, tie, or None if the game is ongoing).
        """

        # Check horizontal and vertical lines
        for check in [self._board.check_horizontals, self._board.check_verticals, self._board.check_diagonals]:
            winner = check()
            if winner is not None:
                self._termination_state: TerminationStateEnum = self._determine_winner(winner)
                return self._termination_state

        # Check for tie
        if self._board.plays == self._board._columns * self._board._rows:
            self._termination_state: TerminationStateEnum = TerminationStateEnum.Tie
            return TerminationStateEnum.Tie

        # Game is still ongoing
        return None


    def _determine_winner(self, symbol: str) -> TerminationStateEnum:
        """
        Determines the winner based on the provided symbol.

        Args:
            symbol (str): The symbol to check for the winner.

        Returns:
            TerminationStateEnum: The winning state (PlayerOneWon or PlayerTwoWon).
        """
        player: Player = get_player_by_symbol(symbol, self._players)
        if player.identifier == PlayerEnum.PLAYER_1:
            return TerminationStateEnum.PlayerOneWon
        else:
            return TerminationStateEnum.PlayerTwoWon

    def _copy_game(self) -> Game:
        """
        Creates a deep copy of the current Game instance.

        This method is useful for creating a new Game instance that preserves the current game's state,
        including player information, current player turn, and the board state, without affecting the original game.
        Especially useful in scenarios like implementing game AI where exploring future moves without altering the
        current game state is required.

        Returns:
            Game: A new instance of Game with a deep copy of the current game's state.
        """
        return Game(
            players=self._players,
            initial_player=self._player,
            initial_board=self._board.copy_board(),
            play_with_adversarial_search=self._play_with_adversarial_search,
        )

    def _switch_player(self) -> Player:
        """
        Switches the active player to the next player in the game.

        This method changes the current player to the other player. It's used to alternate turns between the players.
        If the current player is the first player in the list, it switches to the second, and vice versa.

        Postconditions:
            - The `_player` attribute is updated to reference the next player.
        Returns:
            - (Player): Return sthe new player
        """
        next_player: Player = (
            self._players[1]
            if self._player.identifier == self._players[0].identifier
            else self._players[0]
        )
        self._player: Player = next_player
        return self._player

    def __str__(self) -> str:
        """
        Provides a string representation of the game's current state.

        This representation includes whether the game has terminated and the current state of the game board.
        If the game has terminated, it also displays the winner.

        Returns:
            str: A string describing the current state of the game, including termination status and the game board.
        """

        has_game_terminated: bool = self._termination_state is not None

        termination_info: str = ""
        if has_game_terminated:
            if self._termination_state == TerminationStateEnum.Tie:
                termination_info: str = "It is a tie!"
            else:
                termination_info = f"The winner is Player {self._player.identifier} ({self._player.symbol})"
        return (
            f"Game has terminated: {has_game_terminated}\n"
            f"Board State:\n{self._board}\n"
            f"{termination_info}"
        )
