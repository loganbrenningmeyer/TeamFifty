from flask import Flask, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import json
import http.client

#connect to API-NFL
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-rapidapi-host': "v1.american-football.api-sports.io",
    'x-rapidapi-key': "8b1b4865aab2aebaa8799a5765e40b49"
    }
conn.request("GET", "/leagues", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


#sets up flask for routes
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Create a new client and connect to the database and collection
uri = "mongodb+srv://TeamFifty:s3v6EdcMysAgxbdq@cluster0.uognzqp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('userAccountInfo')
userInfoColl = db.get_collection('userInfo')


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
#how to insert into the database
#userInfoColl.insert_one({"email":"cvan@yahoo.com","password":"turtle"})
    
#how to search for something in the database
query = {"email":"cvan@yahoo.com"}
result = userInfoColl.find_one(query)
print(result)

