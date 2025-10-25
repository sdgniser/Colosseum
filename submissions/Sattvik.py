import random

def get_bot_class():
    return 1

def get_bot_action(current_game_state, game_archive):
    """
    This is the AI for the player's character in AI vs AI mode.
    It receives the current state and the history of all previous states.
    It must return a valid action string.
    """
    player_hp = current_game_state['player']['hp']
    player_sp = current_game_state['player']['skill_points']
    inventory = current_game_state['inventory']
    
    opponent_hp = current_game_state['opponent']['hp']
    opponent_maxhp = current_game_state['opponent']['max_hp']
    opponent_sp = current_game_state['opponent']['skill_points']
    
    #Early game strategies
    if player_hp > 100:
        a = random.random()
        if a > 0.6:
            return 'Attack'
        if 0.2 <= a <= 0.6:
            if (opponent_maxhp - opponent_hp) < 50:
                if player_sp > 3:
                    return 'Cast Ice Shard'
                if player_sp <= 3:
                    return 'Attack'    
            if 50 <= (opponent_maxhp - opponent_hp) <= 140 :
                if player_sp > 5:
                    return 'Cast Fireball'
                if 3 < player_sp <= 5 :
                    return 'Cast Ice Shard'
                if player_sp <= 3:
                    return 'Attack'
            if (opponent_maxhp - opponent_hp) > 140:
                if player_sp > 6:
                    return 'Cast Lightning Bolt'
                if inventory['Bomb'] > 0:
                    return 'Use Bomb'
                if player_sp <= 3:
                    return 'Attack'
        else:
            return 'Defend'

    #Mid Game
    if 50 <= player_hp <= 100:
        a = random.random ()
        if a > 0.7:
            return 'Attack'
        if 0.4 <= a <= 0.7:
            if (opponent_maxhp - opponent_hp) < 50:
                if player_sp > 6:
                    return 'Use Lightning Bolt'
                if 5 < player_sp <= 6:
                    return 'Use Fireball'
                if 3 < player_sp <= 5:
                    return 'Use Ice Shard'
                if player_sp <= 3:
                    return 'Use Attack'
            if 50 <= (opponent_maxhp - opponent_hp) <= 140 :
                if player_sp > 6:
                    return 'Use Lightning Bolt'
                if 5 < player_sp <= 6:
                    return 'Use Fireball'
                if 3 < player_sp <= 5:
                    return 'Use Ice Shard'
                if player_sp <= 3:
                    return 'Use Attack'                
            if (opponent_maxhp - opponent_hp) > 140:
                if player_sp > 6:
                    return 'Use Lightning Bolt'
                if 5 < player_sp <= 6:
                    return 'Use Fireball'
                if 3 < player_sp <= 5:
                    return 'Use Ice Shard'
                if player_sp <= 3:
                    return 'Use Attack'
        if 0.2 <= a < 0.4:
            if inventory['Ether'] > 0:
                return 'Use Ether'
            if inventory['Potion'] > 1:
                return 'Use Potion'
            if inventory['Bomb'] > 0:
                return 'Use Bomb'
            if player_sp > 6:
                return 'Use Arcane Heal'
            if 5 < player_sp <= 6:
                return 'Use Fireball'
            if player_sp <= 5:
                return 'Attack'
        if a < 0.2 :
            return 'Defend'
    

    # #Late game
    if player_hp < 50:
        a = random.random ()
        if inventory['Elixir'] > 0:
            return 'Use Elixir'
        if a > 0.5:
            if inventory['Potion'] > 0:
                return 'Use Potion'
            if player_sp >= 4:
                return 'Cast Arcane Heal'
            if inventory['Ether'] > 0:
                return 'Use Ether'
            if inventory['Bomb'] > 0:
                return 'Use Bomb'
            if player_sp > 6:
                return 'Use Lightning Bolt'
            if 5 < player_sp <= 6:
                return 'Use Fireball'
            if 4 < player_sp <= 5:
                return 'Use Ice Shard'
            return 'Attack'
        if 0.25 <= a <= 0.5:
            if inventory['Bomb'] > 0:
                return 'Use Bomb'
            if player_sp > 6:
                return 'Use Lightning Bolt'
            if 5 < player_sp <= 6:
                return 'Use Fireball'
            if 4 < player_sp <= 5:
                return 'Use Ice Shard'
            if player_sp <= 4:
                return 'Use Arcane Heal'
            return 'Defend'
        if a < 0.25 :
            return 'Defend'
            

    # Simple Logic:
    # 1. If HP is low and has a Potion, heal.
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
    
    


