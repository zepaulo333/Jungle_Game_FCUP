import pygame
from game_optimized.main_files.config import *
from game_optimized.main_files.game import Game
from game_optimized.AI.ai_minimax_rand import get_best_move

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game()

        if game.winner is None:
            pygame.time.delay(500)  # Optional delay for visualization
            if game.turn == 1:
                move = get_best_move(game)
            elif game.turn == 2:
                move = get_best_move(game)
            if move is None:
                print("No valid moves available. Ending game.")
                running = False
            else:
                piece, nx, ny = move
                # Find the matching piece in the current game state.
                for p in game.pieces:
                    if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player:
                        game.move_piece(p, nx, ny)
                        break

        game.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
