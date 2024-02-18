import json
import http.client
import numpy as np

#connect to API-NFL
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-rapidapi-host': "v1.american-football.api-sports.io",
    'x-rapidapi-key': "7d2dc831201816acd7bfce6f275ded21"
    }

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
    for i in range(28, 33):
        x, y = stats['PK'][i].split('-')
        x = float(x)
        y = float(y)
        if (y == 0):
            stats['PK'][i] = 0
        else:
            stats['PK'][i] = x / y

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

compiled_stats = compile_stats(get_stats_by_position(3, 2023))
print(compiled_stats)
print(len(compiled_stats))