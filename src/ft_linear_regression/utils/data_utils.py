import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError


BASE_DIR = Path(__file__).resolve().parent.parent.parent
JSON_PATH = BASE_DIR / "data" / "parameters.json"
CSV_PATH = BASE_DIR / "data" / "data.csv"

class Parameters(BaseModel):
    theta0: float
    theta1: float
    loss: list[float]

def create_default_json(file_path):
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            default_params = {"theta0": 0.0, "theta1": 0.0, "loss": []}
            with open(file_path, 'w') as f:
                json.dump(default_params, f)
            print(f"Created {file_path} with default values.")
    except (IOError, PermissionError) as e:
        raise PermissionError(f"Error creating or accessing {file_path}: {e}")


def load_parameters_from_json():
    """Load and validate the JSON file using Pydantic."""
    try:
        with open(JSON_PATH, 'r') as f:
            parameters_data = json.load(f)
        
        parameters = Parameters(**parameters_data)
        return parameters

    except FileNotFoundError:
        create_default_json(JSON_PATH)
        load_parameters_from_json()
    except ValidationError:
        raise ValueError("Corrupted parameters file")
    except json.JSONDecodeError:
        print('race avoided')
        return load_parameters_from_json()

def modify_json_parameters(new_theta0, new_theta1, loss) -> None:
    new_data = {
        "theta0": new_theta0,
        "theta1": new_theta1,
        "loss": loss
    }
    try:
        # Save the updated JSON back to the file
        with open(JSON_PATH, 'w') as f:
            json.dump(new_data, f, indent=4)

    except FileNotFoundError:
        create_default_json(JSON_PATH)
        modify_json_parameters(new_theta0, new_theta1, loss)

def load_normalized_data():
    data = load_data_from_csv()
    return normalize_data(data)

def load_data_from_csv():
    try:
        data = pd.read_csv(CSV_PATH)
        if data.size == 0:
            raise ValueError("CSV file is empty")
        if data.shape[1] != 2:
            raise ValueError("CSV should contain exactly two columns")
        return data 

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {CSV_PATH}")
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {str(e)}")

def normalize_data(data):
    """Normalize data using Z-score """
    data.meanX = data["km"].mean()
    data.stdX = data["km"].std()
    data.meanY = data["price"].mean()
    data.stdY = data["price"].std()
    data["x_normalized"] = (data["km"] - data.meanX) / data.stdX
    data["y_normalized"] = (data["price"] - data.meanY) / data.stdY
    return data

def denormalize_parameters(theta0, theta1, data):
    denormalized_theta0 = data.meanY + theta0 * data.stdY - (theta1 * data.stdY * data.meanX) / data.stdX
    denormalized_theta1 = (theta1 * data.stdY) / data.stdX

    return (denormalized_theta0, denormalized_theta1)