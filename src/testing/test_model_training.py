import pytest
from src.model_training import train_model, evaluate_model
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def test_train_model():
    # Create a synthetic dataset for testing
    X, y = make_classification(n_samples=100, n_features=10, n_classes=5, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Ensure the model is trained
    assert model is not None, "Model should not be None after training"

def test_evaluate_model():
    # Create a synthetic dataset for testing
    X, y = make_classification(n_samples=100, n_features=10, n_classes=5, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    accuracy = evaluate_model(model, X_val, y_val)

    # Ensure the accuracy is a valid number
    assert isinstance(accuracy, float), "Accuracy should be a float"
    assert 0 <= accuracy <= 1, "Accuracy should be between 0 and 1"