from game_optimized.AI.evaluate import evaluate

def negamax(game, depth, player, color=1):
    # Base case: se atingiu a profundidade máxima ou há um vencedor
    if depth == 0 or game.winner is not None:
        return color * evaluate(game, player), None  # Multiplica pelo "color" para inverter a avaliação do adversário
    
    best_value = float('-inf')
    best_move = None
    
    # Itera sobre todas as peças do jogador atual
    for piece in game.pieces:
        if piece.player == game.turn:
            for (nx, ny) in game.get_valid_moves(piece):
                new_game = game.clone_for_minimax()
                clone_piece = next((p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y), None)
                
                if clone_piece is None:
                    continue
                
                new_game.move_piece(clone_piece, nx, ny, simulate=True)
                eval_score, _ = negamax(new_game, depth - 1, player, -color)
                eval_score = -eval_score  # Invertemos o valor porque estamos alternando o jogador
                
                if eval_score > best_value:
                    best_value = eval_score
                    best_move = (piece, nx, ny)
    
    return best_value, best_move

def get_best_move(game, depth=3):
    current_player = game.turn
    _, move = negamax(game, depth, current_player, 1)
    return move
