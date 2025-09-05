import sys
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def logistic_regression_model(
    df: pd.DataFrame,
    AnimalID: str = r"AnimalID",
    dep_var: str = r"OutcomeType",
    seed: int = 0,
    export_model_path: str = False
) -> LogisticRegression:
    """
    Train a Logistic Regression model for multi-class classification.

    Parameters:
    ----------
    df : pd.DataFrame
        Input DataFrame containing features and target variable.
    AnimalID : str, optional
        Name of the column containing animal identifiers. Default: "AnimalID".
    dep_var : str, optional
        Name of the column containing the target variable (outcome type). Default: "OutcomeType".
    seed : int, optional
        Random state for reproducibility. Default: 0.
    export_model_path : str, optional
        File path to save the trained model using joblib. Default: False (no export).

    Returns:
    -------
    LogisticRegression - A trained logistic regression model.

    Notes:
    -----
    - Drops the `AnimalID` and `dep_var` columns to create features (X).
    - Splits data into 80% training and 20% validation.
    - Outputs classification report and accuracy score.
    - Model is saved if `export_model_path` is provided.
    """
    X = df.drop(columns=[AnimalID, dep_var])
    y = df[dep_var]

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=seed
    )

    lrlm = LogisticRegression(max_iter=1000, random_state=seed)
    lrlm.fit(X_train, y_train)

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
    print("Logistic Regression Model Accuracy: {}".format(accuracy_score(y_val, y_pred)))

    if export_model_path:
        joblib.dump(lrlm, export_model_path)

    return lrlm


def random_forest_model(
    df: pd.DataFrame,
    AnimalID: str = r"AnimalID",
    dep_var: str = r"OutcomeType",
    seed: int = 0,
    export_model_path: str = False
) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier for multi-class classification.

    Parameters:
    ----------
    df : pd.DataFrame
        Input DataFrame containing features and target variable.
    AnimalID : str, optional
        Name of the column containing animal identifiers. Default: "AnimalID".
    dep_var : str, optional
        Name of the column containing the target variable (outcome type). Default: "OutcomeType".
    seed : int, optional
        Random state for reproducibility. Default: 0.
    export_model_path : str, optional
        File path to save the trained model using joblib. Default: False (no export).

    Returns:
    -------
    RandomForestClassifier - A trained random forest model.

    Notes:
    -----
    - Drops the `AnimalID` and `dep_var` columns to create features (X).
    - Splits data into 80% training and 20% validation.
    - Outputs classification report, accuracy score, and feature importances.
    - Model is saved if `export_model_path` is provided.
    """
    X = df.drop(columns=[AnimalID, dep_var])
    y = df[dep_var]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=seed)

    rf_model = RandomForestClassifier(random_state=seed)
    rf_model.fit(X_train, y_train)

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
    print("Random Forest Model Accuracy: {}".format(accuracy_score(y_val, y_pred)))

    feature_importances = rf_model.feature_importances_
    feature_names = X.columns
    feature_importance_df = pd.DataFrame({"feature": feature_names, "importance": feature_importances})
    feature_importance_df = feature_importance_df.sort_values(by="importance", ascending=False)
    print("\nFeature Importances")
    display(feature_importance_df)

    if export_model_path:
        joblib.dump(rf_model, export_model_path)

    return rf_model


def xg_boost(
    home_dir: str,
    df: pd.DataFrame,
    AnimalID: str = r"AnimalID",
    dep_var: str = r"OutcomeType",
    seed: int = 0,
    export_model_path: str = None
):
    """
    Train an XGBoost Classifier for multi-class classification.

    Parameters:
    ----------
    home_dir : str
        Path to the project directory (for importing utils).
    df : pd.DataFrame
        Input DataFrame containing features and target variable.
    AnimalID : str, optional
        Name of the column containing animal identifiers. Default: "AnimalID".
    dep_var : str, optional
        Name of the column containing the target variable (outcome type). Default: "OutcomeType".
    seed : int, optional
        Random state for reproducibility. Default: 0.
    export_model_path : str, optional
        File path to save the trained model using joblib. Default: None (no export).

    Returns:
    -------
    XGBClassifier - A trained XGBoost model.

    Notes:
    -----
    - Cleans feature names using `utils.clean_feature_name`.
    - Drops the `AnimalID` and `dep_var` columns to create features (X).
    - Splits data into 80% training and 20% validation.
    - Outputs classification report and accuracy score.
    - Model is saved if `export_model_path` is provided.
    """
    sys.path.append(home_dir + r"/src")
    import utils

    cleaned_feature_names = [utils.clean_feature_name(name) for name in df.columns.values.tolist()]
    df.columns = cleaned_feature_names

    X = df.drop(columns=[AnimalID, dep_var])
    y = np.array(df[dep_var])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', seed=seed)
    xgb_model.fit(X_train, y_train)

    predicted_classes = xgb_model.predict(X_test)
    accuracy = accuracy_score(y_test, predicted_classes)

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
    print("XGBoost Model Accuracy: {}".format(accuracy))

    if export_model_path:
        joblib.dump(xgb_model, export_model_path)

    return xgb_model
