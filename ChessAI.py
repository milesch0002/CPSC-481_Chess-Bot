import chess
import random
from math import inf

board = chess.Board()

def random_move(board):
    moves = board.legal_moves
    if moves:
        return random.choice(moves)
    

def evaluate(board, maximizing_color):
    if maximizing_color == chess.WHITE:
        return board.whiteScore - board.blackScore
    else:
        return board.blackScore - board.whiteScore

def minimax(board, depth, maximizing_player, maximizing_color):
    if depth == 0 or board.is_checkmate():
        return None, evaluate(board, maximizing_color)
    
    moves = board.legal_moves
    best_move = random.choice(moves)
    
    if maximizing_player:
        max_eval = -inf
        for move in moves:
            board.push(move[0], move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, False, maximizing_color)[1]
            board.pop()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:
            board.push(move[0], move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, True, maximizing_color)[1]
            board.pop()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
    
def play_game():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            # AI's turn
            best_move = None
            best_eval = -inf
            for move in board.legal_moves:
                board.push(move)
                eval = minimax(board, depth=3, alpha=-inf, beta=inf, maximizing_player=False)
                board.pop()
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
            board.push(best_move)
        else:
            # Human player's turn (you can implement this part)
            pass

    print("Game over. Result:", board.result())

if __name__ == "__main__":
    play_game()