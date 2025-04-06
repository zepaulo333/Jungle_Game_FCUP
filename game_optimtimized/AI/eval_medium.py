from game_optimized.main_files.piece import Piece

# High/low values representing a win/loss.
WIN_SCORE = 100000
LOSS_SCORE = -100000

def evaluate_medium(game, player):
    # If the game is already won/lost, return the terminal score.
    if game.winner is not None:
        return WIN_SCORE if game.winner == player else LOSS_SCORE

    score = 0

    # Determine which traps and lairs correspond to which player.
    if player == 1:
        opp_traps = game.traps_2    # our pieces are weakened if on enemy traps
        own_traps = game.traps_1    # enemy pieces are weakened if on our traps
        opp_den = game.lair_2       # target for our pieces
        own_den = game.lair_1       # danger for our pieces (enemy targets our den)
    else:
        opp_traps = game.traps_1
        own_traps = game.traps_2
        opp_den = game.lair_1
        own_den = game.lair_2

    # Parameters for weighting different aspects.
    max_distance = 11
    factor_distance = 0.5     # weight for the Manhattan distance
    factor_mobility = 0.3     # weight for mobility (number of valid moves)
    capture_factor = 0.3      # bonus for having a capture move available
    threat_factor = 0.2       # penalty/bonus if a piece is threatened

    # Helper function: returns the effective value of a piece.
    # Pieces on a trap (from the opponent's perspective) are weakened (value 0).
    def effective_value(piece, traps):
        if (piece.x, piece.y) in traps:
            return 0
        elif piece.name == "mouse":
            return 5
        else:
            return Piece.hierarchy[piece.name]

    # Helper function: returns True if the given piece is threatened
    # (i.e. if any enemy piece can move to its current square).
    def is_threatened(piece):
        for other in game.pieces:
            if other.player != piece.player:
                if (piece.x, piece.y) in game.get_valid_moves(other):
                    return True
        return False

    # Iterate over all pieces and compute an evaluation score for each.
    for piece in game.pieces:
        # Determine the effective value and distance bonus.
        if piece.player == player:
            # For our own pieces, a piece is less valuable if it is on an enemy trap.
            ev = effective_value(piece, opp_traps)
            # Closer to the opponent's lair is better.
            distance = abs(piece.x - opp_den[0]) + abs(piece.y - opp_den[1])
            bonus_distance = (max_distance - distance) * factor_distance
        else:
            # For enemy pieces, use our traps to reduce their value.
            ev = effective_value(piece, own_traps)
            # For enemy pieces, being closer to our den is more dangerous.
            distance = abs(piece.x - own_den[0]) + abs(piece.y - own_den[1])
            bonus_distance = -(max_distance - distance) * factor_distance

        # Mobility bonus: more legal moves increases the score.
        mobility = len(game.get_valid_moves(piece))
        bonus_mobility = mobility * factor_mobility

        # Capture potential: if a piece (whether ours or enemy) can capture an opponent piece,
        # add (or subtract) a bonus proportional to the target’s effective value.
        capture_bonus = 0
        capturable = set()  # to avoid double counting the same enemy piece
        for move in game.get_valid_moves(piece):
            for enemy in game.pieces:
                if enemy.player != piece.player and (enemy.x, enemy.y) == move:
                    capturable.add(enemy)
        for enemy in capturable:
            # For enemy pieces, use our traps for evaluation.
            enemy_ev = effective_value(enemy, own_traps)
            capture_bonus += enemy_ev * capture_factor

        # Threat adjustment: subtract a bonus for our piece if threatened;
        # add bonus if an enemy piece is threatened.
        threat_adjustment = 0
        if piece.player == player:
            if is_threatened(piece):
                threat_adjustment -= ev * threat_factor
        else:
            if is_threatened(piece):
                threat_adjustment += ev * threat_factor

        # Combine all factors into the piece's contribution.
        piece_score = ev + bonus_distance + bonus_mobility + capture_bonus + threat_adjustment

        # Sum up the score (own pieces add, enemy pieces subtract).
        if piece.player == player:
            score += piece_score
        else:
            score -= piece_score

    return score
