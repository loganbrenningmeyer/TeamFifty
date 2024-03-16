import torch
import torch.nn as nn
import torch.nn.functional as F

# Basic customizable FCN
import torch
import torch.nn as nn

class ANN(nn.Module):
    def __init__(self, input_size, output_size, hidden_layers, hidden_sizes, hidden_types):
        super(ANN, self).__init__()
        self.layers = nn.ModuleList()

        # Assuming input_size is for the first layer and hidden_sizes[i] for subsequent layers
        prev_size = input_size
        for i in range(hidden_layers):
            layer_type = hidden_types[i]
            layer_size = hidden_sizes[i]

            if layer_type == 1:  # Fully Connected Layer
                layer = nn.Linear(prev_size, layer_size)
                prev_size = layer_size
            elif layer_type == 2:  # Convolutional Layer Example (Assuming 2D Convolution)
                layer = nn.Conv2d(prev_size, layer_size, kernel_size=3, stride=1, padding=1)
                # Update prev_size for the next layer, assuming square input for simplicity
                prev_size = layer_size  # For CNN, update prev_size based on conv output channels
                # Note: You may need to adjust the size for fully connected layers after conv layers
            elif layer_type == 3:  # Recurrent Layer Example (LSTM)
                layer = nn.LSTM(input_size=prev_size, hidden_size=layer_size, batch_first=True)
                prev_size = layer_size  # For RNN/LSTM/GRU, update prev_size based on hidden_size
            else:
                raise ValueError(f"Unsupported layer type: {layer_type}")
            
            self.layers.append(layer)
            # Note: You might need to handle dimensionality changes between different layer types

        # Output layer
        self.output = nn.Linear(prev_size, output_size)

    def forward(self, x):
        # Iterate over each layer
        for layer in self.layers:
            # Apply the layer and possibly an activation function
            x = layer(x)
            # Handle activations, dimensionality changes, etc., here
        # Output layer
        x = self.output(x)
        return x

    
    def train(self, x, y, epochs, batch_size, learning_rate):
        # Define the loss function
        loss_function = nn.MSELoss()
        # Define the optimizer
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        # Define the data loader
        loader = torch.utils.data.DataLoader(x, batch_size=batch_size, shuffle=True)
        # Train the model
        for epoch in range(epochs):
            for batch in loader:
                # Forward pass
                output = self(batch)
                # Calculate the loss
                loss = loss_function(output, y)
                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            # Print the loss
            print("Epoch {}: {}".format(epoch, loss))

    def predict(self, x):
        # Predict the output
        return self(x)

# def main():
#     # Take user input on configuration
#     input_size = int(input("Input size: "))
#     output_size = int(input("Output size: "))
#     hidden_layers = int(input("Number of hidden layers: "))
#     hidden_size = []
#     hidden_type = []
#     for i in range(hidden_layers):
#         hidden_type.append(int(input("Type of hidden layer {}: ".format(i+1))))
#         hidden_size.append(int(input("Size of hidden layer {}: ".format(i+1))))

#     print(hidden_type)
#     print(hidden_size)
#     # Create the model
#     model = ANN(input_size, output_size, hidden_layers, hidden_size, hidden_type)

#     print(model.__repr__)

# main()