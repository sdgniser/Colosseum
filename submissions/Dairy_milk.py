import random
from copy import deepcopy
from character_presets import CLASS_SKILLS

def get_bot_class():
    return 2

def get_bot_action(current_game_state, game_archive):

    s = deepcopy(current_game_state)
    me = s['player']
    opp = s['opponent']
    inv = s.get('inventory', {}) or {}
    my_class = me.get('character_class', '')
    my_sp = me.get('skill_points', 0)
    opp_sp = opp.get('skill_points', 0)
    skills = CLASS_SKILLS.get(my_class, {})
    opp_skills = CLASS_SKILLS.get(opp.get('character_class', ''), {})


    def avg_damage_from_tuple(d):
        if isinstance(d, (tuple, list)) and len(d) == 2:
            return (d[0] + d[1]) / 2.0
        return float(d or 0)


    my_basic = avg_damage_from_tuple(me.get('basic_attack_damage', (12, 18)))
    opp_basic = avg_damage_from_tuple(opp.get('basic_attack_damage', (10, 16)))


    def opponent_best_threat():
        best_name = None
        best_avg = opp_basic
        best_cost = 0
        for n, d in opp_skills.items():
            if 'damage' in d:
                cost = d.get('cost', 0)
                if cost <= opp_sp:
                    avg = avg_damage_from_tuple(d.get('damage', (0,0)))
                    if avg > best_avg:
                        best_avg = avg
                        best_name = n
                        best_cost = cost
        return best_name, best_avg, best_cost

    opp_threat_name, opp_threat_avg, opp_threat_cost = opponent_best_threat()

    ITEM_VALUES = {
        "Elixir": {"heal": 80},
        "Potion": {"heal": 30},
        "Ether": {"heal": 15},
        "Bomb": {"damage": 40}
    }

    candidates = []

    candidates.append(("Attack", {"damage": my_basic, "sp_cost": 0}))
    candidates.append(("Defend", {"damage": 0, "sp_cost": 0, "defend": True}))

    if inv.get("Bomb", 0) > 0:
        candidates.append(("Use Bomb", {"damage": ITEM_VALUES["Bomb"]["damage"], "sp_cost": 0, "item": "Bomb"}))

    for item in ("Elixir", "Potion", "Ether"):
        if inv.get(item, 0) > 0:
            candidates.append((f"Use {item}", {"heal": ITEM_VALUES[item]["heal"], "sp_cost": 0, "item": item}))

    for name, data in skills.items():
        cost = data.get('cost', 0)
        if cost <= my_sp:
            entry = {"sp_cost": cost}
            if 'damage' in data:
                entry["damage"] = avg_damage_from_tuple(data.get('damage', (0,0)))
            if 'heal' in data:
                entry["heal"] = avg_damage_from_tuple(data.get('heal', (0,0)))
            if 'defense' in data:
                entry["defend_value"] = data.get('defense', 0)
            candidates.append((f"Cast {name}", entry))

    if "Shadow Dodge" in skills and skills["Shadow Dodge"].get('cost', 999) <= my_sp:
        if ("Cast Shadow Dodge", {"sp_cost": skills["Shadow Dodge"]["cost"], "shadow": True}) not in candidates:
            candidates.append(("Cast Shadow Dodge", {"sp_cost": skills["Shadow Dodge"]["cost"], "shadow": True}))

    if my_class == "Rogue" and "Poison Dart" in skills and skills["Poison Dart"].get('cost', 999) <= my_sp:
        pd_avg = avg_damage_from_tuple(skills["Poison Dart"].get('damage', (0,0)))
        candidates.append(("Cast Poison Dart", {"damage": pd_avg + 8, "sp_cost": skills["Poison Dart"]["cost"], "poison": True}))

    best_score = -10**9
    best_actions = []
    my_hp = me.get('hp', 1)
    opp_hp = opp.get('hp', 1)
    my_max_hp = me.get('max_hp', my_hp)

    for action, effect in candidates:
        est_opp_hp = opp_hp
        est_my_hp = my_hp
        est_my_sp = my_sp - effect.get('sp_cost', 0)

        if effect.get('damage', 0):
            est_opp_hp = max(0, est_opp_hp - effect['damage'])
        if effect.get('heal', 0):
            est_my_hp = min(my_max_hp, est_my_hp + effect['heal'])

        will_shadow = effect.get('shadow', False)
        will_defend = effect.get('defend', False) or effect.get('defend_value', 0) >= 50

        incoming = opp_threat_avg

        if will_shadow:
            incoming = 0
        elif will_defend:
            incoming = incoming * 0.5

        if opp_threat_name and opp_threat_avg >= 30 and opp_sp >= opp_threat_cost:
            incoming = max(incoming, opp_threat_avg)

        est_my_hp_after = max(0, est_my_hp - incoming)

        if est_opp_hp <= 0 and est_my_hp_after > 0:
            score = 1_000_000 - (est_my_hp - est_my_hp_after) 
        else:
            opp_damage_done = opp_hp - est_opp_hp
            my_damage_taken = my_hp - est_my_hp_after
            poison_bonus = 50 if effect.get('poison') else 0
            sp_conserve_bonus = est_my_sp * 5
            score = opp_damage_done * 100 - my_damage_taken * 120 + poison_bonus + sp_conserve_bonus

        score += random.uniform(-5, 5)

        if score > best_score:
            best_score = score
            best_actions = [action]
        elif score == best_score:
            best_actions.append(action)

    chosen = random.choice(best_actions) if best_actions else "Attack"

    if my_hp / max(1, my_max_hp) <= 0.30:
        if inv.get("Elixir", 0) > 0:
            return "Use Elixir"
        if inv.get("Potion", 0) > 0:
            return "Use Potion"
        if "Cast Shadow Dodge" in [c[0] for c in candidates] and skills.get("Shadow Dodge", {}).get('cost', 999) <= my_sp:
            return "Cast Shadow Dodge"
        return "Defend"

    return chosen