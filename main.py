import chess
import random

board = chess.Board()

# Table and piece values are given from this website: https://www.chessprogramming.org/Simplified_Evaluation_Function
piece_type_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

pawn_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

knight_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

bishop_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

rook_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

queen_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

king_table_middlegame = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

king_table_endgame = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

# Function to evaluate the board for the AI (higher score for better position)
def evaluate(board):
  if board.is_checkmate():
    return -1000000 if board.turn == chess.WHITE else 1000000
  if board.is_stalemate():
    return -100

  # Material difference (positive for white advantage)
  material = 0
  for piece in board.piece_map().values():
      if piece.color == chess.WHITE:
          material += piece_type_values.get(piece.piece_type, 0)
      else:
          material -= piece_type_values.get(piece.piece_type, 0)

  # Piece position value (needs refinement)
  position_value = 0
  for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            if piece.piece_type == chess.PAWN:
                position_value += pawn_table[square]
            elif piece.piece_type == chess.KNIGHT:
                position_value += knight_table[square]
            elif piece.piece_type == chess.BISHOP:
                position_value += bishop_table[square]
            elif piece.piece_type == chess.ROOK:
                position_value += rook_table[square]
            elif piece.piece_type == chess.QUEEN:
                position_value += queen_table[square]
            elif piece.piece_type == chess.KING:
                if board.fullmove_number <= 30:
                  position_value += king_table_middlegame[square]
                else:
                   position_value += king_table_endgame[square]
        else:
            if piece.piece_type == chess.PAWN:
                position_value -= pawn_table[chess.square_mirror(square)]
            elif piece.piece_type == chess.KNIGHT:
                position_value -= knight_table[chess.square_mirror(square)]
            elif piece.piece_type == chess.BISHOP:
                position_value -= bishop_table[chess.square_mirror(square)]
            elif piece.piece_type == chess.ROOK:
                position_value -= rook_table[chess.square_mirror(square)]
            elif piece.piece_type == chess.QUEEN:
                position_value -= queen_table[chess.square_mirror(square)]
            elif piece.piece_type == chess.KING:
                if board.fullmove_number <= 30:
                  position_value -= king_table_middlegame[chess.square_mirror(square)]
                else:
                   position_value -= king_table_endgame[chess.square_mirror(square)]

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
        if index == 1:
            return board.parse_san("d4")
        elif index == 2:
            if board.piece_at(chess.D5) is None:
                return board.parse_san("d5")
            else:
                return board.parse_san("c4")
        else:
            piece = board.piece_at(chess.D5)
            if piece is not None and piece.color == chess.BLACK and board.piece_at(chess.C4) is not None:
                return board.parse_san("cxd5")
            else:
                return board.parse_san("c4")
    # Vienna Game
    elif opening == 2:
        if index == 1:
            return board.parse_san("e4")
        elif index == 2:
            if board.piece_at(chess.E5) is None:
                return board.parse_san("e5")
            else:
                return board.parse_san("Nc3")
        else:
            piece = board.piece_at(chess.C3)
            if piece is not None and piece.color == chess.WHITE:
                return board.parse_san("Bc4")
            else:
                return board.parse_san("Nc3")
    # Italian Game
    else:
        if index == 1:
            return board.parse_san("e4")
        elif index == 2:
            return board.parse_san("Nf3")
        else:
            return board.parse_san("Bc4")



chosen_opening = random.randint(1,3)
while True:
  print("\n")
  print("="*20)
  turn = ""
  if board.turn == True:
     turn = "White"
  else:
     turn = "Black"
  print("Current Move: ", board.fullmove_number,)
  print("Turn: ", turn)
  print("="*20)
  if board.turn == chess.WHITE and board.fullmove_number <= 3:
    ai_move = openings(board.fullmove_number, chosen_opening)
    san_move = board.san(ai_move)
    board.push(ai_move)
    print("-"*20)
    print(board)
    print("AI Move:", san_move)
    print("-"*20)
  elif board.turn == chess.WHITE and board.fullmove_number > 3:
    ai_move = find_best_move(board, 3)
    san_move = board.san(ai_move)
    board.push(ai_move)
    print("-"*20)
    print(board)
    print("AI Move:", san_move)
    print("-"*20)
  else:
    try:
      human_move = input("Enter your move as black (e.g. a5): ")
      move = board.parse_san(human_move)
      if move in board.legal_moves:
        board.push(move)
        print("-"*20)
        print(board)
        print("Human Move:", human_move)
        print("-"*20)
      else:
        print("Invalid move. Please enter a valid move.")
        continue
    except ValueError:
      print("Invalid input. Please enter your move in the format 'a4'.")
      continue
  
  # Check for game end after player's move
  if board.is_game_over():
    result = board.result()
    if result == '1-0':
        print("AI won!")
    elif result == '0-1':
        print("You won!")
    else:
        print("Stalemate!")
        break