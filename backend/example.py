from flask import Flask, redirect, url_for,request,json,jsonify,session
from flask_session import Session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import http.client
import bcrypt
from redis import Redis

#sets up flask for routes
app = Flask(__name__)
app.secret_key = 'secret'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = Redis(host='localhost',port=5000)
server_session = Session(app)
cors = CORS(app, supports_credentials=True)
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
            session["user"] = userInfo
            return '',204
        else:
            return 'Invalid Password',406


@app.route("/logout")
def logout():
    session.pop("user",None)
    return '',204

#this function checks whether or not the user is logged in
def checkAuth():
    user = session["user"]
    if not user:
        return None
    return user

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