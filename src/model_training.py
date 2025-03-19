from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import joblib

def train_model(train_data_path):
    # Load the training data
    data = pd.read_csv(train_data_path)

    # Preprocess the data (this should be done in the data_processing module)
    # For demonstration, let's assume the preprocessing is done here
    X = data.drop(columns=['OutcomeType'])
    y = data['OutcomeType']

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Validate the model
    y_pred = model.predict(X_val)
    print(classification_report(y_val, y_pred))
    print(f'Accuracy: {accuracy_score(y_val, y_pred)}')

    # Save the trained model
    joblib.dump(model, 'animal_shelter_model.pkl')

if __name__ == "__main__":
    train_model('../data/train.csv')