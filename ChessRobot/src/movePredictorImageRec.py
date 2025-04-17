import cv2
import chess
import chess.engine
import numpy as np

class ChessGameImageRec:
    def __init__(self, engine_path, move_callback=None):
        self.engine_path = engine_path
        self.board = chess.Board()  # Creates an empty board
        self.move_callback = move_callback  # Callback for sending the best move

    def start_game(self):
        cap = cv2.VideoCapture(0)  #starts the video capture
        with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:
            while not self.board.is_game_over():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture frame from video stream.")
                    break

                # Process the frame to detect the board and pieces
                self.update_board_from_image(frame)

                # Display the current board
                self.display_board()

                # Generate the best move using Stockfish
                self.generated_move(engine)

            self.game_result()

        cap.release() # stops the video and deletes the interface 
        cv2.destroyAllWindows()

    def update_board_from_image(self, frame):
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use Canny edge detection to find edges
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edges
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour, assuming it's the chessboard
        largest_contour = max(contours, key=cv2.contourArea)

        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        # Ensure the polygon has 4 points (a rectangle)
        if len(approx) == 4:
            # Warp the perspective to get a top-down view of the board
            pts = np.array([point[0] for point in approx], dtype="float32")
            top_down_view = self.warp_perspective(frame, pts)

            # Divide the board into an 8x8 grid and detect pieces
            self.detect_pieces(top_down_view)
        else:
            print("Chessboard not detected.")

    def warp_perspective(self, frame, pts):
        # Define the destination points for the warp
        dst = np.array([[0, 0], [800, 0], [800, 800], [0, 800]], dtype="float32")

        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts, dst)

        # Perform the warp
        warped = cv2.warpPerspective(frame, matrix, (800, 800))
        return warped

    def detect_pieces(self, board_image):
        square_size = board_image.shape[0] // 8

        for row in range(8):
            for col in range(8):
                # Extract the square region
                x_start = col * square_size
                y_start = row * square_size
                square = board_image[y_start:y_start + square_size, x_start:x_start + square_size]

                # Analyze the square to detect a piece
                piece_detected = self.analyze_square(square)

                # Update the chess.Board object
                if piece_detected:
                    # Example: Update the board with a white pawn at e2
                    self.board.set_piece_at(chess.square(col, 7 - row), chess.Piece.from_symbol(piece_detected))

    def analyze_square(self, square):
        # Load templates of chess pieces
        templates = {
            "P": cv2.imread("templates/whitepawn.jpeg", 0),
            "N": cv2.imread("templates/whiteknight.jpeg", 0),
            "B": cv2.imread("templates/whitebishop.jpeg", 0),
            "R": cv2.imread("templates/whiterook.jpeg", 0),
            "Q": cv2.imread("templates/whitequeen.jpeg", 0),
            "K": cv2.imread("templates/whiteking.jpeg", 0),
            "p": cv2.imread("templates/blackpawn.jpeg", 0),
            "n": cv2.imread("templates/blackknight.jpeg", 0),
            "b": cv2.imread("templates/blackbishop.jpeg", 0),
            "r": cv2.imread("templates/blackrook.jpeg", 0),
            "q": cv2.imread("templates/blackqueen.jpeg", 0),
            "k": cv2.imread("templates/blackking.jpeg", 0),
        }

        # Convert the square to grayscale
        gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)

        # Match each template against the square to find the corresponding piece
        for piece, template in templates.items():
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > 0.8:  # Adjust threshold as needed
                return piece  # Return the matched piece type
        return None

    def display_board(self):
        print(self.board)

    def generated_move(self, engine):
        result = engine.play(self.board, chess.engine.Limit(time=1.0))
        self.board.push(result.move)
        print(f"Engine plays: {result.move}")
        if self.move_callback:
            self.move_callback(result.move)
        # Confirmation message
        print(f"Move {result.move} has been successfully made.")

    def game_result(self):
        if self.board.is_checkmate():
            print("Checkmate")
        elif self.board.is_stalemate():
            print("Draw")
        else:
            print("Game over.")

if __name__ == "__main__":
    engine_path = "C:\\stockfish\\stockfish-windows-x86-64"

    def handle_best_move(move):
        print(f"Best move: {move}")
        

    game = ChessGameImageRec(engine_path, move_callback=handle_best_move)
    game.start_game()