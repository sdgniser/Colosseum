BASE_INVENTORY = {
    "Potion": {"count": 3, "effect": "heal", "value": 30, "description": "Heals 30 HP"},
    "Ether": {"count": 1, "effect": "heal", "value": 15, "description": "Heals 15 HP"},
    "Bomb": {"count": 2, "effect": "damage", "value": 40, "description": "Deals 40 damage"},
    "Elixir": {"count": 0, "effect": "heal", "value": 80, "description": "Heals 80 HP"}
}

# Class-specific starting inventories
CLASS_STARTING_INVENTORY = {
    "Warrior": {
        "Potion": {"count": 4, "effect": "heal", "value": 30, "description": "Heals 35 HP"},
        "Ether": {"count": 1, "effect": "heal", "value": 15, "description": "Heals 20 HP"},
        "Bomb": {"count": 1, "effect": "damage", "value": 40, "description": "Deals 40 damage"},
        "Elixir": {"count": 0, "effect": "heal", "value": 80, "description": "Heals 80 HP"}
    },
    "Mage": {
        "Potion": {"count": 2, "effect": "heal", "value": 30, "description": "Heals 35 HP"},
        "Ether": {"count": 3, "effect": "heal", "value": 15, "description": "Heals 20 HP"},
        "Bomb": {"count": 2, "effect": "damage", "value": 40, "description": "Deals 40 damage"},
        "Elixir": {"count": 0, "effect": "heal", "value": 80, "description": "Heals 80 HP"}
    },
    "Rogue": {
        "Potion": {"count": 3, "effect": "heal", "value": 30, "description": "Heals 35 HP"},
        "Ether": {"count": 2, "effect": "heal", "value": 15, "description": "Heals 20 HP"},
        "Bomb": {"count": 3, "effect": "damage", "value": 40, "description": "Deals 40 damage"},
        "Elixir": {"count": 0, "effect": "heal", "value": 80, "description": "Heals 80 HP"}
    }
}

# Additional items that can be added
EXTRA_ITEMS = {
    "Mega Potion": {"count": 1, "effect": "heal", "value": 50, "description": "Heals 50 HP"},
    "Smoke Bomb": {"count": 2, "effect": "escape", "value": 0, "description": "Allows escape from battle"},
    "Antidote": {"count": 2, "effect": "cure", "value": 0, "description": "Cures poison status"}

}
