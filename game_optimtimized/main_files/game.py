import pygame
from game_optimized.main_files.config import *
from game_optimized.main_files.board import draw_board, is_water
from game_optimized.main_files.piece import Piece

class Game:
    def __init__(self):
        self.pieces = self.create_pieces()
        self.selected_piece = None
        self.turn = 1  # Player 1 starts
        self.traps_1 = [(2, 8), (4, 8), (3, 7)]
        self.traps_2 = [(2, 0), (4, 0), (3, 1)]
        self.lair_1 = (3, 8)  # Lair for Player 1
        self.lair_2 = (3, 0)  # Lair for Player 2
        self.winner = None
        self.visualize = True

    def create_pieces(self):
        return [
            # Player 1 pieces
            Piece("tiger", 0, 8, 1),     
            Piece("lion", 6, 8, 1),       
            Piece("elephant", 0, 6, 1),   
            Piece("dog", 5, 7, 1),        
            Piece("wolf", 2, 6, 1),       
            Piece("cat", 1, 7, 1),        
            Piece("leopard", 4, 6, 1),    
            Piece("mouse", 6, 6, 1),      

            # Player 2 pieces
            Piece("lion", 0, 0, 2),       
            Piece("tiger", 6, 0, 2),      
            Piece("elephant", 6, 2, 2),   
            Piece("dog", 1, 1, 2),        
            Piece("wolf", 4, 2, 2),       
            Piece("cat", 5, 1, 2),        
            Piece("leopard", 2, 2, 2),    
            Piece("mouse", 0, 2, 2)       
        ]

    def is_valid_move(self, piece, x, y, check_only=False):
        # Check board boundaries based on the grid
        if not (0 <= x < BOARD_COLS and 0 <= y < BOARD_ROWS):
            return False

        # Prevent moving into own lair
        if piece.player == 1 and (x, y) == self.lair_1:
            return False
        if piece.player == 2 and (x, y) == self.lair_2:
            return False

        # Prevent other piece's then mouse entering the water
        if piece.name != "mouse" and is_water(x, y):
            return False

        # Determine if the target cell is an enemy trap
        enemy_trap = (x, y) in (self.traps_1 if piece.player == 1 else self.traps_2)

        # Check if there is already a piece on the target cell
        for p in self.pieces:
            if p.x == x and p.y == y:
                # Cannot move onto a cell occupied by a friendly piece
                if p.player == piece.player:
                    return False
                # Elephant cannot capture a mouse
                if piece.name == "elephant" and p.name == "mouse" and not enemy_trap:
                    return False
                # Mouse cannot leave water for land if starting from water, when there is another piece in the target cell
                if piece.name == "mouse" and is_water(piece.x, piece.y) and not is_water(x, y):
                    return False
                # If the enemy piece is on an enemy trap, allow capture regardless of hierarchy
                if enemy_trap:
                    return True
                # Otherwise, check hierarchy (mouse can capture elephant regardless)
                return Piece.hierarchy[piece.name] >= Piece.hierarchy[p.name] or (piece.name == "mouse" and p.name == "elephant")
        return True

    def get_valid_moves(self, piece):
        if piece is None:
            return []
        
        moves = []
        # Standard adjacent moves
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = piece.x + dx, piece.y + dy
            if self.is_valid_move(piece, new_x, new_y):
                moves.append((new_x, new_y))

        # Special case: Lion and Tiger jumping over water using dynamic jump length
        if piece.name in ["lion", "tiger"]:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                jump = 0
                cur_x, cur_y = piece.x, piece.y
                # Continue moving in the direction until a non-water tile is reached or out of bounds
                while True:
                    next_x = cur_x + dx
                    next_y = cur_y + dy
                    if not (0 <= next_x < BOARD_COLS and 0 <= next_y < BOARD_ROWS):
                        break
                    if not is_water(next_x, next_y):
                        break
                    jump += 1
                    cur_x, cur_y = next_x, next_y
                if jump > 0:
                    # Landing square: one tile beyond the water region
                    landing_x = piece.x + dx * (jump + 1)
                    landing_y = piece.y + dy * (jump + 1)
                    if 0 <= landing_x < BOARD_COLS and 0 <= landing_y < BOARD_ROWS:
                        # Check that no mouse is blocking any water tile in the jump path
                        path_clear = True
                        for i in range(1, jump + 1):
                            check_x = piece.x + dx * i
                            check_y = piece.y + dy * i
                            for p in self.pieces:
                                if p.x == check_x and p.y == check_y and p.name == "mouse":
                                    path_clear = False
                                    break
                            if not path_clear:
                                break
                        if path_clear and self.is_valid_move(piece, landing_x, landing_y):
                            moves.append((landing_x, landing_y))
        return moves


    def move_piece(self, piece, x, y, simulate=False):
        if (x, y) in self.get_valid_moves(piece):
            # Check victory by touching the enemy lair
            if piece.player == 1 and (x, y) == self.lair_2:
                piece.move(x, y)
                if not simulate:
                    draw_board([], self.traps_1, self.traps_2, self.lair_1, self.lair_2)
                    for p in self.pieces:
                        p.draw()
                    pygame.display.flip()
                    pygame.time.delay(1000)
                self.winner = 1
                return
            elif piece.player == 2 and (x, y) == self.lair_1:
                piece.move(x, y)
                if not simulate:
                    draw_board([], self.traps_1, self.traps_2, self.lair_1, self.lair_2)
                    for p in self.pieces:
                        p.draw()
                    pygame.display.flip()
                    pygame.time.delay(1000)
                self.winner = 2
                return
            else:
                # Regular move: capture enemy piece if present
                for p in self.pieces:
                    if p.x == x and p.y == y and p.player != piece.player:
                        self.pieces.remove(p)
                        break
                piece.move(x, y)
                self.turn = 3 - self.turn
                self.selected_piece = None

            # End game if one side has no animals left
            if not any(p.player == (3 - piece.player) for p in self.pieces):
                self.winner = piece.player
            else:
                # If the current player's pieces have no legal moves across all pieces, declare victory for the opponent
                if not any(self.get_valid_moves(p) for p in self.pieces if p.player == self.turn):
                    self.winner = 3 - self.turn



    def draw(self):
        if not self.visualize:
            return
        highlighted = self.get_valid_moves(self.selected_piece) if self.selected_piece else []
        draw_board(highlighted, self.traps_1, self.traps_2, self.lair_1, self.lair_2)
        for piece in self.pieces:
            piece.draw()
        font = pygame.font.Font(None, 36)
        if self.winner in [1,2]:
            msg = f"Player {self.winner} wins! Press R to reset."
            text = font.render(msg, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, MARGIN_TOP + BOARD_HEIGHT // 2))
        else:
            msg = f"Next Player: {self.turn}"
            text = font.render(msg, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, MARGIN_TOP + BOARD_HEIGHT + INFO_HEIGHT // 2))
        SCREEN.blit(text, text_rect)

    # Used by minimax
    def clone_for_minimax(self):
        new_game = Game()
        new_game.pieces = [Piece(p.name, p.x, p.y, p.player) for p in self.pieces]
        new_game.winner = self.winner
        new_game.turn = self.turn
        new_game.traps_1 = self.traps_1
        new_game.traps_2 = self.traps_2
        new_game.lair_1 = self.lair_1
        new_game.lair_2 = self.lair_2
        return new_game