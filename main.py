import os
import pandas as pd
import numpy as np
from src.matrix import nn_matrix, init_weights, init_biases, backpropogation
from src.helper import squared_error, absolute_error

file_name = "test.csv"
# file_name = "NAnderson2020MendeleyMangoNIRData.csv"
data_path = os.path.join(os.path.dirname(__file__), "data", file_name)

def load_data(data_path):
    data = pd.read_csv(data_path)
    return data

def clean_data(data):
    # Drop columns that are not needed
    data = data.drop(columns=["Set","Season", "Region", "Date", "Type", "Cultivar", "Pop", "Temp"])
    dry_matter = data["DM"].to_numpy()
    spectral_data = data.drop(columns=["DM"]).to_numpy()
    
    dry_matter = dry_matter.reshape(-1, 1)

    return spectral_data, dry_matter

def main():
    # Load data
    data = load_data(data_path)
    spectral_data, dry_matter = clean_data(data)

    # Hyperparameters
    learning_rate = 0.01                        # Learning rate
    epochs = 1000                               # Number of epochs
    seed = 1                                    # Seed for random number generator
    L = 2                                       # Number of layers
    # U = [5, 8, 1]                             # Shape of neural network U
    U_limit = 4                                 # Upper limit for number of hidden layer neurons

    # Create random shape of neural network U
    np.random.seed(seed)
    U = np.random.randint(1, U_limit-1, L-1)    # Randomly initialise U in shape [U1, ..., UL-1] if rand_U is True
    U = np.append(U, 1)                         # Add 1 to the end of U to match the output layer
    print(f"U: {U}")

    # Initialise weights and biases
    weights = init_weights(spectral_data.shape[1], U, L, seed)
    biases = init_biases(U, L, seed)

    for epoch in range(epochs):
        # Forward pass
        prediction, activations = nn_matrix(spectral_data, U, L, weights, biases, seed)

        # Backpropogation
        weights, biases = backpropogation(dry_matter, prediction, activations, weights, biases, L, spectral_data, learning_rate)

        # Every 100 epochs, print the progress
        if epoch % 100 == 0:
            squared_error_value = squared_error(dry_matter, prediction)
            absolute_error_value = absolute_error(dry_matter, prediction)
            print(f"Epoch {epoch}: Squared Error = {squared_error_value}, Absolute Error = {absolute_error_value}")
    
    # Print prediction and actual values
    if prediction is not None:
        for i in range(3):
            print(f"Prediction: {prediction[i]}, Actual: {dry_matter[i]}")

    squared_error_value = squared_error(dry_matter, prediction)
    absolute_error_value = absolute_error(dry_matter, prediction)

    print(f"Squared error: {squared_error_value}")
    print(f"Absolute error: {absolute_error_value}")

if __name__ == "__main__":
    main()