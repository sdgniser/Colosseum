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
    
    opp_hp = current_game_state['opponent']['hp']
    opp_sp = current_game_state['opponent']['skill_points']
    opp_class = current_game_state['opponent']['character_class']
    
    turns = len(game_archive)
    archive = game_archive
    poison = False
    if turns > 1:
        if ("poisened" in archive[turns-2]["action"][1]) and ("Poison Dart" in archive[turns-2]["action"][0]):
            poison = True
    if turns >= 6:
        if ("poisened" in archive[turns-6]["action"][1]) and ("Poison Dart" in archive[turns-8]["action"][0]):
            poison = True
        elif ("poisened" in archive[turns-4]["action"][1]) and ("Poison Dart" in archive[turns-8]["action"][0]):
            poison = True

    if player_hp < 120 and inventory['Elixir']:
        return "Use Elixir"
    if inventory["Bomb"]:
        return "Use Bomb"
    if player_sp >= 3 and poison==False:
        return "Cast Poison Dart"
    if player_sp >= 4:
        return "Cast Backstab"
    if player_sp >= 2 and opp_hp <= 25:
        return "Cast Quick Strike"
    if player_hp < 130 and inventory['Potion']:
        return "Use Potion"
    if player_hp < 150 and inventory['Ether']:
        return "Use Ether"
    else:
        return "Attack"

