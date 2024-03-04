import json
import http.client
import numpy as np
import copy

#connect to API-NFL
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-rapidapi-host': "v1.american-football.api-sports.io",
    'x-rapidapi-key': "7d2dc831201816acd7bfce6f275ded21"
    }
#Logan's Key 7d2dc831201816acd7bfce6f275ded21
#christian's key c70572c71dea5b9097425435a60d972e
# Given a season and league, pull the teams and store into a dictionary {team_id : team_name}
def get_teams_by_season(league, season):
    conn.request("GET", f"/teams?league={league}&season={season}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Data as dict
    data = json.loads(data.decode("utf-8"))

    teams = {}

    for result in range(data['results']):
        team_id = data['response'][result]['id']
        team_name = data['response'][result]['name']
        teams[team_id] = team_name
    try:
        del teams[33]
        del teams[34]
    except:
        return teams
    return teams

# Given a team's ID, pull the players and store into a dictionary {player_id : player_name}
def get_players_by_team(team_id, season):
    conn.request("GET", f"/players?team={team_id}&season={season}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Data as dict
    data = json.loads(data.decode("utf-8"))

    players = {}

    #print(data['response'])

    for player in data['response']:
        players[player['id']] = [player['name'], player['position']]

    return players

def get_stats_by_player(player_id, season):
    conn.request("GET", f"/players/statistics?id={player_id}&season={season}", headers=headers)

    # Get the player's stats based on their ID
    res = conn.getresponse()
    data = res.read() 
    data = json.loads(data.decode("utf-8"))

    if (data['results'] == 0):
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
def get_stats_by_position(team_id, season):
    players = get_players_by_team(team_id, season)

    # Dictionary containing stats by position
    stats_by_position = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 1, 'yards per rush avg': 2, 'longest rush': 3, 'over 20 yards': 4, 'rushing touchdowns': 5, 'yards per game': 6, 'fumbles': 7, 'fumbles lost': 8, 'rushing first downs': 9}, 'Receiving': {'receptions': 10, 'receiving targets': 11, 'receiving yards': 12, 'yards per reception avg': 13, 'receiving touchdowns': 14, 'longest reception': 15, 'over 20 yards': 16, 'yards per game': 17, 'fumbles': 18, 'fumbles lost': 19, 'yards after catch': 20, 'receiving first downs': 21}, 'Defense': {'unassisted tackles': 22, 'assisted tackles': 23, 'total tackles': 24, 'sacks': 25, 'yards lost on sack': 26, 'tackles for loss': 27, 'passes defended': 28, 'interceptions': 29, 'intercepted returned yards': 30, 'longest interception return': 31, 'interceptions returned for touchdowns': 32, 'forced fumbles': 33, 'fumbles recovered': 34, 'fumbles returned for touchdowns': 35, 'blocked kicks': 36}, 'Scoring': {'rushing touchdowns': 37, 'receiving touchdowns': 38, 'return touchdowns': 39, 'total touchdowns': 40, 'field goals': 41, 'extra points': 42, 'two point conversions': 43, 'total points': 44, 'total points per game': 45}, 'Returning': {'kickoff returned attempts': 46, 'kickoff return yards': 47, 'yards per kickoff avg': 48, 'longes kickoff return': 49, 'kickoff return touchdows': 50, 'punts returned': 51, 'yards returned on punts': 52, 'yards per punt avg': 53, 'longest punt return': 54, 'punt return touchdowns': 55, 'fair catches': 56}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Returning': {'kickoff returned attempts': 27, 'kickoff return yards': 28, 'yards per kickoff avg': 29, 'longes kickoff return': 30, 'kickoff return touchdows': 31, 'punts returned': 32, 'yards returned on punts': 33, 'yards per punt avg': 34, 'longest punt return': 35, 'punt return touchdowns': 36, 'fair catches': 37}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}, 'Scoring': {'rushing touchdowns': 27, 'receiving touchdowns': 28, 'return touchdowns': 29, 'total touchdowns': 30, 'field goals': 31, 'extra points': 32, 'two point conversions': 33, 'total points': 34, 'total points per game': 35}, 'Rushing': {'rushing attempts': 36, 'yards': 37, 'yards per rush avg': 38, 'longest rush': 39, 'over 20 yards': 40, 'rushing touchdowns': 41, 'yards per game': 42, 'fumbles': 43, 'fumbles lost': 44, 'rushing first downs': 45}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 1, 'receiving yards': 2, 'yards per reception avg': 3, 'receiving touchdowns': 4, 'longest reception': 5, 'over 20 yards': 6, 'yards per game': 7, 'fumbles': 8, 'fumbles lost': 9, 'yards after catch': 10, 'receiving first downs': 11}, 'Defense': {'unassisted tackles': 12, 'assisted tackles': 13, 'total tackles': 14, 'sacks': 15, 'yards lost on sack': 16, 'tackles for loss': 17, 'passes defended': 18, 'interceptions': 19, 'intercepted returned yards': 20, 'longest interception return': 21, 'interceptions returned for touchdowns': 22, 'forced fumbles': 23, 'fumbles recovered': 24, 'fumbles returned for touchdowns': 25, 'blocked kicks': 26}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}, 'Scoring': {'rushing touchdowns': 15, 'receiving touchdowns': 16, 'return touchdowns': 17, 'total touchdowns': 18, 'field goals': 19, 'extra points': 20, 'two point conversions': 21, 'total points': 22, 'total points per game': 23}, 'Kicking': {'field goals made': 24, 'field goals attempts': 25, 'field goals made pct': 26, 'longest goal made': 27, 'field goals from 1 19 yards': 28, 'field goals from 20 29 yards': 29, 'field goals from 30 39 yards': 30, 'field goals from 40 49 yards': 31, 'field goals from 50 yards': 32, 'extra points made': 33, 'extra points attempts': 34, 'extra points made pct': 35}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 1, 'longest punt': 2, 'gross punting avg': 3, 'net punting avg': 4, 'blocked punts': 5, 'inside 20 yards punt': 6, 'touchbacks': 7, 'fair catches': 8, 'punts returned': 9, 'yards returned on punts': 10, 'yards returned on punts avg': 11}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 1, 'completion pct': 2, 'yards': 3, 'yards per pass avg': 4, 'yards per game': 5, 'longest pass': 6, 'passing touchdowns': 7, 'passing touchdowns pct': 8, 'interceptions': 9, 'interceptions pct': 10, 'sacks': 11, 'sacked yards lost': 12, 'quaterback rating': 13}, 'Rushing': {'rushing attempts': 14, 'yards': 15, 'yards per rush avg': 16, 'longest rush': 17, 'over 20 yards': 18, 'rushing touchdowns': 19, 'yards per game': 20, 'fumbles': 21, 'fumbles lost': 22, 'rushing first downs': 23}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 1, 'total tackles': 2, 'sacks': 3, 'yards lost on sack': 4, 'tackles for loss': 5, 'passes defended': 6, 'interceptions': 7, 'intercepted returned yards': 8, 'longest interception return': 9, 'interceptions returned for touchdowns': 10, 'forced fumbles': 11, 'fumbles recovered': 12, 'fumbles returned for touchdowns': 13, 'blocked kicks': 14}}}

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

            # For every stat in that position's dictionary, add the stat to the player's stats
            for group in stats_by_position[player_info[1]]:
                # If the group of stats is not in the player's stats, add 0 for all stats in that group
                if group not in player_stats:
                    for stat in stats_by_position[player_info[1]][group]:
                        stats[player_info[1]].append(0)
                    continue
                for stat in stats_by_position[player_info[1]][group]:
                    # Get the player's corresponding stat
                    # If the stat is not in the player's stats, add 0
                    
                    if stat not in player_stats[group]:
                        stats[player_info[1]].append(0)
                    else:
                        value = player_stats[group][stat]
                        # If the value is a string, turn it into a float
                        try:
                            value = float(value.replace(',', ''))
                        except:
                            pass
                        stats[player_info[1]].append(value)
    return stats

#this function will find the average stats for every position in the league for the entire season
def get_average_stats_per_season():
    #holds the average stats per position for each year
    averagesPerYear = {}

    #keeps track of average stat for each position
    average_per_position = {'RB': {'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}, 'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Returning': {'kickoff returned attempts': 0, 'kickoff return yards': 0, 'yards per kickoff avg': 0, 'longes kickoff return': 0, 'kickoff return touchdows': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards per punt avg': 0, 'longest punt return': 0, 'punt return touchdowns': 0, 'fair catches': 0}}, 'FB': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Returning': {'kickoff returned attempts': 0, 'kickoff return yards': 0, 'yards per kickoff avg': 0, 'longes kickoff return': 0, 'kickoff return touchdows': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards per punt avg': 0, 'longest punt return': 0, 'punt return touchdowns': 0, 'fair catches': 0}}, 'WR': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0},'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}}, 'TE': {'Receiving': {'receptions': 0, 'receiving targets': 0, 'receiving yards': 0, 'yards per reception avg': 0, 'receiving touchdowns': 0, 'longest reception': 0, 'over 20 yards': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'yards after catch': 0, 'receiving first downs': 0}, 'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'C': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'G': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'OT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'DE': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'DT': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'LB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'CB': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'S': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}, 'PK': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}, 'Scoring': {'rushing touchdowns': 0, 'receiving touchdowns': 0, 'return touchdowns': 0, 'total touchdowns': 0, 'field goals': 0, 'extra points': 0, 'two point conversions': 0, 'total points': 0, 'total points per game': 0}, 'Kicking': {'field goals made': 0, 'field goals attempts': 0, 'field goals made pct': 0, 'longest goal made': 0, 'field goals from 1 19 yards': 0, 'field goals from 20 29 yards': 0, 'field goals from 30 39 yards': 0, 'field goals from 40 49 yards': 0, 'field goals from 50 yards': 0, 'extra points made': 0, 'extra points attempts': 0, 'extra points made pct': 0}}, 'P': {'Punting': {'punts': 0, 'gross punt yards': 0, 'longest punt': 0, 'gross punting avg': 0, 'net punting avg': 0, 'blocked punts': 0, 'inside 20 yards punt': 0, 'touchbacks': 0, 'fair catches': 0, 'punts returned': 0, 'yards returned on punts': 0, 'yards returned on punts avg': 0}}, 'QB': {'Passing': {'passing attempts': 0, 'completions': 0, 'completion pct': 0, 'yards': 0, 'yards per pass avg': 0, 'yards per game': 0, 'longest pass': 0, 'passing touchdowns': 0, 'passing touchdowns pct': 0, 'interceptions': 0, 'interceptions pct': 0, 'sacks': 0, 'sacked yards lost': 0, 'quaterback rating': 0}, 'Rushing': {'rushing attempts': 0, 'yards': 0, 'yards per rush avg': 0, 'longest rush': 0, 'over 20 yards': 0, 'rushing touchdowns': 0, 'yards per game': 0, 'fumbles': 0, 'fumbles lost': 0, 'rushing first downs': 0}}, 'LS': {'Defense': {'unassisted tackles': 0, 'assisted tackles': 0, 'total tackles': 0, 'sacks': 0, 'yards lost on sack': 0, 'tackles for loss': 0, 'passes defended': 0, 'interceptions': 0, 'intercepted returned yards': 0, 'longest interception return': 0, 'interceptions returned for touchdowns': 0, 'forced fumbles': 0, 'fumbles recovered': 0, 'fumbles returned for touchdowns': 0, 'blocked kicks': 0}}}
    positionCount = {'QB':0, 'RB':0, 'FB':0, 'WR':0, 'TE':0, 'C':0, 'G':0, 'OT':0, 'DE':0, 'DT':0, 'CB':0, 'LB':0,'S':0, 'PK':0, 'P':0, 'LS':0}

    seasons = [2023]
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
    conn.request("GET", "/seasons", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)

    seasonList = []

    for year in data["response"]:
        seasonList.append(int(year))
    return seasonList

#this function takes two team IDs and the season and returns the games played between the two teams
def get_head_to_head_games(team_id_1,team_id_2,season):
    conn.request("GET", f"/games?season={season}&h2h={team_id_1}-{team_id_2}", headers=headers)

    # Gets the head to head games for the given season
    res = conn.getresponse()
    data = res.read() 
    data = json.loads(data.decode("utf-8"))

    gameList = {}
    
    #iterates through all the games played and tracks 
    for game in data['response']:
        gameList[game['teams']['home']['name'] + " vs " + game['teams']['away']['name']] = game['scores']
    return gameList
#this function takes a season year and teamID and returns all the games the team played for that season
#Each entry will be based on the matchup and will include the gameID, date of the game, and scores of the game
def get_games_for_team_for_season(season,teamID):
    conn.request("GET", f"/games?season={season}&team={teamID}", headers=headers)

    # Gets the head to head games for the given season
    res = conn.getresponse()
    data = res.read() 
    data = json.loads(data.decode("utf-8"))

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
        conn.request("GET", f"/games/statistics/teams?id={games}", headers=headers)

        # Gets the head to head games for the given season
        res = conn.getresponse()
        data = res.read() 
        data = json.loads(data.decode("utf-8"))

        gameStats[games] = {data['response'][0]['team']['name']:data['response'][0]['statistics'],data['response'][1]['team']['name']:data['response'][1]['statistics']}
    return gameStats


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
    

#season [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
#teams and IDS {1: 'Las Vegas Raiders', 2: 'Jacksonville Jaguars', 3: 'New England Patriots', 4: 'New York Giants', 5: 'Baltimore Ravens', 6: 'Tennessee Titans', 7: 'Detroit Lions', 8: 'Atlanta Falcons', 9: 'Cleveland Browns', 10: 'Cincinnati Bengals', 11: 'Arizona Cardinals', 12: 'Philadelphia Eagles', 13: 'New York Jets', 14: 'San Francisco 49ers', 15: 'Green Bay Packers', 16: 'Chicago Bears', 17: 'Kansas City Chiefs', 18: 'Washington Commanders', 19: 'Carolina Panthers', 20: 'Buffalo Bills', 21: 'Indianapolis Colts', 22: 'Pittsburgh Steelers', 23: 'Seattle Seahawks', 24: 'Tampa Bay Buccaneers', 25: 'Miami Dolphins', 26: 'Houston Texans', 27: 'New Orleans Saints', 28: 'Denver Broncos', 29: 'Dallas Cowboys', 30: 'Los Angeles Chargers', 31: 'Los Angeles Rams', 32: 'Minnesota Vikings'}
#{'QB': 87, 'RB': 160, 'FB': 13, 'WR': 240, 'TE': 126, 'C': 18, 'G': 38, 'OT': 32, 'DE': 146, 'DT': 181, 'CB': 258, 'LB': 326, 'S': 188, 'PK': 46, 'P': 42, 'LS': 28}
#2023 {'RB': {'Rushing': {'rushing attempts': 76.4375, 'yards': 319.38125, 'yards per rush avg': 3.59813, 'longest rush': 22.94375, 'over 20 yards': 1.65, 'rushing touchdowns': 2.15625, 'yards per game': 24.54375, 'fumbles': 0.525, 'fumbles lost': 0.29375, 'rushing first downs': 16.775}, 'Receiving': {'receptions': 15.83125, 'receiving targets': 20.34375, 'receiving yards': 113.25625, 'yards per reception avg': 6.1775, 'receiving touchdowns': 0.58125, 'longest reception': 20.74375, 'over 20 yards': 0.975, 'yards per game': 8.84563, 'fumbles': 0.19375, 'fumbles lost': 0.10625, 'yards after catch': 125.85, 'receiving first downs': 4.9}, 'Defense': {'unassisted tackles': 0.675, 'assisted tackles': 0.39375, 'total tackles': 1.06875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01875, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 2.1625, 'receiving touchdowns': 0.58125, 'return touchdowns': 0.00625, 'total touchdowns': 2.75, 'field goals': 0.00625, 'extra points': 0.0, 'two point conversions': 0.1375, 'total points': 16.79375, 'total points per game': 1.31}, 'Returning': {'kickoff returned attempts': 1.56875, 'kickoff return yards': 36.4625, 'yards per kickoff avg': 5.84937, 'longes kickoff return': 8.30625, 'kickoff return touchdows': 0.00625, 'punts returned': 0.25, 'yards returned on punts': 2.13125, 'yards per punt avg': 0.215, 'longest punt return': 0.475, 'punt return touchdowns': 0.0, 'fair catches': 0.16875}}, 'FB': {'Receiving': {'receptions': 5.38462, 'receiving targets': 6.69231, 'receiving yards': 35.30769, 'yards per reception avg': 5.31538, 'receiving touchdowns': 0.38462, 'longest reception': 12.69231, 'over 20 yards': 0.38462, 'yards per game': 2.18462, 'fumbles': 0.07692, 'fumbles lost': 0.07692, 'yards after catch': 23.53846, 'receiving first downs': 1.92308}, 'Defense': {'unassisted tackles': 1.92308, 'assisted tackles': 1.0, 'total tackles': 2.92308, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.23077, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Returning': {'kickoff returned attempts': 0.38462, 'kickoff return yards': 10.53846, 'yards per kickoff avg': 6.92308, 'longes kickoff return': 9.84615, 'kickoff return touchdows': 0.07692, 'punts returned': 0.0, 'yards returned on punts': 0.0, 'yards per punt avg': 0.0, 'longest punt return': 0.0, 'punt return touchdowns': 0.0, 'fair catches': 0.0}}, 'WR': {'Receiving': {'receptions': 27.83333, 'receiving targets': 44.25417, 'receiving yards': 352.89583, 'yards per reception avg': 10.775, 'receiving touchdowns': 2.08333, 'longest reception': 34.27083, 'over 20 yards': 5.07083, 'yards per game': 24.6625, 'fumbles': 0.3375, 'fumbles lost': 0.175, 'yards after catch': 121.625, 'receiving first downs': 16.44583}, 'Defense': {'unassisted tackles': 1.07917, 'assisted tackles': 0.22083, 'total tackles': 1.3, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.01667, 'fumbles recovered': 0.00833, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.1, 'receiving touchdowns': 2.10417, 'return touchdowns': 0.05417, 'total touchdowns': 2.25833, 'field goals': 0.0, 'extra points': 0.0, 'two point conversions': 0.10417, 'total points': 13.75833, 'total points per game': 0.98333}, 'Rushing': {'rushing attempts': 2.0125, 'yards': 12.16667, 'yards per rush avg': 2.41708, 'longest rush': 5.72083, 'over 20 yards': 0.10833, 'rushing touchdowns': 0.09583, 'yards per game': 0.87917, 'fumbles': 0.02083, 'fumbles lost': 0.00417, 'rushing first downs': 0.6625}}, 'TE': {'Receiving': {'receptions': 21.03175, 'receiving targets': 29.59524, 'receiving yards': 218.06349, 'yards per reception avg': 9.22619, 'receiving touchdowns': 1.42063, 'longest reception': 24.68254, 'over 20 yards': 2.54762, 'yards per game': 15.15397, 'fumbles': 0.23016, 'fumbles lost': 0.13492, 'yards after catch': 103.57143, 'receiving first downs': 10.97619}, 'Defense': {'unassisted tackles': 1.23016, 'assisted tackles': 0.54762, 'total tackles': 1.77778, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.00794, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.02381, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.01587}}, 'C': {'Defense': {'unassisted tackles': 0.72222, 'assisted tackles': 0.38889, 'total tackles': 1.11111, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.05556, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'G': {'Defense': {'unassisted tackles': 1.0, 'assisted tackles': 0.13158, 'total tackles': 1.13158, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'OT': {'Defense': {'unassisted tackles': 0.90625, 'assisted tackles': 0.28125, 'total tackles': 1.1875, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}, 'DE': {'Defense': {'unassisted tackles': 12.17123, 'assisted tackles': 9.20548, 'total tackles': 21.37671, 'sacks': 2.65068, 'yards lost on sack': 18.23288, 'tackles for loss': 3.47945, 'passes defended': 1.06164, 'interceptions': 0.03425, 'intercepted returned yards': 0.33562, 'longest interception return': 0.29452, 'interceptions returned for touchdowns': 0.00685, 'forced fumbles': 0.39726, 'fumbles recovered': 0.26027, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.11644}}, 'DT': {'Defense': {'unassisted tackles': 12.46961, 'assisted tackles': 11.51381, 'total tackles': 23.98343, 'sacks': 1.71547, 'yards lost on sack': 11.43646, 'tackles for loss': 2.87845, 'passes defended': 0.86188, 'interceptions': 0.03867, 'intercepted returned yards': 0.07735, 'longest interception return': 0.07735, 'interceptions returned for touchdowns': 0.00552, 'forced fumbles': 0.24862, 'fumbles recovered': 0.24862, 'fumbles returned for touchdowns': 0.0221, 'blocked kicks': 0.02762}}, 'LB': {'Defense': {'unassisted tackles': 23.31902, 'assisted tackles': 15.02454, 'total tackles': 38.34356, 'sacks': 1.76687, 'yards lost on sack': 11.93558, 'tackles for loss': 3.26687, 'passes defended': 1.40798, 'interceptions': 0.24847, 'intercepted returned yards': 3.51534, 'longest interception return': 2.80982, 'interceptions returned for touchdowns': 0.03067, 'forced fumbles': 0.46933, 'fumbles recovered': 0.30982, 'fumbles returned for touchdowns': 0.02147, 'blocked kicks': 0.00307}}, 'CB': {'Defense': {'unassisted tackles': 21.67054, 'assisted tackles': 6.55814, 'total tackles': 28.22868, 'sacks': 0.1376, 'yards lost on sack': 0.94961, 'tackles for loss': 1.02713, 'passes defended': 4.21705, 'interceptions': 0.64341, 'intercepted returned yards': 7.70155, 'longest interception return': 5.9186, 'interceptions returned for touchdowns': 0.09302, 'forced fumbles': 0.3062, 'fumbles recovered': 0.18992, 'fumbles returned for touchdowns': 0.00775, 'blocked kicks': 0.00775}}, 'S': {'Defense': {'unassisted tackles': 29.30851, 'assisted tackles': 13.64894, 'total tackles': 42.95745, 'sacks': 0.38298, 'yards lost on sack': 2.90426, 'tackles for loss': 1.38298, 'passes defended': 2.98936, 'interceptions': 0.89362, 'intercepted returned yards': 13.3883, 'longest interception return': 10.31383, 'interceptions returned for touchdowns': 0.07447, 'forced fumbles': 0.45745, 'fumbles recovered': 0.30851, 'fumbles returned for touchdowns': 0.02128, 'blocked kicks': 0.03191}}, 'PK': {'Defense': {'unassisted tackles': 0.34783, 'assisted tackles': 0.0, 'total tackles': 0.34783, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.0, 'fumbles recovered': 0.0, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}, 'Scoring': {'rushing touchdowns': 0.0, 'receiving touchdowns': 0.0, 'return touchdowns': 0.0, 'total touchdowns': 0.0, 'field goals': 22.95652, 'extra points': 27.58696, 'two point conversions': 0.0, 'total points': 96.45652, 'total points per game': 7.01739}, 'Kicking': {'field goals made': 22.95652, 'field goals attempts': 26.5, 'field goals made pct': 86.56304, 'longest goal made': 53.63043, 'field goals from 1 19 yards': 0.02174, 'field goals from 20 29 yards': 0.87319, 'field goals from 30 39 yards': 0.96027, 'field goals from 40 49 yards': 0.76699, 'field goals from 50 yards': 0.62671, 'extra points made': 27.58696, 'extra points attempts': 28.95652, 'extra points made pct': 94.21957}}, 'P': {'Punting': {'punts': 56.11905, 'gross punt yards': 2668.57143, 'longest punt': 67.2381, 'gross punting avg': 47.66905, 'net punting avg': 41.66905, 'blocked punts': 0.11905, 'inside 20 yards punt': 20.30952, 'touchbacks': 4.07143, 'fair catches': 15.69048, 'punts returned': 24.42857, 'yards returned on punts': 238.90476, 'yards returned on punts avg': 10.1}}, 'QB': {'Passing': {'passing attempts': 217.44828, 'completions': 139.34483, 'completion pct': 59.45977, 'yards': 1515.97701, 'yards per pass avg': 6.66897, 'yards per game': 145.70575, 'longest pass': 49.93103, 'passing touchdowns': 8.78161, 'passing touchdowns pct': 0, 'interceptions': 5.18391, 'interceptions pct': 0, 'sacks': 16.51724, 'sacked yards lost': 111.34483, 'quaterback rating': 78.84713}, 'Rushing': {'rushing attempts': 28.08046, 'yards': 119.7931, 'yards per rush avg': 3.37241, 'longest rush': 15.51724, 'over 20 yards': 0.8046, 'rushing touchdowns': 1.34483, 'yards per game': 12.1908, 'fumbles': 1.54023, 'fumbles lost': 0.56322, 'rushing first downs': 9.71264}}, 'LS': {'Defense': {'unassisted tackles': 1.57143, 'assisted tackles': 1.21429, 'total tackles': 2.78571, 'sacks': 0.0, 'yards lost on sack': 0.0, 'tackles for loss': 0.0, 'passes defended': 0.0, 'interceptions': 0.0, 'intercepted returned yards': 0.0, 'longest interception return': 0.0, 'interceptions returned for touchdowns': 0.0, 'forced fumbles': 0.10714, 'fumbles recovered': 0.03571, 'fumbles returned for touchdowns': 0.0, 'blocked kicks': 0.0}}}
#
#2022 