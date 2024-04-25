from flask import Flask, redirect, url_for,request,json,jsonify,session
from flask_session import Session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import http.client
import bcrypt
from datetime import timedelta
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset, random_split
import players
import ANN
from bson.binary import Binary
import io

#sets up flask for routes
app = Flask(__name__)
app.secret_key = 'secret'
app.config["SESSION_TYPE"] = 'filesystem'
app.permanent_session_lifetime = timedelta(days=1)
app.config['CORS_HEADERS'] = 'Content-Type'
Session(app)
cors = CORS(app, supports_credentials=True)

# Create a new client and connect to the database and collection
uri = "mongodb+srv://TeamFifty:s3v6EdcMysAgxbdq@cluster0.uognzqp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('userAccountInfo')
userInfoColl = db.get_collection('userInfo')
savedModels = db.get_collection('modelStorage')

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
            session.permanent = True
            session["email"] = email
            return '',204
        else:
            return 'Invalid Password',406

@app.route("/logout")
def logout():
    session.pop("email",None)
    return '',204

#this function checks whether or not the user is logged in
@app.route("/auth")
def checkAuth():
    if "email" in session:
        print(session['email'])
        return session['email'],204
    return 'not logged in',206

@app.route('/test', methods=['GET'])
def test():
    model = ANN.ANN(10, 1, [128, 64, 32], ['relu', 'relu', 'relu'], dropout=False, dropout_rate=0.5)
    result = str(model)
    return jsonify({'result': result})

@app.route('/data', methods=['POST'])
def data():
    selected_stats = request.json

    print(selected_stats)

    # Get all of the data
    input_data_2022 = torch.load(f"input_data_1_2022.pt")
    target_data_2022 = torch.load(f"target_data_1_2022.pt")

    input_data_2023 = torch.load(f"input_data_1_2023.pt")
    target_data_2023 = torch.load(f"target_data_1_2023.pt")

    input_data = torch.cat((input_data_2022, input_data_2023), dim=0)
    target_data = torch.cat((target_data_2022, target_data_2023), dim=0)

    # Check if any stats are selected
    if not any(selected_stats.values()):
        selected_data = input_data
    else:
        # Filter the data by the selected stats (stat == true)
        selected_data = players.filter_stats(input_data, [key for key in selected_stats.keys() if selected_stats[key]])

    # Save the data to a file
    torch.save(selected_data, "input_data.pt")
    torch.save(target_data, "target_data.pt")

    print(selected_data.shape)
    print(target_data.shape)

    return jsonify({'data': selected_stats})

#this function takes a model name and saves the model to mongodb
@app.route('/save',methods=['POST'])
def saveModel():
    req = request.get_json()

    modelName = req['model name']
    #checks to make sure the user is logged in which they should be
    if "email" in session:
        email = session['email']
        print(email)
        buffer = io.BytesIO()
        torch.save(session["ANNModel"],buffer)
        info = {
            'email':email,
            'model name':modelName,
            'model': buffer.getvalue()
        }
        session.pop("ANNModel",None)
        savedModels.insert_one(info)
        return 'model successfully saved',204
    return 'user not logged in',406

#this function will return information for all of the models the current logged in user has created
@app.route('/retrieveModels')
def getModels():
    if "email" in session:
        model = ANN.ANN 

        email = session['email']
        for entries in savedModels.find({'email':email}):
            buffer = io.BytesIO(entries['model'])
            model = torch.load(buffer,weights_only=False)
            print(model)
            #model.eval()
        return 'successfull retrieval',204


    return 'user not logged in',406

@app.route('/train', methods=['POST'])
def train():
    parameters = request.json

    print(parameters)

    # Get the hidden layer sizes
    hidden_sizes = [int(size) for size in parameters['layers'].split(",")]

    # Dropout rate
    dropout_rate = float(parameters['dropout_rate'])

    # Learning rate
    learning_rate = float(parameters['learning_rate'])

    # Batch size
    batch_size = int(parameters['batch_size'])

    # Loss function
    loss_function = parameters['loss']

    # Optimizer
    optimizer = parameters['optimizer']

    # Activation function
    activation_function = parameters['activation']

    # Load the data
    input_data = torch.load("input_data.pt")
    target_data = torch.load("target_data.pt")
    
    #global model
    model = ANN.ANN(input_data.shape[1], 1,
                    hidden_sizes, 
                    activation_function, 
                    dropout_rate,
                    loss_function,
                    optimizer)
    
    print(model)
    
    # Normalize the data
    input_data = F.normalize(input_data, p=2, dim=0)

    # Calculate training size
    train_size = int(0.8 * len(input_data))

    # Shuffle the data
    shuffle = torch.randperm(input_data.shape[0])
    input_data = input_data[shuffle]
    target_data = target_data[shuffle]

    # Create Datasets
    training_set = TensorDataset(input_data[:train_size], target_data[:train_size])
    validation_set = TensorDataset(input_data[train_size:], target_data[train_size:])

    # Create DataLoaders
    training_loader = DataLoader(training_set, batch_size=batch_size, shuffle=True)
    validation_loader = DataLoader(validation_set, batch_size=batch_size, shuffle=False)
    
    loss, accuracy = model.train(training_loader, 100, learning_rate)

    validation_accuracy = model.test(validation_loader)

    session["ANNModel"] = model

    return jsonify({'loss': "{:.3f}".format(loss), 'accuracy': "{:.2f}%".format(accuracy*100), 'validation_accuracy': "{:.2f}%".format(validation_accuracy*100)})


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