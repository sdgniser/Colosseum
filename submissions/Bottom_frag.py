import random

def get_bot_class():
    return 2

def get_bot_action(current_game_state, game_archive):
    """
    This is the AI for the player's character in AI vs AI mode.
    It receives the current state and the history of all previous states.
    It must return a valid action string.
    """
    last_action = game_archive[-1]['action'][0]
    last_action_text = game_archive[-1]['action'][1]

    player_hp = current_game_state['player']['hp']
    player_sp = current_game_state['player']['skill_points']
    #print(player_sp)
    inventory = current_game_state['inventory']

    opp_hp = current_game_state['opponent']['hp']
    opp_sp = current_game_state['opponent']['skill_points']
    
    if last_action == 'Defend':
        if player_hp < 120 and inventory.get("Elixir", 0) > 0:
            return "Use Elixir"
        if player_hp < 150 and inventory.get("Potion", 0) > 0:
            return "Use Potion"
        if player_hp < 185 and inventory.get("Potion", 0) > 0:
            return "Use Ether   "

    if player_hp <= 50:
        if inventory.get("Elixir", 0) > 0:
            return "Use Elixir"
    
        elif player_sp >= 3:
            return "Cast Shadow Dodge"
    
        elif inventory.get("Potion", 0) > 0:
            return "Use Potion"
    
        elif inventory.get("Ether", 0) > 0:
            return "Use Ether" 
        
    if opp_hp <= 40 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"
    
    elif opp_hp <= 40 and player_sp >= 4:
        return "Cast Backstab"
    
    elif opp_hp <= 30 and player_sp >= 2:
        return "Cast Quick Strike"


    if player_sp > 3 and 'poison' not in last_action_text:
        return "Cast Poison Dart"
    else:
        return "Attack"
