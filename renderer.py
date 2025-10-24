import pygame
import os
from character_presets import CHARACTER_PRESETS

PLAYER_POS = (200, 250); OPPONENT_POS = (600, 250)
PLAYER_COLOR = (50, 150, 255); OPPONENT_COLOR = (255, 80, 80)
WHITE = (255, 255, 255); BLACK = (0, 0, 0); GRAY = (100, 100, 100)
RED = (200, 0, 0); GREEN = (0, 200, 0); LIGHT_BLUE = (173, 216, 230)

class Renderer:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 72)
        # Layout rectangles
        self.battle_display_rect = pygame.Rect(50, 50, 700, 300)
        self.options_box_rect = pygame.Rect(50, 380, 700, 170)
        # Define button rects for PvE menus
        b_width = (self.options_box_rect.width - 60) // 2
        b_height = (self.options_box_rect.height - 50) // 2
        self.button_rects = [
            pygame.Rect(self.options_box_rect.left + 20, self.options_box_rect.top + 20, b_width, b_height),
            pygame.Rect(self.options_box_rect.left + 40 + b_width, self.options_box_rect.top + 20, b_width, b_height),
            pygame.Rect(self.options_box_rect.left + 20, self.options_box_rect.top + 30 + b_height, b_width, b_height),
            pygame.Rect(self.options_box_rect.left + 40 + b_width, self.options_box_rect.top + 30 + b_height, b_width, b_height)
        ]
        # Load sprites
        self.sprites = self._load_sprites()
    
    def _load_sprites(self):
        sprites = {}
        SPRITE_SIZE = (100, 100)  # Set desired size (width, height)
        for preset in CHARACTER_PRESETS:
            sprite_path = preset.get("sprite")
            if sprite_path and os.path.exists(sprite_path):
                img = pygame.image.load(sprite_path).convert_alpha()
                img = pygame.transform.smoothscale(img, SPRITE_SIZE)
                sprites[preset["name"]] = img
            else:
                sprites[preset["name"]] = None
        return sprites

    def draw_frame(self, screen, state):
        screen.fill(LIGHT_BLUE)
        self._draw_battle_scene(screen, state)
        # Draw appropriate menu based on game mode and state
        if state['mode'] == 'pve' and state['is_player_turn'] and not state['game_over']:
            menu_type = state['pve_menu_state']
            if menu_type == 'main': self._draw_main_buttons(screen, state)
            elif menu_type == 'skills': self._draw_skills_menu(screen, state['skills_list'], state['skills_data'])
            elif menu_type == 'items': self._draw_items_menu(screen, state['inventory'])
        elif state['mode'] == 'pvp' and not state['game_over']:
            menu_type = state['pvp_menu_state']
            if menu_type == 'main': self._draw_main_buttons(screen, state)
            elif menu_type == 'skills': self._draw_skills_menu(screen, state['skills_list'], state['skills_data'])
            elif menu_type == 'items': self._draw_items_menu(screen, state['inventory'])
        if state['game_over']: self._draw_game_over_screen(screen, state['game_over_message'])

    def draw_main_menu(self, screen):
        screen.fill(LIGHT_BLUE)
        title = self.large_font.render("NPC Colosseum", True, WHITE)
        pve = self.font.render("1: Player vs. AI", True, BLACK)
        aivai = self.font.render("2: AI vs. AI", True, BLACK)
        pvp = self.font.render("3: Player vs. Player", True, BLACK)
        screen.blit(title, title.get_rect(center=(screen.get_width()/2, 150)))
        screen.blit(pve, pve.get_rect(center=(screen.get_width()/2, 300)))
        screen.blit(aivai, aivai.get_rect(center=(screen.get_width()/2, 350)))
        screen.blit(pvp, pvp.get_rect(center=(screen.get_width()/2, 400)))

    def _draw_battle_scene(self, screen, state):
        pygame.draw.rect(screen, WHITE, self.battle_display_rect)
        pygame.draw.rect(screen, BLACK, self.battle_display_rect, 3)
        
        player_color = state['player'].get('color', PLAYER_COLOR)
        opponent_color = state['opponent'].get('color', OPPONENT_COLOR)
        player_class = state['player'].get('character_class', 'Warrior')
        opponent_class = state['opponent'].get('character_class', 'Mage')
        
        self._draw_character(screen, PLAYER_POS, player_color, False, player_class)
        self._draw_character_info(screen, state['player'], PLAYER_POS)
        self._draw_character(screen, OPPONENT_POS, opponent_color, True, opponent_class)
        self._draw_character_info(screen, state['opponent'], OPPONENT_POS)
        
        # Draw turn indicator for PvP mode
        if state['mode'] == 'pvp' and not state['game_over']:
            turn_text = "Player 1's Turn" if state['is_player_turn'] else "Player 2's Turn"
            turn_surf = self.small_font.render(turn_text, True, BLACK)
            screen.blit(turn_surf, (self.battle_display_rect.centerx - turn_surf.get_width()//2, self.battle_display_rect.top + 5))
        
        # Draw skill points for current character (bottom right)
        if state['mode'] in ['pve', 'pvp'] and not state['game_over']:
            self._draw_skill_points(screen, state['current_character'])
        
        msg = self.small_font.render(state['message'], True, BLACK)
        screen.blit(msg, msg.get_rect(centerx=self.battle_display_rect.centerx, y=self.battle_display_rect.top + 20))

    def _draw_main_buttons(self, screen, state=None):
        pygame.draw.rect(screen, WHITE, self.options_box_rect); pygame.draw.rect(screen, BLACK, self.options_box_rect, 3)
        actions = ["Attack", "Defend", "Skills", "Items"]
        for i, rect in enumerate(self.button_rects):
            self._draw_button(screen, rect, actions[i])
        
        # Show controls - same for both players in PvP
        if state and state['mode'] == 'pvp':
            controls = "A: Attack | D: Defend | S: Skills | I: Items"
        else:
            controls = "A: Attack | D: Defend | S: Skills | I: Items"
        
        self._draw_controls_text(screen, controls)

    def _draw_skills_menu(self, screen, skills_list, skills_data):
        pygame.draw.rect(screen, WHITE, self.options_box_rect); pygame.draw.rect(screen, BLACK, self.options_box_rect, 3)
        for i, rect in enumerate(self.button_rects):
            if i < len(skills_list):
                skill_name = skills_list[i]
                skill_cost = skills_data[skill_name].get("cost", 0)
                self._draw_button(screen, rect, skill_name, f"Cost: {skill_cost}")
        controls = "1-4: Select Skill | ESC: Back"
        self._draw_controls_text(screen, controls)

    def _draw_items_menu(self, screen, inventory):
        pygame.draw.rect(screen, WHITE, self.options_box_rect); pygame.draw.rect(screen, BLACK, self.options_box_rect, 3)
        items = list(inventory.keys())
        for i, rect in enumerate(self.button_rects):
            if i < len(items):
                item_name = items[i]
                count = inventory[item_name]
                self._draw_button(screen, rect, f"{item_name}", f"x{count}")
        controls = "1-4: Select Item | ESC: Back"
        self._draw_controls_text(screen, controls)

    def _draw_button(self, screen, rect, text, subtext=None):
        pygame.draw.rect(screen, GRAY, rect); pygame.draw.rect(screen, BLACK, rect, 2)
        y_offset = 0 if not subtext else -15
        text_surf = self.font.render(text, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=(rect.centerx, rect.centery + y_offset)))
        if subtext:
            sub_surf = self.small_font.render(subtext, True, BLACK)
            screen.blit(sub_surf, sub_surf.get_rect(center=(rect.centerx, rect.centery + 15)))

    def _draw_controls_text(self, screen, text):
        controls_surf = self.small_font.render(text, True, BLACK)
        screen.blit(controls_surf, (self.options_box_rect.left + 15, self.options_box_rect.bottom + 10))

    def _draw_character(self, s, pos, color, is_square, character_class=None):
        sprite = self.sprites.get(character_class)
        if sprite:
            # Flip player sprite horizontally (is_square == False means player)
            if not is_square:
                sprite = pygame.transform.flip(sprite, True, False)
            rect = sprite.get_rect(center=pos)
            s.blit(sprite, rect)
        else:
            # Fallback to shape if sprite missing
            if is_square:
                r = pygame.Rect(pos[0] - 40, pos[1] - 40, 80, 80); pygame.draw.rect(s, color, r); pygame.draw.rect(s, BLACK, r, 3)
            else:
                pygame.draw.circle(s, color, pos, 40); pygame.draw.circle(s, BLACK, pos, 40, 3)

    def _draw_character_info(self, screen, char_state, pos):
        text = f"{char_state['name']}: {max(0, char_state['hp'])}/{char_state['max_hp']}"
        text_surf = self.small_font.render(text, True, BLACK)
        # Increase the vertical offset for the info above the sprite
        GAP = 30  # You can adjust this value for more/less space
        text_rect = text_surf.get_rect(centerx=pos[0], y=pos[1] - 85 - GAP)
        screen.blit(text_surf, text_rect)
        self._draw_health_bar(screen, pos[0] - 75, text_rect.bottom + 5, 150, 20, char_state['hp'], char_state['max_hp'])

    def _draw_skill_points(self, screen, character):
        # Handle both dictionary and Character object
        if hasattr(character, 'skill_points'):  # It's a Character object
            sp_text = f"Skill Points: {character.skill_points}/{character.max_skill_points}"
        else:  # It's a dictionary
            sp_text = f"Skill Points: {character['skill_points']}/{character['max_skill_points']}"
        
        sp_surf = self.small_font.render(sp_text, True, BLACK)
        # Position in bottom right corner (as shown in the image reference)
        screen.blit(sp_surf, (screen.get_width() - sp_surf.get_width() - 20, screen.get_height() - 40))

    def _draw_health_bar(self, s, x, y, w, h, hp, max_hp):
        ratio = hp / max_hp if max_hp > 0 else 0
        pygame.draw.rect(s, RED, (x, y, w, h)); pygame.draw.rect(s, GREEN, (x, y, w * ratio, h)); pygame.draw.rect(s, BLACK, (x, y, w, h), 2)
        
    def _draw_game_over_screen(self, screen, message):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA); overlay.fill((0, 0, 0, 128)); screen.blit(overlay, (0, 0))
        text = self.large_font.render(message, True, WHITE); screen.blit(text, text.get_rect(center=(screen.get_width()/2, screen.get_height()/2 - 50)))
        restart = self.font.render("Press ENTER for Menu", True, WHITE); screen.blit(restart, restart.get_rect(center=(screen.get_width()/2, screen.get_height()/2 + 20)))
    
    def draw_character_selection(self, screen, presets, selected_idx, prompt="Select Your Character"):
        screen.fill(LIGHT_BLUE)
        title = self.large_font.render(prompt, True, WHITE)
        screen.blit(title, title.get_rect(center=(screen.get_width()/2, 100)))
        for i, preset in enumerate(presets):
            x = 200 + i * 200
            y = 250
            color = preset["color"]
            name = preset["name"]
            hp = preset["max_hp"]
            sp = preset["skill_points"]
            sprite = self.sprites.get(name)
            if sprite:
                rect = sprite.get_rect(center=(x, y))
                # Draw yellow outline if selected
                if i == selected_idx:
                    mask = pygame.mask.from_surface(sprite)
                    outline_points = mask.outline()
                    outline_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                    for point in outline_points:
                        # Draw the outline in yellow, slightly thicker
                        pygame.draw.circle(outline_surface, (255, 215, 0), point, 3)
                    # Blit the outline surface behind the sprite
                    screen.blit(outline_surface, rect)
                screen.blit(sprite, rect)
            else:
                pygame.draw.circle(screen, color, (x, y), 40)
            name_surf = self.font.render(name, True, BLACK)
            hp_surf = self.small_font.render(f"HP: {hp}", True, BLACK)
            sp_surf = self.small_font.render(f"SP: {sp}", True, BLACK)
            screen.blit(name_surf, name_surf.get_rect(center=(x, y + 60)))
            screen.blit(hp_surf, hp_surf.get_rect(center=(x, y + 90)))
            screen.blit(sp_surf, sp_surf.get_rect(center=(x, y + 110)))
        controls = "<-/->: Change | ENTER: Select"
        self._draw_controls_text(screen, controls)