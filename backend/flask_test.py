from flask import Flask, jsonify, request
from flask_cors import CORS
import ANN

app = Flask(__name__)
CORS(app, resources={r"/test": {"origins": "http://localhost:3000"}})

@app.route('/test', methods=['GET'])
def test():
    model = ANN.ANN(10, 1, [128, 64, 32], ['relu', 'relu', 'relu'], dropout=False, dropout_rate=0.5)
    result = str(model)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
