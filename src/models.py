# Define a couple of models to train data for multi-level categorical dependent variable
import time
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler



home_dir = r"/Users/wrngnfreeman/Library/CloudStorage/OneDrive-Personal/shared_projects/Shelter Animal Outcomes/Shelter-Animal-Outcomes-by-kaggle.com"
sys.path.append(home_dir + r"/src")
import data_processing, feature_engineering, utils

data_file = r"train"



# Load and process training data
start_time = time.time()
processed_df = data_processing.process_data(
    home_dir=home_dir,
    data_file=data_file,
    AnimalID=r"AnimalID",
    dep_var=r"OutcomeType"
)
print("Data loaded in: {}".format(utils.calculate_elapsed_time(start_time)))

# Engineer features
start_time = time.time()
engineered_df = feature_engineering.engineer_features(
    df=processed_df,
    AnimalID=r"AnimalID",
    dep_var=r"OutcomeType"
)
print("Features engineered in: {}".format(utils.calculate_elapsed_time(start_time)))















# Multi-level Logistic Regression




# Random forest model
class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier()
    def fit(self, X, y):
        self.model.fit(X, y)
        return self
    def predict(self, X):
        return self.model.predict(X)
    def score(self, X, y):
        return accuracy_score(y, self.predict(X))
    def feature_importances_(self):
        return self.model.feature_importances_










# Artificial Nural Network (ANN) model
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Generate synthetic data for demonstration
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.long)

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
input_size = 20
hidden_size = 50
output_size = 2
model = SimpleNN(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training loop
num_epochs = 100
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
    print(f'Accuracy on test set: {accuracy:.2f}%')
