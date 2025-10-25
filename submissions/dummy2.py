from random import random


def get_bot_class():
    return 0

def get_bot_action(current_game_state, game_archive):
    """
    This is the AI for the opponent's character.
    A very simple bot that just attacks.
    """
    # This bot is not very smart. It just attacks every turn.
    #action = "Attack"
    if random() < 0.1:
        action = "Attack"
    else:
        action = "Defend"
    return "Defend"
