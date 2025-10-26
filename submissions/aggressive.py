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
    if inventory.get('Bomb', 0) > 0:
        return "Use Bomb"
    if player_hp < 100 and inventory.get('Potion', 0) > 0:
        return "Use Potion"
    elif inventory.get('Elixir', 0) > 0:
        return "Use Elixir"

    if player_sp >= 4:
        return "Cast Backstab"
    else:
        return "Attack"
