from flask import Flask, redirect, url_for,request,json,jsonify,session
from flask_session import Session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import bcrypt
from datetime import timedelta
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
import players
import ANN
from bson.binary import Binary
import io
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.model_selection import train_test_split
from sklearn import svm, metrics
import numpy as np

# Gradient Boosting
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import log_loss, accuracy_score
import joblib

# ANN visualization
import visualkeras
import tensorflow as tf
import base64
from PIL import ImageFont
# GB visualization
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

import torch2keras

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

    # Save the selected stats to the session
    session["selected_stats"] = [key for key in selected_stats.keys() if selected_stats[key]]

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
        
        buffer = io.BytesIO()
        if (session["model_type"] == "ANN"):
            torch.save(session["model"],buffer)
            info = {
            'email':email,
            'model_name':modelName,
            'model_type' : session["model_type"],
            'model': buffer.getvalue(),
            'selected_stats': session["selected_stats"],
            'training_loss' : session["training_loss"],
            'training_accuracy' : session["training_accuracy"],
            'validation_loss' : session["validation_loss"],
            'validation_accuracy' : session["validation_accuracy"],
            'validation_data' : session["validation_data"]
            }
        elif (session["model_type"] == "GB"):
            joblib.dump(session["model"], buffer)
            buffer.seek(0)  # Rewind the buffer to the beginning after writing
            info = {
            'email':email,
            'model_name':modelName,
            'model_type' : session["model_type"],
            'model': buffer.getvalue(),
            'selected_stats': session["selected_stats"],
            'training_loss' : session["training_loss"],
            'training_accuracy' : session["training_accuracy"],
            'validation_loss' : session["validation_loss"],
            'validation_accuracy' : session["validation_accuracy"],
            'validation_data' : session["validation_data"]
            }
        elif(session["model_type"] == "SVM"):
            joblib.dump(session['model'],buffer)
            buffer.seek(0)
            info = {
            'email':email,
            'model_name':modelName,
            'model_type' : session["model_type"],
            'model': buffer.getvalue(),
            'selected_stats': session["selected_stats"],
            'training_accuracy':session['training_accuracy'],
            'validation_accuracy':session['validation_accuracy'],
            'validation_loss':session['validation_loss'],
            'accuracy':session['accuracy'],
            'confusion_matrix':session['confusion_matrix'],
            'detailed_report':session['detailed_report']
            }

        session.pop("model",None)
        savedModels.insert_one(info)
        return 'model successfully saved',204
    return 'user not logged in',406

def get_input_shape(model):
    for layer in model.modules():
        if isinstance(layer, nn.Conv2d):
            # For Conv2d layers, the input shape includes the number of channels expected
            return (layer.in_channels, layer.kernel_size[0], layer.kernel_size[1])
        elif isinstance(layer, nn.Linear):
            # For Linear layers, the input shape is the number of features (flattened input size)
            return (layer.in_features,)
    return "Input layer type not found or model does not have a recognizable first layer"

@app.route('/getAllModels',methods=['GET'])
def getAllModels():
    modelList = []
    for entries in savedModels.find({},{'_id':0,'model_name':1,'model_type':1,'validation_accuracy':1}):
        modelList.append(entries)
    
    return jsonify(modelList)


#this function will return information for all of the models the current logged in user has created
@app.route('/retrieveModels', methods=['GET'])
def getModels():

    db = client.get_database('userAccountInfo')
    savedModels = db.get_collection('modelStorage')

    saved_models = []

    if "email" in session:
        model = ANN.ANN 

        email = session['email']
        for entry in savedModels.find({'email':email}):

            # Load PyTorch model
            if (entry['model_type'] == "ANN"):
                buffer = io.BytesIO(entry['model'])
                model = torch.load(buffer,weights_only=False)

                model.train(mode=False)

                input_shape = get_input_shape(model)
                
                keras_model = torch2keras.convert_pytorch_model_to_keras(model, input_shape)

                font = ImageFont.truetype("ARIAL.ttf", 16)

                # Get model visualization png
                visualkeras.layered_view(keras_model, to_file='output.png', 
                                        legend=True, 
                                        scale_xy=1, scale_z=0.75, 
                                        min_xy=64,
                                        background_fill=None,
                                        font=font,
                                        font_color='white')

                try:
                    with open('output.png', 'rb') as image_file:
                        model_vis = base64.b64encode(image_file.read()).decode('utf-8')
                except FileNotFoundError:
                    model_vis = "Visualization not available"
                saved_models.append({"email" : entry['email'],
                    "model_name" : entry['model_name'],
                    "model_type" : entry['model_type'],
                    "model_vis" : model_vis,
                    "selected_stats" : entry['selected_stats'],
                    "training_loss" : entry['training_loss'],
                    "training_accuracy" : entry['training_accuracy'],
                    "validation_loss" : entry['validation_loss'],
                    "validation_accuracy" : entry['validation_accuracy']})
                # Load GB model
            elif (entry['model_type'] == "GB"):
                model = joblib.load(io.BytesIO(entry['model']))

                plt.figure(figsize=(20, 10), dpi=300)
                plot_tree(model.estimators_[0][0], filled=True, rounded=True)
                plt.savefig('output.png', transparent=True, bbox_inches='tight')

                with open('output.png', 'rb') as image_file:
                    model_vis = base64.b64encode(image_file.read()).decode('utf-8')

                saved_models.append({"email" : entry['email'],
                    "model_name" : entry['model_name'],
                    "model_type" : entry['model_type'],
                    "model_vis" : model_vis,
                    "selected_stats" : entry['selected_stats'],
                    "training_loss" : entry['training_loss'],
                    "training_accuracy" : entry['training_accuracy'],
                    "validation_loss" : entry['validation_loss'],
                    "validation_accuracy" : entry['validation_accuracy']}) 
                
            elif (entry['model_type'] == "SVM"):
                #model = joblib.load(io.BytesIO(entry['model']))

                saved_models.append({"email" : entry['email'],
                    "model_name" : entry['model_name'],
                    "model_type" : entry['model_type'],
                    "selected_stats" : entry['selected_stats'],
                    "training_accuracy" : entry['training_accuracy'],
                    "validation_loss" : entry['validation_loss'],
                    "validation_accuracy" : entry['validation_accuracy'],
                    'accuracy' : entry['accuracy'],
                    'confusion_matrix': entry['confusion_matrix'],
                    'detailed_report' : entry['detailed_report']
                    })

        

        session["saved_models"] = saved_models

        return jsonify(saved_models)


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
    
    # Learning rate
    learning_rate = float(parameters['learning_rate'])


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
                    optimizer,
                    learning_rate,
                    epochs=100)
    
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

    # For saving
    validation_data_list = [tensor.numpy().tolist() for tensor in validation_set.tensors]

    print("Validation data:", validation_data_list)

    # Create DataLoaders
    training_loader = DataLoader(training_set, batch_size=batch_size, shuffle=True)
    validation_loader = DataLoader(validation_set, batch_size=batch_size, shuffle=False)
    
    training_loss, training_accuracy, validation_loss, validation_accuracy = model.train(training_dataloader=training_loader, validation_dataloader=validation_loader, mode=True) 

    # Save PyTorch model
    session["model"] = model
    session["model_type"] = "ANN"

    # Save training loss/accuracy
    session["training_loss"] = training_loss
    session["training_accuracy"] = training_accuracy
    session["validation_loss"] = validation_loss
    session["validation_accuracy"] = validation_accuracy
    session["validation_data"] = validation_data_list

    return jsonify({'training_loss': training_loss, 'training_accuracy': training_accuracy, 'validation_loss': validation_loss, 'validation_accuracy': validation_accuracy})

@app.route('/train_GB', methods=['POST'])
def train_GB():
    parameters = request.json
    print("Gradient Boosting training parameters:", parameters)
    
    # Get the parameters from the frontend
    n_estimators = int(parameters['n_estimators'])
    learning_rate = float(parameters['gb_learning_rate'])
    max_depth = int(parameters['max_depth'])
    min_samples_split = int(parameters['min_samples_split'])
    min_samples_leaf = int(parameters['min_samples_leaf'])
    subsample = float(parameters['subsample'])
    # Fix max_features naming
    if (parameters['max_features'] == 'null'):
        max_features = None
    else:
        max_features = parameters['max_features']

    # Load the data
    input_data = torch.load("input_data.pt")
    target_data = torch.load("target_data.pt")

    # Normalize the data
    input_data = F.normalize(input_data, p=2, dim=0)

    # Calculate training size
    train_size = int(0.8 * len(input_data))

    # Shuffle the data
    shuffle = torch.randperm(input_data.shape[0])
    input_data = input_data[shuffle]
    target_data = target_data[shuffle]

    # Split the data into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(input_data.numpy(), target_data.numpy(), test_size=0.2)
    
    # Get validation data for saving
    validation_data_list = [X_test.tolist(), y_test.tolist()]

    print("Validation data:", validation_data_list)

    gbc = GradientBoostingClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        subsample=subsample
    )

    # List to hold metrics for each stage
    training_loss = []
    training_accuracy = []
    validation_loss = []
    validation_accuracy = []

    # Fit the model incrementally and calculate metrics at each stage
    gbc.fit(X_train, y_train)

    # Iterate over the staged predictions for both training and testing sets
    for train_pred in gbc.staged_predict(X_train):
        training_accuracy.append(accuracy_score(y_train, train_pred))
        training_loss.append(log_loss(y_train, train_pred))

    for test_pred in gbc.staged_predict(X_test):
        validation_accuracy.append(accuracy_score(y_test, test_pred))
        validation_loss.append(log_loss(y_test, test_pred))

    # Evaluate final model
    final_accuracy = accuracy_score(y_test, gbc.predict(X_test))
    print(f"Final Accuracy: {final_accuracy:.2f}")

    # Save model
    session["model"] = gbc
    session["model_type"] = "GB"

    # Save training loss/accuracy
    session["training_loss"] = training_loss
    session["training_accuracy"] = training_accuracy
    session["validation_loss"] = validation_loss
    session["validation_accuracy"] = validation_accuracy
    session["validation_data"] = validation_data_list

    return jsonify({
        'training_loss': training_loss,
        'training_accuracy': training_accuracy,
        'validation_loss': validation_loss,
        'validation_accuracy': validation_accuracy
    })

@app.route('/train_SVM', methods=['POST'])
def train_SVM():
    parameters = request.json
    print("SVM training parameters:", parameters)

    # Extract parameters
    kernel = parameters.get('kernel', 'rbf')
    C = float(parameters.get('C', 1.0))
    gamma = parameters.get('gamma', 'scale')

    # Load and preprocess data
    input_data = torch.load("input_data.pt").numpy()
    target_data = torch.load("target_data.pt").numpy().ravel()
    scaler = StandardScaler()
    input_data = scaler.fit_transform(input_data)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(input_data, target_data, test_size=0.2, random_state=42)

    # Further split for validation during training (if needed)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=101)

    # Initialize SVM and lists for tracking metrics
    model = svm.SVC(kernel=kernel, C=C, gamma=gamma, probability=True)
    training_accuracy = []
    validation_accuracy = []
    validation_loss = []

    # Fit model and monitor performance
    model.fit(X_train, y_train)
    training_predictions = model.predict(X_train)
    training_accuracy.append(accuracy_score(y_train, training_predictions))

    # Validation performance
    val_predictions = model.predict(X_val)
    validation_accuracy.append(accuracy_score(y_val, val_predictions))
    probs = model.predict_proba(X_val)
    validation_loss.append(log_loss(y_val, probs))

    # Testing and final evaluation
    y_pred = model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
    classification_report = metrics.classification_report(y_test, y_pred, output_dict=True)

    confuse = []
    for array in confusion_matrix:
        for num in array:
            confuse.append(int(num))

    session["model"] = model
    session["model_type"] = "SVM"
    session['training_accuracy'] = f"{training_accuracy[0] * 100:.2f}"
    session['validation_accuracy'] = f"{validation_accuracy[0] * 100:.2f}"
    session['validation_loss'] = validation_loss
    session['accuracy'] = f"{accuracy * 100:.2f}"
    session['confusion_matrix'] = confuse
    session['detailed_report'] = classification_report['weighted avg']

    # Return metrics and reports
    return jsonify({
        'training_accuracy': f"{training_accuracy[0] * 100:.2f}%",
        'validation_accuracy': f"{validation_accuracy[0] * 100:.2f}%",
        'validation_loss': validation_loss,
        'accuracy': f"{accuracy * 100:.2f}%",
        'confusion_matrix': confusion_matrix.tolist(),
        'detailed_report': classification_report['weighted avg']
    })

@app.route("/search",methods=['GET'])
def searchModel():
    search = request.args.get('q','')
    
    result = savedModels.aggregate([
        {
            "$search":{
                "index":"model_search",
                "text":{
                    "query":search,
                    "path":["model_name","model_type"],
                    "fuzzy":{}
                }
            }
        },
        {
            "$project":{
                "_id":0,
                "model":0
            }
        }
    ])
    modelsFound = []
    for r in result:
        modelsFound.append(r)
        print(r['model_name'],r['model_type'])

        
    return jsonify(modelsFound)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


if __name__ == "__main__":
    app.run(debug=True)