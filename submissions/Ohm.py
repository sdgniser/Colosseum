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
    arr = ["Cast Poison Dart", "Attack", "Defend", "Use Bomb", "Cast Quick Strike"]
    if (current_game_state['player']['hp']<=60 and current_game_state['inventory']['Elixir']== 1):
            return "Use Elixir"
    if (current_game_state['opponent']['hp']<=120 and inventory.get("Bomb", 0) > 0):
            return arr[3]
    if (len(game_archive)>2):
           if (game_archive[-2]["action"][0] == arr[3] and player_sp>=3):
            return arr[0]
    if (len(game_archive) > 4):
          if (game_archive[-2]["action"]==arr[0] and game_archive[-4]["action"]==arr[3] and player_sp>=2):
            return arr[4]
    if len(game_archive) == 0:
            return arr[2]
    if len(game_archive) % 5 == 1 and player_sp>=3:
            return arr[0]
    if len(game_archive)  % 5 == 2:
            return arr[1]
    if len(game_archive) % 5 == 3:
            return arr[1]
    if len(game_archive) % 5 == 4:
            return arr[2]
    if (current_game_state['player']['hp']<=150 and current_game_state['inventory']["Potion"]>0):
            return "Use potion"
    if (current_game_state['player']['hp']<=150 and current_game_state['inventory']["Ether"]>0):
            return "Use ether"
        


    # Simple Logic:
    # 1. If HP is low and has a Potion, heal.
'''if player_hp < 100 and inventory.get("Potion", 0) > 0:
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
'''