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
  opponent_hp = current_game_state['opponent']['hp']
  opponent_sp = current_game_state['opponent']['skill_points']
  inventory = current_game_state['inventory']

  if player_hp < 80 and player_sp > 4:
    if opponent_hp <= 10:                                return "Attack"
    elif opponent_hp <= 40 and inventory.get("Bomb", 0): return "Use Bomb"
    elif opponent_hp <= 25 and player_sp >= 3:           return "Cast Ice Shard"
    elif opponent_hp <= 35 and player_sp >= 5:           return "Cast Fireball"
    elif opponent_hp <= 40 and player_sp >= 6:           return "Cast Lightning Bolt"
    elif player_sp > 4:                                  return "Cast Arcane Heal"
    if inventory.get("Elixir", 0) > 0:                   return "Use Elixir"
    if inventory.get("Potion", 0) > 0:                   return "Use Potion"
    if inventory.get("Ether",0) > 0:                     return "Use Ether"
    else:                                                return "Defend"
  else:
    if opponent_hp <= 16: return "Attack"
    elif opponent_hp <= 40 and inventory.get("Bomb", 0):return "Use Bomb"
    elif opponent_hp <= 35 and player_sp >= 3:          return "Cast Ice Shard"
    elif opponent_hp <= 45 and player_sp >= 5:          return "Cast Fireball"
    elif opponent_hp <= 50 and player_sp >= 6:          return "Cast Lightning Bolt"
    else:                                               return "Attack"