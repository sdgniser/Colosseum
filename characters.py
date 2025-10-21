import pygame

# --- Character Drawing Functions ---
# These functions are passed to the Character class
# so each character knows how to draw itself.

def draw_player_character(surface, pos, color):
    """Draws the player's circle character."""
    radius = 40
    # Draw the main circle
    pygame.draw.circle(surface, color, pos, radius)
    # Draw the outline
    pygame.draw.circle(surface, (0, 0, 0), pos, radius, 3)

def draw_opponent_character(surface, pos, color):
    """Draws the opponent's square character."""
    size = 80
    rect = pygame.Rect(pos[0] - size // 2, pos[1] - size // 2, size, size)
    # Draw the main square
    pygame.draw.rect(surface, color, rect)
    # Draw the outline
    pygame.draw.rect(surface, (0, 0, 0), rect, 3)


# --- Character Class ---

class Character:
    """
    A class to represent a combatant in the battle.
    
    Attributes:
        name (str): The character's display name.
        max_hp (int): The maximum health points.
        hp (int): The current health points.
        pos (tuple): The (x, y) coordinates for drawing.
        color (tuple): The (R, G, B) color of the character.
        draw_function (function): The function to call to draw the character.
        is_defending (bool): True if the character is defending this turn.
    """
    
    def __init__(self, name, max_hp, basic_attack_damage, color, skill_points, character_class, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.basic_attack_damage = basic_attack_damage
        self.color = color
        self.max_skill_points = skill_points
        self.skill_points = skill_points
        self.is_defending = False
        self.character_class = character_class
        self.base_defense = defense
        self.defense = defense
        self.status_effects = {}

    def draw(self, surface):
        """Calls the character's specific draw function."""
        self.draw_function(surface, self.pos, self.color)

    def take_damage(self, damage):
        """Reduces the character's HP by a given amount."""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        """Increases the character's HP, capped at max_hp."""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def defend(self):
        """Sets the character's state to defending."""
        self.is_defending = True

    def reset_defense(self):
        """Resets the character's defending state."""
        self.is_defending = False
    
    def is_alive(self):
        """Returns True if the character's HP is above 0."""
        return self.hp > 0
    
    def apply_status(self, effect_name, duration):
        """Apply a status effect for a given number of turns."""
        self.status_effects[effect_name] = duration

    def has_status(self, effect_name):
        return effect_name in self.status_effects

    def update_status_effects(self):
        """Reduce duration of all status effects by 1 turn, remove expired."""
        expired = []
        for effect in self.status_effects:
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                expired.append(effect)
        for effect in expired:
            del self.status_effects[effect]

    def clear_status(self, effect_name):
        if effect_name in self.status_effects:
            del self.status_effects[effect_name]

    def apply_poison(self, stacks):
        """Apply or increase poison stacks."""
        if "Poison" in self.status_effects:
            self.status_effects["Poison"] += stacks
        else:
            self.status_effects["Poison"] = stacks

    def process_poison(self):
        """Deal poison damage and reduce stacks by 1. Remove if 0."""
        if "Poison" in self.status_effects:
            stacks = self.status_effects["Poison"]
            self.take_damage(5 * stacks)
            self.status_effects["Poison"] -= 1
            if self.status_effects["Poison"] <= 0:
                del self.status_effects["Poison"]
            return stacks
        return 0
    
    def apply_status(self, effect_name, duration):
        self.status_effects[effect_name] = duration

    def update_status_effects(self):
        expired = []
        for effect in self.status_effects:
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                expired.append(effect)
        for effect in expired:
            del self.status_effects[effect]

    def process_shadow_dodge(self):
        """Set defense to 100 if Shadow Dodge is active, else restore base defense."""
        if "Shadow Dodge" in self.status_effects:
            self.defense = 100
        else:
            self.defense = self.base_defense