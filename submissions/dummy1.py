import random


def get_bot_class():
    return 1

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
    if player_hp < 100 and inventory.get("Potion", 0) > 0:
        return "Use Potion"

    # 2. If opponent is low HP and we have a bomb, finish them!
    if current_game_state['opponent']['hp'] < 45 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"

    if player_sp < 6:
        return "Attack"
    
        
    if random.random() < 0.3:
        return "Cast Lightning Bolt"
    else:
        return "Attack"
