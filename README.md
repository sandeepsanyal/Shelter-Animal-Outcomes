<h1>Animal Shelter Outcome Prediction</h1>
<h2>The project</h2>
<a href="https://www.kaggle.com/c/shelter-animal-outcomes">https://www.kaggle.com/c/shelter-animal-outcomes</a>

<h2>Ojbective</h2>
This project aims to predict the outcome type of pets in an animal shelter based on various features such as animal type, age, breed, and color. The outcome type is a categorical variable with five levels.

<h2>The training data set</h2>
To get the data click <a href="https://www.kaggle.com/c/shelter-animal-outcomes/data">here</a> and sign up at kaggle.com.

<p>Here's what the first few rows of the training set look like:</p>
<table class="table">
  <thead>
    <tr style="text-align: right;">
      <th>AnimalID</th>
      <th>Name</th>
      <th>DateTime</th>
      <th>OutcomeType</th>
      <th>OutcomeSubtype</th>
      <th>AnimalType</th>
      <th>SexuponOutcome</th>
      <th>AgeuponOutcome</th>
      <th>Breed</th>
      <th>Color</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A671945</th>
      <td>Hambone</td>
      <td>12-02-2014 18:22</td>
      <td>Return_to_owner</td>
      <td></td>
      <td>Dog</td>
      <td>Neutered Male</td>
      <td>1 year</td>
      <td>Shetland Sheepdog Mix</td>
      <td>Brown/White</td>
    </tr>
    <tr>
      <th>A656520</th>
      <td>Emily</td>
      <td>13-10-2013 12:44</td>
      <td>Euthanasia</td>
      <td>Suffering</td>
      <td>Cat</td>
      <td>Spayed Female</td>
      <td>1 year</td>
      <td>Domestic Shorthair Mix</td>
      <td>Cream Tabby</td>
    </tr>
    <tr>
      <th>A686464</th>
      <td>Pearce</td>
      <td>31-01-2015 12:28</td>
      <td>Adoption</td>
      <td>Foster</td>
      <td>Dog</td>
      <td>Neutered Male</td>
      <td>2 years</td>
      <td>Pit Bull Mix</td>
      <td>Blue/White</td>
    </tr>
    <tr>
      <th>A683430</th>
      <td></td>
      <td>11-07-2014 19:09</td>
      <td>Transfer</td>
      <td>Partner</td>
      <td>Cat</td>
      <td>Intact Male</td>
      <td>3 weeks</td>
      <td>Domestic Shorthair Mix</td>
      <td>Blue Cream</td>
    </tr>
    <tr>
      <th>A667013</th>
      <td></td>
      <td>15-11-2013 12:52</td>
      <td>Transfer</td>
      <td>Partner</td>
      <td>Dog</td>
      <td>Neutered Male</td>
      <td>2 years</td>
      <td>Lhasa Apso/Miniature Poodle</td>
      <td>Tan</td>
    </tr>
  </tbody>
</table>


<h2>Project Structure</h2>

```
animal_shelter_outcome_prediction
├── data
│   ├── test.csv          # Test dataset with animal information
│   ├── train.csv         # Training dataset with animal information and outcome types
├── notebooks
│   └── exploratory_analysis.ipynb  # Jupyter notebook for exploratory data analysis
├── src
│   ├── data_processing.py  # Functions for loading and preprocessing datasets
│   ├── feature_engineering.py  # Functions for feature engineering
│   ├── model_training.py    # Code for training machine learning models
│   ├── testing
│   │   ├── test_data_processing.py  # Unit tests for data processing functions
│   │   ├── test_feature_engineering.py  # Unit tests for feature engineering functions
│   │   ├── test_model_training.py  # Unit tests for model training functions
│   ├── model_prediction.py   # Functions for making predictions on new datasets
│   ├── utils.py              # Utility functions used across different modules
├── requirements.txt          # Required Python packages and their versions
└── README.md                 # Documentation for the project
```

<h2>Setup Instructions</h2>
<ol type="1">
  <l1>Clone the repository:<br>
    <code>
      git clone <a href=https://github.com/sandeepsanyal/Shelter-Animal-Outcomes-by-kaggle.com.git>https://github.com/sandeepsanyal/Shelter-Animal-Outcomes-by-kaggle.com.git</a><br>
      cd animal_shelter_outcome_prediction<br>
    </code>
  </li>
  <l1>Install the required packages:<br>
    <code>pip install -r requirements.txt</code>
  </li>
</ol>
