from random import randint

class Board:
    """
    Main board class. Sets the size, the number of ships, the player's name,
    and the board type (player board or computer). Has methods for adding ships,
    handling guesses, and printing the board.
    """
    def __init__(self, size, num_ships, player_name, is_computer=False):
        self.size = size
        self.num_ships = num_ships
        self.player_name = player_name
        self.is_computer = is_computer
        self.board = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = set()

    def place_ships(self):
        """
        Randomly place ships on the board.
        """
        while len(self.ships) < self.num_ships:
            row, col = randint(0, self.size - 1), randint(0, self.size - 1)
            if (row, col) not in self.ships:
                self.ships.add((row, col))
                self.board[row][col] = 'S'
    
    def print_board(self, hide_ships=False):
        """
        Print the board to the console. Optionally hide ships.
        """
        print(f"{self.player_name}'s Board:")
        for row in range(self.size):
            print(' '.join(
                ' ' if hide_ships and self.board[row][col] == 'S' else self.board[row][col]
                for col in range(self.size)
            ))

    # Initialize scores
scores = {"computer": 0, "player": 0}

def get_valid_guess(prompt):
    """
    Prompt the user for a guess and validate it.
    """
    while True:
        try:
            guess = input(prompt)
            guess = int(guess)
            if guess not in range(5):
                raise ValueError("Input out of range. Please enter numbers between 0 and 4.")
            return guess
        except ValueError as e:
            print(f"Invalid input: {e}. Try again.")

def main_game():
    """
    Main game function. Handles the setup of the game, player interactions, 
    and keeps track of scores. The game runs for a specified number of rounds.
    """
    print("Welcome to ULTIMATE BATTLESHIPS!!")
    
    player_name = input("Please enter your name: ")
    player_board = Board(size=5, num_ships=4, player_name=player_name)
    computer_board = Board(size=5, num_ships=4, player_name="Computer", is_computer=True)
    
    player_board.place_ships()
    computer_board.place_ships()
    
    for round_num in range(6):
        print(f"\n--- Round {round_num + 1} ---")
        
        player_board.print_board()
        computer_board.print_board(hide_ships=True)  # Hide computer's ships