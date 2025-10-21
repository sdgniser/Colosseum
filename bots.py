import random

def get_player_bot_action(current_game_state, game_archive):
    """
    This is the AI for the player's character in AI vs AI mode.
    It receives the current state and the history of all previous states.
    It must return a valid action string.
    """
    player_hp = current_game_state['player']['hp']
    inventory = current_game_state['inventory']
    
    # Simple Logic:
    # 1. If HP is low and has a Potion, heal.
    if player_hp < 40 and inventory.get("Potion", 0) > 0:
        return "Use Potion"
    
    # 2. If opponent is low HP and we have a bomb, finish them!
    if current_game_state['opponent']['hp'] < 45 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"
        
    # 3. Otherwise, cast a powerful spell or just attack.
    if random.random() < 0.5: # 50% chance to cast Fireball
        return "Cast Fireball"
    else:
        return "Attack"


def get_opponent_bot_action(current_game_state, game_archive):
    """
    This is the AI for the opponent's character.
    A very simple bot that just attacks.
    """
    # This bot is not very smart. It just attacks every turn.
    action = "Attack"
    return action