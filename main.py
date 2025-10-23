import pygame
import time
from sys import argv
from game_engine import GameEngine
from renderer import Renderer
from character_presets import CHARACTER_PRESETS
from player1 import get_bot_class as get_player_bot_class
from player2 import get_bot_class as get_opponent_bot_class

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
AI_UPDATE_INTERVAL = 0.75 # Seconds between AI actions

def run_game():
    """Initializes Pygame and runs the main game loop, handling different game modes."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("NPC Colosseum")
    clock = pygame.time.Clock()
    
    engine = GameEngine()
    renderer = Renderer()

    running = True
    last_ai_update_time = time.time()

    selected_character_idx = 0
    selected_character = None
    pvp_select_stage = 0 # 0: Player 1 select, 1: Player 2 select
    pvp_p1_character = None
    pvp_p2_character = None

    while running:
        current_state = engine.get_state_for_rendering()
        mode = current_state['mode']
        pve_menu = current_state.get('pve_menu_state', 'main')
        pvp_menu = current_state.get('pvp_menu_state', 'main')

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Menu Input ---
            if mode == 'menu':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        mode = 'select_character'
                        engine.mode = 'select_character'
                    elif event.key == pygame.K_2:
                        # AI vs AI mode - set default characters
                        player_class_num = get_player_bot_class()
                        opponent_class_num = get_opponent_bot_class()
                        if player_class_num not in range(3):
                            raise ValueError(f"Improper Class value of '{player_class_num}' for player 1")
                        if opponent_class_num not in range(3):
                            raise ValueError(f"Improper Class value of '{opponent_class_num}' for player 2")

                        engine.set_player_character(player_class_num)
                        engine.set_opponent_character(opponent_class_num)
                        engine.reset(mode="aivai")
                    elif event.key == pygame.K_3:
                        mode = 'pvp_select_character'
                        engine.mode = 'pvp_select_character'
                        pvp_select_stage = 0
                        selected_character_idx = 0
            
            # --- PvE Character Selection ---
            elif mode == 'select_character':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        selected_character_idx = (selected_character_idx + 1) % len(CHARACTER_PRESETS)
                    elif event.key == pygame.K_LEFT:
                        selected_character_idx = (selected_character_idx - 1) % len(CHARACTER_PRESETS)
                    elif event.key == pygame.K_RETURN:
                        # Set player character and reset game
                        engine.set_player_character(selected_character_idx)

                        opponent_class_num = get_opponent_bot_class()
                        if opponent_class_num not in range(3):
                            raise ValueError(f"Improper Class value of '{opponent_class_num}' for player 2")
                        engine.set_opponent_character(opponent_class_num)
                        engine.reset(mode="pve")
                        mode = 'pve'
                        engine.mode = 'pve'
            
            # --- PvP Character Selection ---
            elif mode == 'pvp_select_character':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        selected_character_idx = (selected_character_idx + 1) % len(CHARACTER_PRESETS)
                    elif event.key == pygame.K_LEFT:
                        selected_character_idx = (selected_character_idx - 1) % len(CHARACTER_PRESETS)
                    elif event.key == pygame.K_RETURN:
                        if pvp_select_stage == 0:
                            pvp_p1_character = CHARACTER_PRESETS[selected_character_idx]
                            pvp_select_stage = 1
                            selected_character_idx = 0
                        else:
                            pvp_p2_character = CHARACTER_PRESETS[selected_character_idx]
                            # Set both characters and reset game
                            engine.set_player_character(CHARACTER_PRESETS.index(pvp_p1_character))
                            engine.set_opponent_character(CHARACTER_PRESETS.index(pvp_p2_character))
                            engine.reset(mode="pvp")
                            mode = 'pvp'
                            engine.mode = 'pvp'

            # --- Battle Input ---
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and engine.is_game_over():
                        engine.reset(mode="menu")
                    
                    # Player action in PvE mode
                    if mode == 'pve' and engine.is_player_turn() and not engine.is_game_over():
                        action = None
                        # Input changes based on which sub-menu is open
                        if pve_menu == 'main':
                            if event.key == pygame.K_a: action = "Attack"
                            elif event.key == pygame.K_d: action = "Defend"
                            elif event.key == pygame.K_s: action = "NAV_SKILLS" # Navigation action
                            elif event.key == pygame.K_i: action = "NAV_ITEMS"  # Navigation action
                        
                        elif pve_menu == 'skills':
                            # Get available skills from current state
                            skills = current_state['skills_list']
                            if event.key == pygame.K_1 and len(skills) > 0: action = f"Cast {skills[0]}"
                            elif event.key == pygame.K_2 and len(skills) > 1: action = f"Cast {skills[1]}"
                            elif event.key == pygame.K_3 and len(skills) > 2: action = f"Cast {skills[2]}"
                            elif event.key == pygame.K_4 and len(skills) > 3: action = f"Cast {skills[3]}"
                            elif event.key == pygame.K_5 and len(skills) > 4: action = f"Cast {skills[4]}"
                            elif event.key == pygame.K_6 and len(skills) > 5: action = f"Cast {skills[5]}"
                            elif event.key == pygame.K_ESCAPE: action = "NAV_MAIN"

                        elif pve_menu == 'items':
                            # Get item names from the state to map keys correctly
                            items = current_state['inventory_list']
                            if event.key == pygame.K_1 and len(items) > 0: action = f"Use {items[0]}"
                            elif event.key == pygame.K_2 and len(items) > 1: action = f"Use {items[1]}"
                            elif event.key == pygame.K_3 and len(items) > 2: action = f"Use {items[2]}"
                            elif event.key == pygame.K_4 and len(items) > 3: action = f"Use {items[3]}"
                            elif event.key == pygame.K_ESCAPE: action = "NAV_MAIN"

                        if action:
                            engine.update(player_action=action)
                            last_ai_update_time = time.time()

                    # Player action in PvP mode - SAME KEYS FOR BOTH PLAYERS
                    if mode == 'pvp' and not engine.is_game_over():
                        action = None
                        current_player = "Player 1" if engine.is_player_turn() else "Player 2"
                        
                        # Both players use the same keys
                        if pvp_menu == 'main':
                            if event.key == pygame.K_a: action = "Attack"
                            elif event.key == pygame.K_d: action = "Defend"
                            elif event.key == pygame.K_s: action = "NAV_SKILLS"
                            elif event.key == pygame.K_i: action = "NAV_ITEMS"
                        elif pvp_menu == 'skills':
                            skills = current_state['skills_list']
                            if event.key == pygame.K_1 and len(skills) > 0: action = f"Cast {skills[0]}"
                            elif event.key == pygame.K_2 and len(skills) > 1: action = f"Cast {skills[1]}"
                            elif event.key == pygame.K_3 and len(skills) > 2: action = f"Cast {skills[2]}"
                            elif event.key == pygame.K_4 and len(skills) > 3: action = f"Cast {skills[3]}"
                            elif event.key == pygame.K_5 and len(skills) > 4: action = f"Cast {skills[4]}"
                            elif event.key == pygame.K_6 and len(skills) > 5: action = f"Cast {skills[5]}"
                            elif event.key == pygame.K_ESCAPE: action = "NAV_MAIN"
                        elif pvp_menu == 'items':
                            items = current_state['inventory_list']
                            if event.key == pygame.K_1 and len(items) > 0: action = f"Use {items[0]}"
                            elif event.key == pygame.K_2 and len(items) > 1: action = f"Use {items[1]}"
                            elif event.key == pygame.K_3 and len(items) > 2: action = f"Use {items[2]}"
                            elif event.key == pygame.K_4 and len(items) > 3: action = f"Use {items[3]}"
                            elif event.key == pygame.K_ESCAPE: action = "NAV_MAIN"
                        
                        if action:
                            print(f"{current_player} action: {action}")  # Debug print
                            engine.update(player_action=action)
                            last_ai_update_time = time.time()

        # --- AI Logic Update (Time-based) ---
        if not engine.is_game_over() and mode != 'menu':
            is_ai_turn = (mode == 'aivai') or (mode == 'pve' and not engine.is_player_turn())
            current_time = time.time()
            if is_ai_turn and (current_time - last_ai_update_time > AI_UPDATE_INTERVAL):
                engine.update()
                last_ai_update_time = current_time

        # --- Drawing ---
        if mode == 'menu':
            renderer.draw_main_menu(screen)
        elif mode == 'select_character':
            renderer.draw_character_selection(screen, CHARACTER_PRESETS, selected_character_idx)
        elif mode == 'pvp_select_character':
            if pvp_select_stage == 0:
                renderer.draw_character_selection(screen, CHARACTER_PRESETS, selected_character_idx, prompt="Player 1: Select Your Character")
            else:
                renderer.draw_character_selection(screen, CHARACTER_PRESETS, selected_character_idx, prompt="Player 2: Select Your Character")
        else:
            renderer.draw_frame(screen, current_state)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    run_game()
