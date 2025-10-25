import random


def get_bot_class():
    return 2

def get_bot_action(current_game_state, game_archive):
    player = current_game_state['player']
    opponent = current_game_state['opponent']

    player_class = player.get('character_class', '')
    player_hp = player['hp']
    player_max = player['max_hp']

    player_health = (player_hp / player_max) * 100

    player_sp = player['skill_points']
    inventory = current_game_state['inventory']
    
    opponent_hp = opponent['hp']
    opponent_max = opponent['max_hp']
    opponent_health = (opponent_hp / opponent_max) * 100

    opponent_sp = opponent['skill_points']
    opponent_class = opponent.get('character_class', '')

    likely_action = None
    try : 
        if opponent_sp >= 6 and opponent_class == 'Mage':
            likely_action = 'Cast Lightning Bolt'
        elif opponent_sp >= 4 and opponent_class == 'Warrior':
            likely_action = 'Cast Power Strike'
        elif opponent_sp >= 3 and opponent_class == 'Rogue':
            likely_action = 'Shadow Dodge' if random.random() < 0.6 else 'Cast Backstab'
        
    
    except Exception:
        likely_action = None
    
    # Random Exploration = To avoid a deterministic bot :P
    EPSILON = 0.12 
    if random.random() < EPSILON:
        choices = ['Attack','Defend']
        if inventory.get('Bomb', 0) > 0:
            choices.append('Use Bomb')
        if inventory.get('Potion', 0) > 0:
            choices.append('Use Potion')

        return random.choice(choices)
      
    # Low HP - Heal Prioritize

    if player_health <= 25:
        if inventory.get('Elixir',0) > 0:
            return 'Use Elixir'
        
        if inventory.get('Potion', 0) > 0:
            return 'Use Potion'
        
        if inventory.get('Ether', 0) > 0:
            return 'Use Ether'
    
    # In case I want to switch classes - finisher move series

    class_finisher = {
        'Warrior' : 'Power Strike',
        'Mage' : 'Lightning Bolt',
        'Rogue' : 'Backstab'
    }

    finisher = class_finisher.get(player_class)
    finisher_damages = {
            'Power Strike': 30,
            'Lightning Bolt': 40,
            'Backstab': 35
        }
    
    damage = finisher_damages.get(finisher)
    defend_likely = likely_action == 'Defend' or (likely_action and 'Dodge' in likely_action)
    required_damage = opponent_health * (2 if defend_likely else 1)
    if player_sp >= 4 and damage >= required_damage:
        return f'Cast {finisher}'


    # Moderate: 40 - 75% -> balanced play
    if 40 <= player_health <= 75:
        if player_sp >= 3 and inventory.get('Bomb', 0) == 0:
            return 'Cast Poison Dart'

        if player_sp >= 4 and opponent_hp <= 45:
            return 'Cast Backstab'

        if player_sp >= 2:
            return 'Cast Quick Strike'

        # Default moderate action
        return 'Attack'

    # Aggressive: >75% -> high damage and finishers
    if player_health> 75:
        if player_sp >= 4:
            return 'Cast Backstab'

        if player_sp >= 2:
            return 'Cast Quick Strike'

        return 'Attack'
    
    # Default Atack
    return 'Attack'
