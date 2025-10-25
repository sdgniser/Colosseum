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
    opp_hp = current_game_state["opponent"]["hp"]
    opp_sp = current_game_state['opponent']['skill_points']
    
    # Simple Logic:
    # 1. If HP is low and has a Potion, heal.
    if player_hp < 100 and inventory.get("Elixir", 0) > 0:
        return "Use Elixir"

    if opp_hp < 100 and inventory.get("Elixir", 0) == 0 and inventory.get("Potion", 0) > 0:
        return "Use Potion"

    if player_hp <= 40 and player_sp >= 3:
        return "Cast Shadow Dodge"

    if player_hp <100 and player_sp <4 and inventory.get("Potion", 0) == 0 and inventory.get("Elixir", 0) == 0:
        return "Attack"

    if player_hp <= 40 and player_sp >= 3:
        return "Cast Shadow Dodge"

    # 2. If opponent is low HP and we have a bomb, finish them!
    if opp_hp <= 40 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"

    if player_sp == 6:
        return "Cast Poison Dart"

    if player_sp < 4:
        return "Attack"

    if player_sp >= 4 and player_sp !=6:
        return "Cast Backstab"
        
    if random.random() < 0.1 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"
    else:
        return "Attack"
