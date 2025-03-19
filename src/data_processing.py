import numpy as np
import pandas as pd
import re
from tqdm import tqdm

def load_data(file_path):
    """
    Load the dataset from a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: The loaded dataset as a pandas DataFrame.
    """
    data = pd.read_csv(file_path)
    return data

# Function to convert age terms into days
def convert_to_days(age_str):
    """
    Converts an age string with specified units into the equivalent number of days.

    This function takes a string representing an age (e.g., "2 years", "3 months") and converts it 
    into an integer value representing the number of days. It handles various time units including
    years, months, weeks, and days. The conversion uses approximate average lengths for each unit.
    
    Parameters:
    age_str (str or pd.NA): A string containing a numeric value followed by a time unit ('years', 
                            'months', 'weeks', or 'days'). If the input is NaN or does not match
                            the expected format, None will be returned.

    Returns:
    int or None: The number of days corresponding to the provided age string if it matches the expected
                 format. Possible return values include:
                 - An integer representing the equivalent days for valid inputs.
                 - None if the input is NaN, does not match the pattern, or has an unsupported unit.

    Example usage:
    >>> convert_to_days("2 years")
    730
    >>> convert_to_days("3 months")
    90
    >>> convert_to_days(pd.NA)
    None

    Notes:
    - This function uses regular expressions to parse the input string and extract numeric values 
      along with their units.
    - The conversion approximates one year as 365 days, one month as 30 days, one week as 7 days,
      and treats 'day' literally as 1 day.
    - It is case-insensitive for unit names (e.g., "Years", "months" are both valid).
    - Ensure that the input string is correctly formatted; otherwise, the function will return None.

    """
    if pd.isna(age_str):
        return None

    # Use regular expressions to find the number and unit
    match = re.match(r'(\d+)\s*(years?|weeks?|months?|days?)', age_str)
    
    if not match:
        return None  # Return None for unmatched formats
    
    number, unit = int(match.group(1)), match.group(2).lower()

    # Convert the units to days
    if 'year' in unit:
        return number * 365 # Approximate year length as 365 days
    elif 'month' in unit:
        return number * 30  # Approximate month length as 30 days
    elif 'week' in unit:
        return number * 7
    elif 'day' in unit:
        return number

    return None

# Group 'AgeuponOutcome' into categories based on the number of days as follows:
def group_age(age):
    """
    Categorizes an age into predefined groups based on its value.

    This function takes an age value (either as a number or NaN) and returns a string representing the 
    age category that the input falls into. It is designed to handle both numeric ages and missing values.
    
    Parameters:
    age (int, float, pd.NA): The age of an individual which can be a number or a pandas NA value (NaN). 
                             If the age is not provided or is NaN, it will return None.

    Returns:
    str or None: A string representing the age category if the input is valid. Possible outputs are:
                 - '<1 week' for ages less than 7 days
                 - '<1 month' for ages between 7 and 29 days (inclusive)
                 - '<6 months' for ages between 30 and 179 days (inclusive)
                 - '<1 year' for ages between 180 and 364 days (inclusive)
                 - '<5 years' for ages between 365 and 1824 days (inclusive)
                 - '<10 years' for ages between 1825 and 3649 days (inclusive)
                 - '<15 years' for ages between 3650 and 5474 days (inclusive)
                 - '15+ years' for ages of 5475 days or more
                 If the input age is NaN, returns None.

    Example usage:
    >>> group_age(10)
    '<1 week'
    >>> group_age(45)
    '<1 month'
    >>> group_age(pd.NA)
    None

    Notes:
    - The function assumes that the input `age` is measured in days.
    - It utilizes pandas' functionality to check for NaN values, so ensure pandas is imported if using NA.
    """
    if pd.isna(age):
        return None
    if age < 7:
        return '<1 week'
    elif age < 30:
        return '<1 month'
    elif age < 180:
        return '<6 months'
    elif age < 365:
        return '<1 year'
    elif age < 1825:
        return '<5 years'
    elif age < 3650:
        return '<10 years'
    elif age < 5475:
        return '<15 years'
    else:
        return '15+ years'

def preprocess_data(df):
    """
    Preprocesses the animal dataset by performing several cleaning and data transformation steps.

    This function cleans the input DataFrame by handling missing values, standardizing breed names,
    extracting patterns from coat colors, grouping breeds into categories, and more. It processes
    mixed breeds separately to ensure accurate categorization and pattern extraction.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing animal data with columns such as 'AnimalID',
                       'Breed', 'Color', etc. This DataFrame is expected to have specific column names
                       that the function will process, including handling whitespace and standardizing
                       breed and color information.

    Returns:
    tuple: A tuple of DataFrames containing:
        - The main preprocessed DataFrame with added columns for grouped breeds and coat patterns.
        - A separate DataFrame for individual breeds extracted from mixed breeds.
        - A DataFrame containing animals categorized by their grouped breeds.
        - Additional DataFrames as needed based on further preprocessing steps (not detailed here).
    
    Example usage:
    >>> import pandas as pd
    >>> df = pd.read_csv('animal_data.csv')
    >>> result_dfs = preprocess_animal_data(df)
    >>> main_df, breed_df, grouped_breed_df = result_dfs[0], result_dfs[1], result_dfs[2]
    
    Notes:
    - This function assumes the input DataFrame has specific columns like 'AnimalID', 'Breed',
      and 'Color'. If your dataset differs, you may need to adjust column names accordingly.
    - The function handles mixed breeds by splitting them into individual components for processing
      before recombining them. This is particularly useful for accurate breed categorization.

    """

    # Age of animals
    df['AgeuponOutcome'] = df['AgeuponOutcome'].str.replace('  ', ' ')

    # Apply the conversion function to each entry in the 'AgeuponOutcome' column
    df['AgeuponOutcome'] = df['AgeuponOutcome'].apply(convert_to_days)
    df['AgeuponOutcome'] = df['AgeuponOutcome'].apply(group_age)


    # Sex of animals
    # remove multiple spaces
    df['SexuponOutcome'] = df['SexuponOutcome'].str.replace('  ', ' ')
    # replace 'Unknown' with NaN
    df['SexuponOutcome'] = df['SexuponOutcome'].str.replace(r'unknown', '', regex=True, flags=re.IGNORECASE).str.strip().replace('', np.nan)
    # split the column into two columns
    df['Sterilization'] = df['SexuponOutcome'].str.split(' ').str[0]
    df['SexuponOutcome'] = df['SexuponOutcome'].str.split(' ').str[1]


    # Breed of animals
    dog_breed_group_map = pd.DataFrame(
        data={
            "dogs": ["Nova Scotia Duck Tolling Retriever", "St. Bernard Rough Coat", "American Pit Bull Terrier", "Wire Hair Fox Terrier", "Soft Coated Wheaten Terrier", "St. Bernard Smooth Coat", "Greater Swiss Mountain Dog", "Smooth Fox Terrier", "Jack Russell Terrier", "Parson Russell Terrier", "Australian Cattle Dog", "Bernese Mountain Dog", "Cardigan Welsh Corgi", "German Shorthair Pointer", "Pembroke Welsh Corgi", "American Staffordshire Terrier", "American Pit Terrier", "Flat Coat Retriever", "Black Mouth Cur", "Dogue De Bordeaux", "Chesa Bay Retr", "German Wirehaired Pointer", "Old English Bulldog", "Treeing Walker Coonhound", "Bull Terrier Miniature", "English Springer Spaniel", "Glen Of Imaal", "Port Water Dog", "Old English Sheepdog", "Toy Fox Terrier", "Welsh Springer Spaniel", "Wirehaired Pointing Griffon", "English Cocker Spaniel", "Treeing Tennesse Brindle", "Spanish Water Dog", "Cardigan Welsh Corgi", "Spinone Italiano", "Shetland Sheepdog", "Miniature Schnauzer", "Border Collie", "German Shepherd", "American Eskimo", "Doberman Pinsch", "Chihuahua Shorthair", "Australian Shepherd", "Rat Terrier", "Siberian Husky", "Chow Chow", "Cocker Spaniel", "Lhasa Apso", "Boston Terrier", "Manchester Terrier", "Miniature Pinscher", "Golden Retriever", "Cairn Terrier", "American Bulldog", "Shih Tzu", "Basset Hound", "Chihuahua Longhair", "Miniature Poodle", "Chinese Sharpei", "Silky Terrier", "Yorkshire Terrier", "Australian Kelpie", "Shiba Inu", "Plott Hound", "Great Dane", "Belgian Malinois", "Toy Poodle", "Podengo Pequeno", "Dutch Shepherd", "Great Pyrenees", "English Bulldog", "Carolina Dog", "Dogo Argentino", "Blue Lacy", "Alaskan Husky", "Border Terrier", "Collie Rough", "Norwich Terrier", "Italian Greyhound", "English Coonhound", "Afghan Hound", "Bluetick Hound", "Anatol Shepherd", "Airedale Terrier", "Dachshund Wirehair", "Cavalier Span", "English Pointer", "Bull Terrier", "Patterdale Terr", "Norfolk Terrier", "Rhod Ridgeback", "Chinese Crested", "American Foxhound", "Collie Smooth", "Standard Poodle", "West Highland", "Finnish Spitz", "Bruss Griffon", "Cane Corso", "Dachshund Longhair", "Irish Terrier", "Queensland Heeler", "Scottish Terrier", "German Pinscher", "Alaskan Malamute", "Ibizan Hound", "Japanese Chin", "Welsh Terrier", "Skye Terrier", "English Setter", "Pharaoh Hound", "Standard Schnauzer", "Bearded Collie", "Bichon Frise", "French Bulldog", "English Foxhound", "Canaan Dog", "Tibetan Terrier", "Irish Wolfhound", "Belgian Sheepdog", "Swiss Hound", "Boykin Span", "Swedish Vallhund", "Tibetan Spaniel", "Presa Canario", "Belgian Tervuren", "Irish Setter", "English Shepherd", "Australian Terrier", "Sealyham Terr", "Treeing Cur", "Bedlington Terr", "Schnauzer Giant", "Spanish Mastiff", "Picardy Sheepdog", "Neapolitan Mastiff", "Mexican Hairless", "Field Spaniel", "Norwegian Elkhound", "Tan Hound", "Labrador Retriever", "Redbone Hound", "Dachshund", "Newfoundland", "Pug", "Catahoula", "Harrier", "Pointer", "Rottweiler", "Beagle", "Keeshond", "Bullmastiff", "Weimaraner", "Pekingese", "Vizsla", "Boxer", "Maltese", "Akita", "Basenji", "Pbgv", "Bulldog", "Staffordshire", "Brittany", "Boerboel", "Black", "Whippet", "Feist", "Beauceron", "Pomeranian", "Schipperke", "Greyhound", "Kuvasz", "Saluki", "Leonberger", "Affenpinscher", "Hovawart", "Havanese", "Bloodhound", "Mastiff", "Entlebucher", "Papillon", "Landseer", "Dalmatian", "Jindo", "Samoyed", "Otterhound", "Lowchen", "Yorkshire", "Borzoi", "Cardigan Welsh Corgi", "Labrador Retriever", "Redbone Hound", "American Pit Terrier", "Dachshund", "Whippet"],
            "breed_group": ["Sporting", "Working", "Terrier", "Terrier", "Terrier", "Working", "Working", "Terrier", "Terrier", "Terrier", "Herding", "Working", "Herding", "Sporting", "Herding", "Terrier", "Terrier", "Sporting", "Herding", "Working", "Sporting", "Sporting", "", "Hound", "Terrier", "Sporting", "Terrier", "Working", "Herding", "Toy", "Sporting", "Sporting", "Sporting", "", "Herding", "Herding", "Sporting", "Herding", "Terrier", "Herding", "Herding", "Non-Sporting", "Working", "Toy", "Herding", "Terrier", "Working", "Non-Sporting", "Sporting", "Non-Sporting", "Non-Sporting", "Terrier", "Toy", "Sporting", "Terrier", "Non-Sporting", "Toy", "Hound", "Toy", "Non-Sporting", "Non-Sporting", "Toy", "Toy", "Working", "Non-Sporting", "Hound", "Working", "Herding", "Toy", "Hound", "Sporting", "Working", "Non-Sporting", "", "", "Herding", "", "Terrier", "Herding", "Terrier", "Toy", "Hound", "Hound", "Hound", "Sporting", "Terrier", "Hound", "Toy", "Sporting", "Terrier", "Terrier", "Terrier", "Hound", "Toy", "Hound", "Herding", "Non-Sporting", "Terrier", "Non-Sporting", "Toy", "Working", "Hound", "Terrier", "Herding", "Terrier", "Working", "Working", "Hound", "Toy", "Terrier", "Terrier", "Sporting", "Hound", "Working", "Herding", "Non-Sporting", "Non-Sporting", "Hound", "Working", "Non-Sporting", "Hound", "Herding", "Hound", "Sporting", "Herding", "Non-Sporting", "", "Herding", "Sporting", "Herding", "Terrier", "Terrier", "", "Terrier", "Working", "", "Herding", "Working", "Non-Sporting", "Sporting", "Hound", "Hound", "Sporting", "Hound", "Hound", "Working", "Toy", "Herding", "Hound", "Sporting", "Working", "Hound", "Non-Sporting", "Working", "Sporting", "Toy", "Sporting", "Working", "Toy", "Working", "Hound", "Hound", "Non-Sporting", "Terrier", "Sporting", "Working", "Herding", "Hound", "Terrier", "Herding", "Toy", "Non-Sporting", "Hound", "Working", "Hound", "Working", "Toy", "", "Toy", "Hound", "Working", "Herding", "Toy", "", "Non-Sporting", "Non-Sporting", "Working", "Hound", "Non-Sporting", "Toy", "Hound", "Herding", "Sporting", "Hound", "Terrier", "Hound", "Hound"]
        }
    ).replace('', np.nan).dropna(how='any')

    # remove multiple spaces
    df['Breed'] = df['Breed'].str.replace('  ', ' ')
    # replace '/Unknown' with 'Mix'
    df['Breed'] = df['Breed'].str.replace(r'/unknown', r' Mix', regex=True, flags=re.IGNORECASE)
    # replace 'Unknown' with ''
    df['Breed'] = df['Breed'].str.replace(r'unknown', '', regex=True, flags=re.IGNORECASE).str.strip()
    # replace "Devon Rex" with"Rex"
    df['Breed'] = df['Breed'].str.replace(r'Devon Rex', 'Rex', flags=re.IGNORECASE)
    # replace "Cornish  Rex" with"Rex"
    df['Breed'] = df['Breed'].str.replace(r'Cornish  Rex', 'Rex', flags=re.IGNORECASE)
    # remove these words from the 'Breed' column ["Wirehair","Smooth Coat","Smooth","Flat Coat "]
    df['Breed'] = df['Breed'].str.replace(r'Wirehair', '', regex=True, flags=re.IGNORECASE).str.strip()
    df['Breed'] = df['Breed'].str.replace(r'Smooth Coat', '', regex=True, flags=re.IGNORECASE).str.strip()
    df['Breed'] = df['Breed'].str.replace(r'Smooth', '', regex=True, flags=re.IGNORECASE).str.strip()
    df['Breed'] = df['Breed'].str.replace(r'Flat Coat', '', regex=True, flags=re.IGNORECASE).str.strip()

    # split the column into two columns
    df['Mix'] = ["Mix" if "Mix" in df.loc[i, 'Breed'] else np.nan for i in range(df.shape[0])]
    df['Breed'] = df['Breed'].str.split(' Mix').str[0]
    # replace rows containing 'Mix' with nan in "Breed" column
    df['Breed'] = df['Breed'].str.replace(r'^Mix$', '', regex=True, flags=re.IGNORECASE).replace('', np.nan)


    # Seperate the 'Breed' column by '/' and create multiple rows for each breed
    breed_list = df['Breed'].str.split('/')
    breed_list = breed_list.explode()
    # Create a seperate breed dataframe
    breed = pd.merge(
        left=df[['AnimalID', "Breed", "Mix"]],
        right=breed_list.to_frame(name='Breed_broken'),
        left_index=True,
        right_index=True,
        how='left'
    ).reset_index(drop=True)
    breed = pd.merge(
        left=breed,
        right=dog_breed_group_map.rename(columns={'breed_group': 'BreedType'}),
        left_on='Breed_broken',
        right_on='dogs',
        how='left'
    )
    del breed_list

    # calculate frequency of each AnimalID in breed data
    breed_freq = breed['AnimalID'].value_counts().reset_index().sort_values("count", ascending=False).reset_index(drop=True)

    for animal in tqdm(df['AnimalID'].unique()):
        # Get the count of breeds for the current animal.
        counts = breed_freq.loc[breed_freq['AnimalID'] == animal, 'count']
        
        if not counts.empty:
            # Case when there is more than one breed
            if counts.values[0] > 1:
                df.loc[df['AnimalID'] == animal, 'Mix'] = 'Mix'
            
            # Case when the count is exactly 1
            elif counts.values[0] == 1:
                # Check if 'Breed' column has NaN values for this AnimalID.
                breed_info = df.loc[df['AnimalID'] == animal, 'Breed']
                
                if pd.isna(breed_info).any():
                    df.loc[df['AnimalID'] == animal, 'Mix'] = np.nan
                else:
                    # Check if 'Mix' column is NaN before assigning 'Pure breed'.
                    if df.loc[df['AnimalID'] == animal, 'Mix'].isna().any():
                        df.loc[df['AnimalID'] == animal, 'Mix'] = 'Pure breed'
        else:
            # Case when there is no entry in breed_freq for this AnimalID.
            if df.loc[df['AnimalID'] == animal, 'Mix'].isna().any():
                df.loc[df['AnimalID'] == animal, 'Mix'] = np.nan

    # Default case (may not be needed with specific conditions)
    else:
        df.loc[df['AnimalID'] == animal, 'Mix'] = 'Mix'
    del breed_freq

    breed = breed.drop(columns=['Breed_broken', 'dogs', 'Mix'])
    breed["BreedType"] = [breed.loc[i, "Breed"] if pd.isna(breed.loc[i, "BreedType"]) else breed.loc[i, "BreedType"] for i in range(breed.shape[0])]
    breed_mix = df[["AnimalID", "Mix"]]


    # Coat of animals
    # remove multiple spaces
    df['Color'] = df['Color'].str.replace('  ', ' ')

    # Coat color and pattern
    coatcolor = df.copy()

    # extract coat patterns from the 'Color' column
    coat_patterns = ["Brindle", "Merle", "Point", "Smoke", "Tabby", "Tick", "Tiger"]
    change_colors = pd.DataFrame(
        {
            "Color": ["Buff", "Pink", "Tan", "Silver", "Apricot", "Flame", "Gold", "Blue"],
            "NewColor": ["Cream", "White", "Cream", "White", "Cream", "Orange", "Yellow", "Gray"]
        }
    )
    coatcolor["CoatPattern"] = np.nan
    for animal in tqdm(coatcolor['AnimalID'].unique()):
        # For coat colors
        if ((coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.contains('Orange', regex=True, flags=re.IGNORECASE)).any() and
            (coatcolor.loc[coatcolor['AnimalID'] == animal, 'AnimalType'] == "Dog").all()):  # Ensure the condition is evaluated properly
            coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'] = coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.replace('Orange', 'Red', regex=True, flags=re.IGNORECASE)
        
        if ((coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.contains('Yellow', regex=True, flags=re.IGNORECASE)).any() and
            (coatcolor.loc[coatcolor['AnimalID'] == animal, 'AnimalType'] == "Cat").all()):  # Ensure the condition is evaluated properly
            coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'] = coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.replace('Yellow', 'Orange', regex=True, flags=re.IGNORECASE)
        
        if ((coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.contains('Tricolor', regex=True, flags=re.IGNORECASE)).any() and
            (coatcolor.loc[coatcolor['AnimalID'] == animal, 'AnimalType'] == "Cat").all()):  # Ensure the condition is evaluated properly
            coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'] = coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.replace('Tricolor', 'Calico', regex=True, flags=re.IGNORECASE)
        
        # Replace colors based on the change_colors DataFrame
        for i in range(change_colors.shape[0]):
            if (coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.contains(change_colors.loc[i, 'Color'], regex=True, flags=re.IGNORECASE)).any():
                coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'] = coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.replace(
                    change_colors.loc[i, 'Color'], change_colors.loc[i, 'NewColor'], regex=True, flags=re.IGNORECASE
                )
        
        # For coat patterns
        pattern_found = False
        for pattern in coat_patterns:
            # For each row, if the pattern is found in the 'Color' column, create a new colum named 'CoatPattern' and set the value to pattern
            if coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.contains(pattern, regex=True, flags=re.IGNORECASE).any():
                coatcolor.loc[coatcolor['AnimalID'] == animal, 'CoatPattern'] = pattern
                coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'] = coatcolor.loc[coatcolor['AnimalID'] == animal, 'Color'].str.replace(
                    pattern, '', regex=True, flags=re.IGNORECASE).str.strip()
                pattern_found = True
                break
        
        if not pattern_found:
            coatcolor.loc[coatcolor['AnimalID'] == animal, 'CoatPattern'] = np.nan

    coat_color = pd.merge(
        left=df[['AnimalID', 'Color']],
        right=coatcolor[['AnimalID', 'Color']].rename(columns={'Color': 'CoatColor'}),
        left_on='AnimalID',
        right_on='AnimalID',
        how='left'
    )

    coat_patterns = coatcolor[['AnimalID', 'Color', 'CoatPattern']]


    # Seperate the 'Color' column by '/' and create multiple rows for each breed
    coatcolor_list = coat_color['CoatColor'].str.split('/')
    coatcolor_list = coatcolor_list.explode()
    # The final coat color dataframe
    coat_color = pd.merge(
        left=coat_color[['AnimalID', "Color"]],
        right=coatcolor_list.to_frame(name='CoatColor'),
        left_index=True,
        right_index=True,
        how='left'
    ).reset_index(drop=True)

    
    return df, breed, breed_mix, coat_color, coat_patterns

def encode_categorical_variables(df):
    """
    Encode categorical variables using one-hot encoding.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame with categorical variables.
    
    Returns:
    pd.DataFrame: The DataFrame with encoded categorical variables.
    """
    df = pd.get_dummies(df, columns=['AnimalType', 'SexuponOutcome', 'Breed', 'Color'], drop_first=True)
    return df

def process_data(file_path):
    """
    Load and preprocess the data from the specified file path.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: The processed DataFrame ready for model training.
    """
    df = load_data(file_path)
    df = preprocess_data(df)
    df = encode_categorical_variables(df)
    return df