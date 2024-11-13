import time
import os


class Board:
    def __init__(self, size=9):
        # Initialize a size x size board with placeholder values (0)
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def update_cell(self, row, col, value):
        # Update a specific cell at (row, col) with a new value
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = value
        else:
            print("Invalid coordinates. Please provide values within the board size.")

    def get_cell(self, row, col):
        # Get the value of a specific cell at (row, col)
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        else:
            print("Invalid coordinates. Please provide values within the board size.")
            return None

    def display(self):
        # Define the horizontal border
        horizontal_border = "+---" * self.size + "+"

        # Print the board with borders
        print("    A   B   C   D   E   F   G   H   I")
        print("  " + horizontal_border)
        i = 1
        for row in self.board:
            print(f"{i} | " + " | ".join(str(cell) for cell in row) + " |")
            i += 1
            print("  " + horizontal_border)

    def display_row(self, row_index):
        # Display a single row from the board with borders
        row = self.board[row_index]
        return f"{row_index + 1} | " + " | ".join(str(cell) for cell in row) + " |"

    def add_ship(self, row, col, size, direction):
        # Add a ship of a specific size at a specific location
        if direction == "N":
            for i in range(size):
                if row - size < 0:
                    print("Invalid ship placement. Ship is out of bounds.")
                    return
                self.update_cell(row - i, col, 1)
        elif direction == "S":
            if row + size >= self.size:
                print("Invalid ship placement. Ship is out of bounds.")
                return
            for i in range(size):
                self.update_cell(row + i, col, 1)
        elif direction == "E":
            if col + size >= self.size:
                print("Invalid ship placement. Ship is out of bounds.")
                return
            for i in range(size):
                self.update_cell(row, col + i, 1)
        elif direction == "W":
            if col - size < 0:
                print("Invalid ship placement. Ship is out of bounds.")
                return
            for i in range(size):
                self.update_cell(row, col - i, 1)


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


# # Usage
# board = Board()
# board2 = Board()

# display_boards_side_by_side(board, board2)

# # Update cells and display the board
# time.sleep(2)
# clear_screen()

# board.add_ship(3, 4, 3, "N")
# board.add_ship(5, 3, 4, "E")

# board2.add_ship(1, 1, 2, "S")
# board2.add_ship(8, 1, 3, "W")

# display_boards_side_by_side(board, board2)

# time.sleep(2)
