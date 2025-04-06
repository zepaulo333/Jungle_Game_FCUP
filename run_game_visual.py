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
    preview_width = 900
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
    volume_title_pos = (WIDTH // 2, 250 + btn_margin)

    # Volume buttons
    vol_btn_size = 50
    vol_minus_rect = pygame.Rect(WIDTH // 2 - 75, 300, vol_btn_size, vol_btn_size)
    vol_plus_rect = pygame.Rect(WIDTH // 2 + 25, 300, vol_btn_size, vol_btn_size)

    # Som ativado/desativado button
    sound_button_rect = pygame.Rect((WIDTH - btn_width) // 2, 380, btn_width, btn_height)
    
    # State variable for sound (True for on, False for off)
    sound_on = True

    # Back button
    back_rect = pygame.Rect((WIDTH - btn_width) // 2, 460, btn_width, btn_height)

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

        # Images button
        pygame.draw.rect(screen, LIGHT_BLUE, images_rect)
        pygame.draw.rect(screen, BLACK, images_rect, 2)
        images_text = button_font.render("Images", True, BLACK)
        images_text_rect = images_text.get_rect(center=images_rect.center)
        screen.blit(images_text, images_text_rect)

        # Volume title
        vol_title = button_font.render("Volume", True, BLACK)
        vol_title_rect = vol_title.get_rect(center=volume_title_pos)
        screen.blit(vol_title, vol_title_rect)

        # Volume buttons
        pygame.draw.rect(screen, LIGHT_BLUE, vol_minus_rect)
        pygame.draw.rect(screen, BLACK, vol_minus_rect, 2)
        minus_text = button_font.render("-", True, BLACK)
        minus_rect = minus_text.get_rect(center=vol_minus_rect.center)
        screen.blit(minus_text, minus_rect)

        pygame.draw.rect(screen, LIGHT_BLUE, vol_plus_rect)
        pygame.draw.rect(screen, BLACK, vol_plus_rect, 2)
        plus_text = button_font.render("+", True, BLACK)
        plus_rect = plus_text.get_rect(center=vol_plus_rect.center)
        screen.blit(plus_text, plus_rect)

        # Volume value display
        current_volume = pygame.mixer.music.get_volume()
        vol_value_text = button_font.render(f"{int(current_volume * 100)}%", True, BLACK)
        vol_value_rect = vol_value_text.get_rect(center=(WIDTH // 2, 330))
        screen.blit(vol_value_text, vol_value_rect)

        # Sound ON/OFF button
        sound_text = "Sound: ON" if sound_on else "Sound: OFF"
        pygame.draw.rect(screen, LIGHT_BLUE, sound_button_rect)
        pygame.draw.rect(screen, BLACK, sound_button_rect, 2)
        sound_text_surface = button_font.render(sound_text, True, BLACK)
        sound_text_rect = sound_text_surface.get_rect(center=sound_button_rect.center)
        screen.blit(sound_text_surface, sound_text_rect)

        # Back button
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
                elif vol_minus_rect.collidepoint(mouse_pos):
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = max(0.0, round(current_volume - 0.05, 2))
                    pygame.mixer.music.set_volume(new_volume)
                elif vol_plus_rect.collidepoint(mouse_pos):
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = min(1.0, round(current_volume + 0.05, 2))
                    pygame.mixer.music.set_volume(new_volume)
                elif sound_button_rect.collidepoint(mouse_pos):
                    # Toggle sound on/off
                    sound_on = not sound_on
                    if sound_on:
                        pygame.mixer.music.unpause()  # Resume music if turned on
                    else:
                        pygame.mixer.music.pause()  # Pause music if turned off
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
        # Trocar a música do menu pela música do jogo
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load("sounds/game_sound.mp3")  # Música da gameplay
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as music_err:
            print(f"Error loading gameplay music: {music_err}")

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
                            import game_optimized.AI.ai_vs_p_main as ai_vs_player
                            ai_vs_player.main(chosen_eval)
                        else:
                            launch_game(module_path)
        clock.tick(60)

if __name__ == "__main__":
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/home_screen_sound.mp3")  # Altere para o caminho da tua música
        pygame.mixer.music.set_volume(0.31)  # Volume suave
        pygame.mixer.music.play(-1)  # -1 para repetir continuamente
    except Exception as e:
        print(f"Error loading background music: {e}")

    main_menu()

