<h1>Animal Shelter Outcome Prediction</h1>

<h2>Objective</h2>
This project aims to predict the outcome type of pets in Austin Animal Shelter based on various features such as animal type, age, breed, and color. The outcome type is a categorical variable with five levels.

<h2>The training data set</h2>
Dataset is downloaded from the city of Austin open data portal. To get the data click <a href="https://data.austintexas.gov/browse?q=austin+animal+center&sortBy=relevance&page=1&pageSize=20">here</a>.

Here's what few rows of the dataset look like:

| AnimalID | Name    | DateTime            | OutcomeType       | OutcomeSubtype | AnimalType | SexuponOutcome   | AgeuponOutcome | Breed                      | Color      |
|----------|---------|---------------------|-------------------|----------------|------------|------------------|----------------|----------------------------|------------|
| A671945  | Hambone | 12-02-2014 18:22    | Return_to_owner   |                | Dog        | Neutered Male    | 1 year         | Shetland Sheepdog Mix      | Brown/White|
| A656520  | Emily   | 13-10-2013 12:44    | Euthanasia        | Suffering      | Cat        | Spayed Female    | 1 year         | Domestic Shorthair Mix     | Cream Tabby|
| A686464  | Pearce  | 31-01-2015 12:28    | Adoption          | Foster         | Dog        | Neutered Male    | 2 years        | Pit Bull Mix               | Blue/White |
| A683430  |         | 11-07-2014 19:09    | Transfer          | Partner        | Cat        | Intact Male      | 3 weeks        | Domestic Shorthair Mix     | Blue Cream |
| A667013  |         | 15-11-2013 12:52    | Transfer          | Partner        | Dog        | Neutered Male    | 2 years        | Lhasa Apso/Miniature Poodle| Tan        |


<h2>Project Structure</h2>

```
Shelter-Animal-Outcomes/
├── requirements.txt          # Lists all the required Python packages and their versions needed to run the project
├── README.md                 # Main documentation file providing an overview of the project, setup instructions, and usage guidelines
├── data/                     # Directory containing datasets used in the project
│   └── Austin_Animal_Center_Outcomes_20250318.csv  # Dataset from Austin Animal Center Outcomes
├── notebooks/
│   ├── exploratory_analysis.ipynb  # Jupyter notebook used for performing exploratory data analysis on the datasets
│   └── prediction.ipynb            # Jupyter notebook for making predictions using the trained models
└── src/                        # Source code directory containing modules and scripts
    ├── feature_engineering.py  # Functions for creating new features from existing ones to improve model performance
    ├── models.py               # Definitions of machine learning models used in the project
    ├── model_training.py       # Scripts dedicated to training machine learning models on the prepared dataset
    ├── utils.py                # Utility functions used across the project, such as logging and configuration management
    ├── data_processing.py      # Functions to load and preprocess datasets, including cleaning and collation
    ├── model_prediction.py     # Functions designed for making predictions on new or unseen datasets using trained models
    ├── tableau_data.py         # Code for preparing data to be used in Tableau visualizations
    └── viz.py                  # Code for creating visualizations using libraries like Matplotlib or Seaborn
    └── testing/                # Directory containing unit tests for the project's modules
        ├── test_data_processing.py  # Unit tests for validating data processing functions
        ├── test_feature_engineering.py  # Unit tests for ensuring feature engineering functions work correctly
        └── test_model_training.py     # Unit tests to check the model training process and outcomes
```

<h2>Setup Instructions</h2>

1. Clone the repository:
   ```bash
   git clone https://github.com/sandeepsanyal/Shelter-Animal-Outcomes.git
   cd animal_shelter_outcome_prediction
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

<h2>Tableau Dashboard</h2>
Explore our interactive Tableau Dashboard to delve deeper into the dataset. This tool provides a user-friendly interface for detailed analysis.

[Interactive Tableau Dashboard (link 1)](https://public.tableau.com/views/InteractivePetManagementDashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) <br>
[Interactive Tableau Dashboard (link 2)](https://public.tableau.com/views/InteractivePetManagementDashboard_17435387085530/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
