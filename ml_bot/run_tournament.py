import time
import argparse
from collections import Counter
from tabulate import tabulate

import random
import json
import csv

from game_engine import GameEngine
import game_engine as ge
import mage
import rogue
import warrior
import random_bot
import importlib
import importlib.util
import os


# Map simple names to modules and preset indices (Warrior=0, Mage=1, Rogue=2)
BOT_MODULES = {
    'mage': (mage, 1),
    'rogue': (rogue, 2),
    'warrior': (warrior, 0),
    'random': (random_bot, random_bot.get_bot_class()),
}


def load_bot_by_name_or_path(name):
    """Load a bot module by known name, importable module name, or file path.

    Returns (module, class_index) where class_index is obtained by calling module.get_bot_class().
    Raises ImportError/AttributeError on failure.
    """
    # 1) Known built-ins
    if name in BOT_MODULES:
        return BOT_MODULES[name]

    # 2) Try importing as a module name
    try:
        mod = importlib.import_module(name)
    except Exception:
        mod = None

    # 3) If import failed, try to load from a .py file (relative or absolute)
    if mod is None:
        # Accept names like 'autism' mapping to './autism.py'
        candidate_paths = [name]
        if not name.endswith('.py'):
            candidate_paths.append(name + '.py')
        loaded = False
        for path in candidate_paths:
            if os.path.isfile(path):
                spec = importlib.util.spec_from_file_location("user_bot_" + os.path.splitext(os.path.basename(path))[0], path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                loaded = True
                break
        if not loaded and mod is None:
            raise ImportError(f"Could not import bot module by name or path: {name}")

    # Validate interface
    if not hasattr(mod, 'get_bot_action') or not hasattr(mod, 'get_bot_class'):
        raise AttributeError(f"Bot module '{name}' must define get_bot_action and get_bot_class")

    cls = mod.get_bot_class()
    if not isinstance(cls, int) or cls not in (0, 1, 2):
        raise ValueError(f"Bot module '{name}' returned invalid class from get_bot_class(): {cls}")

    return mod, cls


def load_bots_from_directory(directory):
    """Load all valid bot .py files from a directory.
    
    Returns list of bot names (file paths) that can be loaded.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")
    
    bot_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('_'):
            filepath = os.path.join(directory, filename)
            try:
                # Try to load it to validate
                load_bot_by_name_or_path(filepath)
                bot_files.append(filepath)
            except Exception as e:
                # Skip files that aren't valid bots
                print(f"Skipping {filename}: {e}")
                continue
    
    return bot_files


def run_match(p1_module, p2_module, max_turns=2000):
    # Monkeypatch the engine-level bot entrypoints to call our chosen modules
    ge.get_player_bot_action = lambda state, archive: p1_module.get_bot_action(state, archive)
    ge.get_opponent_bot_action = lambda state, archive: p2_module.get_bot_action(state, archive)

    engine = GameEngine()
    # Ask each module for its preferred class and set characters accordingly
    p1_idx = p1_module.get_bot_class()
    p2_idx = p2_module.get_bot_class()

    engine.set_player_character(p1_idx)
    engine.set_opponent_character(p2_idx)
    engine.reset(mode='aivai')

    turns = 0
    while not engine.is_game_over() and turns < max_turns:
        engine.update()
        turns += 1

    if not engine.is_game_over():
        # draw due to turn cap
        return 'draw', turns

    # Determine winner
    if engine.player.is_alive() and not engine.opponent.is_alive():
        return 'p1', turns
    elif engine.opponent.is_alive() and not engine.player.is_alive():
        return 'p2', turns
    else:
        return 'draw', turns


def run_series(p1_name, p2_name, games=500, seed=None):
    # Load p1 and p2 modules (built-ins or arbitrary modules/paths)
    p1_module, _ = load_bot_by_name_or_path(p1_name)
    p2_module, _ = load_bot_by_name_or_path(p2_name)

    if seed is not None:
        random.seed(seed)

    results = Counter()
    turn_counts = []
    t0 = time.time()
    for i in range(games):
        winner, turns = run_match(p1_module, p2_module)
        results[winner] += 1
        turn_counts.append(turns)
        # Optional: print progress occasionally
        if (i + 1) % max(1, games // 10) == 0:
            print(f"{i+1}/{games} done...")
    dt = time.time() - t0

    # Summary
    total = games
    p1_wins = results['p1']
    p2_wins = results['p2']
    draws = results['draw']

    summary = {
        'p1': p1_name,
        'p2': p2_name,
        'games': games,
        'p1_wins': p1_wins,
        'p2_wins': p2_wins,
        'draws': draws,
        'p1_win_pct': 100 * p1_wins / total,
        'p2_win_pct': 100 * p2_wins / total,
        'draw_pct': 100 * draws / total,
        'avg_turns': sum(turn_counts) / len(turn_counts) if turn_counts else 0,
        'time_s': dt,
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description='Run AI vs AI tournaments quickly (headless).')
    parser.add_argument('--games', '-g', type=int, default=500, help='Games per matchup (default 500)')
    parser.add_argument('--p1', type=str, default='mage', help='Bot for player 1: mage/rogue/warrior or all')
    parser.add_argument('--p2', type=str, default='rogue', help='Bot for player 2: mage/rogue/warrior or all')
    parser.add_argument('--round-robin', '-r', action='store_true', help='Run a round-robin for the selected bots (each pairing in both directions)')
    parser.add_argument('--bots', type=str, default='mage,rogue,warrior', help='Comma-separated list of bot names or paths to include when using --round-robin or --p1/--p2=all')
    parser.add_argument('--bot-dir', type=str, default=None, help='Directory containing bot .py files - loads all bots from this directory for round-robin')
    parser.add_argument('--include-self', action='store_true', help='Include self vs self matches in round-robin')
    parser.add_argument('--output', '-o', type=str, default=None, help='Optional output file (csv or json) to save aggregated results')
    parser.add_argument('--seed', type=int, default=None, help='Optional random seed')
    args = parser.parse_args()

    # Determine bots list
    if args.bot_dir:
        # Load all bots from directory
        print(f"Loading bots from directory: {args.bot_dir}")
        bots = load_bots_from_directory(args.bot_dir)
        if not bots:
            print(f"No valid bots found in {args.bot_dir}")
            return
        print(f"Found {len(bots)} bots: {', '.join([os.path.basename(b) for b in bots])}\n")
    else:
        # Use comma-separated bot list
        bots = [b.strip() for b in args.bots.split(',') if b.strip()]

    matchups = []
    if args.round_robin:
        # Round-robin: for each unordered pair, run both directions
        for i, a in enumerate(bots):
            for j, b in enumerate(bots):
                if i == j and not args.include_self:
                    continue
                # include both directions (a vs b)
                matchups.append((a, b))
    else:
        # Backwards-compatible behavior for p1/p2 and 'all'
        if args.p1 == 'all' and args.p2 == 'all':
            for a in bots:
                for b in bots:
                    matchups.append((a, b))
        elif args.p1 == 'all':
            for a in bots:
                matchups.append((a, args.p2))
        elif args.p2 == 'all':
            for b in bots:
                matchups.append((args.p1, b))
        else:
            matchups.append((args.p1, args.p2))

    overall = []
    for p1_name, p2_name in matchups:
        print(f"Running {args.games} games: {p1_name} (P1) vs {p2_name} (P2)")
        summary = run_series(p1_name, p2_name, games=args.games, seed=args.seed)
        overall.append(summary)
        print(f"Summary: P1({summary['p1']}) wins: {summary['p1_wins']} ({summary['p1_win_pct']:.1f}%), "
              f"P2({summary['p2']}) wins: {summary['p2_wins']} ({summary['p2_win_pct']:.1f}%), draws: {summary['draws']} ({summary['draw_pct']:.1f}%)\n"
              f"avg turns: {summary['avg_turns']:.1f}, time: {summary['time_s']:.1f}s")

    # Optionally print machine summary
    print('\nAll matchups finished.')

    # Aggregate final results per bot
    bots_seen = set()
    for s in overall:
        bots_seen.add(s['p1'])
        bots_seen.add(s['p2'])

    stats = {b: {'played': 0, 'wins': 0, 'losses': 0, 'draws': 0, 'turns_total': 0.0} for b in bots_seen}
    
    # Head-to-head matrix for cross table: h2h[bot_a][bot_b] = wins by bot_a against bot_b
    h2h = {b: {opponent: 0 for opponent in bots_seen} for b in bots_seen}

    for s in overall:
        p1 = s['p1']
        p2 = s['p2']
        games = s['games']
        p1_w = s['p1_wins']
        p2_w = s['p2_wins']
        draws = s['draws']
        avg_turns = s['avg_turns']

        # For p1
        stats[p1]['played'] += games
        stats[p1]['wins'] += p1_w
        stats[p1]['losses'] += p2_w
        stats[p1]['draws'] += draws
        stats[p1]['turns_total'] += avg_turns * games

        # For p2
        stats[p2]['played'] += games
        stats[p2]['wins'] += p2_w
        stats[p2]['losses'] += p1_w
        stats[p2]['draws'] += draws
        stats[p2]['turns_total'] += avg_turns * games
        
        # Head-to-head
        h2h[p1][p2] += p1_w
        h2h[p2][p1] += p2_w

    # Compute derived stats and print leaderboard
    leaderboard = []
    for b, v in stats.items():
        played = v['played']
        wins = v['wins']
        losses = v['losses']
        draws = v['draws']
        avg_turns = (v['turns_total'] / played) if played > 0 else 0.0
        win_pct = (100.0 * wins / played) if played > 0 else 0.0
        leaderboard.append((b, played, wins, losses, draws, win_pct, avg_turns))

    leaderboard.sort(key=lambda x: x[2], reverse=True)

    print('\nFinal aggregated results:')
    
    # Format data for tabulate
    table_data = []
    for row in leaderboard:
        b, played, wins, losses, draws, win_pct, avg_turns = row
        table_data.append([b, played, wins, losses, draws, f"{win_pct:.1f}%", f"{avg_turns:.1f}"])
    
    headers = ['Bot', 'Played', 'Wins', 'Losses', 'Draws', 'Win%', 'AvgTurns']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Print head-to-head cross table if round-robin
    if args.round_robin and len(bots_seen) > 1:
        print('\nHead-to-Head Cross Table (Row wins vs Column):')
        
        # Get sorted bot names for consistent ordering
        bot_list = [row[0] for row in leaderboard]
        
        # Shorten bot names for display
        def shorten_name(name, max_len=20):
            if len(name) <= max_len:
                return name
            # Try to extract just filename
            basename = os.path.basename(name)
            if len(basename) <= max_len:
                return basename
            # Truncate with ellipsis
            return basename[:max_len-3] + '...'
        
        short_names = [shorten_name(b) for b in bot_list]
        
        # Build cross table
        cross_table = []
        for i, bot_a in enumerate(bot_list):
            row = [short_names[i]]
            for bot_b in bot_list:
                if bot_a == bot_b:
                    row.append('-')
                else:
                    row.append(str(h2h[bot_a][bot_b]))
            cross_table.append(row)
        
        cross_headers = [''] + short_names
        print(tabulate(cross_table, headers=cross_headers, tablefmt='grid'))
        
        # Save cross table to CSV if output specified and round-robin
        if args.output and args.output.lower().endswith('.csv'):
            cross_csv = args.output.replace('.csv', '_crosstable.csv')
            with open(cross_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header with full bot names
                writer.writerow(['Bot'] + bot_list)
                # Write data rows
                for i, bot_a in enumerate(bot_list):
                    row = [bot_a]
                    for bot_b in bot_list:
                        if bot_a == bot_b:
                            row.append('-')
                        else:
                            row.append(h2h[bot_a][bot_b])
                    writer.writerow(row)
            print(f"Wrote cross table to {cross_csv}")

    # Optionally write CSV or JSON
    if args.output:
        out = args.output
        if out.lower().endswith('.csv'):
            with open(out, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['bot', 'played', 'wins', 'losses', 'draws', 'win_pct', 'avg_turns'])
                for row in leaderboard:
                    writer.writerow([row[0], row[1], row[2], row[3], row[4], f"{row[5]:.2f}", f"{row[6]:.2f}"])
            print(f"Wrote aggregated results to {out}")
        else:
            # JSON
            json_obj = []
            for row in leaderboard:
                json_obj.append({'bot': row[0], 'played': row[1], 'wins': row[2], 'losses': row[3], 'draws': row[4], 'win_pct': row[5], 'avg_turns': row[6]})
            with open(out, 'w') as f:
                json.dump(json_obj, f, indent=2)
            print(f"Wrote aggregated results to {out}")


if __name__ == '__main__':
    main()
