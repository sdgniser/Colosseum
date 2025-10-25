"""
Simple tabular RL trainer for NPC Colosseum.

This trainer uses an episodic Monte-Carlo style update to learn a mapping
from a discretized game state to actions for a chosen class. It trains by
playing the agent (Player) against a mixture of built-in bots (or a
specified opponent) and updates a Q-table saved to disk.

Notes:
- No external ML libraries required.
- The state space is discretized to keep Q-table size manageable.
- This is a simple baseline; more advanced function approximation or
  policy-gradient training can be added later.

Usage examples:
  python3 ml_trainer.py --episodes 2000 --class 1 --opponents rogue,warrior,random
  python3 ml_trainer.py --episodes 5000 --class 2 --opponent-dir bots/

Outputs:
  - ml_policy_CLASS.pkl  (pickled dict with 'class' and 'Q')

"""
import argparse
import pickle
import random
import os
import importlib.util
from collections import defaultdict
from game_engine import GameEngine
import game_engine as ge
import mage, rogue, warrior, random_bot
import time


def discretize_state(game_state, bins=(10, 5, 10, 5)):
    """Convert current_game_state into a discrete tuple key.

    bins: (player_hp_bins, player_sp_bins, opp_hp_bins, opp_sp_bins)
    """
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


def get_valid_actions_for_engine(engine):
    """Return list of valid action strings for the current player in the engine."""
    actions = ["Attack", "Defend"]
    inv = engine.player_inventory.get_inventory_dict()
    for item, count in inv.items():
        if count > 0:
            actions.append(f"Use {item}")

    # skills available from engine.player_skills dict
    skills = engine.player_skills
    sp = engine.player.skill_points
    for name, data in skills.items():
        cost = data.get('cost', 0)
        if sp >= cost:
            actions.append(f"Cast {name}")

    # remove duplicates
    seen = set()
    out = []
    for a in actions:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


def load_bot_from_file(filepath):
    """Load a bot module from a .py file path."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Bot file not found: {filepath}")
    
    spec = importlib.util.spec_from_file_location(
        "opponent_bot_" + os.path.splitext(os.path.basename(filepath))[0], 
        filepath
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Validate interface
    if not hasattr(mod, 'get_bot_action') or not hasattr(mod, 'get_bot_class'):
        raise AttributeError(f"Bot '{filepath}' must define get_bot_action and get_bot_class")
    
    return mod


def load_bots_from_directory(directory):
    """Load all valid bot .py files from a directory.
    
    Returns list of bot modules.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")
    
    bot_modules = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('_'):
            filepath = os.path.join(directory, filename)
            try:
                mod = load_bot_from_file(filepath)
                bot_modules.append(mod)
                print(f"Loaded opponent bot: {filename}")
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue
    
    return bot_modules


def train(args):
    Q = defaultdict(lambda: defaultdict(float))  # Q[state][action] = value
    returns_count = defaultdict(lambda: defaultdict(int))

    opponents = []
    
    # Load from directory if specified
    if args.opponent_dir:
        print(f"Loading opponent bots from directory: {args.opponent_dir}")
        opponents = load_bots_from_directory(args.opponent_dir)
        if not opponents:
            print(f"Warning: No valid bots found in {args.opponent_dir}, using defaults")
    
    # Load from comma-separated list if no directory or as supplement
    if not args.opponent_dir or args.opponents != 'rogue,warrior,mage,random':
        for name in args.opponents.split(','):
            name = name.strip()
            if name == 'mage': opponents.append(mage)
            elif name == 'rogue': opponents.append(rogue)
            elif name == 'warrior': opponents.append(warrior)
            elif name == 'random': opponents.append(random_bot)
            else:
                # try to import module by name (not exhaustive)
                try:
                    mod = __import__(name)
                    opponents.append(mod)
                except Exception:
                    print(f"Warning: unknown opponent '{name}', skipping")

    if not opponents:
        opponents = [rogue, warrior, mage]
        print("Using default opponents: rogue, warrior, mage")

    alpha = args.alpha
    epsilon = args.epsilon
    gamma = args.gamma

    t0 = time.time()
    for episode in range(1, args.episodes + 1):
        # pick random opponent module for this episode
        opp_mod = random.choice(opponents)
        # Prepare action holders and monkeypatch engine-level bot entrypoints
        player_action_holder = {'action': None}
        opponent_action_holder = {'action': None}
        ge.get_player_bot_action = lambda state, archive: player_action_holder['action']
        ge.get_opponent_bot_action = lambda state, archive: opponent_action_holder['action']

        engine = GameEngine()
        # Set learner as player class
        engine.set_player_character(args.class_id)
        # set opponent class based on opponent module's preferred class
        try:
            opp_cls = opp_mod.get_bot_class()
        except Exception:
            opp_cls = random.choice([0, 1, 2])
        engine.set_opponent_character(opp_cls)
        engine.reset(mode='aivai')

        episode_trace = []  # list of (state_key, action_str)

        turns = 0
        while not engine.is_game_over() and turns < args.max_turns:
            # Determine whose turn: we train only when it's player's turn
            if engine.is_player_turn():
                state = engine._get_current_game_state_for_bot()
                s_key = discretize_state(state)

                valid_actions = get_valid_actions_for_engine(engine)
                if not valid_actions:
                    action = "Attack"
                else:
                    # epsilon-greedy
                    if random.random() < epsilon:
                        action = random.choice(valid_actions)
                    else:
                        # pick action with highest Q
                        qvals = {a: Q[s_key].get(a, 0.0) for a in valid_actions}
                        maxv = max(qvals.values())
                        best = [a for a, v in qvals.items() if v == maxv]
                        action = random.choice(best)

                # Apply action via engine update using monkeypatched getter
                player_action_holder['action'] = action
                engine.update()
                player_action_holder['action'] = None

                episode_trace.append((s_key, action))
            else:
                # Opponent turn: get action from its module
                state = engine._get_current_game_state_for_bot()
                # swap perspective for opponent call
                swapped = {'player': state['opponent'], 'opponent': state['player'], 'inventory': engine.opponent_inventory.get_inventory_dict()}
                try:
                    opp_action = opp_mod.get_bot_action(swapped, engine.game_archive)
                except Exception:
                    opp_action = random.choice(["Attack", "Defend"])
                opponent_action_holder['action'] = opp_action
                engine.update()
                opponent_action_holder['action'] = None

            turns += 1

        # Determine reward: +1 win, -1 loss, 0 draw
        if engine.player.is_alive() and not engine.opponent.is_alive():
            R = 1.0
        elif engine.opponent.is_alive() and not engine.player.is_alive():
            R = -1.0
        else:
            R = 0.0

        # Monte Carlo update: update every visited state-action towards return R
        visited = set()
        for (s_key, action) in episode_trace:
            if (s_key, action) in visited:
                continue
            visited.add((s_key, action))
            returns_count[s_key][action] += 1
            # incremental average update
            old = Q[s_key].get(action, 0.0)
            Q[s_key][action] = old + alpha * (R - old)

        # decay epsilon slightly
        if episode % args.decay_every == 0 and epsilon > args.epsilon_min:
            epsilon = max(args.epsilon_min, epsilon * args.epsilon_decay)

        if episode % max(1, args.episodes // 10) == 0:
            elapsed = time.time() - t0
            print(f"Episode {episode}/{args.episodes} epsilon={epsilon:.3f} elapsed={elapsed:.1f}s")

    # Save policy
    outname = args.outfile or f"ml_policy_{args.class_id}.pkl"
    payload = {'class': args.class_id, 'Q': dict((k, dict(v)) for k,v in Q.items())}
    with open(outname, 'wb') as f:
        pickle.dump(payload, f)
    print(f"Saved policy to {outname}")


def main():
    parser = argparse.ArgumentParser(description='Train a simple tabular RL policy for Colosseum')
    parser.add_argument('--episodes', type=int, default=2000)
    parser.add_argument('--class', dest='class_id', type=int, default=1, help='Class id to train (0=Warrior,1=Mage,2=Rogue)')
    parser.add_argument('--opponents', type=str, default='rogue,warrior,mage,random', help='Comma-separated opponent modules')
    parser.add_argument('--opponent-dir', type=str, default=None, help='Directory containing opponent bot .py files')
    parser.add_argument('--alpha', type=float, default=0.1)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--epsilon', type=float, default=0.3)
    parser.add_argument('--epsilon-min', dest='epsilon_min', type=float, default=0.05)
    parser.add_argument('--epsilon-decay', dest='epsilon_decay', type=float, default=0.9)
    parser.add_argument('--decay-every', type=int, default=100)
    parser.add_argument('--max-turns', type=int, default=2000)
    parser.add_argument('--outfile', type=str, default=None)
    args = parser.parse_args()

    # Map argument names
    args.epsilon = args.epsilon
    args.epsilon_min = args.epsilon_min
    args.epsilon_decay = args.epsilon_decay

    train(args)


if __name__ == '__main__':
    main()
