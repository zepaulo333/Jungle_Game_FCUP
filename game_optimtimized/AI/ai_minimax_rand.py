import random
from game_optimized.main_files.game import Game
from game_optimized.AI.eval_easy import evaluate_easy
from game_optimized.AI.eval_medium import evaluate_medium
from game_optimized.AI.eval_hard import evaluate_hard
from game_optimized.AI.eval_impossible import evaluate_impossible

game = Game()

choose = [evaluate_easy, evaluate_medium, evaluate_hard, evaluate_impossible]

evaluate1 = random.choice(choose)
evaluate2 = random.choice(choose)

def minimax(game, depth, player):
    if player == 1: evaluate = evaluate_medium
    else: evaluate = evaluate_easy
    if depth == 0 or game.winner is not None:
        return evaluate(game, player), None

    best_moves = []
    if game.turn == player:  # Maximizing player
        best_eval = float('-inf')
        for piece in game.pieces:
            if piece.player == player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()
                    clone_piece = next((p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, depth - 1, player)
                    if eval_score > best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))
    else:  # Minimizing player
        best_eval = float('inf')
        for piece in game.pieces:
            if piece.player != player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()
                    clone_piece = next((p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, depth - 1, player)
                    if eval_score < best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))

    best_move = random.choice(best_moves) if best_moves else None
    return best_eval, best_move

def get_best_move(game, depth=3):
    current_player = game.turn
    score, move = minimax(game, depth, current_player)
    return move
