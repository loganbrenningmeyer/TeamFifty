import players
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset, random_split
import ANN

# torch.set_printoptions(threshold=torch.inf)

league = 1
season = 2023

normalize = 1

# Returns a dictionary of data for each game in a given league/season
# Dictionary in the format: {game_name: {'input': input_data, 'target': target_data}}
input_data, target_data = players.get_pytorch_data(league, season)

print(f"Input data shape: {input_data.shape}")
print(f"Input data: {input_data}")
print(f"Target data shape: {target_data.shape}")
print(f"Target data: {target_data}")


# Normalize
if normalize:
    input_data = F.normalize(input_data, p=2, dim=0)

# Calculate training size
train_size = int(0.8 * len(input_data))

# Create Datasets
training_set = TensorDataset(input_data[:train_size], target_data[:train_size])
validation_set = TensorDataset(input_data[train_size:], target_data[train_size:])

# Define batch size
batch_size = 4

# Create DataLoaders
training_loader = DataLoader(training_set, batch_size=batch_size, shuffle=True)
validation_loader = DataLoader(validation_set, batch_size=batch_size, shuffle=False)

# Create the model
input_size = input_data.shape[1]
output_size = 1

model = ANN.ANN(input_size, output_size, [256, 128, 64], ['tanh', 'tanh', 'tanh'])

# Train the model
model.train(training_loader, 500, 0.001)

# Predict the output on testing data
for input, target in validation_loader:
    pred = model.predict(input)
    print(f"Prediction: {pred}, Actual: {target}")

# print(f"Data pre-normalization: {input_data}")

# print(f"Input shape (pre-norm): {input_data.shape}")



# print(f"Data post-normalization: {input_data}")

# # Check input/target shapes
# print(f"Input shape (post-norm): {input_data.shape}")
# print(f"Target shape: {target_data.shape}")

# # Split the data into training and testing sets
# train_size = int(0.8 * len(input_data))
# # Take the first 80% of the data as the training set and the last 20% as the testing set
# train_input = input_data[:train_size]
# train_target = target_data[:train_size]

# test_input = input_data[train_size:]
# test_target = target_data[train_size:]

# # Create a model with the same number of inputs and outputs as the data
# input_size = input_data.shape[1]
# output_size = 1

# # Create the model
# model = ANN.ANN(input_size, output_size, [512, 256, 128, 64], ['relu', 'relu', 'relu', 'relu'])

# # Train the model
# model.train(train_input, train_target, 500, 2, 0.01)

# # Predict the output on testing data
# count = 0
# corr_pred = 0
# for input, target in zip(test_input, test_target):
#     pred = model.predict(input)
#     print(f"Prediction: {pred}, Actual: {target}")
#     if (pred >= 0.5 and target == 1) or (pred < 0.5 and target == 0):
#         corr_pred += 1
#     count += 1

# print(f"Correct predictions: {corr_pred}/{count} ({corr_pred/count*100}%)")


