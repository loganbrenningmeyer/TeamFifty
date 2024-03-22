from flask import Flask, jsonify, request
from flask_cors import CORS

import torch

import players
import ANN

app = Flask(__name__)
CORS(app, resources={r"/test": {"origins": "http://localhost:3000"}, 
                     r"/data": {"origins": "http://localhost:3000"}})

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
    input_data = players.filter_stats(input_data, [key for key in selected_stats.keys() if selected_stats[key]])

    print(input_data.shape)
    print(target_data.shape)

    return jsonify({'data': selected_stats})

if __name__ == '__main__':
    app.run(debug=True)
