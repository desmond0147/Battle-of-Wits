from random import randint
import os


def clearConsole():
    """Clears the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')


class Board:
    def __init__(self, size, num_ships, player_name, is_computer=False):
        """Initializes the board for the player or computer."""
        self.size = size
        self.num_ships = num_ships
        self.player_name = player_name
        self.is_computer = is_computer
        self.board = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = set()
        self.guesses = set()  # Track guesses to prevent repetition

    def place_ships(self):
        """Randomly places ships on the board without excessive checks."""
        while len(self.ships) < self.num_ships:
            row, col = randint(0, self.size - 1), randint(0, self.size - 1)
            self.ships.add((row, col))
            self.board[row][col] = 'S' if not self.is_computer else '~'

    def print_board(self, hide_ships=False):
        """Prints the current state of the board."""
        print(f"{self.player_name}'s Board:")
        for row in self.board:
            print(' '.join(
                '~' if hide_ships and cell == 'S' else cell for cell in row
            ))

    def make_guess(self, row, col):
        """Processes a guess on the board."""
        if (row, col) in self.guesses:
            return False, "Already guessed."
        self.guesses.add((row, col))
        if (row, col) in self.ships:
            self.board[row][col] = 'H'
            return True, "Hit!"
        else:
            self.board[row][col] = 'O'
            return False, "Miss."


def get_valid_guess(prompt):
    """Prompts the player for a valid guess."""
    while True:
        try:
            guess = input(prompt).strip()
            if len(guess) != 1 or not guess.isdigit():
                raise ValueError(
                    "Please enter a single digit between 0 and 4."
                )
            guess = int(guess)
            if guess not in range(5):
                raise ValueError(
                    "Input out of range. Enter numbers between 0 and 4."
                )
            return guess
        except ValueError as e:
            print(f"Invalid input: {e}. Try again.")


def get_valid_name():
    """Prompts the player for a valid name."""
    while True:
        player_name = input("Please enter your name:\n").strip()
        if len(player_name) > 1 and player_name.isalpha():
            return player_name
        print("Invalid name. Enter a valid name with more than one character.")


def display_instructions():
    """Displays the game instructions."""
    print("\nWelcome to ULTIMATE BATTLESHIPS!!")
    print("Objective: Sink all of the computer's ships before it sinks yours!")
    print("How to Play:")
    print("1. The game is played on a 5x5 grid.")
    print("2. You and the computer will each have 3 ships hidden on the grid.")
    print(
        "3. Each round, you will guess a row and a column to try and hit "
        "the computer's ships."
    )
    print("4. The computer will also guess to try and hit your ships.")
    print(
        "5. The game lasts for 6 rounds. "
        "The player with the most hits wins!"
    )
    print(
        "6. A 'H' marks a hit, 'O' marks a miss, and 'S' shows your ships "
        "on your board."
    )
    print(
        "7. When prompted, enter your name and follow the instructions to "
        "make your guesses."
    )
    print("Good luck!\n")


def main_game():
    """Begins the main game loop."""
    display_instructions()
    player_name = get_valid_name()
    clearConsole()

    player_board = Board(size=5, num_ships=3, player_name=player_name)
    computer_board = Board(
        size=5, num_ships=3, player_name="Computer", is_computer=True
    )
    player_board.place_ships()
    computer_board.place_ships()

    # Initialize scores
    scores = {"computer": 0, "player": 0}

    for round_num in range(6):  # Adjusted to 6 rounds
        print(f"\n--- Round {round_num + 1} ---")
        player_board.print_board()
        computer_board.print_board(hide_ships=True)

        # Player's guess
        while True:
            guess_row = get_valid_guess(
                "Enter a row to guess (enter a single digit between 0 and 4): "
            )
            guess_col = get_valid_guess(
             "Enter a column to guess (enter a single digit between 0 and 4): "
            )

            clearConsole()
            hit, message = computer_board.make_guess(guess_row, guess_col)
            print(message)

            # Only break the loop if the guess is valid
            if message != "Already guessed.":
                if hit:
                    scores["player"] += 1
                break  # Exit the loop if the guess is valid

        # Computer's guess
        while True:
            comp_guess_row, comp_guess_col = randint(0, 4), randint(0, 4)
            if (comp_guess_row, comp_guess_col) not in computer_board.guesses:
                hit, message = player_board.make_guess(comp_guess_row,
                                                       comp_guess_col)
                print(
                    f"Computer's guess at ({comp_guess_row}, "
                    f"{comp_guess_col}): {message}"
                )
                if hit:
                    scores["computer"] += 1
                break  # Exit the loop after a valid guess

    print("\nFinal Scores:")
    print(f"{player_name}: {scores['player']}")
    print(f"Computer: {scores['computer']}")

    if scores["player"] > scores["computer"]:
        print(f"{player_name} wins!")
    elif scores["computer"] > scores["player"]:
        print("Computer wins!")
    else:
        print("It's a tie!")

    print("\nGame Over! Thanks for playing.")
    play_again()


def play_again():
    """Asks the player if they want to play again."""
    while True:
        choice = (
            input("Would you like to play again? (yes/no):\n")
            .strip()
            .lower()
        )
        if choice == 'yes':
            clearConsole()
            main_game()
            break
        elif choice == 'no':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main_game()