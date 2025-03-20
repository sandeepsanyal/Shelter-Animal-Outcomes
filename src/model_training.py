from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import joblib
import sys


def train_model(
        file_path: str,
        code_modules_path: str,
        AnimalID: str=r"AnimalID",
        dep_var: str=r"OutcomeType",
        export_model_path: str=False
    ):
    """
    Trains a Random Forest model using data processed and feature-engineered from the provided dataset.

    This function orchestrates the loading, processing, and engineering of features for training a 
    Random Forest classifier. It evaluates the model's performance on validation data and optionally 
    exports the trained model to a specified path.

    Parameters:
    file_path (str): The path to the CSV file containing the raw dataset.
    codes_folder_path (str): The directory path where additional code modules ('data_processing' and 'feature_engineering') are located.
    AnimalID (str, optional): Column name used for identifying individual animals in the dataset. Defaults to "AnimalID".
    dep_var (str, optional): The target variable column name indicating the outcome type for prediction. Defaults to "OutcomeType".
    export_model_path (str, optional): File path where the trained model should be saved as a .joblib file. If False or None, the model is not exported.

    Returns:
    RandomForestClassifier: The trained Random Forest classifier model.
    
    Workflow Overview:

    1. Append `codes_folder_path` to `sys.path` to ensure custom modules are accessible.
    2. Import necessary modules for data processing and feature engineering from the specified path.
    3. Load and preprocess the dataset using the `process_data` function.
    4. Engineer features with the `engineer_features` function.
    5. Split processed and engineered data into training and validation sets.
    6. Initialize a Random Forest classifier model.
    7. Train the model on the training set.
    8. Validate the model using the validation set, printing out classification report and accuracy score.
    9. Compute and display feature importances from the trained model.
    10. Optionally save the model to `export_model_path` using joblib if a path is provided.

    Example Usage:
        model = train_model(
            file_path='path/to/dataset.csv',
            codes_folder_path='path/to/code/modules',
            export_model_path='path/to/save/model.joblib'
        )
    
    Note: Ensure that the `data_processing` and `feature_engineering` modules contain 
          compatible functions as used within this method.
    """

    sys.path.append(code_modules_path)
    import data_processing, feature_engineering

    # Load and process training data
    processed_df = data_processing.process_data(
        file_path=file_path,
        AnimalID=r"AnimalID",
        dep_var=r"OutcomeType"
    )

    # Engineer features
    engineered_df = feature_engineering.engineer_features(
        df=processed_df,
        AnimalID=r"AnimalID",
        dep_var=r"OutcomeType"
    )


    # Preprocess the data (this should be done in the data_processing module)
    # For demonstration, let's assume the preprocessing is done here
    X = engineered_df.drop(columns=[AnimalID, dep_var])
    y = engineered_df["OutcomeType"]

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Validate the model
    y_pred = model.predict(X_val)
    print("Classification Report\n{}".format((classification_report(y_val, y_pred))))
    print("Accuracy: {}".format(accuracy_score(y_val, y_pred)))


    # Computer feature importances
    feature_importances = model.feature_importances_
    feature_names = X.columns
    feature_importance_df = pd.DataFrame({"feature": feature_names, "importance": feature_importances})
    feature_importance_df = feature_importance_df.sort_values(by="importance", ascending=False)
    print("\nFeature Importances")
    display(feature_importance_df)

    # Save the trained model
    if export_model_path:
        joblib.dump(model, export_model_path)

    return model
