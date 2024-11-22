from board import Board, display_boards_side_by_side, clear_screen
import xmlrpc.client
import time
import json

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
player_name = input("Enter your name: ")


def main():
    # Initialize boards and display
    board1 = Board(5)
    board2 = Board(5)
    display_boards_side_by_side(board1, board2)

    # Add ships to board1
    add_ships_to_board(board1)

    # Display the updated board1
    clear_screen()
    display_boards_side_by_side(board1, board2)

    # Register player with server
    if not proxy.register_player(player_name, board1.board):
        print("Failed to register player. Server may be full.")
        return

    # Wait for the game to start
    while not proxy.is_game_ready():
        time.sleep(1)

    while True:
        if proxy.whose_turn() == player_name:
            print("Your turn!")
            if proxy.is_game_over():
                print("Game over! You lost.")
                break

            # Update board1 with opponent's move
            print(proxy.get_board(player_name))
            board1.board = proxy.get_board(player_name)[0]  # type: ignore

            # Display the updated boards
            clear_screen()
            display_boards_side_by_side(board1, board2)

            player_turn(board2)

            # Display the updated boards
            clear_screen()
            display_boards_side_by_side(board1, board2)

            if proxy.is_game_over():
                print("Game over! You won.")
                break
        else:
            print("Waiting for opponent's move...")
            time.sleep(1)


def add_ships_to_board(board):
    """Add ships to the board based on user input for each ship's size."""
    ship_sizes = [2]
    for size in ship_sizes:
        row, col, direction = get_ship_placement(size)
        board.add_ship(row, col, size, direction)


def get_ship_placement(size):
    """Prompt the user for ship placement and return parsed coordinates and direction."""
    while True:
        coords = input(
            f"Enter coordinates and direction for size {size} ship (e.g., A1 E):\n"
        )
        try:
            row, col, direction = parse_coords(coords)
            return row, col, direction
        except ValueError:
            print("Invalid input. Please try again.")


def extract_coords(coords):
    """Convert coordinates from string format to row and column indices."""
    row = int(coords[1]) - 1
    col = ord(coords[0].upper()) - 65
    return row, col


def parse_coords(coords):
    """Parse user input to get row, column, and direction."""
    row, col = extract_coords(coords)
    direction = coords[3].upper()
    return row, col, direction


def player_turn(attack_board):
    """Handle player's turn to attack."""
    row, col = get_attack_coords()
    # Send attack and receive response from server
    response = proxy.make_guess(player_name, row, col)

    if response == "Hit":
        print("Hit!")
        attack_board.update_cell(row, col, "H")
    elif response == "Miss":
        print("Miss!")
        attack_board.update_cell(row, col, "M")
    else:
        print("Invalid move. Try again.")
        time.sleep(1)


def get_attack_coords():
    """Prompt for and parse attack coordinates."""
    while True:
        attack_coords = input("Enter coordinates to attack (e.g., A1): ")
        try:
            return extract_coords(attack_coords)
        except ValueError:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
