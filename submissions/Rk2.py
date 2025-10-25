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


    if (len(game_archive) ==2 or len(game_archive) ==20) and player_hp>100 and player_sp>3:
        return "Cast Poison Dart"

    if player_hp < 50 and inventory.get("Elixir",0) > 0:
        return "Use Elixir"
    
    if player_hp <50 and inventory.get("Elixir",0)==0 and inventory.get("Potion",0)>0:
        return "Use Potion"
    
    if player_hp< 40 and player_sp>3:
        return "Cast Shadow Dodge"

    if random.random() < 0.5 and player_sp > 3:
        return "Cast Backstab"
    
    if random.random() < 0.2 and player_sp > 2:
        return "Cast Quick Strike"
    
    if current_game_state['opponent']['hp'] < 200 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"
    
    if player_hp<80 and inventory.get("Potion",0) >0:
        return "Use Potion"
    
    else:
        return "Attack"
