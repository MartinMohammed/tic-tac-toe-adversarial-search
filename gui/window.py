from tkinter import Button, Tk, Frame, Label
from models.tic_tac_toe import TicTacToe
from models.grid_location import GridLocation
from gui.helpers.next_turn import next_turn
from gui.helpers.restart_game import restart_game
from shared.constants import FONT


def construct_window_and_game(game: TicTacToe) -> Tk:
    # Initialize the main window for the game
    window = Tk()
    window.title("Tic-Tac-Toe")

    # Initialize a label to display whose turn it is
    label = Label(window, text=f"{game.player}'s turn", font=(FONT, 40))
    label.pack(side="top")

    # Define a function to update the label and restart the game
    def restart_game_and_update_label(game: TicTacToe):
        restart_game(game, buttons, label)
        label.config(text=f"{game.player}'s turn")

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
        [None for _ in range(3)] for _ in range(3)
    ]  # Create a 3x3 matrix of None

    for row in range(3):
        for column in range(3):
            # Function to handle button click, captures current row and column
            def handle_button_click(r=row, c=column):
                next_turn(
                    game,
                    GridLocation(r, c),
                    buttons,
                    label,
                    play_with_adversarial_search=True,
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
