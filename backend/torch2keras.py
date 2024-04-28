import torch
import torch.nn as nn
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Dense, Dropout, Activation
from tensorflow.keras.activations import relu, sigmoid, tanh

def convert_pytorch_model_to_keras(pytorch_model, input_shape):
    # Initialize a Keras Sequential model
    keras_model = Sequential()
    
    # Loop through the layers of the PyTorch model
    for layer in pytorch_model.modules():
        if isinstance(layer, nn.Linear):
            # For a fully connected layer
            units = layer.out_features
            input_dim = layer.in_features
            keras_model.add(Dense(units=units, input_dim=input_dim, activation=None))
        elif isinstance(layer, nn.ReLU):
            # For ReLU activation layers
            keras_model.add(Activation(relu))
        elif isinstance(layer, nn.Sigmoid):
            # For Sigmoid activation layers
            keras_model.add(Activation(sigmoid))
        elif isinstance(layer, nn.Tanh):
            # For Tanh activation layers
            keras_model.add(Activation(tanh))
        elif isinstance(layer, nn.Dropout):
            # For Dropout layers
            rate = layer.p
            keras_model.add(Dropout(rate))
        # Add more conditions if other types of layers are present in the PyTorch model

    # Compile the model (Required to train, adjust according to needs)
    keras_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return keras_model

# Example usage
# Assuming you have a PyTorch model `pytorch_model` already defined
# pytorch_model = SimpleBinaryClassifier() from your provided code

# Convert it to Keras
# keras_model = convert_pytorch_model_to_keras(pytorch_model)
# print(keras_model.summary())
