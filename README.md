# Tic-Tac-Toe with Adversarial Search

## Current State and next steps: 

![current state and next steps of the application](./images/current-state-and-next-steps.png)

## Overview
This Tic-Tac-Toe game presents an enhanced challenge by incorporating advanced AI techniques for player two. Unlike traditional Tic-Tac-Toe games, this version employs adversarial search, specifically the MiniMax algorithm, to create a formidable opponent in player two (O), playing against player one (X).

![key characteristics of this application](./images/key-characteristics.png)

## Features
- **Two Player Modes**: 
  - Player One (X) is controlled by a human player.
  - Player Two (O) is powered by an AI using the MiniMax algorithm.
- **Adversarial Search**: 
  - The game employs a sophisticated adversarial search technique to calculate the best moves for player two.
  - This approach simulates a player that anticipates and counters the human player's moves effectively.

## MiniMax Algorithm
The core of the AI player (player two) is the MiniMax algorithm. This algorithm explores all possible moves in the game, anticipating the opponent's responses to these moves. It then selects the move that maximizes the potential benefit while minimizing the potential losses, assuming the opponent is also playing optimally.

### How MiniMax Works in Tic-Tac-Toe
- The MiniMax algorithm evaluates the game's state to determine the best possible move for player two.
- It recursively explores all possible future game states, considering the moves of both players.
- At each step, it calculates a score representing the desirability of that state, with the goal of maximizing player two's chances of winning while minimizing the chances of losing.
- The algorithm chooses the move that leads to the game state with the highest score from player two's perspective.

![illustration of how the mini-max algorithm works](./images/mini-max-algorith-demo.png)

## Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.8 or higher**: Check your Python version by running `python3 --version` in your terminal. If you don't have Python installed, or if your version is below 3.8, visit [Python's official site](https://www.python.org/downloads/) for installation instructions.
- **pip (Python Package Installer)**: Typically installed with Python. Run `pip --version` to check. If it's not installed, or if you need to upgrade, follow the instructions on [pip's official website](https://pip.pypa.io/en/stable/installing/).

### Installation and Running the Game
1. **Clone or Download the Repository**:
   - Clone the repo using `git clone [repository URL]`, or download the ZIP file and extract it.
2. **Install Required Packages**:
   - Navigate to the project directory in your terminal.
   - Run `pip install -r requirements.txt` to install the necessary Python packages.
3. **Start the Game**:
   - Within the project directory, start the game by running `python3 main.py`.
   - Ensure you're in the correct directory by using `ls | grep main.py`. If there's no output, navigate to the directory containing `main.py`.
4. **Play the Game**:
   - Once the game starts, you'll play as Player One (X).
   - Player Two (O), controlled by the AI, will respond automatically.

### Troubleshooting Common Issues
- **Python Version**: If you encounter issues related to Python version, verify that you're using Python 3.8 or higher.
- **Package Installation**: In case of errors during package installation, ensure your pip is up to date. You might also need administrator privileges (try adding `sudo` before the pip command on macOS/Linux).
- **Running the Game**: If the game doesn't start, double-check you're in the correct directory and that `main.py` exists.

Enjoy the enhanced Tic-Tac-Toe experience with the added complexity of an AI opponent using adversarial search!