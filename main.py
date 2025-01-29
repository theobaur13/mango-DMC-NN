import os
import pandas as pd
import numpy as np
from src.matrix import nn_matrix
from src.loop import single_layer_nn_loop, two_layer_nn_loop, two_layer_nn_loop_input_layer, two_layer_nn_loop_hidden_layer

# file_name = "test.csv"
file_name = "NAnderson2020MendeleyMangoNIRData.csv"
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

    # Single layer neural network
    prediction = nn_matrix(spectral_data, L=1)

    if prediction is not None:
        for i in range(3):
            print(f"Prediction: {prediction[i]}, Actual: {dry_matter[i]}")

if __name__ == "__main__":
    main()