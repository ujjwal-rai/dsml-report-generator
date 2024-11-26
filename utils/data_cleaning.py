import pandas as pd
import json

def clean_data(dataset_path, feature_path):
    data = pd.read_csv(dataset_path)
    with open(feature_path) as f:
        features = json.load(f)
        
    # Convert columns based on feature descriptions
    for column, dtype in features.items():
        if dtype == 'int':
            data[column] = pd.to_numeric(data[column], errors='coerce').fillna(0).astype(int)
        elif dtype == 'float':
            data[column] = pd.to_numeric(data[column], errors='coerce').fillna(0.0)
        elif dtype == 'category':
            data[column] = data[column].astype('category')
    
    # Handle missing values and drop unnecessary columns
    data.dropna(inplace=True)
    data = data[[col for col in features if features[col]["useful"]]]
    
    return data
