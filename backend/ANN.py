import torch
import torch.nn as nn
import torch.nn.functional as F

# Basic customizable FCN
import torch
import torch.nn as nn

class ANN(nn.Module):
    def __init__(self, input_size, output_size, 
                hidden_sizes, 
                activation_function, 
                dropout_rate=0.5, 
                loss_function='BCELoss',
                optimizer='Adam',
                lr=0.001,
                epochs=100):
        super(ANN, self).__init__()
        self.layers = nn.ModuleList()

        # Set loss function
        self.loss_function = loss_function

        # Set optimizer
        self.optimizer = optimizer

        # Set learning rate and epochs
        self.lr = lr
        self.epochs = epochs

        # Assuming input_size is for the first layer and hidden_sizes[i] for subsequent layers
        prev_size = input_size
        for i in range(len(hidden_sizes)):
            layer_size = hidden_sizes[i]

            layer = nn.Linear(prev_size, layer_size)
            prev_size = layer_size

            # Add the layer to the list of layers
            self.layers.append(layer)
            
            # Add the activation function to the list of layers
            if (activation_function == 'relu'):
                self.layers.append(nn.ReLU())
            elif (activation_function == 'sigmoid'):
                self.layers.append(nn.Sigmoid())
            elif (activation_function == 'tanh'):
                self.layers.append(nn.Tanh())

            # Add the dropout layer to the list of layers
            if (dropout_rate > 0):
                self.layers.append(nn.Dropout(p=dropout_rate))

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
        if (self.loss_function == 'BCELoss'):
            x = self.sigmoid(x)
        return x
    
    def train(self, training_dataloader=None, validation_dataloader=None, mode=True):
        # History lists to store loss and accuracy for each epoch
        training_loss_history = []
        training_accuracy_history = []
        validation_loss_history = []
        validation_accuracy_history = []

        if mode and training_dataloader is not None:
            print("Training the model...")
            # Set the loss function based on the configuration
            loss_function = nn.MSELoss() if self.loss_function == 'MSELoss' else nn.BCELoss()

            # Set the optimizer based on the configuration
            optimizer = torch.optim.SGD(self.parameters(), lr=self.lr) if self.optimizer == 'SGD' else torch.optim.Adam(self.parameters(), lr=self.lr)

            # Training loop
            for epoch in range(self.epochs):
                # Training phase
                self.train()  # Ensures the model is in training mode
                running_loss = 0.0
                correct = 0
                total = 0

                for data in training_dataloader:
                    inputs, labels = data
                    optimizer.zero_grad()
                    outputs = self(inputs)
                    loss = loss_function(outputs, labels)
                    loss.backward()
                    optimizer.step()

                    running_loss += loss.item()
                    predicted = (outputs > 0.5).float()
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

                training_loss = running_loss / len(training_dataloader)
                training_accuracy = correct / total
                training_loss_history.append(training_loss)
                training_accuracy_history.append(training_accuracy)

                # Validation phase
                self.train(mode=False, training_dataloader=None)  # Sets the model to evaluation mode
                validation_loss = 0.0
                correct = 0
                total = 0
                with torch.no_grad():
                    for data in validation_dataloader:
                        inputs, labels = data
                        outputs = self(inputs)
                        loss = loss_function(outputs, labels)

                        validation_loss += loss.item()
                        predicted = (outputs > 0.5).float()
                        total += labels.size(0)
                        correct += (predicted == labels).sum().item()

                validation_loss /= len(validation_dataloader)
                validation_accuracy = correct / total
                validation_loss_history.append(validation_loss)
                validation_accuracy_history.append(validation_accuracy)

                print(f"Epoch {epoch+1}/{self.epochs}, Training Loss: {training_loss:.4f}, Training Accuracy: {training_accuracy:.4f}, Validation Loss: {validation_loss:.4f}, Validation Accuracy: {validation_accuracy:.4f}")

            # Return the history of training and validation loss/accuracy
            return training_loss_history, training_accuracy_history, validation_loss_history, validation_accuracy_history
    
    def test(self, validation_loader):
        # Predict the output on testing data and print the percent correct
        correct = 0
        total = 0
        for inputs, targets in validation_loader:
            preds = self.predict(inputs)
            rounded_preds = torch.round(preds)
            
            correct += (rounded_preds == targets).sum().item()
            total += targets.size(0)
            
            for pred, target in zip(preds, targets):
                print(f"Prediction: {pred.item():.4f}, Actual: {target.item()}")

        accuracy = correct / total

        return accuracy

    def predict(self, x):
        # Predict the output
        return self(x)