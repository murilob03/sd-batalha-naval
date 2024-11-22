from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import logging, json

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log all INFO-level and higher messages
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class GameServer:
    def __init__(self):
        self.players = {}  # Stores player boards
        self.turn = None  # Tracks whose turn it is

    def register_player(self, player_name, board_data):
        """Registers a new player with their board."""
        if player_name in self.players:
            logging.warning(f"Player {player_name} already registered.")
            return "Player already registered."

        if len(self.players) >= 2:
            logging.warning(f"Player {player_name} failed to register. Game is full.")
            return "Game is already full."

        self.players[player_name] = {"board": board_data, "hits": 0}
        logging.info(f"Player {player_name} successfully registered.")

        # Assign the first turn to the first player
        if len(self.players) == 1:
            self.turn = player_name
            logging.info(f"Player {player_name} gets the first turn.")

        return "Player registered successfully."

    def is_game_ready(self):
        """Checks if the game has two players ready to play."""
        is_ready = len(self.players) == 2
        logging.info(f"Game ready status: {is_ready}")
        return is_ready

    def whose_turn(self):
        """Returns the name of the player whose turn it is."""
        logging.info(f"It is {self.turn}'s turn.")
        return self.turn

    def make_guess(self, player_name, x, y):
        """Handles a player's guess."""
        if not self.is_game_ready():
            logging.warning(
                f"Player {player_name} tried to guess before the game was ready."
            )
            return "Game is not ready yet."

        if self.turn != player_name:
            logging.warning(f"Player {player_name} tried to guess out of turn.")
            return "Not your turn."

        if not (0 <= x < 5 and 0 <= y < 5):
            logging.warning(
                f"Player {player_name} made an invalid guess at ({x}, {y})."
            )
            return "Invalid move: Out of bounds."

        opponent = self.get_opponent(player_name)
        opponent_board = self.players[opponent]["board"]

        if opponent_board[x][y] == "1":
            opponent_board[x][y] = "H"  # Mark as hit
            self.players[player_name]["hits"] += 1
            self.turn = opponent  # Switch turn
            logging.info(f"Player {player_name} hit a ship at ({x}, {y}).")
            return "Hit"

        elif opponent_board[x][y] == "0":
            opponent_board[x][y] = "M"  # Mark as miss
            self.turn = opponent  # Switch turn
            logging.info(f"Player {player_name} missed at ({x}, {y}).")
            return "Miss"

        logging.warning(f"Player {player_name} made an invalid move at ({x}, {y}).")
        return "Invalid move: Position already guessed."

    def is_game_over(self):
        """Checks if the game is over and declares the winner."""
        for player_name, data in self.players.items():
            if data["hits"] >= 2:  # Assuming 9 hits to win
                logging.info(f"Game over. {player_name} wins!")
                return True
        return False

    def get_board(self, player_name):
        """Returns the board of the given player."""
        if player_name in self.players:
            logging.info(f"Player {player_name} requested their board.")
            return self.players[player_name]["board"],
        logging.warning(
            f"Player {player_name} requested a board but is not registered."
        )
        return {
            "status": "error",
            "message": "Player not found.",
        }

    def get_opponent(self, player_name):
        """Helper method to find the opponent of the given player."""
        return [p for p in self.players if p != player_name][0]


# Create server
server = SimpleXMLRPCServer(
    ("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler
)
game = GameServer()

# Register game instance
server.register_instance(game)
logging.info("Battleship server started and awaiting connections...")
server.serve_forever()
