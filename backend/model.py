import players
import numpy as np
import torch
import ANN

torch.set_printoptions(threshold=torch.inf)

#players.get_player_stats(1, 2023)

#print(players.get_stats_by_player(140, 2023))

league = 1
season = 2023

# Returns a dictionary of data for each game in a given league/season
# Dictionary in the format: {game_name: {'input': input_data, 'target': target_data}}
input_data, target_data = players.get_pytorch_data(league, season)

print(input_data, target_data)
print(input_data.shape)
print(target_data.shape)

# Create a model with the same number of inputs and outputs as the data
input_size = input_data.shape[1]
output_size = 1

# Create the model
model = ANN.ANN(input_size, output_size, 3, [32, 16, 8], [1, 1, 1])

# Train the model
model.train(input_data, target_data, 100, 10, 0.01)

# Predict the output
for input, target in zip(input_data, target_data):
    print(model.predict(input))
    print(target)

