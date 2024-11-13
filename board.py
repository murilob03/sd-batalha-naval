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
        # Mapping directions to row and column increments
        direction_map = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

        if direction not in direction_map:
            print("Invalid direction.")
            return

        d_row, d_col = direction_map[direction]
        end_row = row + d_row * (size - 1)
        end_col = col + d_col * (size - 1)

        # Check if the ship is within bounds
        if not (0 <= end_row < self.size and 0 <= end_col < self.size):
            print("Invalid ship placement. Ship is out of bounds.")
            return

        # Check for overlap and update cells if placement is valid
        for i in range(size):
            new_row, new_col = row + d_row * i, col + d_col * i
            if self.get_cell(new_row, new_col) == 1:
                print("Invalid ship placement. Ships overlap.")
                return
            self.update_cell(new_row, new_col, 1)


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
