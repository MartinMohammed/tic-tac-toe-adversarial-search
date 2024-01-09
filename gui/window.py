from tkinter import Button, Tk, Frame, Label
from models.game import Game
from models.grid_location import GridLocation
from shared.constants import ROWS, COLUMNS, FONT
from gui.helpers.next_turn import next_turn
from gui.helpers.restart_game import restart_game


def construct_window_and_game(
    game: Game, play_with_adversarial_search: bool = False
) -> Tk:
    # Initialize the main window for the game
    window = Tk()
    window.title("Tic-Tac-Toe")

    # Initialize a label to display whose turn it is
    label = Label(
        window,
        text=f"Player {game.player.identifier} ({game.player.symbol}) is next.",
        font=(FONT, 40),
    )
    label.pack(side="top")

    # Define a function to update the label and restart the game
    def restart_game_and_update_label(game: Game):
        restart_game(game, buttons, label)
        label.config(
            text=f"Player {game.player.identifier} ({game.player.symbol}) is next."
        )

    # Define a button to reset the game, linking it to the 'restart_game_and_update_label' function
    reset_button = Button(
        window,
        text="Restart",
        font=(FONT, 20),
        command=lambda: restart_game_and_update_label(game),
    )
    reset_button.pack(side="top")

    # Create a frame to contain the Tic-Tac-Toe grid buttons
    frame = Frame(window)
    frame.pack()

    # Create and place buttons in a 3x3 grid inside the frame
    buttons = [
        [None for _ in range(COLUMNS)] for _ in range(ROWS)
    ]  # Create a 3x3 matrix of None

    for row in range(ROWS):
        for column in range(COLUMNS):
            # Function to handle button click, captures current row and column
            def handle_button_click(r=row, c=column):
                next_turn(
                    game=game,
                    gl=GridLocation(r, c),
                    buttons=buttons,
                    label=label,
                    play_with_adversarial_search=play_with_adversarial_search,
                )

            # Initialize each button and set its action
            buttons[row][column] = Button(
                frame,
                text="",
                font=(FONT, 40),
                width=5,
                height=2,
                command=handle_button_click,
            )
            buttons[row][column].grid(row=row, column=column)
    return window
