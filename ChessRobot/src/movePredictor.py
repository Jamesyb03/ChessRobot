# movePredictor.py
import chess
import chess.engine

def MovePredictor():
    board = chess.Board()

    # Update the path to the Stockfish executable
    engine_path = "C:\\stockfish\\stockfish-windows-x86-64"  # Ensure this is the correct path
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        while not board.is_game_over():
            print(board)
            move = input("Your move: ")
            try:
                board.push_san(move)  # Validate and apply the move
            except ValueError:
                print("Invalid move")
                continue

            # Let the engine play the best move for the other side
            if not board.is_game_over():
                result = engine.play(board, chess.engine.Limit(time=1.0))  # 1-second thinking time
                board.push(result.move)
                print(f"Engine plays: {result.move}")

if __name__ == "__main__":
    MovePredictor()