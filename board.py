import os


class Ship:
    def __init__(self, size, direction, row, col):
        """Initialize the ship with its size, direction, starting row and column."""
        self.size = size
        self.direction = direction.upper()
        self.row = row
        self.col = col
        self.direction_map = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
        
        if self.direction not in self.direction_map:
            raise ValueError("Invalid direction. Use 'N', 'S', 'E', or 'W'.")
        
        self.cells = set(self._init_cells())
        self.hits = [False] * size

    def hit(self, row, col):
        """Register a hit if the ship occupies the cell (row, col)."""
        if (row, col) in self.cells:
            index = list(self.cells).index((row, col))
            self.hits[index] = True
            return True
        return False

    def is_sunk(self):
        """Check if all parts of the ship have been hit."""
        return all(self.hits)

    def _init_cells(self):
        """Generate cells occupied by the ship based on size and direction."""
        cells = []
        d_row, d_col = self.direction_map[self.direction]
        for i in range(self.size):
            cells.append((self.row + d_row * i, self.col + d_col * i))
        return cells


class Board:
    def __init__(self, size=9):
        """Initialize a size x size board with placeholder values (0)."""
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.ships = []

    def update_cell(self, row, col, value):
        """Update the cell at (row, col) with the given value."""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = value
        else:
            print("Invalid coordinates. Out of bounds.")

    def get_cell(self, row, col):
        """Retrieve the value of the cell at (row, col)."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        print("Invalid coordinates. Out of bounds.")
        return None

    def display(self):
        """Display the board in a readable format with column and row labels."""
        headers = "    " + "   ".join(chr(65 + i) for i in range(self.size))
        separator = "  " + "+---" * self.size + "+"
        
        print(headers)
        print(separator)
        for i, row in enumerate(self.board):
            row_content = " | ".join(str(cell) for cell in row)
            print(f"{i + 1:<2} | {row_content} |")
            print(separator)

    def add_ship(self, row, col, size, direction):
        """Attempt to place a ship on the board, checking bounds and overlap."""
        ship = Ship(size, direction, row, col)
        
        # Validate placement
        if not self._is_within_bounds(ship):
            print("Invalid ship placement. Ship is out of bounds.")
            return False
        
        if self._has_overlap(ship):
            print("Invalid ship placement. Ships overlap.")
            return False

        # Place ship if valid
        self.ships.append(ship)
        for cell in ship.cells:
            self.update_cell(*cell, 1)
        return True

    def _is_within_bounds(self, ship):
        """Check if all ship cells are within board boundaries."""
        for row, col in ship.cells:
            if not (0 <= row < self.size and 0 <= col < self.size):
                return False
        return True

    def _has_overlap(self, ship):
        """Check if any cell of the ship overlaps with existing ships on the board."""
        for row, col in ship.cells:
            if self.get_cell(row, col) == 1:
                return True
        return False

    def hit(self, row, col):
        """Attempt to hit a cell on the board; update and report hit or miss."""
        for ship in self.ships:
            if ship.hit(row, col):
                self.update_cell(row, col, "X")
                print("Hit!")
                if ship.is_sunk():
                    print("You sunk a ship!")
                return True
        self.update_cell(row, col, "O")
        print("Miss!")
        return False

    def is_game_over(self):
        """Determine if all ships are sunk, indicating game over."""
        return all(ship.is_sunk() for ship in self.ships)



def display_boards_side_by_side(board1, board2):
    # Display two boards side by side
    horizontal_border = "+---" * board1.size + "+"
    column_headers = "    A   B   C   D   E   F   G   H   I"

    # Print the headers
    print(f"{column_headers}          {column_headers}")
    print(f"  {horizontal_border}          {horizontal_border}")

    # Print each row from both boards side by side
    for i in range(board1.size):
        row1 = board1.display_row(i)
        row2 = board2.display_row(i)
        print(f"{row1}        {row2}")
        print(f"  {horizontal_border}          {horizontal_border}")


def clear_screen():
    # Clear the screen
    os.system("cls" if os.name == "nt" else "clear")


def display_row(self, row_index):
        # Display a single row from the board with borders
        row = self.board[row_index]
        return f"{row_index + 1} | " + " | ".join(str(cell) for cell in row) + " |"