#!/usr/bin/env python
ITEMS = [
    # [items, effect, cost, description]
    ["long sword", 10, 10, "10 base dmg"],
    ["great sword", 20, 40, "40 base dmg"],
    ["shield", 2, 20, "increase DEF by 2"],
]

POTIONS = [
    # [item, effect, cost, description]
    ["healing", 5, 10, "heal 5 health"],
    ["stamina", 5, 10, "heal 10 health"],
]

SKILLS = [
    # [skill, cost, description]
    ["heavy attack", 2, "increases DMG by 25%"],
    ["mana dart", 4, "Guaranteed hit with d4 DMG"],
    ["heal", 3, "heal 20 health over 4 turns"],
]

ACTIONS = ["basic attack", "defend", "use item", "use skill"]
