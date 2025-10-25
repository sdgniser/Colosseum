"""
Simple ML bot loader that uses saved Q-table from ml_trainer.

If a policy file named `ml_policy_CLASS.pkl` exists, this bot will load it
and act greedily. Otherwise it will fall back to a simple random action.

To manually specify which policy to use, set the ML_BOT_CLASS environment variable:
    export ML_BOT_CLASS=2  # Use Rogue policy (ml_policy_2.pkl)
    export ML_BOT_CLASS=1  # Use Mage policy (ml_policy_1.pkl)
    export ML_BOT_CLASS=0  # Use Warrior policy (ml_policy_0.pkl)
"""
import pickle
import os
import random


POLICY_TEMPLATE = "ml_policy_{}.pkl"


def _discretize_state(game_state, bins=(10, 5, 10, 5)):
    player = game_state['player']
    opp = game_state['opponent']

    def bucket(value, maximum, nbins):
        if maximum <= 0:
            return 0
        frac = value / float(maximum)
        idx = int(frac * nbins)
        if idx < 0: idx = 0
        if idx >= nbins: idx = nbins - 1
        return idx

    p_hp = bucket(player['hp'], player['max_hp'], bins[0])
    p_sp = bucket(player['skill_points'], player.get('max_skill_points', player['skill_points']), bins[1])
    o_hp = bucket(opp['hp'], opp['max_hp'], bins[2])
    o_sp = bucket(opp['skill_points'], opp.get('max_skill_points', opp['skill_points']), bins[3])
    p_class = player.get('character_class', '')
    o_class = opp.get('character_class', '')

    return (p_class, p_hp, p_sp, o_class, o_hp, o_sp)


def _get_valid_actions(current_game_state):
    actions = ["Attack", "Defend"]
    inv = current_game_state.get('inventory', {})
    for item, count in inv.items():
        if count > 0:
            actions.append(f"Use {item}")

    # Heuristics: include class skills names with approximate costs
    cls = current_game_state['player']['character_class']
    if cls == 'Warrior':
        skills = [("Power Strike", 3), ("Shield Bash", 2), ("Battle Cry", 3), ("Whirlwind", 4)]
    elif cls == 'Mage':
        skills = [("Fireball", 5), ("Ice Shard", 3), ("Arcane Heal", 4), ("Lightning Bolt", 6)]
    elif cls == 'Rogue':
        skills = [("Backstab", 4), ("Poison Dart", 3), ("Shadow Dodge", 3), ("Quick Strike", 2)]
    else:
        skills = []

    sp = int(current_game_state['player'].get('skill_points', 0))
    for name, cost in skills:
        if sp >= cost:
            actions.append(f"Cast {name}")

    # deduplicate
    out = []
    seen = set()
    for a in actions:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


# Load policy if available. We prefer a file named ml_policy_{class}.pkl in cwd.
_policy = None
_policy_class = None

def _load_policy_for_class(cls):
    global _policy, _policy_class
    
    # Try loading in order of preference:
    # 1. Self-play policy (ml_policy_selfplay_{cls}.pkl)
    # 2. Standard policy (ml_policy_{cls}.pkl)
    
    candidates = [
        f"ml_policy_selfplay_{cls}.pkl",
        POLICY_TEMPLATE.format(cls)
    ]
    
    for fname in candidates:
        if os.path.isfile(fname):
            try:
                with open(fname, 'rb') as f:
                    data = pickle.load(f)
                if 'class' in data and 'Q' in data:
                    _policy = data['Q']
                    _policy_class = data['class']
                    return True
            except Exception:
                continue
    
    return False


def get_bot_class():
    # Check for manual override via environment variable
    manual_class = os.environ.get('ML_BOT_CLASS')
    if manual_class is not None:
        try:
            cls = int(manual_class)
            if cls in (0, 1, 2) and _load_policy_for_class(cls):
                return cls
        except ValueError:
            pass
    
    # Prefer loading any available policy files; otherwise default to Mage (1)
    global _policy_class
    # attempt to find a policy file for any class (2 -> 0,1,2)
    for cls in (1, 0, 2):
        if _load_policy_for_class(cls):
            return cls
    return 1


def get_bot_action(current_game_state, game_archive):
    global _policy
    cls = current_game_state['player']['character_class']
    # try to load policy for reported class if not loaded yet
    if _policy is None:
        # try policy file for class id inferred by class name
        mapping = {'Warrior': 0, 'Mage': 1, 'Rogue': 2}
        try_cls = mapping.get(cls, 1)
        _load_policy_for_class(try_cls)

    valid = _get_valid_actions(current_game_state)
    if _policy is None or not valid:
        # fallback random
        return random.choice(valid) if valid else "Attack"

    s_key = _discretize_state(current_game_state)
    qdict = _policy.get(s_key, {})
    if not qdict:
        return random.choice(valid)
    # pick best available action among valid
    best_val = None
    best_actions = []
    for a in valid:
        v = qdict.get(a, 0.0)
        if best_val is None or v > best_val:
            best_val = v
            best_actions = [a]
        elif v == best_val:
            best_actions.append(a)

    return random.choice(best_actions)
