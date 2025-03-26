import sys


home_dir = r"/Users/wrngnfreeman/Library/CloudStorage/OneDrive-Personal/shared_projects/Shelter Animal Outcomes/Shelter-Animal-Outcomes"
data_file = r"train"
AnimalID=r"AnimalID"
dep_var=r"OutcomeType"
seed=42

# import required modules
sys.path.append(home_dir + r"/src")
import data_processing, feature_engineering, models, utils

# Load and process training data
processed_df = data_processing.process_data(
    home_dir=home_dir,
    data_file=data_file,
    AnimalID=AnimalID,
    dep_var=dep_var
)
# Engineer features
engineered_df = feature_engineering.engineer_features(
    df=processed_df,
    AnimalID=AnimalID,
    dep_var=dep_var
)


# Model development
## Multinomial Logistic Regression model
models.logistic_regression_model(
    df=engineered_df,
    AnimalID=r"AnimalID",
    dep_var=r"OutcomeType",
    seed=seed
)
## Random Forest model
models.random_forest_model(
    df=engineered_df,
    AnimalID=r"AnimalID",
    dep_var=r"OutcomeType",
    seed=seed
)
## XGBoost
models.xg_boost(
    home_dir=home_dir,
    df=engineered_df,
    AnimalID=r"AnimalID",
    dep_var=r"OutcomeType",
    seed=seed
)






# Artificial Nural Network (ANN) model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

import torch
import torch.nn as nn
import torch.optim as optim

X = engineered_df.drop(columns=[AnimalID, dep_var])
y = engineered_df[dep_var]

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
print("ANN Model Accuracy: {}".format(accuracy))

