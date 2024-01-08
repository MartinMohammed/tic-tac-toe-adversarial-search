from typing import Optional, List, Union, Tuple, Any, Callable
from models.mini_max import MiniMax
from models.node import Node
from models.grid_location import GridLocation
from enums.mini_max_objective import MiniMaxObjective
from enums.termination_state import TerminationState
import random 

class TicTacToe:
    """
    Represents a TicTacToe game with functionalities to manage the game TerminationState, 
    perform moves, and check game status.

    Attributes:
        _play_with_adversarial_search (bool): Whether to play with adversarial search.
        _players (List[str]): List of player symbols.
        _plays (int): Number of plays made in the game.
        _player (str): The current player.
        _initial_player (str): The initial player. Reset to this player if game restarts and no player switch.
        _grid (List[List[str]]): The game board.
        _termination_state (Union[None, TerminationState]): The termination of the game if it has ended.
        _mini_max: (MiniMax[TicTacToe, GridLocation]): MiniMax instance for adversarial search.
    """

    def __init__(self,
                 play_with_adversarial_search: bool = False, 
                 players: Optional[List[str]] = None, 
                 initial_player: Optional[str] = None, 
                 initial_grid: Optional[List[List[str]]] = None,
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
        self._quiet = kwargs.get('quiet', True)  # Example of handling a 'quiet' keyword argument
        self._play_with_adversarial_search: bool = play_with_adversarial_search
        self._mini_max: Optional[MiniMax[TicTacToe, GridLocation]] = None
        
        if players is None:
            players: List[str] = ["x", "o"]
        if initial_player is None:
            initial_player: str = random.choice(players)

        # Needed when restarting the game and resetting current player
        self._initial_player: str = initial_player

        if len(players) != 2:
            raise ValueError("The number of players must be exactly 2.")
        if initial_player not in players:
            raise ValueError("The initial player must be one of the players.")
        
        self._players: List[str] = players
        self._player: str = initial_player

        if initial_grid is None:
            self._grid: List[List[str]] = [["" for _ in range(3)] for _ in range(3)]
            self._plays: int = 0
            self._termination_state: Union[None, TerminationState] = None
        else:
            self._grid: List[List[str]] = initial_grid
            # The number of plays is the number of fields that are not available.
            self._plays: int = sum(cell != "" for row in self._grid for cell in row)
            self._termination_state: Union[None, TerminationState] = self._get_termination_state()

    def start(self) -> None:
        print("The game begins: ")
        if not self._quiet:
            self.show_game()
        # Game is initialized, ready to make first step if Player 2 has first move and play_with_adversarial_search = True
        if self._play_with_adversarial_search and self.identify_player(self._initial_player) == 2:
            self.adversarial_move(make_move=True)

    @property
    def plays(self) -> int:
        """
        Retrieves the number of plays made so far in the game.

        Returns:
            int: The total number of plays made.
        """
        return self._plays

    @property
    def player(self) -> str:
        """
        Gets the current player's symbol.

        Returns:
            str: The symbol of the current player.
        """
        return self._player

    @property
    def players(self) -> List[str]:
        """
        Retrieves the list of player symbols.
        
        Returns:
            List[str]: The symbols of the players.
        """
        return self._players

    @property
    def termination_state(self) -> Union[None, TerminationState]:
        """
        Retrieves the current termination state of the game.

        Returns:
            Union[None, TerminationState]: Termination State of the game. 
        """
        return self._termination_state


    @staticmethod
    def utility(instance) -> Union[None, TerminationState]:
        """
        Determines the utility of the game if it has reached a terminal state.
        """
        return instance.termination_state
            
        
    @staticmethod
    def result(instance, gl: GridLocation):
        """
        Predicts the game state resulting from making a move at the specified location.
        """
        copy = instance._copy_game()    
        copy.next_turn(gl)
        return copy
        

    @staticmethod
    def actions(instance) -> List[GridLocation]:
        """
        Provides a list of all possible legal moves in the current game state.
        """
        return [GridLocation(row=row, column=column) for column in range(3) for row in range(3) if instance._grid[row][column] == ""]

    @staticmethod
    def terminal(instance) -> bool:
        """
        Checks if the current game state is terminal.
        """
        return instance.termination_state != None

    def next_turn(self, gl: GridLocation) -> None:
        """
        Processes the next turn in the game at the specified grid location.
    
        Args:
            gl (GridLocation): The location where the next move is made.
        """
        if self._termination_state is not None:
            if not self._quiet:
                print("The game has ended. Please restart the game.")
            return
    
        if not self._check_valid_move(gl):
            print(f"The specified move {gl} is not valid. Please try again.")
            return
    
        # Make the move
        self._plays += 1
        row, column = gl.row, gl.column
        self._grid[row][column] = self._player

        winner: Optional[TerminationState] = self._get_termination_state(); 
        
        # Game has not ended yet.
        if winner is None:
            self._switch_player()
        else:
            # The game terminated.
            self._termination_state = winner
            
        if not self._quiet:
            self.show_game()
        
        if self._play_with_adversarial_search and self.identify_player(self.player) == 2 and self._termination_state is None:
            self.adversarial_move(make_move=True)
            
    def empty_spaces(self) -> None:
        """
        Resets the game board, clearing all occupied spaces.
        """
        self._grid: List[List[str]] = [["" for _ in range(3)] for _ in range(3)]
    
    def new_game(self, change_players: bool = False) -> None:
        """
        Starts a new game, optionally switching the starting player.

        Args:
            change_players (bool): Whether to switch the starting player for the new game.
        """
        self.empty_spaces()
        self._plays: int = 0
        self._termination_state: Union[None, TerminationState] = None
        self._player = self._initial_player
        if change_players:
            self._switch_player()

        if self._play_with_adversarial_search:
            # A new instace for the minimax object since the current state has been reseted.
            self._mini_max = MiniMax[TicTacToe, GridLocation] = MiniMax(initial_node=Node(state=self, parent=None, action=None), initial_objective=MiniMaxObjective.MAX, terminal=TicTacToe.terminal, utility=TicTacToe.utility, result=TicTacToe.result, actions=TicTacToe.actions)

        if not self._quiet:
            self.show_game()
        
    def show_game(self) -> None:
        """
        Displays the current state of the game board to the console.
        This includes showing who's turn it is, the winner, or if the game is a tie.
        """
        if self._termination_state == TerminationState.PlayerOneWon:
            winner = "Player 1"
        elif self._termination_state == TerminationState.PlayerTwoWon:
            winner = "Player 2"
        else:
            winner = None
    
        # Display the winner if there is one
        if winner:
            print(f"{winner} wins!")
        # Check for a tie
        elif self._plays == 9:  # Assuming _plays keeps track of the number of moves
            print("Tie!")
        # Otherwise, it's the next player's turn
        else:
            current_player = self.identify_player(self.player)
            print(f"Player {current_player}'s ({self.player}) turn")
    
        # Display the current board
        print(self)
        

    def adversarial_move(self, make_move=False) -> Tuple[int, Node[Any, GridLocation]]:
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
        self._mini_max = MiniMax[TicTacToe, GridLocation](initial_node=Node(state=self, parent=None, action=None), initial_objective=MiniMaxObjective.MAX, terminal=TicTacToe.terminal, utility=TicTacToe.utility, result=TicTacToe.result, actions=TicTacToe.actions)
    
        score, next_node = self._mini_max.start_mini_max()
        if make_move:
            self.next_turn(next_node.action)
        return (score, next_node)


        
    def _get_termination_state(self) -> Union[None, TerminationState]:
        """
        Determines whether there is a winner, looser or if there is a tie in the current state.
        """
        winner: Optional[str] = None

        determine_winner_state: Callable[[Optional[str]], TerminationState] = lambda winner: TerminationState.PlayerOneWon if self.identify_player(winner) == 1 else TerminationState.PlayerTwoWon
        for i in range(3):
            # Check for horizontal and vertical win
            if self._grid[i][0] == self._grid[i][1] == self._grid[i][2] != "":
                winner = self._grid[i][0]
            elif self._grid[0][i] == self._grid[1][i] == self._grid[2][i] != "":
                winner = self._grid[0][i]
    
            if winner:
                return determine_winner_state(winner)
        # Check for diagonal win
        if self._grid[0][0] == self._grid[1][1] == self._grid[2][2] != "":
            winner = self._grid[0][0]
        elif self._grid[0][2] == self._grid[1][1] == self._grid[2][0] != "":
            winner = self._grid[0][2]
        
        if winner:
            return determine_winner_state(winner)
        # Check for tie
        if self._plays == 9:
            return TerminationState.Tie
        # Game has not terminated yet. 
        return None

    def identify_player(self, player: str) -> Optional[int]:
        """
        Determines the numerical identifier of the current player based on their symbol.
    
        The method checks against the symbols provided in the self.players list, where the first 
        item represents the first player and the second item the second player. 
    
        Returns:
        - 1 if the player is the first player.
        - 2 if the player is the second player.
        - None if the player symbol is not recognized as a valid player.
    
        Parameters:
        - player: The symbol representing the player to identify.
        """
        if player not in self.players:
            print(f"{player} is not a valid player.")
            return None
        if player == self.players[0]:
            return 1
        return 2


    def _check_valid_move(self, gl: GridLocation) -> bool:
        """Determines whether a given move is valid. Not out of bounds, and the field is not occupied: """
        if self._check_out_of_boundary(gl) or self._is_location_occupied(gl):
            return False
        return True

    def _check_out_of_boundary(self, gl: GridLocation) -> bool:
        """
        Checks if the specified grid location is out of the game board's boundaries.

        Args:
            gl (GridLocation): The grid location to check.

        Returns:
            bool: True if the location is out of bounds, False otherwise.
        """
        row, column = gl.row, gl.column
        return not (0 <= row <= 2 and 0 <= column <= 2)
    
    def _is_location_occupied(self, gl: GridLocation) -> bool:
        """
        Determines if the specified grid location is already occupied.

        Args:
            gl (GridLocation): The grid location to check.

        Returns:
            bool: True if the location is occupied, False if it is free.
        """
        assert not self._check_out_of_boundary(gl), f"The specified GridLocation is out of bounds: {gl}"
        row, column = gl.row, gl.column
        return self._grid[row][column] != ""
    
    def _copy_game(self):
        """
        Creates a deep copy of the current TicTacToe game instance.

        Returns:
            TicTacToe: A new instance of TicTacToe with the same TerminationState as the current game.
        """
        # Make deep copy of grid so that they do not share the same reference to the underlying grid)
        return TicTacToe(players=self._players, initial_player=self._player, initial_grid=self._copy_grid(), play_with_adversarial_search=self._play_with_adversarial_search)
        
    def _copy_grid(self) -> List[List[str]]:
        """
        Creates a deep copy of the game grid.

        Returns:
            List[List[str]]: A deep copy of the game grid.
        """
        return [[self._grid[row][col] for col in range(3)] for row in range(3)]

    def _switch_player(self) -> None:
        """
        Switches the turn to the other player.
        """
        self._player: str = self._players[1] if self._player == self._players[0] else self._players[0]
        
    def __str__(self) -> str:
        """
        Provides a string representation of the game board.

        Returns:
            str: The string representation of the current TerminationState of the game board.
        """
        return "\n".join([" ".join([cell if cell else '.' for cell in row]) for row in self._grid])