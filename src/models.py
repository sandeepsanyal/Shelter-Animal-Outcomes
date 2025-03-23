# Define a couple of models to train data for multi-level categorical dependent variable
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

import torch
import torch.nn as nn
import torch.optim as optim


# Multi-level Logistic Regression
def logistic_regression_model(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID",
    dep_var: str=r"OutcomeType",
    seed: int=0,
    export_model_path: str=False
) -> LogisticRegression:
       
    X = df.drop(columns=[AnimalID, dep_var])
    y = df[dep_var]

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=seed
    )

    lrlm = LogisticRegression(max_iter=1000, random_state=seed)
    # Train the model
    lrlm.fit(X_train, y_train)
    
    # Validate the model
    y_pred = lrlm.predict(X_val)
    print("Classification Report\n{}".format(
        classification_report(
            y_val,
            y_pred,
            target_names=[
                'Adoption',
                'Return_to_owner',
                'Transfer',
                'Died',
                'Euthanasia'
            ]
        )
    ))
    print("Accuracy: {}".format(accuracy_score(y_val, y_pred)))

    # Save the trained model
    if export_model_path:
        joblib.dump(lrlm, export_model_path)


    return lrlm



# Random forest model
def random_forest_model(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID",
    dep_var: str=r"OutcomeType",
    seed: int=0,
    export_model_path: str=False
) -> RandomForestClassifier:

    """
    Train a Random Forest Classifier on the given dataset and evaluate its performance.

    This function accepts a DataFrame containing animal-related data, splits it into features 
    and target variable based on specified column names, trains a Random Forest model, evaluates 
    it using accuracy score and classification report, computes feature importances, and optionally 
    exports the trained model to a file.

    Parameters:
    ----------
    df : pd.DataFrame
        A DataFrame containing the data with at least two columns: one for animal IDs and one 
        for the outcome type (target variable).
    AnimalID : str, optional, default="AnimalID"
        The name of the column in `df` that contains unique identifiers for each animal.
    dep_var : str, optional, default="OutcomeType"
        The name of the column in `df` that represents the target variable for prediction.
    seed : int, optional, default=0
        A random state integer used to ensure reproducibility in model training and data splitting.
    export_model_path : str, optional, default=False
        If provided with a valid file path (string), the trained Random Forest model will be saved 
        to this location using joblib. If False or None, the model is not exported.

    Returns:
    -------
    RandomForestClassifier
        The trained Random Forest model fitted on the training data.

    Notes:
    -----
    - The function splits the input DataFrame into features (X) and target variable (y), then 
      further divides these into training and validation sets with an 80-20 split.
    - A Random Forest Classifier is initialized, trained, and evaluated using accuracy score and a
      classification report.
    - Feature importances are computed and printed in descending order to understand the contribution 
      of each feature to the model's predictions.

    Example:
    -------
    >>> import pandas as pd
    >>> df = pd.read_csv('animal_data.csv')
    >>> model = rf_model(df, AnimalID='ID', dep_var='Outcome', seed=42, export_model_path='rf_model.joblib')
    """

    X = df.drop(columns=[AnimalID, dep_var])
    y = df[dep_var]

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=seed)

    # Initialize the model
    rf_model = RandomForestClassifier(random_state=seed)

    # Train the model
    rf_model.fit(X_train, y_train)

    # Validate the model
    y_pred = rf_model.predict(X_val)
    print("Classification Report\n{}".format(
        classification_report(
            y_val,
            y_pred,
            target_names=[
                'Adoption',
                'Return_to_owner',
                'Transfer',
                'Died',
                'Euthanasia'
            ]
        )
    ))
    print("Accuracy: {}".format(accuracy_score(y_val, y_pred)))

    # Computer feature importances
    feature_importances = rf_model.feature_importances_
    feature_names = X.columns
    feature_importance_df = pd.DataFrame({"feature": feature_names, "importance": feature_importances})
    feature_importance_df = feature_importance_df.sort_values(by="importance", ascending=False)
    print("\nFeature Importances")
    display(feature_importance_df)

    # Save the trained model
    if export_model_path:
        joblib.dump(rf_model, export_model_path)
    

    return rf_model



# ANN model
def nn_model(
    df: pd.DataFrame,
    AnimalID: str,
    dep_var: str,
    seed: int = 0,
    export_model_path: str = None

):
    # Artificial Nural Network (ANN) model
    X = df.drop(columns=[AnimalID, dep_var])
    y = df[dep_var]

    # Split the data into training and validation sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=seed
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Convert data to PyTorch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train.to_numpy(), dtype=torch.long)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test.to_numpy(), dtype=torch.long)

    # Define the neural network architecture
    class SimpleNN(nn.Module):
        def __init__(self, input_size, hidden_size, output_size):
            super(SimpleNN, self).__init__()
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_size, output_size)

        def forward(self, x):
            out = self.fc1(x)
            out = self.relu(out)
            out = self.fc2(out)
            return out

    # Initialize the model, loss function, and optimizer
    input_size = 70
    hidden_size = 128
    output_size = 5
    model = SimpleNN(input_size, hidden_size, output_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # Training loop
    num_epochs = 1000
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # Evaluation
    model.eval()
    with torch.no_grad():
        predictions = model(X_test)
        _, predicted_classes = torch.max(predictions, 1)
        accuracy = (predicted_classes == y_test).sum().item() / len(y_test)

    # Classification Report
    print("Classification Report\n{}".format(
        classification_report(
            y_test,
            predicted_classes,
            target_names=[
                'Adoption',
                'Return_to_owner',
                'Transfer',
                'Died',
                'Euthanasia'
            ]
        )
    ))
    print("Accuracy: {}".format(accuracy_score(y_test, predicted_classes)))

    # Save the trained model
    if export_model_path:
        joblib.dump(nn_model, export_model_path)
    

    return nn_model
