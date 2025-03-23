import pandas as pd

def encode_categorical_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes categorical variables in a DataFrame into numeric and dummy-encoded formats.

    This function processes specific categorical columns within the input DataFrame by mapping their values 
    to numeric codes or creating dummy/indicator variables. It also manages the inclusion of NaN categories 
    where applicable and ensures certain original or redundant columns are dropped after encoding.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing data with categorical features that need encoding.

    Returns:
    pandas.DataFrame: A new DataFrame with encoded categorical variables, retaining only relevant transformed data.
    
    Process Overview:
    1. Maps specific values in the 'OutcomeType' column to predefined numeric codes and creates a new 'OutcomeCode' column.
    2. Generates dummy variables for specified columns such as "AnimalType", "SexuponOutcome", "AgeuponOutcome",
       "Sterilization", "BreedType", "Mix", "CoatColor", and "CoatPattern". These are prefixed accordingly 
       to differentiate them from other potential dummies.
    3. Drops the original categorical columns and certain dummy variables that may be redundant or unnecessary, 
       specifically keeping only informative or unique indicators for analysis.
    
    Example usage:
        encoded_df = encode_categorical_variables(input_data)
        
    Assumptions:
    - It is designed to handle NaN values appropriately by creating a dummy variable for them if they exist.
    """
    
    # Mapping specific categorical values to numeric codes
    outcome_type_mapping = {
        'Adoption': 1,
        'Return_to_owner': 2,
        'Transfer': 3,
        'Died': 4,
        'Euthanasia': 5
    }
    
    # Check if 'OutcomeType' column exists in the DataFrame before proceeding
    if "OutcomeType" in df.columns:
        df['OutcomeType'] = df['OutcomeType'].map(outcome_type_mapping)
    else:
        pass
    
    # Creating dummy variables for specified categorical columns
    columns_with_prefixes = [
        ("AnimalType", "AnimalType"),
        ("SexuponOutcome", "Sex"),
        ("AgeuponOutcome", "Age"),
        ("Sterilization", "Sterilization"),
        ("BreedType", "BreedType"),
        ("Mix", "Mix"),
        ("CoatColor", "CoatColor"),
        ("CoatPattern", "CoatPattern")
    ]
    
    for column, prefix in columns_with_prefixes:
        dummies = pd.get_dummies(df[column], dtype=int, dummy_na=True, prefix=prefix, prefix_sep="_")
        df = pd.concat([df, dummies], axis=1)
    
    # Drop original and certain dummy columns
    columns_to_drop = [
        ["AnimalType", "AnimalType_Dog", "AnimalType_nan"],
        ["Sex", "Sex_Male", "Sex_nan"],
        ["AgeuponOutcome", "Age_< 5 years", "Age_nan"],
        ["SterilizationType", "Sterilization_Intact", "Sterilization_nan"],
        ["BreedType", "BreedType_nan"],
        ["Mix", "Mix_Pure breed", "Mix_nan"],
        ["CoatColor", "CoatColor_White", "CoatColor_nan"],
        ["CoatPattern", "CoatPattern_nan"]
    ]
    
    for column_group in columns_to_drop:
        existing_columns = [col for col in column_group if col in df.columns]
        if existing_columns:  # Proceed only if there are existing columns to drop
            df.drop(existing_columns, axis=1, inplace=True)
    

    return df


def select_features(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID",
    dep_var: str=r"OutcomeType"
) -> pd.DataFrame:
    """
    Selects relevant features from a DataFrame for model training.

    This function filters out unnecessary columns from the input DataFrame to retain only those that are 
    pertinent for building and training machine learning models. It ensures that identifiers and dependent 
    variables are excluded, focusing on meaningful feature data.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing both features and metadata.
    AnimalID (str, optional): The name of the column used to uniquely identify animals in the dataset. Defaults to "AnimalID".
    dep_var (str, optional): The name of the dependent variable column, which is the target for prediction. Defaults to 'OutcomeType'.

    Returns:
    pandas.DataFrame: A DataFrame containing only the selected features, excluding non-relevant columns.

    Process Overview:
    1. Identifies and excludes columns that are not relevant for model training, including the identifier, 
       dependent variable, and other specified metadata such as 'Name', 'DateTime', 'SexuponOutcome', 'Sterilization',
       and 'Mix'.
    2. Constructs a list of existing columns from the DataFrame that match the selected features and required identifiers.
    3. Filters the DataFrame to include only these relevant columns, effectively creating a dataset optimized for 
       model training.

    Example usage:
        feature_df = select_features(input_data)
        
    Assumptions:
    - The function assumes the presence of certain columns like 'Name', 'DateTime', etc., which are consistently named across datasets.
    """

    features = [col for col in df.columns if col not in [AnimalID, dep_var, 'Name', 'DateTime', 'SexuponOutcome', 'Sterilization', 'Mix']]

    existing_columns = [col for col in [AnimalID, dep_var] + features if col in df.columns]
    df = df[existing_columns]


    return df


def engineer_features(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID",
    dep_var: str=r"OutcomeType"
) -> pd.DataFrame:
    """
    Engineers and selects features from a DataFrame for machine learning model preparation.

    This function performs feature engineering by encoding categorical variables and selecting relevant 
    features necessary for model training. It utilizes helper functions to transform the input data into a 
    format suitable for analysis or predictive modeling tasks.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing raw data that requires feature transformation.
    AnimalID (str, optional): The column name used to identify individual animals in the dataset. Defaults to "AnimalID".
    dep_var (str, optional): The name of the dependent variable column, which is the target for prediction. Defaults to 'OutcomeType'.

    Returns:
    pandas.DataFrame: A DataFrame with engineered and selected features, ready for model training or analysis.

    Process Overview:
    1. Calls `encode_categorical_variables` to transform categorical columns into numerical representations,
       including creating dummy variables where applicable.
    2. Invokes `select_features` to filter the dataset down to only those columns that are relevant for 
       machine learning models, based on predefined criteria or feature selection logic.

    Example usage:
        engineered_df = engineer_features(input_data)
        
    Assumptions:
    - The function assumes the presence of specific helper functions (`encode_categorical_variables`, `select_features`)
      which perform necessary subtasks within this function.
    """

    # Encode categorical variables in the DataFrame
    df_encoded = encode_categorical_variables(df)

    # Select relevant features for model training
    df_selected = select_features(df_encoded, AnimalID=AnimalID, dep_var=dep_var)


    return df_selected
