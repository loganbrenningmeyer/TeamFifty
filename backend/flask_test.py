from flask import Flask, jsonify, request, session
from flask_cors import CORS

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset, random_split

import players
import ANN

app = Flask(__name__)

app.secret_key = 'secret'

CORS(app, resources={r"/test": {"origins": "http://localhost:3000"}, 
                     r"/data": {"origins": "http://localhost:3000"},
                     r"/train": {"origins": "http://localhost:3000"}})

@app.route('/test', methods=['GET'])
def test():
    model = ANN.ANN(10, 1, [128, 64, 32], ['relu', 'relu', 'relu'], dropout=False, dropout_rate=0.5)
    result = str(model)
    return jsonify({'result': result})

@app.route('/data', methods=['POST'])
def data():
    selected_stats = request.json

    # Check if any stats are selected
    if not any(selected_stats.values()):
        return jsonify({'data': selected_stats})

    print(selected_stats)

    # Get all of the data
    input_data_2022 = torch.load(f"input_data_1_2022.pt")
    target_data_2022 = torch.load(f"target_data_1_2022.pt")

    input_data_2023 = torch.load(f"input_data_1_2023.pt")
    target_data_2023 = torch.load(f"target_data_1_2023.pt")

    input_data = torch.cat((input_data_2022, input_data_2023), dim=0)
    target_data = torch.cat((target_data_2022, target_data_2023), dim=0)

    # Filter the data by the selected stats (stat == true)
    selected_data = players.filter_stats(input_data, [key for key in selected_stats.keys() if selected_stats[key]])

    # Save the data to a file
    torch.save(selected_data, "input_data.pt")
    torch.save(target_data, "target_data.pt")

    print(selected_data.shape)
    print(target_data.shape)

    return jsonify({'data': selected_stats})

@app.route('/train', methods=['POST'])
def train():
    parameters = request.json

    # Load the data
    input_data = torch.load("input_data.pt")
    target_data = torch.load("target_data.pt")
    
    model = ANN.ANN(input_data.shape[1], 1,
                    [128, 64, 32], parameters['activation'],
                    dropout=True, dropout_rate=0.5,
                    loss_function=parameters['loss'],
                    optimizer=parameters['optimizer'])
    
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

    # Define batch size
    batch_size = 8

    # Create DataLoaders
    training_loader = DataLoader(training_set, batch_size=batch_size, shuffle=True)
    validation_loader = DataLoader(validation_set, batch_size=batch_size, shuffle=False)
    
    model.train(training_loader, 100, 0.001)

    return jsonify({'parameters': parameters})

if __name__ == '__main__':
    app.run(debug=True)
