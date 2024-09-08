from random import randint


class Board:
    def __init__(self, size, num_ships, player_name, is_computer=False):
        self.size = size
        self.num_ships = num_ships
        self.player_name = player_name
        self.is_computer = is_computer
        self.board = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = set()
        self.guesses = set()  # Track guesses to prevent repetition

    def place_ships(self):
        while len(self.ships) < self.num_ships:
            row, col = randint(0, self.size - 1), randint(0, self.size - 1)
            if (row, col) not in self.ships:
                self.ships.add((row, col))
                if not self.is_computer:  # Show ships only on player's board
                    self.board[row][col] = 'S'

    def print_board(self, hide_ships=False):
        print(f"{self.player_name}'s Board:")
        for row in range(self.size):
            print(' '.join(
                '~' if hide_ships and self.board[row][col] == 'S'
                else self.board[row][col]
                for col in range(self.size)
            ))

    def make_guess(self, row, col):
        if (row, col) in self.guesses:
            raise ValueError(
                "You've already guessed that. Try a different number."
            )
        self.guesses.add((row, col))
        if (row, col) in self.ships:
            self.board[row][col] = 'H'
            return True
        else:
            self.board[row][col] = 'O'
            return False


# Initialize scores
scores = {"computer": 0, "player": 0}


def get_valid_guess(prompt, board):
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
            if guess in board.guesses:
                raise ValueError(
                    "You've already guessed that. Try a different number."
                )
            return guess
        except ValueError as e:
            print(f"Invalid input: {e}. Try again.")


def get_valid_name():
    while True:
        player_name = input("Please enter your name:\n ").strip()
        if len(player_name) > 1 and player_name.isalpha():
            return player_name
        print(
            "Invalid name. Enter a valid name with more than one character."
        )


def main_game():
    print("Welcome to ULTIMATE BATTLESHIPS!!")
    player_name = get_valid_name()
    player_board = Board(size=5, num_ships=3, player_name=player_name)
    computer_board = Board(
        size=5, num_ships=3, player_name="Computer", is_computer=True
    )
    player_board.place_ships()
    computer_board.place_ships()

    for round_num in range(4):  # Shortened the game to 4 rounds
        print(f"\n--- Round {round_num + 1} ---")
        player_board.print_board()
        computer_board.print_board(hide_ships=True)

        # Player's guess
        guess_row = get_valid_guess(
            "Enter a row to guess (0-4): ", player_board
        )
        guess_col = get_valid_guess(
            "Enter a column to guess (0-4): ", player_board
        )

        try:
            if computer_board.make_guess(guess_row, guess_col):
                print("You hit a ship!")
                scores["player"] += 1
            else:
                print("You missed.")
        except ValueError as e:
            print(e)

        # Computer's guess
        while True:
            try:
                comp_guess_row = randint(0, 4)
                comp_guess_col = randint(0, 4)
                if not player_board.make_guess(
                    comp_guess_row, comp_guess_col
                ):
                    print(
                        "Computer missed at "
                        f"({comp_guess_row}, {comp_guess_col})."
                    )
                else:
                    print(
                        "Computer hit a ship at "
                        f"({comp_guess_row}, {comp_guess_col})!"
                    )
                    scores["computer"] += 1
                break
            except ValueError:
                # The computer guessed a previously guessed spot; try again
                continue

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


if __name__ == "__main__":
    main_game()