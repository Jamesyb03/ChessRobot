import chess
import chess.engine

class ChessGame:
    def start(self, engine_path):
        self.board = chess.Board() # creates the board 
        self.engine_path = engine_path # gets stockfish path

    def start_game(self): # starts the chess game 
            with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:# gets the stockfish exe 
                while not self.board.is_game_over():
                    self.display_board() # displays the current board 
                    self.myMove() # gets the move from the user
                    if self.board.is_game_over(): #checks if game is over
                        break
                    self.generatedMove(engine) # generates the move using stockfish and plays it
                self.gameResult()# gives result if game is over 

    def display_board(self):
        print(self.board)

    def myMove(self):
        while True:
            move = input("Your move: ")
            try:
                self.board.push_san(move) #check that move is valid and then play it 
                break
            except ValueError:
                print("Invalid move. Please try again.")

    def generatedMove(self, engine): ## This function generates a move using stockfish
        result = engine.play(self.board, chess.engine.Limit(time=1.0))  
        self.board.push(result.move)
        print(f"Engine plays: {result.move}")

    def gameResult(self): 
        if self.board.is_checkmate():
            print("Checkmate! Game over.")
        elif self.board.is_stalemate():
            print("Stalemate! Game over.")
        else:
            print("Game over.")

if __name__ == "__main__":
    engine_path = "C:\\stockfish\\stockfish-windows-x86-64"  
    game = ChessGame(engine_path)
    game.start_game()