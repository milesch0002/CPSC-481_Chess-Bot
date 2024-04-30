import chess

# Function to evaluate the board for the AI (higher score for better position)
def evaluate(board):
  if board.is_checkmate():
    return -1000 if board.turn == chess.WHITE else 1000
  if board.is_stalemate():
    return 0

  # Material difference (positive for white advantage)
  material = sum(piece.value for piece in board.piece_map().values() if piece.color == chess.WHITE)
  material -= sum(piece.value for piece in board.piece_map().values() if piece.color == chess.BLACK)

  # Piece position value (needs refinement)
  position_value = 0
  for piece in board.piece_map().values():
    position_value += piece_type_values.get(piece.piece_type, 0)

  return material + position_value

# Sample piece position values (adjust these based on your strategy)
piece_type_values = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 0,  # King's value depends on the endgame scenario
}

def alphabeta(board, depth, alpha, beta, maximizing_player):
  if depth == 0 or board.is_game_over():
    return evaluate(board), None

  if maximizing_player:
    best_move = None
    best_score = -float('inf')
    for move in board.legal_moves:
      board.push(move)
      score, _ = alphabeta(board.copy(), depth - 1, alpha, beta, False)
      board.pop()
      if score > best_score:
        best_move = move
        best_score = score
      alpha = max(alpha, score)
      if beta <= alpha:
        break  # Prune branch if beta <= alpha
    return best_score, best_move
  else:
    best_move = None
    best_score = float('inf')
    for move in board.legal_moves:
      board.push(move)
      score, _ = alphabeta(board.copy(), depth - 1, alpha, beta, True)
      board.pop()
      if score < best_score:
        best_move = move
        best_score = score
      beta = min(beta, score)
      if beta <= alpha:
        break  # Prune branch if beta <= alpha
    return best_score, best_move

def find_best_move(board, depth):
  # Identify all legal moves
  legal_moves = list(board.legal_moves)

  # If no moves available, handle checkmate/stalemate
  if not legal_moves:
    return None, evaluate(board)

  # Find best move using alphabeta
  best_score, best_move = alphabeta(board.copy(), depth, -float('inf'), float('inf'), True)

  return best_move, best_score

# Example usage
board = chess.Board()
print(board)
print(board.legal_moves)

while True:
  # Get player's move (assume they control white pieces)
  while True:
    human_move = input("Enter your move as white (e.g. e2e4): ")
    try:
      if board.turn == chess.WHITE and board.push_san(human_move):
        break
      else:
        print("Invalid move or wrong color. You play white pieces. Try again.")
    except ValueError:
      print("Invalid move. Try again.")
  print(board)

  # Check for game end after player's move
  if board.is_game_over():
    result = board.result()
    if result == 1:
      print("You won!")
    elif result == 0:
      print("Stalemate!")
    else:
      print("AI won!")
    break

  # AI's move (assuming it controls black pieces)
  ai_move, _ = find_best_move(board.copy(), 2)  # Adjust search depth for better play, but slower

  # Make AI's move
  board.push(ai_move)