from flask import Flask, redirect, url_for,request,json,jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import http.client

teamDict = {
    "Las Vegas Raiders": 1,
    "Jacksonville Jaguars":2,
    "New England Patriots":3,
    "New York Giants":4,
    "Baltimore Ravens":5,
    "Tennessee Titans":6,
    "Detroit Lions":7,
    "Atlanta Falcons":8,
    "Cleveland Browns":9,
    "Cincinnati Bengals":10,
    "Arizona Cardinals":11,
    "Philadelphia Eagles":12,
    "New York Jets":13,
    "San Francisco 49ers":14,
    "Green Bay Packers":15,
    "Chicago Bears":16,
    "Kansas City Chiefs":17,
    "Washington Commanders":18,
    "Carolina Panthers":19,
    "Buffalo Bills":20,
    "Indianapolis Colts":21,
    "Pittsburgh Steelers":22,
    "Seattle Seahawks":23,
    "Tampa Bay Buccaneers":24,
    "Miami Dolphins":25,
    "Houston Texans":26,
    "New Orleans Saints":27,
    "Denver Broncos":28,
    "Dallas Cowboys":29,
    "Los Angeles Chargers":30,
    "Los Angeles Rams":31,
    "Minnesota Vikings":32
}
#connect to API-NFL
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-rapidapi-host': "v1.american-football.api-sports.io",
    'x-rapidapi-key': "c70572c71dea5b9097425435a60d972e"
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
        players[player['id']] = player['name']

    return players

def get_stats_by_player(player_id, season):
    conn.request("GET", f"/players/statistics?id={player_id}&season={season}", headers=headers)

    # Get the player's stats based on their ID
    res = conn.getresponse()
    data = res.read() 
    data = json.loads(data.decode("utf-8"))

    stats = {}

    # Prints the player's stats divided by category (Rushing, Receiving, Defense, Passing, Scoring, Returning)
    for group in data['response'][0]['teams'][0]['groups']:
        
        stats[group['name']] = {}
        # Print the stats for each category
        for stat in group['statistics']:
            stats[group['name']][stat['name']] = stat['value']
    
    return stats

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
    print(seasonList)
    return seasonList

def playerStats():
    conn.request("GET", "/players?team=1&season=2023", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Data as dict
    data = json.loads(data)
    # --- Read an entire team's player stats ---
    # First, read the players from the team
    # conn.request("GET", "/players?team=#&season=#", headers=headers)

    # Then, read the stats for each player
    # conn.request("GET", f"/players/statistics?id={player['id']}&season=#", headers=headers)

    # Finally, print the stats for each player
    # for group in stat_data['response'][0]['teams'][0]['groups']:
    #     print(f"\n---{group['name']}---\n")
    #     for stat in group['statistics']:
    #         print(f"{stat['name']}: {stat['value']}")
    print(data)
    count = 0

    for player in data['response']:

        # Retrieve the first player's stats based on their ID
        if count == 0:

            conn.request("GET", f"/players/statistics?id={player['id']}&season=2023", headers=headers)

            # Get the player's stats based on their ID
            res = conn.getresponse()
            stat_data = res.read() 
            stat_data = json.loads(stat_data.decode("utf-8"))

            print(f"{player['name']}: {player['id']}")

            # Prints the player's stats divided by category (Rushing, Receiving, Defense, Passing, Scoring, Returning)
            for group in stat_data['response'][0]['teams'][0]['groups']:
                print(f"\n---{group['name']}---\n")
                # Print the stats for each category
                for stat in group['statistics']:
                    print(f"{stat['name']}: {stat['value']}")

            count += 1
        
        print(f"\n{player['name']}: {player['id']}")

#sets up flask for routes
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Create a new client and connect to the database and collection
uri = "mongodb+srv://TeamFifty:s3v6EdcMysAgxbdq@cluster0.uognzqp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('userAccountInfo')
userInfoColl = db.get_collection('userInfo')

#Parameters:user email and password
#This function will make sure a user doesn't already exist with the given email and if not the account info will be saved to the database
@app.route('/signup',methods=['POST'])
def createUser():
    #get the email and password of user who wants to create account
    userInfo = request.get_json()
    email = userInfo['email']
    password = userInfo['password']
    
    #attempt to see if an account already exists
    search = userInfoColl.find_one({'email':email})

    #if search is None then no user with that email exists so we can create an account for that user, otherwise there is already an account with that email
    if search is None:
        userInfoColl.insert_one(userInfo)
        return '',204
    else:
        return 'User Already Exists',406

#Parameters:user email and password
#this function will take a user's email and password and check if the account exists and if the correct password is input. If the user doesn't exist or a wrong password is input an error will be returned.
@app.route('/signin',methods=['POST'])
def signInUser():
    #get the email and password of user who wants to sign in
    userInfo = request.get_json()
    email = userInfo['email']
    password = userInfo['password']

    #attempt to see if an account already exists
    search = userInfoColl.find_one({'email':email})

    #if search is None then a user with that email doesnt exist, if the search does exist we must check that the password input is correct
    if search is None:
        return 'Account does not Exist',404
    else:
        #now we check if the input password matches correct password
        if password == search['password']:
            return '',204
        else:
            return 'Invalid Password',406


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
#how to insert into the database
#userInfoColl.insert_one({"email":"cvan@yahoo.com","password":"turtle"})
    
#how to search for something in the database
# query = {"email":"cvan@yahoo.com"}
# result = userInfoColl.find_one(query)
# print(result)

if __name__ == "__main__":
    print(get_head_to_head_games(1,3,2023))
    #print(get_players_by_team(1,2022))
    #print(get_stats_by_player(1,2022))
    #get_teams_by_season(1,2020)
    #playerStats()
    #getSeasons()
    #app.run(debug=True)