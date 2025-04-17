import chess
import chess.engine

class ChessGame:
    def start(self, engine_path):
        self.board = chess.Board()  # Creates the board
        self.engine_path = engine_path  # Gets Stockfish path

    def start_game(self):  # Starts the chess game
        with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:  # Gets the Stockfish exe
            while not self.board.is_game_over():
                self.display_board()  # Displays the current board
                self.myMove()  # Gets the move from the user
                if self.board.is_game_over():  # Checks if game is over
                    break
                coords = self.generatedMove(engine)  # Generates the move using Stockfish
                print(f"Engine move coordinates: {coords}")
            self.gameResult()  # Gives result if game is over

    def display_board(self):
        print(self.board)

    def myMove(self):
        while True:
            move = input("Your move: ")
            try:
                self.board.push_san(move)  # Check that move is valid and then play it
                break
            except ValueError:
                print("Invalid move. Please try again.")

    def generatedMove(self, engine):  # Generates a move using Stockfish
        result = engine.play(self.board, chess.engine.Limit(time=1.0))
        self.board.push(result.move)
        print(f"Engine plays: {result.move}")

        # Convert UCI move to coordinates
        move_uci = result.move.uci()
        start_col = ord(move_uci[0]) - ord('a')  # Convert 'a'-'h' to 0-7
        start_row = int(move_uci[1]) - 1         # Convert '1'-'8' to 0-7
        end_col = ord(move_uci[2]) - ord('a')    # Convert 'a'-'h' to 0-7
        end_row = int(move_uci[3]) - 1           # Convert '1'-'8' to 0-7

        return start_col, start_row, end_col, end_row

    def gameResult(self):
        if self.board.is_checkmate():
            print("Checkmate! Game over.")
        elif self.board.is_stalemate():
            print("Stalemate! Game over.")
        else:
            print("Game over.")

if __name__ == "__main__":
    engine_path = "C:\\stockfish\\stockfish-windows-x86-64"
    game = ChessGame()
    game.start(engine_path)  # Initialize the board and engine path
    game.start_game()