from random import random


def get_bot_class():
    return 2

def get_bot_action(current_game_state, game_archive):
    """
    This is the AI for the opponent's character.
    A very simple bot that just attacks.
    """
    # This bot is not very smart. It just attacks every turn.
    #action = "Attack"
    if random() < 0.1 and current_game_state["player"]["skill_points"] >= 4:
        action = "Cast Backstab"
    else:
        action = "Attack"
    return action
