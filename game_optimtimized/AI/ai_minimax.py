from game_optimized.AI.eval_impossible import evaluate_impossible

# Tabela de transposição para memoização
transposition_table = {}

def get_state_key(game):
    """
    Gera uma chave única para o estado do jogo baseada no turno, vencedor e nas peças.
    """
    pieces_state = tuple(sorted((p.name, p.x, p.y, p.player) for p in game.pieces))
    return (game.turn, game.winner, pieces_state)

def get_piece_in_clone(cloned_game, original_piece):
    """
    Busca na cópia do jogo a peça correspondente à peça original, utilizando nome, jogador e posição.
    """
    for p in cloned_game.pieces:
        if p.name == original_piece.name and p.player == original_piece.player and p.x == original_piece.x and p.y == original_piece.y:
            return p
    return None

def get_ordered_moves(game, player):
    """
    Retorna uma lista ordenada de movimentos válidos para o jogador,
    priorizando os movimentos que levam a estados com melhor avaliação.
    """
    moves = []
    for piece in game.pieces:
        if piece.player == player:
            for (nx, ny) in game.get_valid_moves(piece):
                moves.append((piece, nx, ny))
    
    def move_score(move):
        piece, nx, ny = move
        new_game = game.clone_for_minimax()
        cloned_piece = get_piece_in_clone(new_game, piece)
        if cloned_piece is None:
            return 0
        new_game.move_piece(cloned_piece, nx, ny, simulate=True)
        return evaluate_impossible(new_game, player)
    
    moves.sort(key=move_score, reverse=True)
    return moves

def minimax(game, depth, alpha, beta, player):
    state_key = get_state_key(game)
    if state_key in transposition_table:
        return transposition_table[state_key], None

    # Caso base: profundidade máxima atingida ou jogo finalizado
    if depth == 0 or game.winner is not None:
        score = evaluate_impossible(game, player)
        transposition_table[state_key] = score
        return score, None

    best_move = None

    # Jogada do jogador maximizador
    if game.turn == player:
        best_eval = float('-inf')
        moves = get_ordered_moves(game, player)
        for piece, nx, ny in moves:
            new_game = game.clone_for_minimax()
            clone_piece = get_piece_in_clone(new_game, piece)
            if clone_piece is None:
                continue
            new_game.move_piece(clone_piece, nx, ny, simulate=True)
            eval_score, _ = minimax(new_game, depth - 1, alpha, beta, player)
            if eval_score > best_eval:
                best_eval = eval_score
                best_move = (piece, nx, ny)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Poda beta
        transposition_table[state_key] = best_eval
        return best_eval, best_move

    # Jogada do oponente (minimizador)
    else:
        best_eval = float('inf')
        moves = get_ordered_moves(game, game.turn)
        for piece, nx, ny in moves:
            new_game = game.clone_for_minimax()
            clone_piece = get_piece_in_clone(new_game, piece)
            if clone_piece is None:
                continue
            new_game.move_piece(clone_piece, nx, ny, simulate=True)
            eval_score, _ = minimax(new_game, depth - 1, alpha, beta, player)
            if eval_score < best_eval:
                best_eval = eval_score
                best_move = (piece, nx, ny)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Poda alfa
        transposition_table[state_key] = best_eval
        return best_eval, best_move

def get_best_move(game, depth=4):
    """
    Retorna o melhor movimento para o jogador cujo turno está ativo.
    Se não houver movimento identificado pelo minimax, tenta retornar
    o primeiro movimento válido encontrado (fallback).
    """
    current_player = game.turn
    score, move = minimax(game, depth, float('-inf'), float('inf'), current_player)
    if move is None:
        # Fallback: procurar o primeiro movimento válido entre as peças do jogador
        for piece in game.pieces:
            if piece.player == current_player:
                valid_moves = game.get_valid_moves(piece)
                if valid_moves:
                    return (piece, valid_moves[0][0], valid_moves[0][1])
        return None
    return move
