# import tables from the sqlite3 to pandas

sharepoint_path = r"/Users/wrngnfreeman"

# import libraries
import numpy as np
import pandas as pd
import sqlite3

# create a connection to the database
conn = sqlite3.connect(sharepoint_path + r"/Library/CloudStorage/OneDrive-Personal/shared_projects/sql_databases/shelter_animal_outcomes.db")

# create a cursor object
cur = conn.cursor()

# get the table names
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
tables = [table[0] for table in tables] # convert to list of strings

# create a dictionary of tables
tables_dict = {}
for table in tables:
    tables_dict[table] = pd.read_sql_query("SELECT * from " + table, conn)

# close the connection
conn.close()

# merge the tables
processed_df = pd.merge(
    left=tables_dict["coat_pattern"],
    right=pd.merge(
        left=tables_dict["coat_color"],
        right=pd.merge(
            left=tables_dict["breed_mix"],
            right=pd.merge(
                left=tables_dict["breed_type"],
                right=tables_dict["animal_data"],
                how="right",
                left_on=["AnimalID"],
                right_on=["AnimalID"]
            ),
            how="right",
            left_on=["AnimalID"],
            right_on=["AnimalID"]
        ),
        how="right",
        left_on=["AnimalID"],
        right_on=["AnimalID"]
    ),
    how="right",
    left_on=["AnimalID"],
    right_on=["AnimalID"]
)

# if the animal is a cat, then the "BreedType" is the "Breed"
processed_df.loc[processed_df["AnimalType"] == "Cat", "BreedType"] = processed_df.loc[processed_df["AnimalType"] == "Cat", "Breed"]

# selecting relevant columns
processed_df = processed_df[
    [
        "AnimalID",
        "OutcomeType",
        "AnimalType",
        "Sex",
        "AgeGroup",
        "SterilizationType",
        "BreedType",
        "MixType",
        "CoatColor",
        "CoatPattern"
    ]
]

# Replace all '' with np.nan
processed_df.replace("", np.nan, inplace=True)

# Creating dummy variables
## OutcomeType
train_df = pd.concat([processed_df, pd.get_dummies(processed_df["OutcomeType"], dtype=int, dummy_na=True, prefix="OutcomeType")], axis=1)
train_df.drop(["OutcomeType"], axis=1, inplace=True)
## AnimalType
train_df = pd.concat([train_df, pd.get_dummies(train_df["AnimalType"], dtype=int, dummy_na=True, prefix="AnimalType")], axis=1)
train_df.drop(["AnimalType", "AnimalType_Dog", "AnimalType_nan"], axis=1, inplace=True)
## Sex
train_df = pd.concat([train_df, pd.get_dummies(train_df["Sex"], dtype=int, dummy_na=True, prefix="Sex")], axis=1)
train_df.drop(["Sex", "Sex_Male", "Sex_nan"], axis=1, inplace=True)
## AgeGroup
train_df = pd.concat([train_df, pd.get_dummies(train_df["AgeGroup"], dtype=int, dummy_na=True, prefix="AgeGroup")], axis=1)
train_df.drop(["AgeGroup", "AgeGroup_< 5 years", "AgeGroup_nan"], axis=1, inplace=True)
## SterilizationType
train_df = pd.concat([train_df, pd.get_dummies(train_df["SterilizationType"], dtype=int, dummy_na=True, prefix="SterilizationType")], axis=1)
train_df.drop(["SterilizationType", "SterilizationType_Intact", "SterilizationType_nan"], axis=1, inplace=True)
## BreedType
train_df = pd.concat([train_df, pd.get_dummies(train_df["BreedType"], dtype=int, dummy_na=True, prefix="BreedType")], axis=1)
train_df.drop(["BreedType", "BreedType_nan"], axis=1, inplace=True)
## MixType
train_df = pd.concat([train_df, pd.get_dummies(train_df["MixType"], dtype=int, dummy_na=True, prefix="MixType")], axis=1)
train_df.drop(["MixType", "MixType_Pure breed", "MixType_nan"], axis=1, inplace=True)
## CoatColor
train_df = pd.concat([train_df, pd.get_dummies(train_df["CoatColor"], dtype=int, dummy_na=True, prefix="CoatColor")], axis=1)
train_df.drop(["CoatColor", "CoatColor_White", "CoatColor_nan"], axis=1, inplace=True)
## CoatPattern
train_df = pd.concat([train_df, pd.get_dummies(train_df["CoatPattern"], dtype=int, dummy_na=True, prefix="CoatPattern")], axis=1)
train_df.drop(["CoatPattern", "CoatPattern_nan"], axis=1, inplace=True)


# Model development
id_var = "AnimalID"
dep_var = "OutcomeType"
indep_vars = [
    "AnimalType_Cat",
    "Sex_Female",
    "AgeGroup_< 1 week",
    "AgeGroup_< 1 month",
    "AgeGroup_< 6 months",
    "AgeGroup_< 1 year",
    "AgeGroup_< 10 years",
    "AgeGroup_< 15 years",
    "AgeGroup_>= 15 years",
    "SterilizationType_Sterilized",
    "MixType_Mix",
    "BreedType_Domestic Shorthair",
    "BreedType_Domestic Medium Hair",
    "BreedType_Domestic Longhair",
    "BreedType_Herding",
    "BreedType_Himalayan",
    "BreedType_Hound",
    "BreedType_Maine Coon",
    "BreedType_Manx",
    "BreedType_Non-Sporting",
    "BreedType_Persian",
    "BreedType_Russian Blue",
    "BreedType_Siamese",
    "BreedType_Snowshoe",
    "BreedType_Sporting",
    "BreedType_Terrier",
    "BreedType_Toy",
    "BreedType_Working",
    "CoatColor_Black",
    "CoatColor_Brown",
    "CoatColor_Calico",
    "CoatColor_Chocolate",
    "CoatColor_Cream",
    "CoatColor_Fawn",
    "CoatColor_Gray",
    "CoatColor_Lilac",
    "CoatColor_Liver",
    "CoatColor_Lynx",
    "CoatColor_Orange",
    "CoatColor_Red",
    "CoatColor_Sable",
    "CoatColor_Seal",
    "CoatColor_Torbie",
    "CoatColor_Tortie",
    "CoatColor_Tricolor",
    "CoatColor_Yellow",
    "CoatPattern_Brindle",
    "CoatPattern_Merle",
    "CoatPattern_Point",
    "CoatPattern_Smoke",
    "CoatPattern_Tabby",
    "CoatPattern_Tick",
    "CoatPattern_Tiger"
]

# Random forest model




import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

age_order = [
    '< 1 week',
    '< 1 month',
    '< 6 months',
    '< 1 year',
    '< 5 years',
    '< 10 years',
    '< 15 years',
    '>= 15 years'
]
# Plotting
plt.figure(figsize=(10, 6))
sns.countplot(data=processed_df, x='AgeGroup', hue='OutcomeType', palette='Set3', order=age_order)

# Adding titles and labels
plt.title('Relationship Between Age and Outcome Type')
plt.xlabel('AgeGroup')
plt.ylabel('Count')

# Show legend
plt.legend(title='Outcome Type', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
plt.tight_layout()
plt.show()




# Association check
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

# Function to calculate Cramér's V
def cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2, _, _, _ = chi2_contingency(contingency_table)
    
    # Number of observations
    n = contingency_table.sum().sum()
    
    # Calculate phi coefficient
    phi2 = chi2 / n
    
    # Minimum dimension for normalization
    r, k = contingency_table.shape
    min_dim = min(r - 1, k - 1)
    
    # Cramér's V
    return np.sqrt(phi2 / min_dim)


variables = [
    'OutcomeType',
    'AnimalType',
    'Sex',
    'AgeGroup',
    'SterilizationType',
    'BreedType',
    'MixType',
    'CoatColor',
    'CoatPattern'
]

# Create a DataFrame to store Cramér's V values
cramers_v_matrix = pd.DataFrame(index=variables, columns=variables)

# Compute Cramér's V for each pair of variables
for var1 in variables:
    for var2 in variables:
        cramers_v_matrix.loc[var1, var2] = cramers_v(processed_df[var1], processed_df[var2])

# Plotting the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(cramers_v_matrix.astype(float), annot=True, cmap='coolwarm', center=0,
            cbar_kws={'label': "Cramér's V"}, vmin=0, vmax=1)
plt.title('Correlation Heatmap (Cramér\'s V)')
plt.show()