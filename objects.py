#!/usr/bin/env python


class Player:
    def __init__(name, stats, items, skills, is_bot=False):
        """Stats = (ATA, DEF, HLT, STA)"""
        # TODO: add validation tests
        self.name = name
        self.stats = stats
        # assert [condition to check that stats are valid]
        self.health = stats[2]
        self.stamina = stats[3]
        self.items = items
        # assert [condition to check that items are valid (eg. their value doesn't exceed starting gold)]
        # assert [the first entry should be their main weapon, this will be shared to the opponent in the game]
        self.skills = skills
        # assert [condition to check that the skill are valid (eg. can be bought from starting skill points)]
        self.status_effects = []
        self.is_bot = is_bot

    def add_item(self, item):
        self.items.append(item)

    def del_item(self, item):
        self.remove(item)

    def add_status(self, status):
        self.status.append(status)

    def del_status(self, status):
        self.remove(status)

    def get_public_info(self):
        return [
            self.name,
            self.health,
            self.stamina,
            self.status_effects,
            self.items[0],
        ]


class GameState:
    def __init__(player0, player1):
        self.player0 = player0
        self.player1 = player1
        self.turn = 0
        self.parity = 0  # 0 if it is player0's turn and 1 if it is player1's
        self.history = []  # A list that contains all the past turns in the game
