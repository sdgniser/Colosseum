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
    oppo_hp=current_game_state['opponent']['hp']
    oppo_sp=current_game_state['opponent']['skill_points']
    
    # Simple Logic:
    # 1. If HP is low and has a Potion, heal.

    if inventory.get("Bomb",0)==3:
        return "Use Bomb"
    
    if player_hp<=45 and inventory.get("Elixer",0)>0:
        return "Use Elixer"
    
    if player_hp <= 100 and inventory.get("Potion", 0) > 0:
        return "Use Potion"
    

    # 2. If opponent is low HP and we have a bomb, finish them!
    if current_game_state['opponent']['hp'] < 45 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"
    
    if player_sp>=10 and oppo_hp<=55:
        return "Cast Backstab"
    
    if current_game_state['opponent']['skill_points'] >=8 and (player_hp<=125 and player_hp>105):
        return "Defend"
    
    if player_sp>=4 and oppo_hp<=70:
        return "Cast Quick Strike"

    else:
        return "Attack"
