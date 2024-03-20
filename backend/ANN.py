import torch
import torch.nn as nn
import torch.nn.functional as F

# Basic customizable FCN
import torch
import torch.nn as nn

class ANN(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes, activation_functions):
        super(ANN, self).__init__()
        self.layers = nn.ModuleList()

        # Assuming input_size is for the first layer and hidden_sizes[i] for subsequent layers
        prev_size = input_size
        for i in range(len(hidden_sizes)):
            layer_size = hidden_sizes[i]

            layer = nn.Linear(prev_size, layer_size)
            prev_size = layer_size

            # Add the layer to the list of layers
            self.layers.append(layer)
            
            # Add the activation function to the list of layers
            if (activation_functions[i] == 'relu'):
                self.layers.append(nn.ReLU())
            elif (activation_functions[i] == 'sigmoid'):
                self.layers.append(nn.Sigmoid())
            elif (activation_functions[i] == 'tanh'):
                self.layers.append(nn.Tanh())

        # Output layer
        self.output = nn.Linear(prev_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # Iterate over each layer
        for layer in self.layers:
            # Apply the layer and possibly an activation function
            x = layer(x)
            # Handle activations, dimensionality changes, etc., here
        # Output layer
        x = self.output(x)
        x = self.sigmoid(x)
        return x
    
    def train(self, dataloader, epochs, lr):
        # Define the loss function
        criterion = nn.BCELoss()

        # Define the optimizer
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)

        # Training loop
        for epoch in range(epochs):
            running_loss = 0.0
            correct = 0
            total = 0

            for i, data in enumerate(dataloader):
                # Get the inputs and labels
                inputs, labels = data

                # Zero the parameter gradients
                optimizer.zero_grad()

                # Forward pass
                outputs = self(inputs)

                # Compute the loss and gradients
                loss = criterion(outputs, labels)
                loss.backward()

                # Update the parameters
                optimizer.step()

                # Update loss and accuracy metrics
                running_loss += loss.item()
                predicted = (outputs > 0.5).float()
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            # Print the loss and accuracy for every epoch
            epoch_loss = running_loss / len(dataloader)
            epoch_accuracy = correct / total
            if (epoch_accuracy > 0.9): # Stop early if accuracy is high enough
                break
            print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.4f}")

    def predict(self, x):
        # Predict the output
        return self(x)