import pygame
import sys
import importlib

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Fonts
title_font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 36)

# Load and scale the background image
try:
    background_image = pygame.image.load("images/lobby_background.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error loading background image: {e}")
    background_image = None

# Game modes and corresponding module paths
options = [
    ("Mode 1 - Player vs Player", "game_optimized.Player's.p_vs_p_main"),
    ("Mode 2 - Random vs Player", "game_optimized.Random.p_vs_rand_main"),
    ("Mode 3 - Random vs Random", "game_optimized.Random.rand_vs_rand_main"),
    ("Mode 4 - Ai vs Player", "game_optimized.AI.ai_vs_player"),
    ("Mode 5 - Ai vs Ai", "game_optimized.AI.ai_vs_ai_main"),
    ("Tutorial", "game_optimized.main_files.Tutorial")
]

# Calculate positions for buttons in the main menu
button_width = 500
button_height = 50
button_margin = 20
start_y = 150

buttons = []
for idx, (text, module_path) in enumerate(options):
    x = (WIDTH - button_width) // 2
    y = start_y + idx * (button_height + button_margin)
    rect = pygame.Rect(x, y, button_width, button_height)
    buttons.append((rect, text, module_path))

def draw_menu():
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(WHITE)
    screen.blit(overlay, (0, 0))
    
    title_text = title_font.render("Welcome to the Jungle Game!", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_text, title_rect)
    
    for rect, text, _ in buttons:
        pygame.draw.rect(screen, LIGHT_BLUE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surface = button_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    config_width, config_height = 100, 30
    config_button_rect = pygame.Rect(20, HEIGHT - config_height - 20, config_width, config_height)
    pygame.draw.rect(screen, LIGHT_BLUE, config_button_rect)
    pygame.draw.rect(screen, BLACK, config_button_rect, 2)
    config_text = button_font.render("Config", True, BLACK)
    config_text_rect = config_text.get_rect(center=config_button_rect.center)
    screen.blit(config_text, config_text_rect)
    
    pygame.display.flip()

def image_selection_menu():
    from game_optimized.main_files.images import update_images

    # Load preview images
    try:
        img_v1 = pygame.image.load("images/images_v1.png")
        img_v2 = pygame.image.load("images/images_v2.png")
    except Exception as e:
        print(f"Error loading preview images: {e}")
        return

    # Set preview dimensions using a larger width (same aspect ratio as background)
    preview_width = 300
    bg_width = background_image.get_width() if background_image else WIDTH
    bg_height = background_image.get_height() if background_image else HEIGHT
    preview_height = int(preview_width * bg_height / bg_width)
    
    img_v1 = pygame.transform.scale(img_v1, (preview_width, preview_height))
    img_v2 = pygame.transform.scale(img_v2, (preview_width, preview_height))
    
    # Position the images in a layout that fits the full 800x600 screen
    img_v1_rect = img_v1.get_rect(center=(WIDTH // 3, HEIGHT // 2))
    img_v2_rect = img_v2.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2))
    
    # Back button at the bottom center
    back_rect = pygame.Rect((WIDTH - 250) // 2, HEIGHT - 100, 250, 50)
    
    selecting = True
    while selecting:
        # Draw the full-screen background (800x600)
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        
        # Optional overlay (for consistent style with the main menu)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        # Title text at the top
        title = title_font.render("Select Your Animals", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Draw preview images
        screen.blit(img_v1, img_v1_rect)
        screen.blit(img_v2, img_v2_rect)
        
        # Draw Back button
        pygame.draw.rect(screen, LIGHT_BLUE, back_rect)
        pygame.draw.rect(screen, BLACK, back_rect, 2)
        back_text = button_font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if img_v1_rect.collidepoint(mouse_pos):
                    update_images("v1")
                    print("Selected Images v1")
                    selecting = False  # auto-return to main menu
                elif img_v2_rect.collidepoint(mouse_pos):
                    update_images("v2")
                    print("Selected Images v2")
                    selecting = False  # auto-return to main menu
                elif back_rect.collidepoint(mouse_pos):
                    selecting = False


def configuration_menu():
    config_running = True
    btn_width = 250
    btn_height = 50
    btn_margin = 20
    
    images_rect = pygame.Rect((WIDTH - btn_width) // 2, 150, btn_width, btn_height)
    back_rect = pygame.Rect((WIDTH - btn_width) // 2, 150 + btn_height + btn_margin, btn_width, btn_height)
    
    while config_running:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        config_title = title_font.render("Configuration", True, BLACK)
        config_title_rect = config_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(config_title, config_title_rect)
        
        pygame.draw.rect(screen, LIGHT_BLUE, images_rect)
        pygame.draw.rect(screen, BLACK, images_rect, 2)
        images_text = button_font.render("Images", True, BLACK)
        images_text_rect = images_text.get_rect(center=images_rect.center)
        screen.blit(images_text, images_text_rect)
        
        pygame.draw.rect(screen, LIGHT_BLUE, back_rect)
        pygame.draw.rect(screen, BLACK, back_rect, 2)
        back_text = button_font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if images_rect.collidepoint(mouse_pos):
                    image_selection_menu()
                elif back_rect.collidepoint(mouse_pos):
                    config_running = False

def difficulty_menu():
    difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard"), ("Impossible", "impossible")]
    diff_button_width = 300
    diff_button_height = 50
    diff_button_margin = 20
    diff_start_y = 150

    diff_buttons = []
    for idx, (text, level) in enumerate(difficulties):
        x = (WIDTH - diff_button_width) // 2
        y = diff_start_y + idx * (diff_button_height + diff_button_margin)
        rect = pygame.Rect(x, y, diff_button_width, diff_button_height)
        diff_buttons.append((rect, text, level))
    
    selecting = True
    while selecting:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        diff_title = title_font.render("Select Difficulty", True, BLACK)
        diff_title_rect = diff_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(diff_title, diff_title_rect)
        
        for rect, text, _ in diff_buttons:
            pygame.draw.rect(screen, LIGHT_BLUE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text_surface = button_font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for rect, text, level in diff_buttons:
                    if rect.collidepoint(mouse_pos):
                        return level
    return None

def launch_game(module_path, difficulty=None):
    try:
        game_module = importlib.import_module(module_path)
        if hasattr(game_module, "main"):
            if difficulty is not None:
                game_module.main(difficulty)
            else:
                game_module.main()
        else:
            print(f"No 'main' function found in module {module_path}")
    except ImportError as e:
        print(f"Error importing module {module_path}: {e}")

def main_menu():
    running = True
    clock = pygame.time.Clock()
    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                config_rect = pygame.Rect(20, HEIGHT - 30 - 20, 100, 30)
                if config_rect.collidepoint(mouse_pos):
                    configuration_menu()
                    continue

                for rect, text, module_path in buttons:
                    if rect.collidepoint(mouse_pos):
                        if text == "Tutorial":
                            import game_optimized.main_files.tutorial as tutorial
                            tutorial.tutorial_mode()
                        elif text == "Mode 4 - Ai vs Player":
                            difficulty = difficulty_menu()
                            if difficulty not in ("easy", "medium", "hard", "impossible"):
                                print("Invalid difficulty selected.")
                                continue
                            if difficulty == "easy":
                                from game_optimized.AI.eval_easy import evaluate_easy as chosen_eval
                            elif difficulty == "medium":
                                from game_optimized.AI.eval_medium import evaluate_medium as chosen_eval
                            elif difficulty == "hard":
                                from game_optimized.AI.eval_hard import evaluate_hard as chosen_eval
                            elif difficulty == "impossible":
                                from game_optimized.AI.eval_impossible import evaluate_impossible as chosen_eval
                            import game_optimized.AI.ai_vs_p_main as ai_vs_p_main
                            ai_vs_p_main.main(chosen_eval)
                        else:
                            launch_game(module_path)
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
