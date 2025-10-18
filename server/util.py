import json
import os
import pickle
import numpy as np
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index=__data_columns.index(location.lower())
    except:
        loc_index=-1

    x=np.zeros(len(__data_columns))
    x[0]=sqft
    x[1]=bath
    x[2]=bhk
    if loc_index>=0:
        x[loc_index]=1

    return round(__model.predict([x])[0],2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns, __locations, __model

    base_dir = os.path.dirname(__file__)            # directory of util.py
    artifacts_dir = os.path.join(base_dir, "artifacts")
    cols_path = os.path.join(artifacts_dir, "columns.json")
    model_path = os.path.join(artifacts_dir, "bangalore_home_prices_model.pickle")

    # fail fast with helpful message
    if not os.path.exists(artifacts_dir):
        raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
    contents = os.listdir(artifacts_dir)
    if not os.path.exists(cols_path) or not os.path.exists(model_path):
        raise FileNotFoundError(f"Missing artifacts in {artifacts_dir}. Found: {contents}")

    with open(cols_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        # JSON might be {'data_columns': [...]} or just a list
        if isinstance(data, dict) and "data_columns" in data:
            __data_columns = data["data_columns"]
        elif isinstance(data, dict) and "columns" in data:
            __data_columns = data["columns"]
        elif isinstance(data, list):
            __data_columns = data
        else:
            raise ValueError("Unexpected format in columns.json")

    # assume first three columns are numeric features and rest are one-hot location columns
    __locations = [c for c in __data_columns[3:]]

    with open(model_path, "rb") as f:
        __model = pickle.load(f)

    print("Loading saved artifacts...done")
if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st phase jp nagar',1000,3,3))
    print(get_estimated_price('1st phase jp nagar', 1000,2,2))
    print(get_estimated_price('kalhalli', 1000, 2, 2))
    print(get_estimated_price('ejipura', 1000, 2, 2))
