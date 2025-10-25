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
    
    # # Simple Logic:
    # # 1. If HP is low and has a Potion, heal.
    # if player_hp < 100 and inventory.get("Potion", 0) > 0:
    #     return "Use Potion"

    # # 2. If opponent is low HP and we have a bomb, finish them!
    # if current_game_state['opponent']['hp'] < 45 and inventory.get("Bomb", 0) > 0:
    #     return "Use Bomb"

    # if player_sp < 6:
    #     return "Attack"
    
        
    # if random.random() < 0.3:
    #     return "Cast Lightning Bolt"
    # else:
    #     return "Attack"


    # if random.random() < 0.5:
    #     return "Attack"
    # elif random.random()<0.8:
    #     return "Skills"
    # elif random.random()<1:
    #     return "Items"

    if player_hp < 40:
        if current_game_state['opponent']['hp']<30:
            if inventory.get("Bomb", 0) > 0:
                return "Use Bomb"
            elif current_game_state['player']['skill_points']>=4:
                return "Cast Backstab"
            else:
                if inventory.get("Elixir", 0) > 0:
                    return "Use Elixir"
                elif inventory.get("Potion", 0) > 0:
                    return "Use Potion"
                elif inventory.get("Ether", 0) > 0:
                    return "Use Ether"
                else:
                    if random.random()<0.5:
                        return "Defend"
                    elif random.random()<0.9:
                        return "Attack"
                    elif random.random()<=1:
                        if inventory.get("Bomb", 0) > 0:
                            return "Use Bomb"
                        elif current_game_state['player']['skill_points']>=4:
                            return "Cast Backstab"
                        else:
                            return "Attack"
                
        if inventory.get("Elixir", 0) > 0:
            return "Use Elixir"
        elif inventory.get("Potion", 0) > 0:
            return "Use Potion"
        elif inventory.get("Ether", 0) > 0:
            return "Use Ether"
        else:
            if random.random()<0.5:
                return "Defend"
            elif random.random()<0.9:
                return "Attack"
            elif random.random()<=1:
                if inventory.get("Bomb", 0) > 0:
                    return "Use Bomb"
                elif current_game_state['player']['skill_points']>=4:
                    return "Cast Backstab"
                else:
                    return "Attack"
        
    elif player_hp < 60:
        if current_game_state['opponent']['hp']<55:
            if inventory.get("Bomb", 0) > 0:
                return "Use Bomb"
            elif current_game_state['player']['skill_points']>=4:
                return "Cast Backstab"
            else:
                return "Attack"
        elif random.random()<0.8:
            if inventory.get("Potion", 0) > 0:
                return "Use Potion"
            elif inventory.get("Ether", 0) > 0:
                return "Use Ether"
            else:
                return "Defend"
            
        elif random.random()<1:
                if current_game_state['player']['skill_points']>=3:
                    return "Cast Poison Dart"
                else:
                    return "Attack"
        else:
            return "Attack"


    elif player_hp < 80:
        if random.random()<0.6:
            if inventory.get("Ether", 0) > 0:
                return "Use Ether"
            else:
                return "Defend"
        
        else:
            if current_game_state['opponent']['hp']<90:
                if current_game_state['player']['skill_points']>=3:
                    return "Cast Poison Dart"
                else:
                    return "Attack"
            else:
                if inventory.get("Ether", 0) > 0:
                    return "Use Ether"
                else:
                    return "Defend"


    else:
        if random.random()<0.66:
            return "Attack"
        elif random.random()<0.98:
            if current_game_state['player']['skill_points']>=3:
                return "Cast Poison Dart"
            else:
                return "Attack"
        else:
            return "Defend"