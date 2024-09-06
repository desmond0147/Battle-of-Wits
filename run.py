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