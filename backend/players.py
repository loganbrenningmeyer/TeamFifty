import json
import http.client
import numpy as np
import copy
import torch
import time
#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi

#connect to API-NFL
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-rapidapi-host': "v1.american-football.api-sports.io",
    'x-rapidapi-key': "7d2dc831201816acd7bfce6f275ded21"
    }
#Logan's Key 7d2dc831201816acd7bfce6f275ded21
#christian's key c70572c71dea5b9097425435a60d972e
# Given a season and league, pull the teams and store into a dictionary {teamID : team_name}
def get_teams_by_season(league, season):
    while (True):
        conn.request("GET", f"/teams?league={league}&season={season}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        # Data as dict
        data = json.loads(data.decode("utf-8"))
        # If data is pulled correctly, break out of the loop
        if (data['results'] != 0):
            print('Teams found')
            break
        else:
            print('Teams not found')
            # If there is an error, print the error and wait 60 seconds
            if (len(data['errors']) != 0):
                print('Error:', data['errors'])
                print('Waiting...')
                time.sleep(60)
            # Otherwise, there must be no data so break
            else:
                break
            
               

    teams = {}

    for result in range(data['results']):
        teamID = data['response'][result]['id']
        team_name = data['response'][result]['name']
        teams[teamID] = team_name
    try:
        del teams[33]
        del teams[34]
    except:
        return teams
    return teams

# Given a team's ID, pull the players and store into a dictionary {player_id : player_name}
def get_players_by_team(teamID, season):

    while (True):
        conn.request("GET", f"/players?team={teamID}&season={season}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        # Data as dict
        data = json.loads(data.decode("utf-8"))

        if (data['results'] != 0):
            print('Players found')
            break
        else:
            print('Players not found, waiting...')
            # If there is an error, print the error and wait 60 seconds
            if (len(data['errors']) != 0):
                print('Error:', data['errors'])
                print('Waiting...')
                time.sleep(60)
            # Otherwise, there must be no data so break
            else:
                break

    players = {}

    #print(data['response'])

    for player in data['response']:
        players[player['id']] = [player['name'], player['position']]

    return players

def get_stats_by_player(player_id, season):
    while (True):
        conn.request("GET", f"/players/statistics?id={player_id}&season={season}", headers=headers)

        # Get the player's stats based on their ID
        res = conn.getresponse()
        data = res.read() 
        data = json.loads(data.decode("utf-8"))

        if (data['results'] != 0):
            print('Player stats found')
            break
        else:
            print('Player stats not found')
            # If there is an error, print the error and wait 60 seconds
            if (len(data['errors']) != 0):
                print('Error:', data['errors'])
                print('Waiting...')
                time.sleep(60)
            # Otherwise, there must be no data so break
            else:
                return None

    #print(data)

    stats = {}

    # Prints the player's stats divided by category (Rushing, Receiving, Defense, Passing, Scoring, Returning)
    for group in data['response'][0]['teams'][0]['groups']:
        
        stats[group['name']] = {}
        # Print the stats for each category
        for stat in group['statistics']:
            stats[group['name']][stat['name']] = stat['value']
    
    return stats

def print_stats(stats):
    for group, stat in stats.items():
        print(f"\n---{group}---\n")
        for name, value in stat.items():
            print(f"{name}: {value}")

# # Order of stats by position
# Offense: QB, RB, FB, WR, TE, C, G, OT
# Defense: DE, DT, CB, LB, S
# Special: PK, P, LS
def compile_stats(stats):

    # Dictionary containing all stats for each possible position
    # Used to fill in missing stats with 0
    stats_by_position = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 1, 'yards per rush avg': 2, 'longest rush': 3, 'over 20 yards': 4, 'rushing touchdowns': 5, 'yards per game': 6, 'fumbles': 7, 'fumbles lost': 8, 'rushing first downs': 9}, 'Receiving': {'receptions': 10, 'receiving targets': 11, 'receiving yards': 12, 'yards per reception avg': 13, 'receiving touchdowns': 14, 'longest reception': 15, 'over 20 yards': 16, 'yards per game': 17, 'fumbles': 18, 'fumbles lost': 19, 'yards after catch': 20, 'receiving first downs': 21}, 'Defense': {'unassisted tackles': 22, 'assisted tackles': 23, 'total tackles': 24, 'sacks': 25, 'yards lost on sack': 26, 'tackles for loss': 27, 'passes defended': 28, 'interceptions': 29, 'intercepted returned yards': 30, 'longest interception return': 31, 'interceptions returned for touchdowns': 32, 'forced fumbles': 33, 'fumbles recovered': 34, 'fumbles returned for touchdowns': 35, 'blocked kicks': 36}, 'Scoring': {'rushing touchdowns': 37, 'receiving touchdowns': 38, 'return touchdowns': 39, 'total touchdowns': 40, 'field goals': 41, 'extra points': 42, 'two point conversions': 43, 'total points': 44, 'total points per game': 45}, 'Returning': {'kickoff returned attempts': 46, 'kickoff return yards': 47, 'yards per kickoff avg': 48, 'longes kickoff return': 49, 'kickoff return touchdows': 50, 'punts returned': 51, 'yards returned on punts': 52, 'yards per punt avg': 53, 'longest punt return': 54, 'punt return touchdowns': 55, 'fair catches': 56}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Returning': {'kickoff returned attempts': 27, 'kickoff return yards': 28, 'yards per kickoff avg': 29, 'longes kickoff return': 30, 'kickoff return touchdows': 31, 'punts returned': 32, 'yards returned on punts': 33, 'yards per punt avg': 34, 'longest punt return': 35, 'punt return touchdowns': 36, 'fair catches': 37}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Scoring': {'rushing touchdowns': 27, 'receiving touchdowns': 28, 'return touchdowns': 29, 'total touchdowns': 30, 'field goals': 31, 'extra points': 32, 'two point conversions': 33, 'total points': 34, 'total points per game': 35}, 'Rushing': {'rushing attempts': 36, 'yards': 37, 'yards per rush avg': 38, 'longest rush': 39, 'over 20 yards': 40, 'rushing touchdowns': 41, 'yards per game': 42, 'fumbles': 43, 'fumbles lost': 44, 'rushing first downs': 45}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}, 'Scoring': {'rushing touchdowns': 15, 'receiving touchdowns': 16, 'return touchdowns': 17, 'total touchdowns': 18, 'field goals': 19, 'extra points': 20, 'two point conversions': 21, 'total points': 22, 'total points per game': 23}, 'Kicking': {'field goals made': 24, 'field goals attempts': 25, 'field goals made pct': 26, 'longest goal made': 27, 'field goals from 1 19 yards': 28, 'field goals from 20 29 yards': 29, 'field goals from 30 39 yards': 30, 'field goals from 40 49 yards': 31, 'field goals from 50 yards': 32, 'extra points made': 33, 'extra points attempts': 34, 'extra points made pct': 35}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 1, 'longest punt': 2, 'gross punting avg': 3, 'net punting avg': 4, 'blocked punts': 5, 'inside 20 yards punt': 6, 'touchbacks': 7, 'fair catches': 8, 'punts returned': 9, 'yards returned on punts': 10, 'yards returned on punts avg': 11}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 1, 'completion pct': 2, 'yards': 3, 'yards per pass avg': 4, 'yards per game': 5, 'longest pass': 6, 'passing touchdowns': 7, 'passing touchdowns pct': 8, 'interceptions': 9, 'interceptions pct': 10, 'sacks': 11, 'sacked yards lost': 12, 'quaterback rating': 13}, 'Rushing': {'rushing attempts': 14, 'yards': 15, 'yards per rush avg': 16, 'longest rush': 17, 'over 20 yards': 18, 'rushing touchdowns': 19, 'yards per game': 20, 'fumbles': 21, 'fumbles lost': 22, 'rushing first downs': 23}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}}
    
    compiled_stats = np.array([])
    
    # Fix PK values (28-32) (turn from string to float)
    # These values are written as 'x-y' (x made, y attempted)
    if ('PK' in stats):
        pk = stats['PK']
        for i in range(28,33):
            x,y = stats['PK'][i].split('-')
            x = float(x)
            y = float(y)
            if y == 0:
                stats['PK'][i] = 0
            else:
                stats['PK'][i] = round(x / y,5)

    # Set order of stats by position in the compiled stats array
    order = ['QB', 'RB', 'FB', 'WR', 'TE', 'C', 'G', 'OT', 'DE', 'DT', 'CB', 'LB', 'S', 'PK', 'P', 'LS']
    for position in order:
        # If the position does not have stats, add 0s for each stat
        if position not in stats:
            # Get number of stats for the position
            for group in stats_by_position[position]:
                for stat in stats_by_position[position][group]:
                    compiled_stats = np.append(compiled_stats, 0)
        else:
            compiled_stats = np.append(compiled_stats, stats[position])
    # Replace None values with 0
    compiled_stats[compiled_stats == None] = 0

    return compiled_stats

# Using the dictionary of all stats by position, fill in stats that are within the dictionary
# and fill any missing stats with 0

'''
Choosing which players to include in the model:

- Select a set number of players based on the position
- For each position, select the top players based on the stats
    - Average the stats for each player and select the top players based on the average stats

- NUMBER OF PLAYERS TO SELECT FOR EACH POSITION (38 total)
    - QB: 1
    - RB: 3
    - FB: 1
    - WR: 5
    - TE: 3
    - OT: 1
    - C: 1
    - G: 1
    - DE: 2
    - DT: 3
    - CB: 5
    - S: 3
    - LB: 6
    - PK: 1
    - P: 1
    - LS: 1

New function to get the top players for each position
- Get the stats for each player (by position)
- Average the stats for each player
- Sort the players by the average stats
- Select the top players based on the number of players to select for each position
    - If there are less players than the number to select, fill in the remaining spots with league averages

'''
def get_player_stats(teamID, season):
    # --- STEP 1. Get all stats for each player on the team (fill blanks w/ averages) ---
    players = get_players_by_team(teamID, season)

    # Dictionary containing stats by position
    stats_by_position = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 1, 'yards per rush avg': 2, 'longest rush': 3, 'over 20 yards': 4, 'rushing touchdowns': 5, 'yards per game': 6, 'fumbles': 7, 'fumbles lost': 8, 'rushing first downs': 9}, 'Receiving': {'receptions': 10, 'receiving targets': 11, 'receiving yards': 12, 'yards per reception avg': 13, 'receiving touchdowns': 14, 'longest reception': 15, 'over 20 yards': 16, 'yards per game': 17, 'fumbles': 18, 'fumbles lost': 19, 'yards after catch': 20, 'receiving first downs': 21}, 'Defense': {'unassisted tackles': 22, 'assisted tackles': 23, 'total tackles': 24, 'sacks': 25, 'yards lost on sack': 26, 'tackles for loss': 27, 'passes defended': 28, 'interceptions': 29, 'intercepted returned yards': 30, 'longest interception return': 31, 'interceptions returned for touchdowns': 32, 'forced fumbles': 33, 'fumbles recovered': 34, 'fumbles returned for touchdowns': 35, 'blocked kicks': 36}, 'Scoring': {'rushing touchdowns': 37, 'receiving touchdowns': 38, 'return touchdowns': 39, 'total touchdowns': 40, 'field goals': 41, 'extra points': 42, 'two point conversions': 43, 'total points': 44, 'total points per game': 45}, 'Returning': {'kickoff returned attempts': 46, 'kickoff return yards': 47, 'yards per kickoff avg': 48, 'longes kickoff return': 49, 'kickoff return touchdows': 50, 'punts returned': 51, 'yards returned on punts': 52, 'yards per punt avg': 53, 'longest punt return': 54, 'punt return touchdowns': 55, 'fair catches': 56}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Returning': {'kickoff returned attempts': 27, 'kickoff return yards': 28, 'yards per kickoff avg': 29, 'longes kickoff return': 30, 'kickoff return touchdows': 31, 'punts returned': 32, 'yards returned on punts': 33, 'yards per punt avg': 34, 'longest punt return': 35, 'punt return touchdowns': 36, 'fair catches': 37}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Scoring': {'rushing touchdowns': 27, 'receiving touchdowns': 28, 'return touchdowns': 29, 'total touchdowns': 30, 'field goals': 31, 'extra points': 32, 'two point conversions': 33, 'total points': 34, 'total points per game': 35}, 'Rushing': {'rushing attempts': 36, 'yards': 37, 'yards per rush avg': 38, 'longest rush': 39, 'over 20 yards': 40, 'rushing touchdowns': 41, 'yards per game': 42, 'fumbles': 43, 'fumbles lost': 44, 'rushing first downs': 45}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}, 'Scoring': {'rushing touchdowns': 15, 'receiving touchdowns': 16, 'return touchdowns': 17, 'total touchdowns': 18, 'field goals': 19, 'extra points': 20, 'two point conversions': 21, 'total points': 22, 'total points per game': 23}, 'Kicking': {'field goals made': 24, 'field goals attempts': 25, 'field goals made pct': 26, 'longest goal made': 27, 'field goals from 1 19 yards': 28, 'field goals from 20 29 yards': 29, 'field goals from 30 39 yards': 30, 'field goals from 40 49 yards': 31, 'field goals from 50 yards': 32, 'extra points made': 33, 'extra points attempts': 34, 'extra points made pct': 35}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 1, 'longest punt': 2, 'gross punting avg': 3, 'net punting avg': 4, 'blocked punts': 5, 'inside 20 yards punt': 6, 'touchbacks': 7, 'fair catches': 8, 'punts returned': 9, 'yards returned on punts': 10, 'yards returned on punts avg': 11}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 1, 'completion pct': 2, 'yards': 3, 'yards per pass avg': 4, 'yards per game': 5, 'longest pass': 6, 'passing touchdowns': 7, 'passing touchdowns pct': 8, 'interceptions': 9, 'interceptions pct': 10, 'sacks': 11, 'sacked yards lost': 12, 'quaterback rating': 13}, 'Rushing': {'rushing attempts': 14, 'yards': 15, 'yards per rush avg': 16, 'longest rush': 17, 'over 20 yards': 18, 'rushing touchdowns': 19, 'yards per game': 20, 'fumbles': 21, 'fumbles lost': 22, 'rushing first downs': 23}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}}

    # Dictionary containing average stats by position
    avg_stats_by_position = {'RB': {'Rushing': {'rushing attempts': 76.4375, 'yards': 319.38125, 'yards per rush avg': 3.59813, 'longest rush': 22.94375, 'over 20 yards': 1.65, 'rushing touchdowns': 2.15625, 'yards per game': 24.54375, 'fumbles': 0.525, 'fumbles lost': 0.29375, 'rushing first downs': 16.775}, 'Receiving': {'receptions': 15.83125, 'receiving targets': 20.34375, 'receiving yards': 113.25625, 'yards per reception avg': 6.1775, 'receiving touchdowns': 0.58125, 'longest reception': 20.74375, 'over 20 yards': 0.975, 'yards per game': 8.84563, 'fumbles': 0.19375, 'fumbles lost': 0.10625, 'yards after catch': 125.85, 'receiving first downs': 4.9}, 'Defense': {'unassisted tackles': 0.675, 'assisted tackles': 0.39375, 'total tackles': 1.06875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01875, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 2.1625, 'receiving touchdowns': 0.58125, 'return touchdowns': 0.00625, 'total touchdowns': 2.75, 'field goals': 0.00625, 'extra points': 0.0, 'two point conversions': 0.1375, 'total points': 16.79375, 'total points per game': 1.31}, 'Returning': {'kickoff returned attempts': 1.56875, 'kickoff return yards': 36.4625, 'yards per kickoff avg': 5.84937, 'longes kickoff return': 8.30625, 'kickoff return touchdows': 0.00625, 'punts returned': 0.25, 'yards returned on punts': 2.13125, 'yards per punt avg': 0.215, 'longest punt return': 0.475, 'punt return touchdowns': 0.0, 'fair catches': 0.16875}}, 'FB': {'Receiving': {'receptions': 5.38462, 'receiving targets': 6.69231, 'receiving yards': 35.30769, 'yards per reception avg': 5.31538, 'receiving touchdowns': 0.38462, 'longest reception': 12.69231, 'over 20 yards': 0.38462, 'yards per game': 2.18462, 'fumbles': 0.07692, 'fumbles lost': 0.07692, 'yards after catch': 23.53846, 'receiving first downs': 1.92308}, 'Defense': {'unassisted tackles': 1.92308, 'assisted tackles': 1.0, 'total tackles': 2.92308, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.23077, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Returning': {'kickoff returned attempts': 0.38462, 'kickoff return yards': 10.53846, 'yards per kickoff avg': 6.92308, 'longes kickoff return': 9.84615, 'kickoff return touchdows': 0.07692, 'punts returned': 0.0, 'yards returned on punts': 0.0, 'yards per punt avg': 0.0, 'longest punt return': 0.0, 'punt return touchdowns': 0.0, 'fair catches': 0.0}}, 'WR': {'Receiving': {'receptions': 27.83333, 'receiving targets': 44.25417, 'receiving yards': 352.89583, 'yards per reception avg': 10.775, 'receiving touchdowns': 2.08333, 'longest reception': 34.27083, 'over 20 yards': 5.07083, 'yards per game': 24.6625, 'fumbles': 0.3375, 'fumbles lost': 0.175, 'yards after catch': 121.625, 'receiving first downs': 16.44583}, 'Defense': {'unassisted tackles': 1.07917, 'assisted tackles': 0.22083, 'total tackles': 1.3, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01667, 'fumbles recovered': 0.00833, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.1, 'receiving touchdowns': 2.10417, 'return touchdowns': 0.05417, 'total touchdowns': 2.25833, 'field goals': 0.0, 'extra points': 0.0, 'two point conversions': 0.10417, 'total points': 13.75833, 'total points per game': 0.98333}, 'Rushing': {'rushing attempts': 2.0125, 'yards': 12.16667, 'yards per rush avg': 2.41708, 'longest rush': 5.72083, 'over 20 yards': 0.10833, 'rushing touchdowns': 0.09583, 'yards per game': 0.87917, 'fumbles': 0.02083, 'fumbles lost': 0.00417, 'rushing first downs': 0.6625}}, 'TE': {'Receiving': {'receptions': 21.03175, 'receiving targets': 29.59524, 'receiving yards': 218.06349, 'yards per reception avg': 9.22619, 'receiving touchdowns': 1.42063, 'longest reception': 24.68254, 'over 20 yards': 2.54762, 'yards per game': 15.15397, 'fumbles': 0.23016, 'fumbles lost': 0.13492, 'yards after catch': 103.57143, 'receiving first downs': 10.97619}, 'Defense': {'unassisted tackles': 1.23016, 'assisted tackles': 0.54762, 'total tackles': 1.77778, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.00794, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.02381, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.01587}}, 'C': {'Defense': {'unassisted tackles': 0.72222, 'assisted tackles': 0.38889, 'total tackles': 1.11111, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.05556, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'G': {'Defense': {'unassisted tackles': 1.0, 'assisted tackles': 0.13158, 'total tackles': 1.13158, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'OT': {'Defense': {'unassisted tackles': 0.90625, 'assisted tackles': 0.28125, 'total tackles': 1.1875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'DE': {'Defense': {'unassisted tackles': 12.17123, 'assisted tackles': 9.20548, 'total tackles': 21.37671, 'sacks': 2.65068, 'yards lost on sack': 18.23288, 'tackles for loss': 3.47945, 'passes defended': 1.06164, 'interceptions': 0.03425, 'intercepted returned yards': 0.33562, 'longest interception return': 0.29452, 'interceptions returned for touchdowns': 0.00685, 'forced fumbles': 0.39726, 'fumbles recovered': 0.26027, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.11644}}, 'DT': {'Defense': {'unassisted tackles': 12.46961, 'assisted tackles': 11.51381, 'total tackles': 23.98343, 'sacks': 1.71547, 'yards lost on sack': 11.43646, 'tackles for loss': 2.87845, 'passes defended': 0.86188, 'interceptions': 0.03867, 'intercepted returned yards': 0.07735, 'longest interception return': 0.07735, 'interceptions returned for touchdowns': 0.00552, 'forced fumbles': 0.24862, 'fumbles recovered': 0.24862, 'fumbles returned for touchdowns': 0.0221, 'blocked kicks': 0.02762}}, 'LB': {'Defense': {'unassisted tackles': 23.31902, 'assisted tackles': 15.02454, 'total tackles': 38.34356, 'sacks': 1.76687, 'yards lost on sack': 11.93558, 'tackles for loss': 3.26687, 'passes defended': 1.40798, 'interceptions': 0.24847, 'intercepted returned yards': 3.51534, 'longest interception return': 2.80982, 'interceptions returned for touchdowns': 0.03067, 'forced fumbles': 0.46933, 'fumbles recovered': 0.30982, 'fumbles returned for touchdowns': 0.02147, 'blocked kicks': 0.00307}}, 'CB': {'Defense': {'unassisted tackles': 21.67054, 'assisted tackles': 6.55814, 'total tackles': 28.22868, 'sacks': 0.1376, 'yards lost on sack': 0.94961, 'tackles for loss': 1.02713, 'passes defended': 4.21705, 'interceptions': 0.64341, 'intercepted returned yards': 7.70155, 'longest interception return': 5.9186, 'interceptions returned for touchdowns': 0.09302, 'forced fumbles': 0.3062, 'fumbles recovered': 0.18992, 'fumbles returned for touchdowns': 0.00775, 'blocked kicks': 0.00775}}, 'S': {'Defense': {'unassisted tackles': 29.30851, 'assisted tackles': 13.64894, 'total tackles': 42.95745, 'sacks': 0.38298, 'yards lost on sack': 2.90426, 'tackles for loss': 1.38298, 'passes defended': 2.98936, 'interceptions': 0.89362, 'intercepted returned yards': 13.3883, 'longest interception return': 10.31383, 'interceptions returned for touchdowns': 0.07447, 'forced fumbles': 0.45745, 'fumbles recovered': 0.30851, 'fumbles returned for touchdowns': 0.02128, 'blocked kicks': 0.03191}}, 'PK': {'Defense': {'unassisted tackles': 0.34783, 'assisted tackles': 0.0, 'total tackles': 0.34783, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.0, 'receiving touchdowns': 0.0, 'return touchdowns': 0.0, 'total touchdowns': 0.0, 'field goals': 22.95652, 'extra points': 27.58696, 'two point conversions': 0.0, 'total points': 96.45652, 'total points per game': 7.01739}, 'Kicking': {'field goals made': 22.95652, 'field goals attempts': 26.5, 'field goals made pct': 86.56304, 'longest goal made': 53.63043, 'field goals from 1 19 yards': 0.02174, 'field goals from 20 29 yards': 0.87319, 'field goals from 30 39 yards': 0.96027, 'field goals from 40 49 yards': 0.76699, 'field goals from 50 yards': 0.62671, 'extra points made': 27.58696, 'extra points attempts': 28.95652, 'extra points made pct': 94.21957}}, 'P': {'Punting': {'punts': 56.11905, 'gross punt yards': 2668.57143, 'longest punt': 67.2381, 'gross punting avg': 47.66905, 'net punting avg': 41.66905, 'blocked punts': 0.11905, 'inside 20 yards punt': 20.30952, 'touchbacks': 4.07143, 'fair catches': 15.69048, 'punts returned': 24.42857, 'yards returned on punts': 238.90476, 'yards returned on punts avg': 10.1}}, 'QB': {'Passing': {'passing attempts': 217.44828, 'completions': 139.34483, 'completion pct': 59.45977, 'yards': 1515.97701, 'yards per pass avg': 6.66897, 'yards per game': 145.70575, 'longest pass': 49.93103, 'passing touchdowns': 8.78161, 'passing touchdowns pct': 0, 'interceptions': 5.18391, 'interceptions pct': 0, 'sacks': 16.51724, 'sacked yards lost': 111.34483, 'quaterback rating': 78.84713}, 'Rushing': {'rushing attempts': 28.08046, 'yards': 119.7931, 'yards per rush avg': 3.37241, 'longest rush': 15.51724, 'over 20 yards': 0.8046, 'rushing touchdowns': 1.34483, 'yards per game': 12.1908, 'fumbles': 1.54023, 'fumbles lost': 0.56322, 'rushing first downs': 9.71264}}, 'LS': {'Defense': {'unassisted tackles': 1.57143, 'assisted tackles': 1.21429, 'total tackles': 2.78571, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.10714, 'fumbles recovered': 0.03571, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}}

    # --- STEP 2. Group player stats by position ---
    # Make a dictionary of players by position (including their playerID)

    # Order of stats by position:
    # Offense: QB, RB, FB, WR, TE, C, G, OT
    # Defense: DE, DT, CB, LB, S
    # Special: PK, P, LS
    players_by_position = {'QB': {}, 'RB': {}, 'FB': {}, 'WR': {}, 'TE': {}, 'C': {}, 'G': {}, 'OT': {}, 'DE': {}, 'DT': {}, 'CB': {}, 'LB': {}, 'S': {}, 'PK': {}, 'P': {}, 'LS': {}}

    # Iterate through players and add them to the dictionary
    for playerID, player_info in players.items():
        # Position
        position = player_info[1]
        # Stats
        player_stats = get_stats_by_player(playerID, season)

        # Check if the player's stats are available
        # If not, fill with average values
        if (player_stats == None):
            player_stats = avg_stats_by_position[position]

        # Fill stats with average values
        # Check if the player's stats are missing any groups
        for group in avg_stats_by_position[position]:
            if group not in player_stats:
                player_stats[group] = avg_stats_by_position[position][group]
        
        # Flatten the stats dictionary into an array in the proper order
        stats = []
        for group in stats_by_position[position]:
            for stat in stats_by_position[position][group]:
                # Attempt conversion to float, otherwise convert to ratio
                # If the stat is a ratio (not a negative number), convert to a float
                if ('-' in str(player_stats[group][stat]) and str(player_stats[group][stat][0]).isdigit()):
                    num, den = player_stats[group][stat].split('-')
                    if (den == '0'):
                        stats.append(0)
                    else:
                        stats.append(float(num) / float(den))
                # If the stat is >= 1,000 and written with a comma, remove the comma and convert to a float
                elif (',' in str(player_stats[group][stat])):
                    stats.append(float(player_stats[group][stat].replace(',', '')))
                # If the stat is None, fill with 0
                elif (player_stats[group][stat] == None):
                    stats.append(0)
                else:
                    stats.append(float(player_stats[group][stat]))

        # Add the player to the dictionary
        players_by_position[position][playerID] = stats

    # --- STEP 3. Average stats for each player in each position and sort positions by the average ---
    avg_stats_by_player = {position: {} for position in players_by_position.keys()}
    # Average each player's stats
    for position, players in players_by_position.items():
        for playerID, stats in players.items():
            avg_stats_by_player[position][playerID] = np.mean(stats, axis=0)

    # Sort the dictionary by player's averages
    avg_stats_by_player = {
        position: dict(sorted(player_stats.items(), key=lambda x: x[1], reverse=True))
        for position, player_stats in avg_stats_by_player.items()
    }

    # --- STEP 4. Take the top n players per position ---
    # - NUMBER OF PLAYERS TO SELECT FOR EACH POSITION (38 total)
    # - QB: 1
    # - RB: 3
    # - FB: 1
    # - WR: 5
    # - TE: 3
    # - OT: 1
    # - C: 1
    # - G: 1
    # - DE: 2
    # - DT: 3
    # - CB: 5
    # - S: 3
    # - LB: 6
    # - PK: 1
    # - P: 1
    # - LS: 1

    # Dictionary containing the top n players per position
    players_per_position = {'QB': 1, 'RB': 3, 'FB': 1, 'WR': 5, 'TE': 3, 'OT': 1, 'C': 1, 'G': 1, 'DE': 2, 'DT': 3, 'CB': 5, 'S': 3, 'LB': 6, 'PK': 1, 'P': 1, 'LS': 1}

    # Select the top n players per position
    for position in players_per_position:
        players_by_position[position] = {k: v for k, v in players_by_position[position].items() if k in list(avg_stats_by_player[position].keys())[:players_per_position[position]]}
    
    # Condense all player stats into one 1D array
    condensed_stats = [stat for position in players_by_position for player in players_by_position[position] for stat in players_by_position[position][player]]

    return condensed_stats

def get_stats_by_position(teamID, season):
    players = get_players_by_team(teamID, season)

    # Dictionary containing stats by position
    stats_by_position = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 1, 'yards per rush avg': 2, 'longest rush': 3, 'over 20 yards': 4, 'rushing touchdowns': 5, 'yards per game': 6, 'fumbles': 7, 'fumbles lost': 8, 'rushing first downs': 9}, 'Receiving': {'receptions': 10, 'receiving targets': 11, 'receiving yards': 12, 'yards per reception avg': 13, 'receiving touchdowns': 14, 'longest reception': 15, 'over 20 yards': 16, 'yards per game': 17, 'fumbles': 18, 'fumbles lost': 19, 'yards after catch': 20, 'receiving first downs': 21}, 'Defense': {'unassisted tackles': 22, 'assisted tackles': 23, 'total tackles': 24, 'sacks': 25, 'yards lost on sack': 26, 'tackles for loss': 27, 'passes defended': 28, 'interceptions': 29, 'intercepted returned yards': 30, 'longest interception return': 31, 'interceptions returned for touchdowns': 32, 'forced fumbles': 33, 'fumbles recovered': 34, 'fumbles returned for touchdowns': 35, 'blocked kicks': 36}, 'Scoring': {'rushing touchdowns': 37, 'receiving touchdowns': 38, 'return touchdowns': 39, 'total touchdowns': 40, 'field goals': 41, 'extra points': 42, 'two point conversions': 43, 'total points': 44, 'total points per game': 45}, 'Returning': {'kickoff returned attempts': 46, 'kickoff return yards': 47, 'yards per kickoff avg': 48, 'longes kickoff return': 49, 'kickoff return touchdows': 50, 'punts returned': 51, 'yards returned on punts': 52, 'yards per punt avg': 53, 'longest punt return': 54, 'punt return touchdowns': 55, 'fair catches': 56}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Returning': {'kickoff returned attempts': 27, 'kickoff return yards': 28, 'yards per kickoff avg': 29, 'longes kickoff return': 30, 'kickoff return touchdows': 31, 'punts returned': 32, 'yards returned on punts': 33, 'yards per punt avg': 34, 'longest punt return': 35, 'punt return touchdowns': 36, 'fair catches': 37}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Scoring': {'rushing touchdowns': 27, 'receiving touchdowns': 28, 'return touchdowns': 29, 'total touchdowns': 30, 'field goals': 31, 'extra points': 32, 'two point conversions': 33, 'total points': 34, 'total points per game': 35}, 'Rushing': {'rushing attempts': 36, 'yards': 37, 'yards per rush avg': 38, 'longest rush': 39, 'over 20 yards': 40, 'rushing touchdowns': 41, 'yards per game': 42, 'fumbles': 43, 'fumbles lost': 44, 'rushing first downs': 45}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}, 'Scoring': {'rushing touchdowns': 15, 'receiving touchdowns': 16, 'return touchdowns': 17, 'total touchdowns': 18, 'field goals': 19, 'extra points': 20, 'two point conversions': 21, 'total points': 22, 'total points per game': 23}, 'Kicking': {'field goals made': 24, 'field goals attempts': 25, 'field goals made pct': 26, 'longest goal made': 27, 'field goals from 1 19 yards': 28, 'field goals from 20 29 yards': 29, 'field goals from 30 39 yards': 30, 'field goals from 40 49 yards': 31, 'field goals from 50 yards': 32, 'extra points made': 33, 'extra points attempts': 34, 'extra points made pct': 35}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 1, 'longest punt': 2, 'gross punting avg': 3, 'net punting avg': 4, 'blocked punts': 5, 'inside 20 yards punt': 6, 'touchbacks': 7, 'fair catches': 8, 'punts returned': 9, 'yards returned on punts': 10, 'yards returned on punts avg': 11}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 1, 'completion pct': 2, 'yards': 3, 'yards per pass avg': 4, 'yards per game': 5, 'longest pass': 6, 'passing touchdowns': 7, 'passing touchdowns pct': 8, 'interceptions': 9, 'interceptions pct': 10, 'sacks': 11, 'sacked yards lost': 12, 'quaterback rating': 13}, 'Rushing': {'rushing attempts': 14, 'yards': 15, 'yards per rush avg': 16, 'longest rush': 17, 'over 20 yards': 18, 'rushing touchdowns': 19, 'yards per game': 20, 'fumbles': 21, 'fumbles lost': 22, 'rushing first downs': 23}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}}

    # Dictionary containing average stats by position
    avg_stats_by_position = {'RB': {'Rushing': {'rushing attempts': 76.4375, 'yards': 319.38125, 'yards per rush avg': 3.59813, 'longest rush': 22.94375, 'over 20 yards': 1.65, 'rushing touchdowns': 2.15625, 'yards per game': 24.54375, 'fumbles': 0.525, 'fumbles lost': 0.29375, 'rushing first downs': 16.775}, 'Receiving': {'receptions': 15.83125, 'receiving targets': 20.34375, 'receiving yards': 113.25625, 'yards per reception avg': 6.1775, 'receiving touchdowns': 0.58125, 'longest reception': 20.74375, 'over 20 yards': 0.975, 'yards per game': 8.84563, 'fumbles': 0.19375, 'fumbles lost': 0.10625, 'yards after catch': 125.85, 'receiving first downs': 4.9}, 'Defense': {'unassisted tackles': 0.675, 'assisted tackles': 0.39375, 'total tackles': 1.06875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01875, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 2.1625, 'receiving touchdowns': 0.58125, 'return touchdowns': 0.00625, 'total touchdowns': 2.75, 'field goals': 0.00625, 'extra points': 0.0, 'two point conversions': 0.1375, 'total points': 16.79375, 'total points per game': 1.31}, 'Returning': {'kickoff returned attempts': 1.56875, 'kickoff return yards': 36.4625, 'yards per kickoff avg': 5.84937, 'longes kickoff return': 8.30625, 'kickoff return touchdows': 0.00625, 'punts returned': 0.25, 'yards returned on punts': 2.13125, 'yards per punt avg': 0.215, 'longest punt return': 0.475, 'punt return touchdowns': 0.0, 'fair catches': 0.16875}}, 'FB': {'Receiving': {'receptions': 5.38462, 'receiving targets': 6.69231, 'receiving yards': 35.30769, 'yards per reception avg': 5.31538, 'receiving touchdowns': 0.38462, 'longest reception': 12.69231, 'over 20 yards': 0.38462, 'yards per game': 2.18462, 'fumbles': 0.07692, 'fumbles lost': 0.07692, 'yards after catch': 23.53846, 'receiving first downs': 1.92308}, 'Defense': {'unassisted tackles': 1.92308, 'assisted tackles': 1.0, 'total tackles': 2.92308, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.23077, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Returning': {'kickoff returned attempts': 0.38462, 'kickoff return yards': 10.53846, 'yards per kickoff avg': 6.92308, 'longes kickoff return': 9.84615, 'kickoff return touchdows': 0.07692, 'punts returned': 0.0, 'yards returned on punts': 0.0, 'yards per punt avg': 0.0, 'longest punt return': 0.0, 'punt return touchdowns': 0.0, 'fair catches': 0.0}}, 'WR': {'Receiving': {'receptions': 27.83333, 'receiving targets': 44.25417, 'receiving yards': 352.89583, 'yards per reception avg': 10.775, 'receiving touchdowns': 2.08333, 'longest reception': 34.27083, 'over 20 yards': 5.07083, 'yards per game': 24.6625, 'fumbles': 0.3375, 'fumbles lost': 0.175, 'yards after catch': 121.625, 'receiving first downs': 16.44583}, 'Defense': {'unassisted tackles': 1.07917, 'assisted tackles': 0.22083, 'total tackles': 1.3, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01667, 'fumbles recovered': 0.00833, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.1, 'receiving touchdowns': 2.10417, 'return touchdowns': 0.05417, 'total touchdowns': 2.25833, 'field goals': 0.0, 'extra points': 0.0, 'two point conversions': 0.10417, 'total points': 13.75833, 'total points per game': 0.98333}, 'Rushing': {'rushing attempts': 2.0125, 'yards': 12.16667, 'yards per rush avg': 2.41708, 'longest rush': 5.72083, 'over 20 yards': 0.10833, 'rushing touchdowns': 0.09583, 'yards per game': 0.87917, 'fumbles': 0.02083, 'fumbles lost': 0.00417, 'rushing first downs': 0.6625}}, 'TE': {'Receiving': {'receptions': 21.03175, 'receiving targets': 29.59524, 'receiving yards': 218.06349, 'yards per reception avg': 9.22619, 'receiving touchdowns': 1.42063, 'longest reception': 24.68254, 'over 20 yards': 2.54762, 'yards per game': 15.15397, 'fumbles': 0.23016, 'fumbles lost': 0.13492, 'yards after catch': 103.57143, 'receiving first downs': 10.97619}, 'Defense': {'unassisted tackles': 1.23016, 'assisted tackles': 0.54762, 'total tackles': 1.77778, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.00794, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.02381, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.01587}}, 'C': {'Defense': {'unassisted tackles': 0.72222, 'assisted tackles': 0.38889, 'total tackles': 1.11111, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.05556, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'G': {'Defense': {'unassisted tackles': 1.0, 'assisted tackles': 0.13158, 'total tackles': 1.13158, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'OT': {'Defense': {'unassisted tackles': 0.90625, 'assisted tackles': 0.28125, 'total tackles': 1.1875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'DE': {'Defense': {'unassisted tackles': 12.17123, 'assisted tackles': 9.20548, 'total tackles': 21.37671, 'sacks': 2.65068, 'yards lost on sack': 18.23288, 'tackles for loss': 3.47945, 'passes defended': 1.06164, 'interceptions': 0.03425, 'intercepted returned yards': 0.33562, 'longest interception return': 0.29452, 'interceptions returned for touchdowns': 0.00685, 'forced fumbles': 0.39726, 'fumbles recovered': 0.26027, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.11644}}, 'DT': {'Defense': {'unassisted tackles': 12.46961, 'assisted tackles': 11.51381, 'total tackles': 23.98343, 'sacks': 1.71547, 'yards lost on sack': 11.43646, 'tackles for loss': 2.87845, 'passes defended': 0.86188, 'interceptions': 0.03867, 'intercepted returned yards': 0.07735, 'longest interception return': 0.07735, 'interceptions returned for touchdowns': 0.00552, 'forced fumbles': 0.24862, 'fumbles recovered': 0.24862, 'fumbles returned for touchdowns': 0.0221, 'blocked kicks': 0.02762}}, 'LB': {'Defense': {'unassisted tackles': 23.31902, 'assisted tackles': 15.02454, 'total tackles': 38.34356, 'sacks': 1.76687, 'yards lost on sack': 11.93558, 'tackles for loss': 3.26687, 'passes defended': 1.40798, 'interceptions': 0.24847, 'intercepted returned yards': 3.51534, 'longest interception return': 2.80982, 'interceptions returned for touchdowns': 0.03067, 'forced fumbles': 0.46933, 'fumbles recovered': 0.30982, 'fumbles returned for touchdowns': 0.02147, 'blocked kicks': 0.00307}}, 'CB': {'Defense': {'unassisted tackles': 21.67054, 'assisted tackles': 6.55814, 'total tackles': 28.22868, 'sacks': 0.1376, 'yards lost on sack': 0.94961, 'tackles for loss': 1.02713, 'passes defended': 4.21705, 'interceptions': 0.64341, 'intercepted returned yards': 7.70155, 'longest interception return': 5.9186, 'interceptions returned for touchdowns': 0.09302, 'forced fumbles': 0.3062, 'fumbles recovered': 0.18992, 'fumbles returned for touchdowns': 0.00775, 'blocked kicks': 0.00775}}, 'S': {'Defense': {'unassisted tackles': 29.30851, 'assisted tackles': 13.64894, 'total tackles': 42.95745, 'sacks': 0.38298, 'yards lost on sack': 2.90426, 'tackles for loss': 1.38298, 'passes defended': 2.98936, 'interceptions': 0.89362, 'intercepted returned yards': 13.3883, 'longest interception return': 10.31383, 'interceptions returned for touchdowns': 0.07447, 'forced fumbles': 0.45745, 'fumbles recovered': 0.30851, 'fumbles returned for touchdowns': 0.02128, 'blocked kicks': 0.03191}}, 'PK': {'Defense': {'unassisted tackles': 0.34783, 'assisted tackles': 0.0, 'total tackles': 0.34783, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.0, 'receiving touchdowns': 0.0, 'return touchdowns': 0.0, 'total touchdowns': 0.0, 'field goals': 22.95652, 'extra points': 27.58696, 'two point conversions': 0.0, 'total points': 96.45652, 'total points per game': 7.01739}, 'Kicking': {'field goals made': 22.95652, 'field goals attempts': 26.5, 'field goals made pct': 86.56304, 'longest goal made': 53.63043, 'field goals from 1 19 yards': 0.02174, 'field goals from 20 29 yards': 0.87319, 'field goals from 30 39 yards': 0.96027, 'field goals from 40 49 yards': 0.76699, 'field goals from 50 yards': 0.62671, 'extra points made': 27.58696, 'extra points attempts': 28.95652, 'extra points made pct': 94.21957}}, 'P': {'Punting': {'punts': 56.11905, 'gross punt yards': 2668.57143, 'longest punt': 67.2381, 'gross punting avg': 47.66905, 'net punting avg': 41.66905, 'blocked punts': 0.11905, 'inside 20 yards punt': 20.30952, 'touchbacks': 4.07143, 'fair catches': 15.69048, 'punts returned': 24.42857, 'yards returned on punts': 238.90476, 'yards returned on punts avg': 10.1}}, 'QB': {'Passing': {'passing attempts': 217.44828, 'completions': 139.34483, 'completion pct': 59.45977, 'yards': 1515.97701, 'yards per pass avg': 6.66897, 'yards per game': 145.70575, 'longest pass': 49.93103, 'passing touchdowns': 8.78161, 'passing touchdowns pct': 0, 'interceptions': 5.18391, 'interceptions pct': 0, 'sacks': 16.51724, 'sacked yards lost': 111.34483, 'quaterback rating': 78.84713}, 'Rushing': {'rushing attempts': 28.08046, 'yards': 119.7931, 'yards per rush avg': 3.37241, 'longest rush': 15.51724, 'over 20 yards': 0.8046, 'rushing touchdowns': 1.34483, 'yards per game': 12.1908, 'fumbles': 1.54023, 'fumbles lost': 0.56322, 'rushing first downs': 9.71264}}, 'LS': {'Defense': {'unassisted tackles': 1.57143, 'assisted tackles': 1.21429, 'total tackles': 2.78571, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.10714, 'fumbles recovered': 0.03571, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}}

    # Dictionary to store the stats for each player
    stats = {}

    # Get the stats for each player
    for player_id, player_info in players.items():
        # Get the stats for each player
        player_stats = get_stats_by_player(player_id, season)

        # If the player has stats and the position isn't in the dictionary, add them
        if player_stats != None and player_info[1] not in stats:

            # Start with an empty list and fill with stats
            stats[player_info[1]] = []

            # -- IF GROUP/STAT MISSING, FILL WITH SEASON'S AVERAGES --
            # For every stat in that position's dictionary, add the stat to the player's stats
            for group in stats_by_position[player_info[1]]:
                # If the group of stats is not in the player's stats, add 0 for all stats in that group
                if group not in player_stats:
                    for stat_name, stat_value in avg_stats_by_position[player_info[1]][group].items():
                        print(f"Filling group ({group}) with average: ", stat_name, stat_value)
                        stats[player_info[1]].append(stat_value)
                    continue
                for stat in stats_by_position[player_info[1]][group]:
                    # Get the player's corresponding stat
                    # If the stat is not in the player's stats, add 0
                    
                    if stat not in player_stats[group]:
                        print("Filling stat with average: ", stat, avg_stats_by_position[player_info[1]][group][stat])
                        stats[player_info[1]].append(avg_stats_by_position[player_info[1]][group][stat])
                    else:
                        value = player_stats[group][stat]
                        # If the value is a string, turn it into a float
                        try:
                            value = float(value.replace(',', ''))
                        except:
                            pass
                        stats[player_info[1]].append(value)
    return stats
#this function is being used to accumulate the stats for all players for all teams for a given season
#the data will be stored in a database to reduce the number of API calls necessary for training the model
def player_stats_per_team_per_year(leagueID,season):
    teamList = get_teams_by_season(1,season)
    playerListPerTeam = {}
    statsList = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}, 'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Returning': {'kickoff returned attempts': 0, 'kickoff return yards': 0, 'yards per kickoff avg': 0, 'longes kickoff return': 0, 'kickoff return touchdows': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards per punt avg': 0, 'longest punt return': 0, 'punt return touchdowns': 0, 'fair catches': 0}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Returning': {'kickoff returned attempts': 0, 'kickoff return yards': 0, 'yards per kickoff avg': 0, 'longes kickoff return': 0, 'kickoff return touchdows': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards per punt avg': 0, 'longest punt return': 0, 'punt return touchdowns': 0, 'fair catches': 0}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0},'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Kicking': {'field goals made': 0, 'field goals attempts': 0, 'field goals made pct': 0, 'longest goal made': 0, 'field goals from 1 19 yards': 0, 'field goals from 20 29 yards': 0, 'field goals from 30 39 yards': 0, 'field goals from 40 49 yards': 0, 'field goals from 50 yards': 0, 'extra points made': 0, 'extra points attempts': 0, 'extra points made pct': 0}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 0, 'longest punt': 0, 'gross punting avg': 0, 'net punting avg': 0, 'blocked punts': 0, 'inside 20 yards punt': 0, 'touchbacks': 0, 'fair catches': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards returned on punts avg': 0}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 0, 'completion pct': 0, 'yards': 0, 'yards per pass avg': 0, 'yards per game': 0, 'longest pass': 0, 'passing touchdowns': 0, 'passing touchdowns pct': 0, 'interceptions': 0, 'interceptions pct': 0, 'sacks': 0, 'sacked yards lost': 0, 'quaterback rating': 0}, 'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}}
    for teams in teamList:
        playerList = []
        print(teams)
        players = get_players_by_team(teams,season)
        print(players)
        for player_id, player_info in players.items():

            player_stats = get_stats_by_player(player_id, season)
            #if stats for the player doesnt exist
            if player_stats is not None:
                #print(s,teamList[teamId],player_info[0])
                # Fix PK values (28-32) (turn from string to float)
                # These values are written as 'x-y' (x made, y attempted)
                if player_info[1] == 'PK':
                    if 'Kicking' in player_stats and player_stats['Kicking'] is not None:
                        for stat in player_stats['Kicking']:
                            if "-" in player_stats['Kicking'][stat]:
                                    x,y = player_stats['Kicking'][stat].split('-')
                                    x = float(x)
                                    y = float(y)
                                    if y == 0:
                                        player_stats['Kicking'][stat] = 0
                                    else:
                                        player_stats['Kicking'][stat] = round(x / y,5)
                #for each stats group
                for group in statsList[player_info[1]]:
                    #fills in stats as zero if a player doesn't have a certain stat group
                    if group not in player_stats:
                        player_stats.update({group:{}})
                        for stat in statsList[player_info[1]][group]:
                                player_stats[group][stat] = 0
                        continue
                    else:
                        #goes through each stat and adds it to total
                        for stat in statsList[player_info[1]][group]:
                            if stat not in player_stats[group]:
                                continue
                            else:
                                value = player_stats[group][stat]
                                # If the value is a string, turn it into a float
                                try:
                                    value = float(value.replace(',', ''))
                                except:
                                    pass
                                if value is not None:
                                    player_stats[group][stat] = value
            print(player_stats)
            playerName = players[player_id][0]
            print(playerName)
            player_stats = {playerName:{player_id:player_stats}}
            playerList.append(player_stats)
        playerListPerTeam = {teamList[teams]:{teams:playerList}}
        break
    print(playerListPerTeam)
    


#this function will find the average stats for every position in the league for the entire season
def get_average_stats_per_season():
    
    #holds the average stats per position for each year
    averagesPerYear = {}

    #keeps track of average stat for each position
    average_per_position = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}, 'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Returning': {'kickoff returned attempts': 0, 'kickoff return yards': 0, 'yards per kickoff avg': 0, 'longes kickoff return': 0, 'kickoff return touchdows': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards per punt avg': 0, 'longest punt return': 0, 'punt return touchdowns': 0, 'fair catches': 0}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Returning': {'kickoff returned attempts': 0, 'kickoff return yards': 0, 'yards per kickoff avg': 0, 'longes kickoff return': 0, 'kickoff return touchdows': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards per punt avg': 0, 'longest punt return': 0, 'punt return touchdowns': 0, 'fair catches': 0}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0},'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Kicking': {'field goals made': 0, 'field goals attempts': 0, 'field goals made pct': 0, 'longest goal made': 0, 'field goals from 1 19 yards': 0, 'field goals from 20 29 yards': 0, 'field goals from 30 39 yards': 0, 'field goals from 40 49 yards': 0, 'field goals from 50 yards': 0, 'extra points made': 0, 'extra points attempts': 0, 'extra points made pct': 0}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 0, 'longest punt': 0, 'gross punting avg': 0, 'net punting avg': 0, 'blocked punts': 0, 'inside 20 yards punt': 0, 'touchbacks': 0, 'fair catches': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards returned on punts avg': 0}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 0, 'completion pct': 0, 'yards': 0, 'yards per pass avg': 0, 'yards per game': 0, 'longest pass': 0, 'passing touchdowns': 0, 'passing touchdowns pct': 0, 'interceptions': 0, 'interceptions pct': 0, 'sacks': 0, 'sacked yards lost': 0, 'quaterback rating': 0}, 'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}}
    positionCount = {'QB':0, 'RB':0, 'FB':0, 'WR':0, 'TE':0, 'C':0, 'G':0, 'OT':0, 'DE':0, 'DT':0, 'CB':0, 'LB':0,'S':0, 'PK':0, 'P':0, 'LS':0}

    seasons = [2022]
    #interates through seassons
    for s in seasons:
        averagesPerYear[s] = copy.deepcopy(average_per_position)
        
        teamList = get_teams_by_season(1,s)
        #iterates through each team in NFL
        for teamId in teamList:
            # Get the stats for each player of the team
            players = get_players_by_team(teamId, s)
            #print(s,teamList[teamId])

            for player_id, player_info in players.items():
                
                player_stats = get_stats_by_player(player_id, s)
                #if stats for the player doesnt exist
                if player_stats is not None:
                    positionCount[player_info[1]] = positionCount[player_info[1]] + 1
                    #print(s,teamList[teamId],player_info[0])
                    # Fix PK values (28-32) (turn from string to float)
                    # These values are written as 'x-y' (x made, y attempted)
                    if player_info[1] == 'PK':
                        if 'Kicking' in player_stats and player_stats['Kicking'] is not None:
                            for stat in player_stats['Kicking']:
                                if "-" in player_stats['Kicking'][stat]:
                                        x,y = player_stats['Kicking'][stat].split('-')
                                        x = float(x)
                                        y = float(y)
                                        if y == 0:
                                            player_stats['Kicking'][stat] = 0
                                        else:
                                            player_stats['Kicking'][stat] = round(x / y,5)
                    #for each stats group
                    for group in average_per_position[player_info[1]]:
                        #fills in stats as zero if a player doesn't have a certain stat group
                        if group not in player_stats:
                            player_stats.update({group:{}})
                            for stat in average_per_position[player_info[1]][group]:
                                    player_stats[group][stat] = 0
                            continue
                        else:
                            #goes through each stat and adds it to total
                            for stat in average_per_position[player_info[1]][group]:
                                if stat not in player_stats[group]:
                                    continue
                                else:
                                    value = player_stats[group][stat]
                                    # If the value is a string, turn it into a float
                                    try:
                                        value = float(value.replace(',', ''))
                                    except:
                                        pass
                                    if value is not None:
                                        averagesPerYear[s][player_info[1]][group][stat] = averagesPerYear[s][player_info[1]][group][stat] + value
            print(s,teamList[teamId],positionCount)
        #goes through each stat and divides it by the number of players per position in the league to get the average
        for position in positionCount:
            count = positionCount[position]
            for group in average_per_position[position]:
                for stat in average_per_position[position][group]:
                    if averagesPerYear[s][position][group][stat] == 0:
                        continue
                    else:
                        averagesPerYear[s][position][group][stat] = round(averagesPerYear[s][position][group][stat] / (count * 1.0),5)
        #resets position counts back to 0
        positionCount = positionCount.fromkeys(positionCount,0)
    return averagesPerYear

#this function returns the season years that are supported
#All seasons are only 4-digit keys, so for a league whose season is 2018-2019 the season in the API will be 2018
def getSeasons():
    
    while (True):
        conn.request("GET", "/seasons", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)

        if (data['results'] != 0):
            print("Seasons stats found")
            break
        else:
            print("Seasons stats not found, waiting...")
            # If there is an error, print the error and wait 60 seconds
            if (len(data['errors']) != 0):
                print('Error:', data['errors'])
                print('Waiting...')
                time.sleep(60)
            # Otherwise, there must be no data so break
            else:
                break

    seasonList = []

    for year in data["response"]:
        seasonList.append(int(year))
    return seasonList

#this function takes two team IDs and the season and returns the games played between the two teams
def get_head_to_head_games(teamID_1,teamID_2,season):
    
    while (True):
        conn.request("GET", f"/games?season={season}&h2h={teamID_1}-{teamID_2}", headers=headers)

        # Gets the head to head games for the given season
        res = conn.getresponse()
        data = res.read() 
        data = json.loads(data.decode("utf-8"))

        if (data['results'] != 0):
            print("Head to head games found")
            break
        else:
            print("Head to head games not found")
            # If there is an error, print the error and wait 60 seconds
            if (len(data['errors']) != 0):
                print('Error:', data['errors'])
                print('Waiting...')
                time.sleep(60)
            # Otherwise, there must be no data so break
            else:
                break

    gameList = {}
    
    #iterates through all the games played and tracks 
    for game in data['response']:
        gameList[game['teams']['home']['name'] + " vs " + game['teams']['away']['name']] = game['scores']
    return gameList
#this function takes a season year and teamID and returns all the games the team played for that season
#Each entry will be based on the matchup and will include the gameID, date of the game, and scores of the game
def get_games_for_team_for_season(season,teamID):
        
    while (True):
        conn.request("GET", f"/games?season={season}&team={teamID}", headers=headers)

        # Gets the head to head games for the given season
        res = conn.getresponse()
        data = res.read() 
        data = json.loads(data.decode("utf-8"))

        if (data['results'] != 0):
            print("Games found")
            break
        else:
            print("Games not found, waiting...")
            # If there is an error, print the error and wait 60 seconds
            if (len(data['errors']) != 0):
                print('Error:', data['errors'])
                print('Waiting...')
                time.sleep(60)
            # Otherwise, there must be no data so break
            else:
                break

    gameList = {}

    #for each game store the team matchups,date and score
    for game in data["response"]:
        homeTeam = game['teams']['home']['name']
        awayTeam = game['teams']['away']['name']

        gameList[f"{homeTeam} vs {awayTeam}"] = {"gameID":game['game']['id'],"date":game['game']['date']['date'],"scores":game['scores']}
    return gameList
#this function takes a list of gameIDs and returns the team stats for each team for the given game
#Format is key: gameID, team1:team stats,team2:team stats
def get_team_stats_for_game(gameIDs):
    #holds the team stats for the game
    gameStats = {}
    #for each gameID in the lsit
    for games in gameIDs:
            
        while (True):
            conn.request("GET", f"/games/statistics/teams?id={games}", headers=headers)

            # Gets the head to head games for the given season
            res = conn.getresponse()
            data = res.read() 
            data = json.loads(data.decode("utf-8"))

            if (data['results'] != 0):
                print('Team stats found')
                break
            else:
                print('Team stats not found, waiting...')
                # If there is an error, print the error and wait 60 seconds
                if (len(data['errors']) != 0):
                    print('Error:', data['errors'])
                    print('Waiting...')
                    time.sleep(60)
                # Otherwise, there must be no data so break
                else:
                    break

        gameStats[games] = {data['response'][0]['team']['name']:data['response'][0]['statistics'],data['response'][1]['team']['name']:data['response'][1]['statistics']}
    return gameStats

def get_average_team_stats(season, teamID):
    games = get_games_for_team_for_season(season, teamID)

    num_games = len(games)

    print(num_games)

    game_stats = {}

    for game_name, game_info in games.items():
        
        while (True):
            conn.request("GET", f"/games/statistics/teams?id={game_info['gameID']}&team={teamID}", headers=headers)

            # Gets the head to head games for the given season
            res = conn.getresponse()
            data = res.read() 
            data = json.loads(data.decode("utf-8"))

            if (data['results'] != 0):
                print('Game stats found')
                break
            else:
                print('Game stats not found, waiting...')
                # If there is an error, print the error and wait 60 seconds
                if (len(data['errors']) != 0):
                    print('Error:', data['errors'])
                    print('Waiting...')
                    time.sleep(60)
                # Otherwise, there must be no data so break
                else:
                    break

        for group_name, group_stats in data['response'][0]['statistics'].items():
            for stat_name, stat in group_stats.items():

                # Add group name to stat name
                stat_name = group_name + '_' + stat_name

                # Check for non-castable stats
                if stat_name in ['first_downs_third_down_efficiency', 'first_downs_fourth_down_efficiency', 
                                    'passing_comp_att', 'red_zone_made_att']:
                    num, den = stat.split('-')
                    if (float(den) == 0):
                        stat = 0
                    else:
                        stat = float(num) / float(den)
                # Convert possession time to seconds
                elif stat_name == 'posession_total':                    
                    stat = float(stat.split(':')[0]) * 60 + float(stat.split(':')[1])
                elif stat_name in ['penalties_total', 'passing_sacks_yards_lost']:
                    stat = float(stat.split('-')[0])

                # Insert stat into game_stats
                if stat_name not in game_stats.keys():
                    game_stats[stat_name] = float(stat)
                else:
                    game_stats[stat_name] += float(stat)

        # Save API calls
        break

    for stat_name, stat in game_stats.items():
        game_stats[stat_name] = stat / num_games

    return game_stats

# Data Accumulation:

# Want to get data for every game in a specific season/league
# and compile the data into input/target for the PyTorch model

# 1. Pull all of the games that occur in a season/league
# 2. For each game, pull player stats/team stats as input data
# 3. Pull the winner of the game [0, 1] as target data
# 4. Compile the input/target data into a list of tuples for PyTorch

# INPUT DATA FORMAT
# [h2h_winner, 
#  home_id, home_player_stats, home_team_stats, 
#  away_id, away_player_stats, away_team_stats]

# h2h_winner: 1
# home_id: 2
# home_player_stats: 

# TARGET DATA FORMAT
# [winner] (0 - home or 1 - away)
def get_pytorch_data(league, season):

    # Dictionary containing input/target data for each game
    # {game_name: {'input': [input_data], 'target': [target_data]}}
    games_stats = {}

    # Get all teams in a given season/league
    teams = get_teams_by_season(league, season)
    # Flip the dictionary so that the team name is the key
    teams = {value: key for key, value in teams.items()}

    # Get all games for each team
    games = {}
    for team_name, teamID in teams.items():
        # Get games for teamID
        team_games = get_games_for_team_for_season(season, teamID)
        # Add each game to the games dictionary
        for game_name, game_info in team_games.items():
            # Determine if home (0) or away (1) won
            if game_info['scores']['home']['total'] >= game_info['scores']['away']['total']:
                winner = 0
            else:
                winner = 1
            # Add the game to the games dictionary
            games[game_name] = {'gameID': game_info['gameID'], 'winner': winner}

    #--- 2. For each game, pull player stats/team stats as input data ---#
    count = 0
    for game in games:

        # # Get the teamID for the home and away teams
        home_name, away_name = game.split(' vs ')

        home_id = teams[home_name]
        away_id = teams[away_name]

        # HEAD2HEAD STATS
        # Get the head-to-head stats for the home and away teams for the previous season
        h2h_games = get_head_to_head_games(home_id, away_id, season-1)
        # Determine if home/away won more
        wins = 0
        for game_name, game_info in h2h_games.items():
            if game_info['home']['total'] >= game_info['away']['total']:
                wins += 0
            else:
                wins += 1

        if (len(h2h_games) == 0):
            h2h_winner = 0
        else:
            wins = float(wins / len(h2h_games))
            # If home and away have the same number of wins, 
            # give the win to the home team
            if wins > 0.5:
                h2h_winner = 1
            else:
                h2h_winner = 0

        # PLAYER STATS
        # Get the player stats for the home and away teams
        # home_player_stats = compile_stats(get_stats_by_position(home_id, season))
        # away_player_stats = compile_stats(get_stats_by_position(away_id, season))
        home_player_stats = get_player_stats(home_id, season)
        away_player_stats = get_player_stats(away_id, season)

        # TEAM STATS
        # Get the team stats for the home and away teams
        # (Average the team stats for the season)
        avg_home_team_stats = list(get_average_team_stats(season, home_id).values())
        print(f"Avg Home Team Stats Length: {len(avg_home_team_stats)}")
        avg_away_team_stats = list(get_average_team_stats(season, away_id).values())
        print(f"Avg Away Team Stats Length: {len(avg_away_team_stats)}")
        # Add the game stats to the games_stats list
        games_stats[game] = {}

        games_stats[game]['input'] = [h2h_winner,
                                    home_id, home_player_stats, avg_home_team_stats,
                                    away_id, away_player_stats, avg_away_team_stats]
        games_stats[game]['target'] = np.array([games[game]['winner']], dtype=np.float32)
        
        # Flatten the input list of lists into a single list
        numpy_games_stats = np.array([], dtype=np.float32)
        for i in games_stats[game]['input']:
            if type(i) == list or type(i) == np.ndarray:
                for j in i:
                    numpy_games_stats = np.append(numpy_games_stats, float(j))
            else:
                numpy_games_stats = np.append(numpy_games_stats, float(i))
                
        games_stats[game]['input'] = numpy_games_stats

        # print(games_stats[game])

        count += 1
        if count == 1:
            break

    #--- 4. Compile the input/target data into a list of tuples for PyTorch ---#
        
    input_data = []
    target_data = []

    for game in games_stats:
        input_data.append(torch.from_numpy(games_stats[game]['input']).float())
        target_data.append(torch.from_numpy(games_stats[game]['target']).float())

    input_data = torch.stack(input_data)
    target_data = torch.stack(target_data)

    return input_data, target_data

# games =get_games_for_team_for_season(2022,1)
# for game in games:
#     print(game)
#     print(games[game])
#     print()
# gameList = get_team_stats_for_game([4189,4113])
# for games in gameList:
#     print(gameList[games])
#     print()
# stats = get_average_stats_per_season()
# print(stats[2022])
#compiled_stats = compile_stats(get_stats_by_position(3, 2023))
#print(compiled_stats)
#print(len(compiled_stats))
#player_stats_per_team_per_year(1,2023)
    

#season [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
#teams and IDS {1: 'Las Vegas Raiders', 2: 'Jacksonville Jaguars', 3: 'New England Patriots', 4: 'New York Giants', 5: 'Baltimore Ravens', 6: 'Tennessee Titans', 7: 'Detroit Lions', 8: 'Atlanta Falcons', 9: 'Cleveland Browns', 10: 'Cincinnati Bengals', 11: 'Arizona Cardinals', 12: 'Philadelphia Eagles', 13: 'New York Jets', 14: 'San Francisco 49ers', 15: 'Green Bay Packers', 16: 'Chicago Bears', 17: 'Kansas City Chiefs', 18: 'Washington Commanders', 19: 'Carolina Panthers', 20: 'Buffalo Bills', 21: 'Indianapolis Colts', 22: 'Pittsburgh Steelers', 23: 'Seattle Seahawks', 24: 'Tampa Bay Buccaneers', 25: 'Miami Dolphins', 26: 'Houston Texans', 27: 'New Orleans Saints', 28: 'Denver Broncos', 29: 'Dallas Cowboys', 30: 'Los Angeles Chargers', 31: 'Los Angeles Rams', 32: 'Minnesota Vikings'}
#{'QB': 87, 'RB': 160, 'FB': 13, 'WR': 240, 'TE': 126, 'C': 18, 'G': 38, 'OT': 32, 'DE': 146, 'DT': 181, 'CB': 258, 'LB': 326, 'S': 188, 'PK': 46, 'P': 42, 'LS': 28}
#2023 {'RB': {'Rushing': {'rushing attempts': 76.4375, 'yards': 319.38125, 'yards per rush avg': 3.59813, 'longest rush': 22.94375, 'over 20 yards': 1.65, 'rushing touchdowns': 2.15625, 'yards per game': 24.54375, 'fumbles': 0.525, 'fumbles lost': 0.29375, 'rushing first downs': 16.775}, 'Receiving': {'receptions': 15.83125, 'receiving targets': 20.34375, 'receiving yards': 113.25625, 'yards per reception avg': 6.1775, 'receiving touchdowns': 0.58125, 'longest reception': 20.74375, 'over 20 yards': 0.975, 'yards per game': 8.84563, 'fumbles': 0.19375, 'fumbles lost': 0.10625, 'yards after catch': 125.85, 'receiving first downs': 4.9}, 'Defense': {'unassisted tackles': 0.675, 'assisted tackles': 0.39375, 'total tackles': 1.06875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01875, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 2.1625, 'receiving touchdowns': 0.58125, 'return touchdowns': 0.00625, 'total touchdowns': 2.75, 'field goals': 0.00625, 'extra points': 0.0, 'two point conversions': 0.1375, 'total points': 16.79375, 'total points per game': 1.31}, 'Returning': {'kickoff returned attempts': 1.56875, 'kickoff return yards': 36.4625, 'yards per kickoff avg': 5.84937, 'longes kickoff return': 8.30625, 'kickoff return touchdows': 0.00625, 'punts returned': 0.25, 'yards returned on punts': 2.13125, 'yards per punt avg': 0.215, 'longest punt return': 0.475, 'punt return touchdowns': 0.0, 'fair catches': 0.16875}}, 'FB': {'Receiving': {'receptions': 5.38462, 'receiving targets': 6.69231, 'receiving yards': 35.30769, 'yards per reception avg': 5.31538, 'receiving touchdowns': 0.38462, 'longest reception': 12.69231, 'over 20 yards': 0.38462, 'yards per game': 2.18462, 'fumbles': 0.07692, 'fumbles lost': 0.07692, 'yards after catch': 23.53846, 'receiving first downs': 1.92308}, 'Defense': {'unassisted tackles': 1.92308, 'assisted tackles': 1.0, 'total tackles': 2.92308, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.23077, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Returning': {'kickoff returned attempts': 0.38462, 'kickoff return yards': 10.53846, 'yards per kickoff avg': 6.92308, 'longes kickoff return': 9.84615, 'kickoff return touchdows': 0.07692, 'punts returned': 0.0, 'yards returned on punts': 0.0, 'yards per punt avg': 0.0, 'longest punt return': 0.0, 'punt return touchdowns': 0.0, 'fair catches': 0.0}}, 'WR': {'Receiving': {'receptions': 27.83333, 'receiving targets': 44.25417, 'receiving yards': 352.89583, 'yards per reception avg': 10.775, 'receiving touchdowns': 2.08333, 'longest reception': 34.27083, 'over 20 yards': 5.07083, 'yards per game': 24.6625, 'fumbles': 0.3375, 'fumbles lost': 0.175, 'yards after catch': 121.625, 'receiving first downs': 16.44583}, 'Defense': {'unassisted tackles': 1.07917, 'assisted tackles': 0.22083, 'total tackles': 1.3, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01667, 'fumbles recovered': 0.00833, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.1, 'receiving touchdowns': 2.10417, 'return touchdowns': 0.05417, 'total touchdowns': 2.25833, 'field goals': 0.0, 'extra points': 0.0, 'two point conversions': 0.10417, 'total points': 13.75833, 'total points per game': 0.98333}, 'Rushing': {'rushing attempts': 2.0125, 'yards': 12.16667, 'yards per rush avg': 2.41708, 'longest rush': 5.72083, 'over 20 yards': 0.10833, 'rushing touchdowns': 0.09583, 'yards per game': 0.87917, 'fumbles': 0.02083, 'fumbles lost': 0.00417, 'rushing first downs': 0.6625}}, 'TE': {'Receiving': {'receptions': 21.03175, 'receiving targets': 29.59524, 'receiving yards': 218.06349, 'yards per reception avg': 9.22619, 'receiving touchdowns': 1.42063, 'longest reception': 24.68254, 'over 20 yards': 2.54762, 'yards per game': 15.15397, 'fumbles': 0.23016, 'fumbles lost': 0.13492, 'yards after catch': 103.57143, 'receiving first downs': 10.97619}, 'Defense': {'unassisted tackles': 1.23016, 'assisted tackles': 0.54762, 'total tackles': 1.77778, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.00794, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.02381, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.01587}}, 'C': {'Defense': {'unassisted tackles': 0.72222, 'assisted tackles': 0.38889, 'total tackles': 1.11111, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.05556, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'G': {'Defense': {'unassisted tackles': 1.0, 'assisted tackles': 0.13158, 'total tackles': 1.13158, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'OT': {'Defense': {'unassisted tackles': 0.90625, 'assisted tackles': 0.28125, 'total tackles': 1.1875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'DE': {'Defense': {'unassisted tackles': 12.17123, 'assisted tackles': 9.20548, 'total tackles': 21.37671, 'sacks': 2.65068, 'yards lost on sack': 18.23288, 'tackles for loss': 3.47945, 'passes defended': 1.06164, 'interceptions': 0.03425, 'intercepted returned yards': 0.33562, 'longest interception return': 0.29452, 'interceptions returned for touchdowns': 0.00685, 'forced fumbles': 0.39726, 'fumbles recovered': 0.26027, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.11644}}, 'DT': {'Defense': {'unassisted tackles': 12.46961, 'assisted tackles': 11.51381, 'total tackles': 23.98343, 'sacks': 1.71547, 'yards lost on sack': 11.43646, 'tackles for loss': 2.87845, 'passes defended': 0.86188, 'interceptions': 0.03867, 'intercepted returned yards': 0.07735, 'longest interception return': 0.07735, 'interceptions returned for touchdowns': 0.00552, 'forced fumbles': 0.24862, 'fumbles recovered': 0.24862, 'fumbles returned for touchdowns': 0.0221, 'blocked kicks': 0.02762}}, 'LB': {'Defense': {'unassisted tackles': 23.31902, 'assisted tackles': 15.02454, 'total tackles': 38.34356, 'sacks': 1.76687, 'yards lost on sack': 11.93558, 'tackles for loss': 3.26687, 'passes defended': 1.40798, 'interceptions': 0.24847, 'intercepted returned yards': 3.51534, 'longest interception return': 2.80982, 'interceptions returned for touchdowns': 0.03067, 'forced fumbles': 0.46933, 'fumbles recovered': 0.30982, 'fumbles returned for touchdowns': 0.02147, 'blocked kicks': 0.00307}}, 'CB': {'Defense': {'unassisted tackles': 21.67054, 'assisted tackles': 6.55814, 'total tackles': 28.22868, 'sacks': 0.1376, 'yards lost on sack': 0.94961, 'tackles for loss': 1.02713, 'passes defended': 4.21705, 'interceptions': 0.64341, 'intercepted returned yards': 7.70155, 'longest interception return': 5.9186, 'interceptions returned for touchdowns': 0.09302, 'forced fumbles': 0.3062, 'fumbles recovered': 0.18992, 'fumbles returned for touchdowns': 0.00775, 'blocked kicks': 0.00775}}, 'S': {'Defense': {'unassisted tackles': 29.30851, 'assisted tackles': 13.64894, 'total tackles': 42.95745, 'sacks': 0.38298, 'yards lost on sack': 2.90426, 'tackles for loss': 1.38298, 'passes defended': 2.98936, 'interceptions': 0.89362, 'intercepted returned yards': 13.3883, 'longest interception return': 10.31383, 'interceptions returned for touchdowns': 0.07447, 'forced fumbles': 0.45745, 'fumbles recovered': 0.30851, 'fumbles returned for touchdowns': 0.02128, 'blocked kicks': 0.03191}}, 'PK': {'Defense': {'unassisted tackles': 0.34783, 'assisted tackles': 0.0, 'total tackles': 0.34783, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.0, 'receiving touchdowns': 0.0, 'return touchdowns': 0.0, 'total touchdowns': 0.0, 'field goals': 22.95652, 'extra points': 27.58696, 'two point conversions': 0.0, 'total points': 96.45652, 'total points per game': 7.01739}, 'Kicking': {'field goals made': 22.95652, 'field goals attempts': 26.5, 'field goals made pct': 86.56304, 'longest goal made': 53.63043, 'field goals from 1 19 yards': 0.02174, 'field goals from 20 29 yards': 0.87319, 'field goals from 30 39 yards': 0.96027, 'field goals from 40 49 yards': 0.76699, 'field goals from 50 yards': 0.62671, 'extra points made': 27.58696, 'extra points attempts': 28.95652, 'extra points made pct': 94.21957}}, 'P': {'Punting': {'punts': 56.11905, 'gross punt yards': 2668.57143, 'longest punt': 67.2381, 'gross punting avg': 47.66905, 'net punting avg': 41.66905, 'blocked punts': 0.11905, 'inside 20 yards punt': 20.30952, 'touchbacks': 4.07143, 'fair catches': 15.69048, 'punts returned': 24.42857, 'yards returned on punts': 238.90476, 'yards returned on punts avg': 10.1}}, 'QB': {'Passing': {'passing attempts': 217.44828, 'completions': 139.34483, 'completion pct': 59.45977, 'yards': 1515.97701, 'yards per pass avg': 6.66897, 'yards per game': 145.70575, 'longest pass': 49.93103, 'passing touchdowns': 8.78161, 'passing touchdowns pct': 0, 'interceptions': 5.18391, 'interceptions pct': 0, 'sacks': 16.51724, 'sacked yards lost': 111.34483, 'quaterback rating': 78.84713}, 'Rushing': {'rushing attempts': 28.08046, 'yards': 119.7931, 'yards per rush avg': 3.37241, 'longest rush': 15.51724, 'over 20 yards': 0.8046, 'rushing touchdowns': 1.34483, 'yards per game': 12.1908, 'fumbles': 1.54023, 'fumbles lost': 0.56322, 'rushing first downs': 9.71264}}, 'LS': {'Defense': {'unassisted tackles': 1.57143, 'assisted tackles': 1.21429, 'total tackles': 2.78571, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.10714, 'fumbles recovered': 0.03571, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}}
#{'QB': 75, 'RB': 151, 'FB': 12, 'WR': 225, 'TE': 107, 'C': 9, 'G': 23, 'OT': 22, 'DE': 132, 'DT': 159, 'CB': 216, 'LB': 294, 'S': 171, 'PK': 53, 'P': 36, 'LS': 20}
#2022 {'RB': {'Rushing': {'rushing attempts': 50.47682, 'yards': 219.87417, 'yards per rush avg': 3.64371, 'longest rush': 19.45695, 'over 20 yards': 1.03974, 'rushing touchdowns': 1.45033, 'yards per game': 25.75563, 'fumbles': 0.37086, 'fumbles lost': 0.2053, 'rushing first downs': 11.23179}, 'Receiving': {'receptions': 10.2053, 'receiving targets': 13.3245, 'receiving yards': 75.83444, 'yards per reception avg': 6.65497, 'receiving touchdowns': 0.31788, 'longest reception': 16.49669, 'over 20 yards': 0.58278, 'yards per game': 9.72318, 'fumbles': 0.13907, 'fumbles lost': 0.07947, 'yards after catch': 80.61589, 'receiving first downs': 3.30464}, 'Defense': {'unassisted tackles': 0.75497, 'assisted tackles': 0.27152, 'total tackles': 1.02649, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.00662, 'fumbles recovered': 0.00662, 'fumbles returned for touchdowns': 0.00662, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 1.45033, 'receiving touchdowns': 0.31788, 'return touchdowns': 0.00662, 'total touchdowns': 1.77483, 'field goals': 0.0, 'extra points': 0.0, 'two point conversions': 0.07947, 'total points': 10.80795, 'total points per game': 1.46821}, 'Returning': {'kickoff returned attempts': 1.95364, 'kickoff return yards': 46.2649, 'yards per kickoff avg': 6.45563, 'longes kickoff return': 9.36424, 'kickoff return touchdows': 0.00662, 'punts returned': 0.18543, 'yards returned on punts': 1.25828, 'yards per punt avg': 0.25033, 'longest punt return': 0.54967, 'punt return touchdowns': 0.0, 'fair catches': 0.05298}}, 'FB': {'Receiving': {'receptions': 2.16667, 'receiving targets': 3.33333, 'receiving yards': 11.41667, 'yards per reception avg': 3.65, 'receiving touchdowns': 0.08333, 'longest reception': 5.58333, 'over 20 yards': 0.16667, 'yards per game': 0.96667, 'fumbles': 0.08333, 'fumbles lost': 0.0, 'yards after catch': 8.25, 'receiving first downs': 0.41667}, 'Defense': {'unassisted tackles': 2.16667, 'assisted tackles': 0.41667, 'total tackles': 2.58333, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Returning': {'kickoff returned attempts': 0.33333, 'kickoff return yards': 4.33333, 'yards per kickoff avg': 2.275, 'longes kickoff return': 2.58333, 'kickoff return touchdows': 0.0, 'punts returned': 0.0, 'yards returned on punts': 0.0, 'yards per punt avg': 0.0, 'longest punt return': 0.0, 'punt return touchdowns': 0.0, 'fair catches': 0.0}}, 'WR': {'Receiving': {'receptions': 16.32, 'receiving targets': 26.53778, 'receiving yards': 202.98667, 'yards per reception avg': 10.78978, 'receiving touchdowns': 1.03556, 'longest reception': 27.45333, 'over 20 yards': 2.83111, 'yards per game': 24.65467, 'fumbles': 0.22222, 'fumbles lost': 0.11556, 'yards after catch': 67.56889, 'receiving first downs': 9.68}, 'Defense': {'unassisted tackles': 0.65333, 'assisted tackles': 0.16444, 'total tackles': 0.81778, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.00889, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.06667, 'receiving touchdowns': 1.06667, 'return touchdowns': 0.01333, 'total touchdowns': 1.14667, 'field goals': 0.0, 'extra points': 0.0, 'two point conversions': 0.05778, 'total points': 6.99556, 'total points per game': 0.90667}, 'Rushing': {'rushing attempts': 1.32, 'yards': 8.27556, 'yards per rush avg': 2.02933, 'longest rush': 4.83111, 'over 20 yards': 0.10222, 'rushing touchdowns': 0.06222, 'yards per game': 0.85956, 'fumbles': 0.02222, 'fumbles lost': 0.01333, 'rushing first downs': 0.44444}}, 'TE': {'Receiving': {'receptions': 13.63551, 'receiving targets': 20.2243, 'receiving yards': 147.4486, 'yards per reception avg': 9.78318, 'receiving touchdowns': 1.11215, 'longest reception': 23.4486, 'over 20 yards': 1.88785, 'yards per game': 18.35701, 'fumbles': 0.1215, 'fumbles lost': 0.04673, 'yards after catch': 71.19626, 'receiving first downs': 7.35514}, 'Defense': {'unassisted tackles': 1.02804, 'assisted tackles': 0.36449, 'total tackles': 1.39252, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.00935, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.02804, 'fumbles recovered': 0.01869, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'C': {'Defense': {'unassisted tackles': 1.0, 'assisted tackles': 0.22222, 'total tackles': 1.22222, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'G': {'Defense': {'unassisted tackles': 1.0, 'assisted tackles': 0.21739, 'total tackles': 1.21739, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'OT': {'Defense': {'unassisted tackles': 0.90909, 'assisted tackles': 0.36364, 'total tackles': 1.27273, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.09091, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'DE': {'Defense': {'unassisted tackles': 9.5303, 'assisted tackles': 7.75758, 'total tackles': 17.28788, 'sacks': 1.85985, 'yards lost on sack': 12.13636, 'tackles for loss': 2.59091, 'passes defended': 0.70455, 'interceptions': 0.03788, 'intercepted returned yards': 0.59091, 'longest interception return': 0.02273, 'interceptions returned for touchdowns': 0.00758, 'forced fumbles': 0.2803, 'fumbles recovered': 0.13636, 'fumbles returned for touchdowns': 0.01515, 'blocked kicks': 0.12121}}, 'DT': {'Defense': {'unassisted tackles': 8.3522, 'assisted tackles': 8.06289, 'total tackles': 16.41509, 'sacks': 0.96541, 'yards lost on sack': 5.98742, 'tackles for loss': 1.77987, 'passes defended': 0.61635, 'interceptions': 0.01887, 'intercepted returned yards': 0.01887, 'longest interception return': 0.01887, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.09434, 'fumbles recovered': 0.13836, 'fumbles returned for touchdowns': 0.00629, 'blocked kicks': 0.04403}}, 'LB': {'Defense': {'unassisted tackles': 15.4932, 'assisted tackles': 10.2449, 'total tackles': 25.7381, 'sacks': 0.91497, 'yards lost on sack': 5.88776, 'tackles for loss': 1.93537, 'passes defended': 0.84694, 'interceptions': 0.13265, 'intercepted returned yards': 1.67347, 'longest interception return': 0.10204, 'interceptions returned for touchdowns': 0.02041, 'forced fumbles': 0.28231, 'fumbles recovered': 0.12925, 'fumbles returned for touchdowns': 0.0068, 'blocked kicks': 0.02041}}, 'CB': {'Defense': {'unassisted tackles': 16.52315, 'assisted tackles': 5.34722, 'total tackles': 21.87037, 'sacks': 0.09954, 'yards lost on sack': 0.65741, 'tackles for loss': 0.60185, 'passes defended': 2.86111, 'interceptions': 0.49537, 'intercepted returned yards': 6.25463, 'longest interception return': 0.27315, 'interceptions returned for touchdowns': 0.04167, 'forced fumbles': 0.23148, 'fumbles recovered': 0.14352, 'fumbles returned for touchdowns': 0.01389, 'blocked kicks': 0.01389}}, 'S': {'Defense': {'unassisted tackles': 19.32164, 'assisted tackles': 9.7193, 'total tackles': 29.04094, 'sacks': 0.17836, 'yards lost on sack': 1.1345, 'tackles for loss': 0.69591, 'passes defended': 1.73099, 'interceptions': 0.55556, 'intercepted returned yards': 9.02339, 'longest interception return': 0.23977, 'interceptions returned for touchdowns': 0.05848, 'forced fumbles': 0.24561, 'fumbles recovered': 0.21053, 'fumbles returned for touchdowns': 0.01754, 'blocked kicks': 0.0117}}, 'PK': {'Defense': {'unassisted tackles': 0.26415, 'assisted tackles': 0.18868, 'total tackles': 0.45283, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.0, 'receiving touchdowns': 0.0, 'return touchdowns': 0.0, 'total touchdowns': 0.0, 'field goals': 11.73585, 'extra points': 12.88679, 'two point conversions': 0.0, 'total points': 48.09434, 'total points per game': 7.05094}, 'Kicking': {'field goals made': 11.73585, 'field goals attempts': 13.66038, 'field goals made pct': 85.13962, 'longest goal made': 45.92453, 'field goals from 1 19 yards': 0.01887, 'field goals from 20 29 yards': 0.76334, 'field goals from 30 39 yards': 0.64073, 'field goals from 40 49 yards': 0.53797, 'field goals from 50 yards': 0.49441, 'extra points made': 12.88679, 'extra points attempts': 13.66038, 'extra points made pct': 89.79434}}, 'P': {'Punting': {'punts': 40.38889, 'gross punt yards': 1893.72222, 'longest punt': 60.47222, 'gross punting avg': 45.00278, 'net punting avg': 39.79722, 'blocked punts': 0.27778, 'inside 20 yards punt': 14.61111, 'touchbacks': 2.72222, 'fair catches': 10.80556, 'punts returned': 17.83333, 'yards returned on punts': 166.72222, 'yards returned on punts avg': 8.53611}}, 'QB': {'Passing': {'passing attempts': 146.57333, 'completions': 91.94667, 'completion pct': 58.84267, 'yards': 999.46667, 'yards per pass avg': 6.48133, 'yards per game': 161.052, 'longest pass': 46.34667, 'passing touchdowns': 5.36, 'passing touchdowns pct': 0, 'interceptions': 3.82667, 'interceptions pct': 0, 'sacks': 11.65333, 'sacked yards lost': 79.08, 'quaterback rating': 77.33333}, 'Rushing': {'rushing attempts': 19.10667, 'yards': 85.49333, 'yards per rush avg': 3.16667, 'longest rush': 13.56, 'over 20 yards': 0.46667, 'rushing touchdowns': 0.77333, 'yards per game': 12.62933, 'fumbles': 1.32, 'fumbles lost': 0.30667, 'rushing first downs': 6.42667}}, 'LS': {'Defense': {'unassisted tackles': 1.25, 'assisted tackles': 1.2, 'total tackles': 2.45, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}}