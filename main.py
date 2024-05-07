import chess
import random

board = chess.Board()

piece_type_values = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 999,  # King is valued higher
}

# Function to evaluate the board for the AI (higher score for better position)
def evaluate(board):
  if board.is_checkmate():
    return -1000 if board.turn == chess.WHITE else 1000
  if board.is_stalemate():
    return 0

  # Material difference (positive for white advantage)
  material = 0
  for piece in board.piece_map().values():
      if piece.color == chess.WHITE:
          material += piece_type_values.get(piece.piece_type, 0)
      else:
          material -= piece_type_values.get(piece.piece_type, 0)

  # Piece position value (needs refinement)
  position_value = 0
  for piece in board.piece_map().values():
    position_value += piece_type_values.get(piece.piece_type, 0)

  return material + position_value

def alphabeta(board, depth, alpha, beta, maximizing_player):
  if depth == 0 or board.is_game_over():
    return evaluate(board), None

  if maximizing_player:
    best_move = None
    best_score = -float('inf')
    for move in board.legal_moves:
      board.push(move)
      score, _ = alphabeta(board, depth - 1, alpha, beta, False)
      board.pop()
      if score > best_score:
        best_move = move
        best_score = score
      alpha = max(alpha, best_score)
      if beta <= alpha:
        break  # Prune branch if beta <= alpha
    return best_score, best_move
  else:
    best_move = None
    best_score = float('inf')
    for move in board.legal_moves:
      board.push(move)
      score, _ = alphabeta(board, depth - 1, alpha, beta, True)
      board.pop()
      if score < best_score:
        best_move = move
        best_score = score
      beta = min(beta, best_score)
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

  return best_move

def openings(index, opening):
    # Queen's Gambit
    if opening == 1:
        print("Queen's Gambit Openings")
        if index == 1:
            return chess.Move.from_uci("d2d4")
        elif index == 2:
            if board.piece_at(chess.D5) is None:
                return chess.Move.from_uci("d4d5")
            else:
                return chess.Move.from_uci("c2c4")
        else:
            piece = board.piece_at(chess.D5)
            if piece is not None and piece.color == chess.BLACK and board.piece_at(chess.C4) is not None:
                return chess.Move.from_uci("c4d5")
            else:
                return chess.Move.from_uci("c2c4")
    # Vienna Game
    elif opening == 2:
        print("Vienna Game Opening")
        if index == 1:
            return chess.Move.from_uci("e2e4")
        elif index == 2:
            if board.piece_at(chess.E5) is None:
                return chess.Move.from_uci("e4e5")
            else:
                return chess.Move.from_uci("b1c3")
        else:
            piece = board.piece_at(chess.C3)
            if piece is not None and piece.color == chess.WHITE:
                return chess.Move.from_uci("f1c4")
            else:
                return chess.Move.from_uci("b1c3")
    # Italian Game
    else:
      print("Italian Game Opening")
      if index == 1:
          return chess.Move.from_uci("e2e4")
      elif index == 2:
          return chess.Move.from_uci("g1f3")
      else:
          return chess.Move.from_uci("f1c4")



chosen_opening = random.randint(1,3)
while True:
  if board.turn == chess.WHITE and board.fullmove_number <= 3:
    ai_move = openings(board.fullmove_number, chosen_opening)
    board.push(ai_move)
    print(board)
  elif board.turn == chess.WHITE and board.fullmove_number > 3:
    ai_move = find_best_move(board.copy(), 3)  # Adjust search depth for better play, but slower
    board.push(ai_move)
    print(board)
  else:
    try:
      human_move = input("Enter your move as black (e.g. e2e4): ")
      move = chess.Move.from_uci(human_move)
      if move in board.legal_moves:
        board.push(move)
      else:
        print("Invalid move. Please enter a valid move.")
        continue
    except ValueError:
      print("Invalid input. Please enter your move in the format 'e2e4'.")
      continue

  # Check for game end after player's move
  if board.is_game_over():
      result = board.result()
      if result == '1-0':
          print("You won!")
      elif result == '0-1':
          print("AI won!")
      else:
          print("Stalemate!")
      break