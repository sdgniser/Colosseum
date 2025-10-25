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
    if player_hp > 150 and current_game_state['opponent']['hp'] >= 160 and player_sp >= 5:
        return "Cast Poison Dart"
    
    if player_hp <= 150 and player_hp > 100 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"
    
    if player_hp > 100 and player_sp >= 4:
        return "Cast Backstab"
    
    if player_hp > 100 and current_game_state['opponent']['hp'] <= 100 and player_sp >= 2:
        return "Cast Quick Strike"
    if player_hp >=100:
        return "Attack"
    
    if player_hp < 100 and player_hp >= 75 and inventory.get("Ether", 0) > 0:
        return "Use Ether"
    
    if player_hp >= 75:
        return "Attack"
    
    if player_hp < 75 and player_hp > 50 and inventory.get("Potion", 0) > 0:
        return "Use Potion"
    
    if player_hp >= 50:
        return "Attack"
    
    if player_hp < 50 and inventory.get("Elixir", 0) > 0:
        return "Use Elixir"

    if random.random() < 0.5:
        if player_sp >= 2:
            return  "Cast Quick Strike"
    else:
        return "Attack"
    
    
