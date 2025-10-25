import random


def get_bot_class():
    return 2

def get_bot_action(current_game_state, game_archive):
    """
    This is the AI for the player's character in AI vs AI mode.
    It receives the current state and the history of all previous states.
    It must return a valid action string.
    """
    player_hp = current_game_state['player']['hp']
    player_sp = current_game_state['player']['skill_points']
    inventory = current_game_state['inventory']
    
    # Simple Logic:
    # 1. If HP is low and has a Potion, heal.
    if player_hp < 80 and inventory.get("Potion", 0) > 0:
        return "Use Potion"
    
    if player_hp < 45 and inventory.get("Elixir", 0) > 0:
        return "Use Elixir"
    
    if player_hp < 120 and inventory.get("Ether", 0) > 0:
        return "Use Ether"

    # 2. If opponent is low HP and we have a bomb, finish them!
    if current_game_state['opponent']['hp'] < 40 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"

    if current_game_state['opponent'] == "Attack":
        return "Defend"

    if player_sp < 6:
        return "Attack"
    
        
    if random.random() < 0.10:
        return "Cast Backstab"

    if random.random() < 0.10:
        return "Cast Poison Dart"

    if random.random() < 0.10:
        return "Cast Shadow Dodge"

    if random.random() < 0.10:
        return "Cast Quick Strike"
    
    else:
        return "Attack"
