from random import randint
import os


def clear_console():
    """
    Clears the console output.
    This function clears the terminal screen to improve the user experience
    by removing previous outputs and presenting a clean interface.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class Board:
    def __init__(self, size, num_ships, player_name, is_computer=False):
        """
        Initializes the board for the player or computer.

        Args:
            size (int): The size of the board (NxN grid).
            num_ships (int): The number of ships to be placed on the board.
            player_name (str): The name of the player.
            is_computer (bool): A flag to indicate if the board belongs to the computer.
        """
        self.size = size
        self.num_ships = num_ships
        self.player_name = player_name
        self.is_computer = is_computer
        self.board = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = set()
        self.guesses = set()  # Track guesses to prevent repetition

    def place_ships(self):
        """
        Randomly places ships on the board.

        Ships are placed at random positions on the board. If the board belongs
        to the player, the ships are displayed. If it belongs to the computer,
        the ships are hidden.
        """
        while len(self.ships) < self.num_ships:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            if (row, col) not in self.ships:
                self.ships.add((row, col))
                if not self.is_computer:  # Show ships only on player's board
                    self.board[row][col] = 'S'

    def print_board(self, hide_ships=False):
        """
        Prints the current state of the board.

        Args:
            hide_ships (bool): If True, hides the ships from the display
                (used for computer's board).
        """
        print(f"{self.player_name}'s Board:")
        header = '  ' + ' '.join(str(i) for i in range(self.size))
        print(header)
        for idx, row in enumerate(self.board):
            display_row = []
            for col in range(self.size):
                cell = row[col]
                if hide_ships and cell == 'S':
                    display_row.append('~')
                else:
                    display_row.append(cell)
            print(f"{idx} " + ' '.join(display_row))
        print()  # Add an empty line for better readability

    def make_guess(self, row, col):
        """
        Processes a guess on the board.

        Args:
            row (int): The row number of the guess.
            col (int): The column number of the guess.

        Returns:
            bool: True if the guess hits a ship, False otherwise.

        Raises:
            ValueError: If the guess has already been made.
        """
        if (row, col) in self.guesses:
            raise ValueError("This coordinate has already been guessed.")
        
        self.guesses.add((row, col))
        if (row, col) in self.ships:
            self.board[row][col] = 'H'
            return True
        else:
            self.board[row][col] = 'O'
            return False


def get_valid_guess(prompt, board):
    """
    Prompts the player for a valid guess.

    Args:
        prompt (str): The message to prompt the user.
        board (Board): The current player's board.

    Returns:
        tuple: A valid guess as (row, column).
    """
    while True:
        try:
            guess = input(prompt).strip().split(',')
            if len(guess) != 2:
                raise ValueError("Please enter two digits separated by a comma (e.g., 1,3).")
            row, col = guess
            if not (row.isdigit() and col.isdigit()):
                raise ValueError("Both row and column must be digits.")
            row, col = int(row), int(col)
            if not (0 <= row < board.size and 0 <= col < board.size):
                raise ValueError(
                    f"Coordinates out of range. Enter numbers between 0 and {board.size - 1}."
                )
            if (row, col) in board.guesses:
                raise ValueError("You have already guessed this coordinate. Try a different one.")
            return row, col
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.\n")


def get_valid_name():
    """
    Prompts the player for a valid name.

    Returns:
        str: A valid player name (more than one character and alphabetic).
    """
    while True:
        player_name = input("Please enter your name:\n").strip()
        if len(player_name) > 1 and player_name.replace(" ", "").isalpha():
            return player_name
        print("Invalid name. Enter a valid name with more than one character and alphabetic characters only.\n")


def display_instructions():
    """
    Displays the game instructions.

    Provides an overview of how to play ULTIMATE BATTLESHIPS, including the
    objective, game mechanics, and how to input guesses.
    """
    print("\n=== Welcome to ULTIMATE BATTLESHIPS ===\n")
    print("How to Play:")
    print("1. The game is played on a 5x5 grid.")
    print("2. You and the computer will each have 3 ships hidden on the grid.")
    print("3. Each round, you will guess a row and a column to try and hit the computer's ships.")
    print("4. The computer will also guess to try and hit your ships.")
    print("5. The game lasts for 6 rounds. The player with the most hits wins!")
    print("6. A 'H' marks a hit, 'O' marks a miss, and 'S' shows your ships on your board.")
    print("7. When prompted, enter your name and follow the instructions to make your guesses.")
    print("8. Coordinates should be entered in the format 'row,column' (e.g., 2,3).\n")
    print("Good luck!\n")


def main_game():
    """
    Begins the main game loop.

    This function initializes the game, sets up the boards, and handles
    the rounds where the player and computer take turns guessing. At the end
    of the game, the scores are displayed, and the player is asked if they
    want to play again.
    """
    display_instructions()
    player_name = get_valid_name()
    clear_console()

    player_board = Board(size=5, num_ships=3, player_name=player_name)
    computer_board = Board(size=5, num_ships=3, player_name="Computer", is_computer=True)
    player_board.place_ships()
    computer_board.place_ships()

    # Initialize scores
    scores = {"computer": 0, "player": 0}

    for round_num in range(1, 7):  # 6 rounds
        print(f"\n--- Round {round_num} ---")
        player_board.print_board()
        computer_board.print_board(hide_ships=True)

        # Player's guess
        guess_prompt = "Enter your guess as 'row,column' (e.g., 1,3): "
        guess_row, guess_col = get_valid_guess(guess_prompt, computer_board)

        try:
            if computer_board.make_guess(guess_row, guess_col):
                print(f"Hit! You hit a ship at ({guess_row}, {guess_col}).")
                scores["player"] += 1
            else:
                print(f"Missed at ({guess_row}, {guess_col}).")
        except ValueError as e:
            print(e)

        # Computer's guess
        while True:
            comp_guess_row = randint(0, 4)
            comp_guess_col = randint(0, 4)
            if (comp_guess_row, comp_guess_col) not in player_board.guesses:
                try:
                    if player_board.make_guess(comp_guess_row, comp_guess_col):
                        print(f"Computer hit your ship at ({comp_guess_row}, {comp_guess_col})!")
                        scores["computer"] += 1
                    else:
                        print(f"Computer missed at ({comp_guess_row}, {comp_guess_col}).")
                except ValueError:
                    # This should not happen as we check for repeated guesses
                    pass
                break  # Exit the loop after a successful guess

        clear_console()

    # Final Scores
    print("\n=== Final Scores ===")
    print(f"{player_name}: {scores['player']}")
    print(f"Computer: {scores['computer']}\n")

    # Determine Winner
    if scores["player"] > scores["computer"]:
        print(f"Congratulations, {player_name}! You win!")
    elif scores["player"] < scores["computer"]:
        print("The computer wins! Better luck next time.")
    else:
        print("It's a tie!")

    # Ask to play again
    while True:
        play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if play_again in ('yes', 'no'):
            break
        print("Invalid input. Please enter 'yes' or 'no'.")
    
    if play_again == 'yes':
        clear_console()
        main_game()


if __name__ == "__main__":
    main_game()
