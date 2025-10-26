#!/usr/bin/env python
import time
from importlib import import_module
import os
import csv
import numpy as np
from pandas import read_csv
from game_engine import GameEngine

NUM_OF_GAMES = 64

def run_headless_ai_vs_ai(player1_class, player2_class, get_player1_action, get_player2_action):
    """Run AI vs AI without graphics and return winner"""
    engine = GameEngine(get_player1_action, get_player2_action)

    # Set up characters
    engine.set_player_character(player1_class)
    engine.set_opponent_character(player2_class)
    engine.reset(mode="aivai")

    max_turns = 512  # Prevent infinite games
    turn_count = 0

    while not engine.is_game_over() and turn_count < max_turns:
        engine.update()
        turn_count += 1

    if turn_count >= max_turns:
        # Game timed out
        return "Draw"

    return engine.game_over_message

def play(player1, player2):
    '''Run multiple games for testing'''
    player1mod = import_module("submissions."+player1)
    player2mod = import_module("submissions."+player2)
    get_player1_action = getattr(player1mod, "get_bot_action")
    get_player1_class = getattr(player1mod, "get_bot_class")
    get_player2_action = getattr(player2mod, "get_bot_action")
    get_player2_class = getattr(player2mod, "get_bot_class")
    results = []
    for i in range(NUM_OF_GAMES):  # Run multiple games
        player_class_num = get_player1_class()
        opponent_class_num = get_player2_class()
        if player_class_num not in range(3):
            raise ValueError(f"Improper Class value of '{player_class_num}' for player 1")
        if opponent_class_num not in range(3):
            raise ValueError(f"Improper Class value of '{opponent_class_num}' for player 2")

        winner = run_headless_ai_vs_ai(player_class_num, opponent_class_num, get_player1_action, get_player2_action)
        if "Player" in winner:
            results.append(1)
        elif "Opponent" in winner:
            results.append(2)
        elif winner == "Draw":
            results.append(0)
        else:
            raise Error("Unknown result")

    score1 = results.count(1)
    score2 = results.count(2)
    if score1 > score2:
        result = 1
    elif score1 < score2: 
        result = 2
    else:
        result = 0

    print(f"{player1}:{score1}\n{player2}:{score2}\nDraw:{results.count(0)}\n-----------------")
    return result, score1, score2

def print_ranking_table(teams, results):
    """Print a cross-table sorted by rankings"""
    num_teams = len(teams)

    # Calculate total wins for each team
    total_wins = [0] * num_teams
    for i in range(num_teams):
        for j in range(num_teams):
            if i != j:
                total_wins[i] += results[i][j]

    # Create a list of (team_index, team_name, total_wins) and sort by wins
    rankings = [(i, teams[i], total_wins[i]) for i in range(num_teams)]
    rankings.sort(key=lambda x: x[2], reverse=True)

    # Print header
    print("\n" + "=" * 80)
    print("TOURNAMENT RESULTS - SORTED BY RANKINGS")
    print("=" * 80)

    # Print column headers (team names in ranking order)
    header = "Team".ljust(20)
    for _, team_name, _ in rankings:
        header += team_name[:8].ljust(10)  # Shorten names for display
    header += "Total".ljust(10)
    print(header)
    print("-" * len(header))

    # Print each row
    for row_idx, (row_team_idx, row_team_name, row_total_wins) in enumerate(rankings):
        row_str = f"{row_team_name}".ljust(20)

        for col_idx, (col_team_idx, col_team_name, col_total_wins) in enumerate(rankings):
            if row_team_idx == col_team_idx:
                row_str += "X".ljust(10)  # Mark self-match
            else:
                row_str += f"{results[row_team_idx][col_team_idx]}".ljust(10)

        row_str += f"{row_total_wins}".ljust(10)
        print(row_str)

    # Print final rankings
    print("\nFINAL RANKINGS:")
    print("-" * 40)
    for rank, (team_idx, team_name, wins) in enumerate(rankings, 1):
        print(f"{rank}. {team_name}: {wins} wins with a {100* wins/( NUM_OF_GAMES*2*( len(names)-1 ) ):.2f}% win rate")

    return rankings, results

def save_cross_table_to_csv(teams, results, rankings, filename="tournament_results.csv"):
    """Save the cross-table and rankings to a CSV file"""
    num_teams = len(teams)

    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(["Tournament Results - Cross Table"])
        writer.writerow([])

        # Write column headers (team names in ranking order)
        header = ["Team"]
        for _, team_name, _ in rankings:
            header.append(team_name)
        header.append("Total Wins")
        writer.writerow(header)

        # Write each row
        for row_idx, (row_team_idx, row_team_name, row_total_wins) in enumerate(rankings):
            row = [row_team_name]

            for col_idx, (col_team_idx, col_team_name, col_total_wins) in enumerate(rankings):
                if row_team_idx == col_team_idx:
                    row.append("X")  # Mark self-match
                else:
                    row.append(results[row_team_idx][col_team_idx])

            row.append(row_total_wins)
            writer.writerow(row)

        # Add empty row
        writer.writerow([])

        # Write final rankings
        writer.writerow(["Final Rankings:"])
        writer.writerow(["Rank", "Team", "Total Wins"])
        for rank, (team_idx, team_name, wins) in enumerate(rankings, 1):
            writer.writerow([rank, team_name, wins])

        # Add timestamp
        writer.writerow([])
        writer.writerow(["Generated on:", time.strftime("%Y-%m-%d %H:%M:%S")])

    print(f"\nCross-table saved to: {filepath}")

def save_raw_results_matrix(teams, results, filename="raw_results_matrix.csv"):
    """Save the raw results matrix for further analysis"""
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = [""] + list(teams)
        writer.writerow(header)
        
        # Write each row
        for i, team in enumerate(teams):
            row = [team] + list(results[i])
            writer.writerow(row)
    
    print(f"Raw results matrix saved to: {filepath}")


if __name__ == "__main__":
    teams = read_csv('teams.csv')["name"]
    #teams = ['dummy1','dummy2','dummy3','dummy4']
    names = list(teams)
    #names = names[:-2]
    names.sort()
    print(names)
    num_of_teams = len(names)
    results = np.zeros((num_of_teams, num_of_teams), dtype=np.int32)

    for team1 in range(num_of_teams):
        for team2 in range(team1, num_of_teams):
            if team1 == team2:
                continue
            
            result, score1, score2 = play(names[team1], names[team2])
            results[team1][team2] += score1
            results[team2][team1] += score2

            result, score2, score1 = play(names[team2], names[team1])
            results[team1][team2] += score1
            results[team2][team1] += score2
    
    #print("\nRaw Results Matrix:")
    #print(results)
    
    # Print the ranking table
    rankings, final_results = print_ranking_table(names, results)
    # save_cross_table_to_csv(names, final_results, rankings)
    # save_raw_results_matrix(names, final_results)
    save_cross_table_to_csv(names, final_results, rankings, "Results with AI_ML.csv")
    save_raw_results_matrix(names, final_results, "Raw results with AI_ML.csv")
