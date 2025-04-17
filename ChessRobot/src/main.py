# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       jbate                                                        #
# 	Created:      4/11/2025, 11:51:58 AM                                       #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from movePredictor import ChessGame, convert_move_to_coordinates

# Brain should be defined by default
brain = Brain()

def handle_best_move(move):
    try:
        # Convert the move to coordinates using movePredictor
        start_col_num, start_row_num, end_col_num, end_row_num = convert_move_to_coordinates(move)

        # Reconstruct the transformed move
        transformed_move = f"{start_col_num}{start_row_num} -> {end_col_num}{end_row_num}"

        # Display the transformed move and new coordinates
        brain.screen.clear_screen()
        brain.screen.print(f"Moving piece: {transformed_move}")
        print(f"Moving piece: {transformed_move}")
        print(f"New coordinates: Start({start_col_num}, {start_row_num}), End({end_col_num}, {end_row_num})")
    except ValueError as e:
        # Handle invalid move format
        brain.screen.clear_screen()
        brain.screen.print("Invalid move format")
        print(f"Invalid move format: {e}")

if __name__ == "__main__":
    # brain.screen.print("Starting Game")
    print("Starting Game")

    engine_path = "C:\\stockfish\\stockfish-windows-x86-64"
    game = ChessGame(engine_path, move_callback=handle_best_move)
    game.start_game()



