from flask import Flask, redirect, url_for,request,json,jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import http.client
import bcrypt

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
    
    #attempt to see if an account already exists
    search = userInfoColl.find_one({'email':email})

    #if search is None then no user with that email exists so we can create an account for that user, otherwise there is already an account with that email
    if search is None:
        userInfo['password'] = bcrypt.hashpw(userInfo['password'].encode('utf-8'),bcrypt.gensalt())
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
        if bcrypt.checkpw(password.encode('utf-8'),search['password']) == True:
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
    app.run(debug=True)