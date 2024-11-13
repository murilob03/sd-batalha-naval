from board import Board, display_boards_side_by_side, clear_screen


def main():
    # Initialize the boards and display
    board1 = Board()
    board2 = Board()
    display_boards_side_by_side(board1, board2)

    # Add ships to board1
    ships_sizes = [4, 3, 2]

    for size in ships_sizes:
        coords = input(
            f"Input coordinates and direction for size {size} ship: e.g(A1 E)\n"
        )
        row = int(coords[1]) - 1
        col = ord(coords[0].upper()) - 65
        direction = coords[3]
        print(f"{row} {col} {direction}")
        board1.add_ship(row, col, size, direction)

    # Display the updated board1
    clear_screen()
    display_boards_side_by_side(board1, board2)


if __name__ == "__main__":
    main()
