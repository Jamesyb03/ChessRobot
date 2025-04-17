import chess
import chess.engine

class ChessGame:
    def __init__(self, engine_path, move_callback=None):
        self.engine_path = engine_path
        self.board = chess.Board()  # Creates the board
        self.move_callback = move_callback  # Callback for sending the best move

    def start_game(self):  # Starts the chess game
        with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:  # Gets the Stockfish exe
            while not self.board.is_game_over():
                self.display_board()  # Displays the current board
                self.myMove()
                if self.board.is_game_over():  # Checks if game is over
                    break
                self.generatedMove(engine)  # Generates the move using Stockfish and plays it
            self.gameResult()  # Gives result if game is over

    def display_board(self):
        print(self.board)

    def myMove(self):
        while True:
            move = input("Your move: ")
            try:
                self.board.push_san(move)  # Check that move is valid and then play it
                # Convert the move to coordinates and output them
                uci_move = self.board.peek().uci()  # Get the last move in UCI format
                convert_move_to_coordinates(uci_move)
                break
            except ValueError:
                print("Invalid move. Please try again.")

    def generatedMove(self, engine):  # Generates a move using Stockfish
        result = engine.play(self.board, chess.engine.Limit(time=1.0))
        self.board.push(result.move)
        print(f"Engine plays: {result.move}")
        if self.move_callback:  # Call the callback with the engine's move
            self.move_callback(result.move)

    def gameResult(self):
        if self.board.is_checkmate():
            print("Checkmate")
        elif self.board.is_stalemate():
            print("Draw")
        else:
            print("Game over.")

def convert_move_to_coordinates(move):
    if len(move) != 4:
        raise ValueError("Move must be in the format 'e2e4'.")

    # Split the move into components
    start_col, start_row, end_col, end_row = move[0], move[1], move[2], move[3]

   
    start_col_num = ord(start_col.lower()) - ord('a') 
    end_col_num = ord(end_col.lower()) - ord('a') 

    
    start_row_num = int(start_row) -1
    end_row_num = int(end_row) -1

    print(f"Your move: Start({start_col_num}, {start_row_num}), End({end_col_num}, {end_row_num})")

    return start_col_num, start_row_num, end_col_num, end_row_num

if __name__ == "__main__":
    engine_path = "C:\\stockfish\\stockfish-windows-x86-64"  
    game = ChessGame(engine_path)
    game.start_game()