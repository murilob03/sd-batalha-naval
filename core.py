import json
from board import Board, display_boards_side_by_side, clear_screen


def main():
    # Initialize boards and display
    board1 = Board()
    board2 = Board()
    display_boards_side_by_side(board1, board2)

    # Add ships to board1
    add_ships_to_board(board1)

    # Display the updated board1
    clear_screen()
    display_boards_side_by_side(board1, board2)

    # Start game loop
    our_turn = True

    while not game_over():
        if our_turn:
            player_turn(board2)
        else:
            opponent_turn(board1)

        # Display the boards
        clear_screen()
        display_boards_side_by_side(board1, board2)

        # Toggle turn
        our_turn = not our_turn


def add_ships_to_board(board):
    """Add ships to the board based on user input for each ship's size."""
    ship_sizes = [4, 3, 2]
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
    response = send_attack(row, col)  # Assuming send_attack interacts with server

    if response:  # Assuming response is a boolean indicating hit or miss
        print("Hit!")
        attack_board.update_cell(row, col, "X")
    else:
        print("Miss!")
        attack_board.update_cell(row, col, "O")


def get_attack_coords():
    """Prompt for and parse attack coordinates."""
    while True:
        attack_coords = input("Enter coordinates to attack (e.g., A1): ")
        try:
            return extract_coords(attack_coords)
        except ValueError:
            print("Invalid input. Please try again.")


def opponent_turn(defense_board):
    """Handle opponent's turn based on received attack coordinates."""
    attack_coords = receive_attack()  # Stub for receiving attack coordinates
    row, col = extract_coords(attack_coords)

    # Check if the attack is a hit or miss
    hit = defense_board.get_cell(row, col) == 1
    send_attack_response(hit)  # Stub for sending response to server

    if hit:
        print("You have been hit!")
        defense_board.update_cell(row, col, "X")
    else:
        print("You have been missed!")
        defense_board.update_cell(row, col, "O")


def game_over():
    """Placeholder for game over logic."""
    # Implement game over conditions here
    pass


def receive_attack():
    """Placeholder for receiving an attack from the server."""
    pass


def send_attack(row, col):
    """Placeholder for sending an attack to the server."""
    # Return True for hit, False for miss (mocking response for now)
    return True


def send_attack_response(hit):
    """Placeholder for sending attack response to server."""
    pass


if __name__ == "__main__":
    main()
