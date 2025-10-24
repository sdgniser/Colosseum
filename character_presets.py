CHARACTER_PRESETS = [
    {
        "name": "Warrior",
        "max_hp": 120*2,
        "basic_attack_damage": (18, 25),
        "color": (200, 100, 50),
        "skill_points": 4,
        "defense": 15
    },
    {
        "name": "Mage",
        "max_hp": 80*2,
        "basic_attack_damage": (10, 16),
        "color": (100, 50, 200),
        "skill_points": 8,
        "defense": 25
    },
    {
        "name": "Rogue",
        "max_hp": 100*2,
        "basic_attack_damage": (15, 22),
        "color": (150, 150, 150),
        "skill_points": 6,
        "defense": 40
    }
]

# Class-specific skills
WARRIOR_SKILLS = {
    "Power Strike": {"damage": (30, 40), "cost": 3, "description": "Heavy weapon attack"},
    "Shield Bash": {"damage": (20, 30), "cost": 2, "description": "Damages"},
    "Battle Cry": {"heal": (20, 30), "cost": 3, "description": "Heals HP"},
    "Whirlwind": {"damage": (25, 35), "cost": 4, "description": "Hits all enemies"}
}

MAGE_SKILLS = {
    "Fireball": {"damage": (35, 45), "cost": 5, "description": "High damage fire spell"},
    "Ice Shard": {"damage": (25, 35), "cost": 3, "description": "Freezing damage"},
    "Arcane Heal": {"heal": (35, 45), "cost": 4, "description": "Powerful healing"},
    "Lightning Bolt": {"damage": (40, 50), "cost": 6, "description": "Massive lightning damage"}
}

ROGUE_SKILLS = {
    "Backstab": {"damage": (35, 45), "cost": 4, "description": "High damage from behind"},
    "Poison Dart": {"damage": (0, 10), "cost": 3, "description": "Damage over time"},
    "Shadow Dodge": {"defense": 100, "cost": 3, "description": "Evade next attack"},
    "Quick Strike": {"damage": (25, 35), "cost": 2, "description": "Fast, low cost attack"}
}

# Map classes to their skills
CLASS_SKILLS = {
    "Warrior": WARRIOR_SKILLS,
    "Mage": MAGE_SKILLS,
    "Rogue": ROGUE_SKILLS
}

