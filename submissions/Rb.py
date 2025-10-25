from random import random
from character_presets import CLASS_SKILLS


def get_bot_class():
    return 2

def get_bot_action(current_game_state, game_archive):
    """
    This is the AI for the opponent's character.
    A very simple bot that just attacks.
    """
    # This bot is not very smart. It just attacks every turn.
    #action = "Attack"
    player_hp = current_game_state['player']['hp']
    player_sp = current_game_state['player']['skill_points']
    inventory = current_game_state['inventory']
    
    
    # if len(game_archive) >= 2:
    #current_hp = current_game_state['opponent']['hp']
        # two_turns_ago = game_archive[-2]['opponent']['hp']
        # damage_taken_in_two_turns = two_turns_ago - current_hp
        # This only records damage taken in two turns idk wtf do I do with this shit.

    opponent_class = current_game_state['opponent']['character_class']
    opponent_skills = CLASS_SKILLS[opponent_class]
    
    opponent_sp = current_game_state['opponent']['skill_points']
    likely_actions = []

    if opponent_sp < 3:
        likely_actions.extend(["Attack", "Defend"])
    else:
        for skill, data in opponent_skills.items():
            if data.get("cost", 0) <= opponent_sp:
                likely_actions.append(f"Cast {skill}")    
    
    if current_game_state['opponent']['hp'] > 159 and player_sp > 5:
            return "Cast Poison Dart"
    
    if current_game_state['opponent']['hp'] < 241 and inventory.get("Bomb", 0) > 1:
            return "Use Bomb"
    
    if current_game_state['opponent']['hp'] < 65 and player_sp >= 3:
        return "Cast Poison Dart"
    
    if current_game_state['opponent']['hp'] < 41 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"


    if player_hp < 180 and inventory.get("Ether", 0) > 0:
        return "Use Ether"
    
    elif player_hp < 165 and inventory.get("Ether", 0) <= 0 and inventory.get("Potion", 0) > 0:
        return "Use Potion"
    
    elif player_hp < 120 and inventory.get("Potion", 0) <= 0 and inventory.get("Elixir") > 0:
        return "Use Elixir"
    
    if player_sp < 2:
        return "Attack"
    else:
        return "Cast Quick Strike"
       

    if opponent_class == "Warrior":
        if "Cast Power Strike" in likely_actions and player_hp < 51:
            return "Defend"
        if "Cast Shield Bash" in likely_actions and player_hp < 41:
            return "Defend"
        
        if "Cast Whirlwind" in likely_actions and player_hp < 46:
            return "Defend"        

    if opponent_class == "Mage":
        if "Cast Fireball" in likely_actions and player_hp < 56:
            return "Defend"
        if "Cast Ice Shard" in likely_actions and player_hp < 46:
            return "Defend"

        if "Cast Lightning Bolt" in likely_actions and player_hp < 71:
            return "Defend"
        
    if opponent_class == "Rogue":
        if "Cast Backstab" in likely_actions and player_hp < 61:
            return "Defend"
        if "Cast Quick Strike" in likely_actions and player_hp < 41:
            return "Defend"
        if "Cast Poison Dart" in likely_actions and player_hp < 46:
            return "Defend"


    
    


