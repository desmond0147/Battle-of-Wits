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