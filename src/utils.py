def log_message(message):
    """Logs a message to the console."""
    print(f"[LOG] {message}")

def load_config(config_file):
    """Loads configuration settings from a JSON file."""
    import json
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def save_model(model, filename):
    """Saves a trained model to a file."""
    import joblib
    joblib.dump(model, filename)

def load_model(filename):
    """Loads a trained model from a file."""
    import joblib
    return joblib.load(filename)

def encode_categorical(data, columns):
    """Encodes categorical variables using one-hot encoding."""
    return pd.get_dummies(data, columns=columns, drop_first=True)