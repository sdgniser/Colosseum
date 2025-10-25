def get_bot_class():
    
    # We are using Rogue for this bot
    return 2


def get_bot_action(current_game_state, game_archive):
    player = current_game_state["player"]
    opponent = current_game_state["opponent"]
    inventory = current_game_state["inventory"]

    my_hp = player["hp"]
    my_max = player["max_hp"]
    my_sp = player["skill_points"]

    opp_hp = opponent["hp"]
    opp_max = opponent["max_hp"]
    opp_sp = opponent["skill_points"]

    #Check what the opponent did
    opp_healed_last_turn = False
    opp_defended_last_turn = False
    last_opp_hp = None
    last_opp_action = None

    if game_archive:
        prev = game_archive[-1]
        last_opp_hp = prev["opponent"]["hp"]
        last_opp_action = prev.get("action", [None, None])[0]

        if last_opp_action == "Defend":
            opp_defended_last_turn = True

        # if their HP went up, they healed
        if opp_hp > last_opp_hp:
            opp_healed_last_turn = True

    
    if len(game_archive) == 0 and my_sp >= 3:
        return "Cast Poison Dart"

    
    # if our HP is getting low, try to survive
    if my_hp < 50:
        if inventory.get("Elixir", 0) > 0:
            return "Use Elixir"  
        if inventory.get("Potion", 0) > 0:
            return "Use Potion"  
        if inventory.get("Ether", 0) > 0:
            return "Use Ether"   
        if my_sp >= 3:
            return "Cast Shadow Dodge" 

    
    # if enemy healed or defended, and our HP < 100, we heal up too
    if my_hp < 100 and (opp_healed_last_turn or opp_defended_last_turn):
        if inventory.get("Potion", 0) > 0:
            return "Use Potion"
        elif inventory.get("Ether", 0) > 0:
            return "Use Ether"
        elif inventory.get("Elixir", 0) > 0 and my_hp < 0.4 * my_max:
            return "Use Elixir"

    
    # if we have SP and their HP < 80 (or our HP < 80), throw poison again
    if my_sp >= 3 and (opp_hp < 80 and my_hp >100):
        return "Cast Poison Dart"

    
    # if their HP is under 60 and we have a bomb, use it to hit big
    if opp_hp < 60 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"

    
    # when their HP is between 60–80, just attack
    if 60 <= opp_hp < 80:
        return "Attack"

    
    # if we have enough SP, use backstab for heavy damage
    if my_sp >= 4 and opp_hp < opp_max - 60:
        return "Cast Backstab"

    
    # if they just defended , and we don’t have enough SP for poison
    if (opp_defended_last_turn or opp_healed_last_turn) and my_sp < 3:
        # if our HP lead is big, don’t care about defense, just attack
        if (my_hp - opp_hp) > 40:
            return "Attack"
        # otherwise, play it safe if our HP isn’t great
        if my_hp < 0.8 * my_max:
            return "Defend"
        else:
            return "Attack"

    
    # if we already have 40+ HP more than them, keep attacking even if they defend
    if (my_hp - opp_hp) >= 40:
        return "Attack"

    
    # if their HP is really low and we still have a bomb, finish them
    if opp_hp < 40 and inventory.get("Bomb", 0) > 0:
        return "Use Bomb"

    
    # otherwise, just keep attacking
    return "Attack"
