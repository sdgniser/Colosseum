import random
from copy import deepcopy
#from bots import get_player_bot_action, get_opponent_bot_action
from player1 import get_bot_action as get_player_bot_action
from player2 import get_bot_action as get_opponent_bot_action
from character_presets import CHARACTER_PRESETS, CLASS_SKILLS
from inventory_presets import BASE_INVENTORY, CLASS_STARTING_INVENTORY

class Character:
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
        
    def take_damage(self, damage): 
        self.hp = max(0, self.hp - damage)
    
    def heal(self, amount): 
        self.hp = min(self.max_hp, self.hp + amount)
    
    def defend(self): 
        self.is_defending = True
    
    def reset_defense(self): 
        self.is_defending = False
    
    def is_alive(self): 
        return self.hp > 0
    
    def use_skill_points(self, cost):
        if self.skill_points >= cost:
            self.skill_points -= cost
            return True
        return False
    
    def restore_skill_points(self):
        self.skill_points = self.max_skill_points

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
            self.take_damage(8 * stacks)
            self.status_effects["Poison"] -= 1
            if self.status_effects["Poison"] <= 0:
                del self.status_effects["Poison"]
            return stacks
        return 0

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

class InventoryManager:
    def __init__(self, character_class="Warrior"):
        self.items = self._get_starting_inventory(character_class)
    
    def _get_starting_inventory(self, character_class):
        """Get class-specific starting inventory"""
        if character_class in CLASS_STARTING_INVENTORY:
            # Create a deep copy to avoid modifying the original preset
            inventory = deepcopy(CLASS_STARTING_INVENTORY[character_class])
        else:
            inventory = deepcopy(BASE_INVENTORY)
        return inventory
    
    def get_item_count(self, item_name):
        """Get the count of a specific item"""
        if item_name in self.items:
            return self.items[item_name]["count"]
        return 0
    
    def use_item(self, item_name):
        """Use an item and decrement its count"""
        if item_name in self.items and self.items[item_name]["count"] > 0:
            self.items[item_name]["count"] -= 1
            return self.items[item_name]
        return None
    
    def add_item(self, item_name, count=1):
        """Add items to inventory"""
        if item_name in self.items:
            self.items[item_name]["count"] += count
        # If it's a new item, you could add it here
    
    def get_inventory_dict(self):
        """Return inventory as a simple count dictionary for rendering"""
        return {item: data["count"] for item, data in self.items.items()}
    
    def get_inventory_list(self):
        """Return list of available items (with count > 0)"""
        return [item for item, data in self.items.items() if data["count"] > 0]
    
    def reset_inventory(self, character_class):
        """Reset inventory for a new character"""
        self.items = self._get_starting_inventory(character_class)

class GameEngine:
    def __init__(self):
        self.mode = "menu"
        self.pve_menu_state = 'main'
        self.pvp_menu_state = 'main'
        self.player, self.opponent = None, None
        self.player_inventory = InventoryManager()
        self.opponent_inventory = InventoryManager()
        self.player_skills, self.opponent_skills = {}, {}
        self.turn_number, self.game_archive = 0, []
        self.player_turn, self.game_over = True, False
        self.game_over_message = ""
        self.action_message = "Welcome! Select a mode."
        self.character_presets = CHARACTER_PRESETS
        self.class_skills = CLASS_SKILLS
        self.setup_new_game()
        self.action_string = ""

    def setup_new_game(self):
        # Default characters if no selection made
        warrior_preset = self.character_presets[0]
        mage_preset = self.character_presets[1]
        
        self.player = Character(
            name="Player", 
            max_hp=warrior_preset["max_hp"],
            basic_attack_damage=warrior_preset["basic_attack_damage"],
            color=warrior_preset["color"],
            skill_points=warrior_preset["skill_points"],
            character_class="Warrior",
            defense=warrior_preset["defense"]
        )
        self.opponent = Character(
            name="Opponent Bot", 
            max_hp=mage_preset["max_hp"],
            basic_attack_damage=mage_preset["basic_attack_damage"],
            color=mage_preset["color"],
            skill_points=mage_preset["skill_points"],
            character_class="Mage",
            defense=mage_preset["defense"]
        )
        
        # Initialize inventories based on character classes
        self.player_inventory.reset_inventory(self.player.character_class)
        self.opponent_inventory.reset_inventory(self.opponent.character_class)
        
        # Assign class-specific skills
        self.player_skills = self.class_skills[self.player.character_class]
        self.opponent_skills = self.class_skills[self.opponent.character_class]
        
    def set_player_character(self, preset_index):
        preset = self.character_presets[preset_index]
        self.player = Character(
            name=preset["name"],
            max_hp=preset["max_hp"],
            basic_attack_damage=preset["basic_attack_damage"],
            color=preset["color"],
            skill_points=preset["skill_points"],
            character_class=preset["name"],
            defense=preset["defense"]
        )
        # Assign class-specific skills and inventory
        self.player_skills = self.class_skills[self.player.character_class]
        self.player_inventory.reset_inventory(self.player.character_class)
        
    def set_opponent_character(self, preset_index):
        preset = self.character_presets[preset_index]
        self.opponent = Character(
            name=preset["name"] + " Bot",
            max_hp=preset["max_hp"],
            basic_attack_damage=preset["basic_attack_damage"],
            color=preset["color"],
            skill_points=preset["skill_points"],
            character_class=preset["name"],
            defense=preset["defense"]
        )
        # Assign class-specific skills and inventory
        self.opponent_skills = self.class_skills[self.opponent.character_class]
        self.opponent_inventory.reset_inventory(self.opponent.character_class)

    def reset(self, mode="aivai"):
        self.mode, self.pve_menu_state = mode, 'main'
        self.pvp_menu_state = 'main'
        
        # Reset characters with their respective presets
        if mode == "pve":
            self.player.name = "Player"
            self.opponent.name = "Opponent Bot"
        elif mode == "pvp":
            self.player.name = "Player 1"
            self.opponent.name = "Player 2"
        else:  # aivai
            self.player.name = "Player Bot"
            self.opponent.name = "Opponent Bot"
            
        # Restore HP and skill points
        self.player.hp = self.player.max_hp
        self.player.is_defending = False
        self.player.restore_skill_points()
        
        self.opponent.hp = self.opponent.max_hp
        self.opponent.is_defending = False
        self.opponent.restore_skill_points()
        
        # Reset inventories based on character classes
        self.player_inventory.reset_inventory(self.player.character_class)
        self.opponent_inventory.reset_inventory(self.opponent.character_class)
        
        # Reassign class-specific skills
        self.player_skills = self.class_skills[self.player.character_class]
        self.opponent_skills = self.class_skills[self.opponent.character_class]
        
        self.turn_number, self.game_archive = 0, []
        self.player_turn, self.game_over = True, False
        self.game_over_message = ""
        self.action_message = "Battle Start!" if self.mode != 'menu' else "Welcome! Select a mode."

    def update(self, player_action=None):
        if self.game_over: return

        current_actor = self.player if self.player_turn else self.opponent

        # --- Update status effects except Poison (including Shadow Dodge) BEFORE applying their effects ---
        effects_to_update = [e for e in current_actor.status_effects if e != "Poison"]
        expired = []
        for effect in effects_to_update:
            current_actor.status_effects[effect] -= 1
            if current_actor.status_effects[effect] <= 0:
                expired.append(effect)
        for effect in expired:
            del current_actor.status_effects[effect]

        # --- Now apply Shadow Dodge effect (defense buff) ---
        current_actor.process_shadow_dodge()

        # --- Poison damage at the start of the affected character's turn only ---
        poison_message = ""
        if "Poison" in current_actor.status_effects:
            poison_stacks = current_actor.process_poison()
            if poison_stacks > 0:
                poison_message = f"{current_actor.name} takes {8 * poison_stacks} poison damage!"

        # Update other status effects (but NOT poison, which is handled above)
        # If you add more status effects, update them here:
        effects_to_update = [e for e in current_actor.status_effects if e != "Poison"]
        expired = []
        for effect in effects_to_update:
            current_actor.status_effects[effect] -= 1
            if current_actor.status_effects[effect] <= 0:
                expired.append(effect)
        for effect in expired:
            del current_actor.status_effects[effect]

        # PvE menu navigation
        if self.mode == 'pve' and self.player_turn and player_action and "NAV_" in player_action:
            if player_action == "NAV_SKILLS": self.pve_menu_state = 'skills'
            elif player_action == "NAV_ITEMS": self.pve_menu_state = 'items'
            elif player_action == "NAV_MAIN": self.pve_menu_state = 'main'
            self.action_message = "Choose an option..."
            return

        # PvP menu navigation (for both players)
        if self.mode == 'pvp' and player_action and "NAV_" in player_action:
            if player_action == "NAV_SKILLS": self.pvp_menu_state = 'skills'
            elif player_action == "NAV_ITEMS": self.pvp_menu_state = 'items'
            elif player_action == "NAV_MAIN": self.pvp_menu_state = 'main'
            self.action_message = "Choose an option..."
            return

        # PvP mode: both players use their own inventory/skills
        if self.mode == 'pvp':
            current_actor = self.player if self.player_turn else self.opponent
            current_target = self.opponent if self.player_turn else self.player
            inventory_manager = self.player_inventory if self.player_turn else self.opponent_inventory
            skills = self.player_skills if self.player_turn else self.opponent_skills
            action_string = player_action
            result_message = self._process_action(current_actor, current_target, inventory_manager, skills, action_string)
            # Check for insufficient SP message
            if result_message.startswith("Not enough skill points"):
                self.action_message = (poison_message + "\n" if poison_message else "") + result_message
                return
            self.action_message = (poison_message + "\n" if poison_message else "") + result_message
            self.player_turn = not self.player_turn
            self.pvp_menu_state = 'main'
            if not self.player.is_alive() or not self.opponent.is_alive():
                self.game_over = True
                winner = self.player if self.player.is_alive() else self.opponent
                self.game_over_message = f"{winner.name} Wins!"
            return

        # PvE and AI vs AI
        action_string, inventory_manager, skills = "", None, {}
        current_actor = self.player if self.player_turn else self.opponent
        current_target = self.opponent if self.player_turn else self.player
        
        if self.player_turn:
            self.turn_number += 1
            game_state = self._get_current_game_state_for_bot()
            inventory_manager = self.player_inventory
            skills = self.player_skills
            action_string = player_action if self.mode == "pve" else get_player_bot_action(game_state, self.game_archive)
        else:
            game_state = self._get_current_game_state_for_bot()
            inventory_manager = self.opponent_inventory
            skills = self.opponent_skills
            action_string = get_opponent_bot_action(game_state, self.game_archive)

        self.action_string = action_string
        
        turn = deepcopy(game_state)
        result_message = self._process_action(current_actor, current_target, inventory_manager, skills, action_string)
        # Check for insufficient SP message
        if self.player_turn and result_message.startswith("Not enough skill points"):
            self.action_message = (poison_message + "\n" if poison_message else "") + result_message
            return

        self.action_message = (poison_message + "\n" if poison_message else "") + result_message

        turn['action'] = [self.action_string, self.action_message]
        self.game_archive.append(turn)
        
        if self.player_turn and action_string:
            self.pve_menu_state = 'main'
            self.player_turn = False
        elif not self.player_turn:
            self.player_turn = True

        if not self.player.is_alive() or not self.opponent.is_alive():
            self.game_over = True
            winner = self.player if self.player.is_alive() else self.opponent
            self.game_over_message = f"{winner.name} Wins!"
        
    def _process_action(self, actor, target, inventory_manager, skills, action_string):
        if not action_string: return "Awaiting your command..."
        actor.reset_defense()
        parts = action_string.split(" ")
        action_type, action_subject = parts[0], " ".join(parts[1:])

        # Skill point restoration logic
        def restore_skill_points_for_action(actor, action_type):
            if action_type == "Defend" and actor.character_class == "Warrior":
                actor.skill_points = min(actor.max_skill_points, actor.skill_points + 1)
            elif action_type == "Attack":
                if actor.character_class == "Mage":
                    actor.skill_points = min(actor.max_skill_points, actor.skill_points + 2)
                elif actor.character_class == "Rogue":
                    actor.skill_points = min(actor.max_skill_points, actor.skill_points + 1)
        
        # Dodge logic
        def is_dodged(defender):
            return random.randint(1, 100) <= defender.defense

        if action_string == "Attack":
            restore_skill_points_for_action(actor, "Attack")
            if is_dodged(target):
                return f"{target.name} dodged the attack!"
            damage = random.randint(*actor.basic_attack_damage)
            damage //= 2 if target.is_defending else 1
            target.take_damage(damage)
            return f"{actor.name} attacked for {damage} damage!"
            
        elif action_string == "Defend":
            actor.defend()
            restore_skill_points_for_action(actor, "Defend")
            return f"{actor.name} is defending!"

        elif action_type == "Use" and action_subject in inventory_manager.items:
            item_data = inventory_manager.use_item(action_subject)
            if item_data:
                if item_data["effect"] == "heal":
                    actor.heal(item_data["value"])
                    return f"Used a {action_subject} and healed {item_data['value']} HP!"
                elif item_data["effect"] == "damage":
                    if is_dodged(target):
                        return f"{target.name} dodged the {action_subject}!"
                    damage = item_data["value"]
                    damage //= 2 if target.is_defending else 1
                    target.take_damage(damage)
                    return f"Used a {action_subject} for {damage} damage!"
                elif item_data["effect"] == "full_heal":
                    actor.hp = actor.max_hp
                    return f"Used an {action_subject}! HP fully restored!"
            return f"You have no {action_subject}s left!"
            
        elif action_type == "Cast" and action_subject in skills:
            skill = skills[action_subject]
            skill_cost = skill.get("cost", 0)
            
            # Check if actor has enough skill points
            if not actor.use_skill_points(skill_cost):
                return f"Not enough skill points to cast {action_subject}! Need {skill_cost}, have {actor.skill_points}."
            
            if "damage" in skill:
                if is_dodged(target):
                    return f"{target.name} dodged {action_subject}!"
                damage = random.randint(*skill["damage"])
                damage //= 2 if target.is_defending else 1
                target.take_damage(damage)
                # Poison Dart logic
                if action_subject == "Poison Dart":
                    if "Poison" in target.status_effects:
                        target.apply_poison(1)
                        return f"{actor.name} cast Poison Dart for {damage} damage! Poison stacks increased to {target.status_effects['Poison']}. (-{skill_cost} SP)"
                    else:
                        target.apply_poison(3)
                        return f"{actor.name} cast Poison Dart for {damage} damage! {target.name} is poisoned (3 stacks)! (-{skill_cost} SP)"
                return f"{actor.name} cast {action_subject} for {damage} damage! (-{skill_cost} SP)"
            if "heal" in skill:
                heal_amount = random.randint(*skill["heal"])
                actor.heal(heal_amount)
                return f"{actor.name} cast {action_subject} and healed {heal_amount} HP! (-{skill_cost} SP)"
            if "defense" in skill:
                # Shadow Dodge logic
                if action_subject == "Shadow Dodge":
                    actor.apply_status("Shadow Dodge", 1)
                    actor.defense = 100  # Apply the effect immediately
                    return f"{actor.name} used Shadow Dodge! Defense is maxed for 1 turn. (-{skill_cost} SP)"
                actor.defend()
                return f"{actor.name} cast {action_subject} and is ready to evade! (-{skill_cost} SP)"
        
        return f"{actor.name} tried an invalid action: '{action_string}'!"

    def _get_current_game_state_for_bot(self):
        return {
            "player": {
                "hp": self.player.hp, 
                "max_hp": self.player.max_hp,
                "skill_points": self.player.skill_points,
                "character_class": self.player.character_class
            },
            "opponent": {
                "hp": self.opponent.hp, 
                "max_hp": self.opponent.max_hp,
                "skill_points": self.opponent.skill_points,
                "character_class": self.opponent.character_class
            },
            "inventory": self.player_inventory.get_inventory_dict()
        }

    def get_state_for_rendering(self):
        # For PvP, show correct inventory/skills for current turn
        if self.mode == "pvp":
            if self.player_turn:
                inventory = self.player_inventory.get_inventory_dict()
                inventory_list = self.player_inventory.get_inventory_list()
                skills = self.player_skills
                current_character = self.player
            else:
                inventory = self.opponent_inventory.get_inventory_dict()
                inventory_list = self.opponent_inventory.get_inventory_list()
                skills = self.opponent_skills
                current_character = self.opponent
        else:
            inventory = self.player_inventory.get_inventory_dict()
            inventory_list = self.player_inventory.get_inventory_list()
            skills = self.player_skills
            current_character = self.player

        return {
            "mode": self.mode,
            "pve_menu_state": self.pve_menu_state,
            "pvp_menu_state": self.pvp_menu_state,
            "is_player_turn": self.player_turn,
            "player": {
                "name": self.player.name, 
                "hp": self.player.hp, 
                "max_hp": self.player.max_hp,
                "skill_points": self.player.skill_points,
                "max_skill_points": self.player.max_skill_points,
                "color": self.player.color,
                "character_class": self.player.character_class
            },
            "opponent": {
                "name": self.opponent.name, 
                "hp": self.opponent.hp, 
                "max_hp": self.opponent.max_hp,
                "skill_points": self.opponent.skill_points,
                "max_skill_points": self.opponent.max_skill_points,
                "color": self.opponent.color,
                "character_class": self.opponent.character_class
            },
            "current_character": current_character,
            "turn_number": self.turn_number,
            "message": self.action_message,
            "inventory": inventory,
            "inventory_list": inventory_list,
            "skills_list": list(skills.keys()),
            "skills_data": skills,
            "game_over": self.game_over,
            "game_over_message": self.game_over_message,
        }

    def is_game_over(self): 
        return self.game_over
        
    def is_player_turn(self): 
        return self.player_turn

