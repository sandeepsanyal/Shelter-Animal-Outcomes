<h1>Animal Shelter Outcome Prediction</h1>
<h2>The project</h2>
<a href="https://www.kaggle.com/c/shelter-animal-outcomes">Shelter Animal Outcomes by kaggle.com</a>

<h2>Objective</h2>
This project aims to predict the outcome type of pets in an animal shelter based on various features such as animal type, age, breed, and color. The outcome type is a categorical variable with five levels.

<h2>The training data set</h2>
To get the data click <a href="https://www.kaggle.com/c/shelter-animal-outcomes/data">here</a> and sign up at <a href="kaggle.com">kaggle.com</a>.

Here's what the first few rows of the training set look like:

| AnimalID | Name    | DateTime            | OutcomeType       | OutcomeSubtype | AnimalType | SexuponOutcome   | AgeuponOutcome | Breed                      | Color      |
|----------|---------|---------------------|-------------------|----------------|------------|------------------|----------------|----------------------------|------------|
| A671945  | Hambone | 12-02-2014 18:22    | Return_to_owner   |                | Dog        | Neutered Male    | 1 year         | Shetland Sheepdog Mix      | Brown/White|
| A656520  | Emily   | 13-10-2013 12:44    | Euthanasia        | Suffering      | Cat        | Spayed Female    | 1 year         | Domestic Shorthair Mix     | Cream Tabby|
| A686464  | Pearce  | 31-01-2015 12:28    | Adoption          | Foster         | Dog        | Neutered Male    | 2 years        | Pit Bull Mix               | Blue/White |
| A683430  |         | 11-07-2014 19:09    | Transfer          | Partner        | Cat        | Intact Male      | 3 weeks        | Domestic Shorthair Mix     | Blue Cream |
| A667013  |         | 15-11-2013 12:52    | Transfer          | Partner        | Dog        | Neutered Male    | 2 years        | Lhasa Apso/Miniature Poodle| Tan        |


<h2>Project Structure</h2>

```
animal_shelter_outcome_prediction
├── data
│   ├── test.csv          # Dataset to predict on. Does not contain dependent variable.
│   ├── train.csv         # Training dataset containing both animal information and outcome types
│   └── sample_submission.csv  # Sample submission file format for model predictions
├── notebooks
│   ├── exploratory_analysis.ipynb  # Jupyter notebook used for performing exploratory data analysis on the datasets
│   └── prediction.ipynb            # Jupyter notebook for making predictions using the trained models
├── src
│   ├── data_processing.py  # Contains functions to load and preprocess datasets, such as cleaning and feature scaling
│   ├── feature_engineering.py  # Includes methods for creating new features from existing ones to improve model performance
│   ├── model_training.py    # Code dedicated to training machine learning models on the prepared dataset
│   ├── testing
│   │   ├── test_data_processing.py  # Unit tests for validating data processing functions
│   │   ├── test_feature_engineering.py  # Unit tests for ensuring feature engineering functions work correctly
│   │   └── test_model_training.py  # Unit tests to check the model training process and outcomes
│   └── model_prediction.py   # Contains functions designed for making predictions on new or unseen datasets using trained models
├── pickle_files
│   ├── rf_model.pkl        # Pickled Random Forest model saved after training, ready for deployment or prediction
├── requirements.txt          # Lists all the required Python packages and their versions needed to run the project
└── README.md                 # Main documentation file providing an overview of the project, setup instructions, and usage guidelines
```

<h2>Setup Instructions</h2>

1. Clone the repository:
   ```bash
   git clone https://github.com/sandeepsanyal/Shelter-Animal-Outcomes-by-kaggle.com.git
   cd animal_shelter_outcome_prediction
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```