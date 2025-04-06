from game_optimized.main_files.piece import Piece
from game_optimized.main_files.board import is_water

# Constants for win/loss scores
WIN_SCORE = 10000
LOSS_SCORE = -10000
MAX_DISTANCE = 11  # Maximum Manhattan distance on the 7x9 board
BOARD_COLS, BOARD_ROWS = 7, 9  # From config.py

# Weights for various evaluation components (tunable)
WEIGHT_PIECE_VALUE = 1.0
WEIGHT_DISTANCE = 0.5
WEIGHT_MOBILITY = 0.3
WEIGHT_TRAP_CONTROL = 0.2
WEIGHT_LAIR_DEFENSE = 1.0
WEIGHT_MOUSE_POSITION = 0.1
WEIGHT_PIECE_PROTECTION = 0.1
WEIGHT_CENTRAL_CONTROL = 0.05

def get_adjacent_positions(x, y):
    """Return list of adjacent positions within board boundaries."""
    return [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if 0 <= x + dx < BOARD_COLS and 0 <= y + dy < BOARD_ROWS]

def evaluate_hard(game, player):
    """
    Evaluate the game state from the perspective of the given player.
    Returns a score where higher is better for the player.
    """
    # Check for win/loss conditions
    if game.winner is not None:
        return WIN_SCORE if game.winner == player else LOSS_SCORE

    score = 0

    # Determine player-specific board elements
    if player == 1:
        opp_traps = game.traps_2
        own_traps = game.traps_1
        opp_den = game.lair_2  # (3, 0)
        own_den = game.lair_1  # (3, 8)
    else:
        opp_traps = game.traps_1
        own_traps = game.traps_2
        opp_den = game.lair_1  # (3, 8)
        own_den = game.lair_2  # (3, 0)

    # 1. Piece Values and Distance to Lair
    for piece in game.pieces:
        # Piece value adjusted for traps
        is_on_opp_trap = (piece.x, piece.y) in (opp_traps if piece.player == player else own_traps)
        effective_value = 0 if is_on_opp_trap else Piece.hierarchy[piece.name]

        # Distance component
        if piece.player == player:
            distance = abs(piece.x - opp_den[0]) + abs(piece.y - opp_den[1])
            bonus_distance = (MAX_DISTANCE - distance) * WEIGHT_DISTANCE
            score += effective_value * WEIGHT_PIECE_VALUE + bonus_distance
        else:
            distance = abs(piece.x - own_den[0]) + abs(piece.y - own_den[1])
            bonus_distance = (MAX_DISTANCE - distance) * WEIGHT_DISTANCE
            score -= effective_value * WEIGHT_PIECE_VALUE + bonus_distance

    # 2. Mobility
    for piece in game.pieces:
        mobility = len(game.get_valid_moves(piece))
        if piece.player == player:
            score += mobility * WEIGHT_MOBILITY
        else:
            score -= mobility * WEIGHT_MOBILITY

    # 3. Trap Control
    for trap in opp_traps:
        adjacent = get_adjacent_positions(trap[0], trap[1])
        control = sum(1 for pos in adjacent for p in game.pieces
                      if p.player == player and (p.x, p.y) == pos)
        score += control * WEIGHT_TRAP_CONTROL

    for trap in own_traps:
        adjacent = get_adjacent_positions(trap[0], trap[1])
        control = sum(1 for pos in adjacent for p in game.pieces
                      if p.player != player and (p.x, p.y) == pos)
        score -= control * WEIGHT_TRAP_CONTROL

    # 4. Lair Defense Penalty
    opp_pieces = [p for p in game.pieces if p.player != player]
    if opp_pieces:
        min_opp_distance = min(abs(p.x - own_den[0]) + abs(p.y - own_den[1]) for p in opp_pieces)
        penalty = (MAX_DISTANCE - min_opp_distance) * WEIGHT_LAIR_DEFENSE
        score -= penalty

    # 5. Mouse Positioning
    player_mouse = next((p for p in game.pieces if p.player == player and p.name == "mouse"), None)
    if player_mouse:
        if is_water(player_mouse.x, player_mouse.y):
            score += WEIGHT_MOUSE_POSITION
        for p in game.pieces:
            if (p.player != player and p.name == "elephant" and
                abs(p.x - player_mouse.x) + abs(p.y - player_mouse.y) == 1):
                score += WEIGHT_MOUSE_POSITION

    opp_mouse = next((p for p in game.pieces if p.player != player and p.name == "mouse"), None)
    if opp_mouse:
        if is_water(opp_mouse.x, opp_mouse.y):
            score -= WEIGHT_MOUSE_POSITION
        for p in game.pieces:
            if (p.player == player and p.name == "elephant" and
                abs(p.x - opp_mouse.x) + abs(p.y - opp_mouse.y) == 1):
                score -= WEIGHT_MOUSE_POSITION

    # 6. Piece Protection
    for piece in game.pieces:
        adjacent = get_adjacent_positions(piece.x, piece.y)
        if piece.player == player:
            protectors = sum(1 for pos in adjacent for p in game.pieces
                             if p.player == player and (p.x, p.y) == pos)
            score += protectors * WEIGHT_PIECE_PROTECTION
        else:
            protectors = sum(1 for pos in adjacent for p in game.pieces
                             if p.player != player and (p.x, p.y) == pos)
            score -= protectors * WEIGHT_PIECE_PROTECTION

    # 7. Central Control
    central_squares = [(x, y) for x in range(BOARD_COLS) for y in range(BOARD_ROWS)
                       if not is_water(x, y) and any(is_water(nx, ny) for nx, ny in get_adjacent_positions(x, y))]
    for pos in central_squares:
        for p in game.pieces:
            if (p.x, p.y) == pos:
                score += WEIGHT_CENTRAL_CONTROL if p.player == player else -WEIGHT_CENTRAL_CONTROL

    return score