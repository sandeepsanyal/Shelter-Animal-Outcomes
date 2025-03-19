def create_features(df):
    # Example feature engineering: Create a new feature for the age in months
    df['AgeuponOutcome'] = df['AgeuponOutcome'].str.replace(' months', '').str.replace(' years', '').astype(float)
    df['AgeuponOutcome'] = df['AgeuponOutcome'].fillna(0)  # Fill NaN values with 0
    df['AgeuponOutcome'] = df['AgeuponOutcome'].apply(lambda x: x * 12 if 'years' in df['AgeuponOutcome'] else x)

    # Example feature: Create a binary feature for whether the animal is neutered
    df['IsNeutered'] = df['SexuponOutcome'].apply(lambda x: 1 if 'Neutered' in x else 0)

    # Example feature: Create a feature for the length of the name
    df['NameLength'] = df['Name'].apply(len)

    return df

def select_features(df):
    # Select relevant features for model training
    features = ['AgeuponOutcome', 'IsNeutered', 'NameLength', 'Breed', 'Color']
    return df[features]