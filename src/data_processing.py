import numpy as np
import pandas as pd
import re


def load_data(
    raw_data_path: str,
    dep_var: str = r"OutcomeType"
) -> pd.DataFrame:
    """
    Load and preprocess a dataset from a CSV file.

    This function reads a CSV file into a pandas DataFrame, renames specific columns for consistency,
    removes duplicate entries, and filters the data based on predefined categories for 'AnimalType'
    and the dependent variable.

    Parameters:
    raw_data_path (str): The full path to the CSV file to be loaded.
    dep_var (str, optional): The name of the dependent variable column used for prediction. Defaults to 'OutcomeType'.

    Returns:
    pd.DataFrame: A cleaned and filtered pandas DataFrame containing the dataset.

    Raises:
    - FileNotFoundError: If the specified CSV file does not exist at the given path.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If there is an issue parsing the CSV file.

    Example:
    data = load_data('/path/to/data.csv')

    Notes:
    - The function assumes the CSV file has no spaces in the filename other than those included in the path.
    - The 'AnimalType' column is filtered to include only 'Cat' and 'Dog'.
    - The dependent variable is filtered to include only ['Adoption', 'Euthanasia', 'Transfer', 'Return to Owner', 'Died'].
    """
    data = pd.read_csv(raw_data_path)

    data.rename(
        columns={
            "Outcome Type": "OutcomeType",
            "Date of Birth": "DateOfBirth",
            "Outcome Subtype": "OutcomeSubtype",
            "Animal Type": "AnimalType",
            "Sex upon Outcome": "SexuponOutcome",
            "Age upon Outcome": "AgeuponOutcome"
        },
        inplace=True
    )
    data.drop_duplicates(inplace=True)
    data = data[
        (data["AnimalType"].isin(["Cat", "Dog"])) &
        (data[dep_var].isin(['Adoption', 'Euthanasia', 'Transfer', 'Return to Owner', 'Died']))
    ]
    data.reset_index(drop=True, inplace=True)

    return data


# Function to convert age terms into days
def convert_to_days(age_str) -> int:
    """
    Converts an age string with specified units into the equivalent number of days.

    This function takes a string representing an age (e.g., "2 years", "3 months") and converts it into an integer value representing the number of days. It handles various time units including years, months, weeks, and days. The conversion uses approximate average lengths for each unit.
    
    Parameters:
    age_str (str or pd.NA): A string containing a numeric value followed by a time unit ('years', 'months', 'weeks', or 'days'). If the input is NaN or does not match the expected format, None will be returned.

    Returns:
    int or None: The number of days corresponding to the provided age string if it matches the expected format. Possible return values include:
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
    - This function uses regular expressions to parse the input string and extract numeric values along with their units.
    - The conversion approximates one year as 365 days, one month as 30 days, one week as 7 days, and treats 'day' literally as 1 day.
    - It is case-insensitive for unit names (e.g., "Years", "months" are both valid).
    - Ensure that the input string is correctly formatted; otherwise, the function will return None.

    """
    if pd.isna(age_str):
        return None

    # Use regular expressions to find the number and unit
    match = re.match(r'(\d+)\s*(years?|months?|weeks?|days?)', age_str)
    if not match:
        return None  # Return None for unmatched formats
    
    number, unit = int(match.group(1)), match.group(2).lower()

    # Convert the units to days
    if 'year' in unit:
        return number * 365  # Approximate year length as 365 days
    elif 'month' in unit:
        return number * 30   # Approximate month length as 30 days
    elif 'week' in unit:
        return number * 7
    elif 'day' in unit:
        return number

    return None


def group_age(age) -> str:
    """
    Categorizes an age into predefined groups based on its value.

    This function takes an age value (either as a number or NaN) and returns a string representing the age category that the input falls into. It is designed to handle both numeric ages and missing values.
    
    Parameters:
    age (int, float, pd.NA): The age of an individual which can be a number or a pandas NA value (NaN). If the age is not provided or is NaN, it will return None.

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
        - If the input age is NaN, returns None.

    Example usage:
    >>> group_age(10)
    '<1 month'
    >>> group_age(45)
    '<6 months'
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


def process_breed_data(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID"
) -> tuple:
    """
    Processes and standardizes breed data from an animal dataset.

    This function performs several transformations on the 'Breed' column of the input DataFrame to ensure consistency, handle mixed breeds appropriately, and categorize each breed into predefined groups. The resulting DataFrames provide detailed insights into breed information and mix statuses for further analysis or reporting.

    Parameters:
    df (pandas.DataFrame): A DataFrame containing animal data with at least 'Breed' and a column specified by AnimalID.
    AnimalID (str, optional): The name of the column in `df` that identifies individual animals. Defaults to "AnimalID".

    Returns:
    tuple: A tuple containing three DataFrames:
        - df (pandas.DataFrame): The modified input DataFrame with updated 'Breed' and 'Mix' columns.
        - breed (pandas.DataFrame): A new DataFrame detailing each animal's breeds, including separated mixed breeds and their types categorized by dog breed group.
        - breed_mix (pandas.DataFrame): A DataFrame showing the original 'Breed' column values alongside the 'Mix' status.

    The function performs the following operations:
    1. Standardizes text in the 'Breed' column using regular expressions to handle spaces, unknowns, and specific terms.
    2. Splits breeds containing 'Mix', creating a new 'Mix' column indicating mixed breed status.
    3. Separates multiple breeds listed in the same entry of the 'Breed' column into individual rows.
    4. Maps each breed to its respective type (e.g., Terrier, Working) using a predefined dictionary and assigns an 'Unknown' category if no match is found.
    5. Calculates the frequency of each animal's occurrence in the breed data and updates the 'Mix' status based on these counts.
    6. Ensures that breeds are properly categorized and mixed status is accurately reflected across all related DataFrames.

    Example usage:
    updated_df, detailed_breed_info, mix_status = process_breed_data(animal_data)

    Notes:
    - The function handles mixed breeds by splitting them into individual components for processing before recombining them. This is particularly useful for accurate breed categorization.
    """

    # For dog breeds
    dog_breed_group_dict = {
        "Herding": ["Australian Cattle Dog", "Australian Shepherd", "Bearded Collie", "Beauceron", "Belgian Malinois", "Belgian Sheepdog", "Belgian Tervuren", "Black", "Black Mouth Cur", "Blue Lacy", "Border Collie", "Cardigan Welsh Corgi", "Catahoula", "Collie Rough", "Collie Smooth", "English Shepherd", "Entlebucher", "German Shepherd", "Old English Sheepdog", "Pembroke Welsh Corgi", "Picardy Sheepdog", "Queensland Heeler", "Shetland Sheepdog", "Spanish Water Dog", "Swedish Vallhund"],
        "Hound": ["Afghan Hound", "American Foxhound", "Basenji", "Basset Hound", "Beagle", "Bloodhound", "Bluetick Hound", "Borzoi", "Dachshund", "Dachshund Longhair", "Dachshund Wirehair", "English Coonhound", "English Foxhound", "Greyhound", "Harrier", "Ibizan Hound", "Irish Wolfhound", "Norwegian Elkhound", "Otterhound", "Pbgv", "Pharaoh Hound", "Plott Hound", "Podengo Pequeno", "Redbone Hound", "Rhod Ridgeback"],
        "Non-Sporting": ["American Bulldog", "American Eskimo", "Bichon Frise", "Boston Terrier", "Bulldog", "Chinese Sharpei", "Chow Chow", "Dalmatian", "English Bulldog", "Finnish Spitz", "French Bulldog", "Jindo", "Keeshond", "Lhasa Apso", "Lowchen", "Mexican Hairless", "Miniature Poodle", "Schipperke", "Shiba Inu", "Standard Poodle", "Tibetan Spaniel", "Tibetan Terrier"],
        "Sporting": ["Anatol Shepherd", "Boykin Span", "Brittany", "Chesa Bay Retr", "Cocker Spaniel", "Dutch Shepherd", "English Cocker Spaniel", "English Pointer", "English Setter", "English Springer Spaniel", "Field Spaniel", "Flat Coat Retriever", "German Shorthair Pointer", "German Wirehaired Pointer", "Golden Retriever", "Irish Setter", "Labrador Retriever", "Nova Scotia Duck Tolling Retriever", "Pointer", "Spinone Italiano", "Vizsla", "Weimaraner", "Welsh Springer Spaniel", "Wirehaired Pointing Griffon"],
        "Terrier": ["Airedale Terrier", "American Pit Bull Terrier", "American Pit Terrier", "American Staffordshire Terrier", "Australian Terrier", "Bedlington Terr", "Border Terrier", "Bull Terrier", "Bull Terrier Miniature", "Cairn Terrier", "Feist", "Glen Of Imaal", "Irish Terrier", "Jack Russell Terrier", "Manchester Terrier", "Miniature Schnauzer", "Norfolk Terrier", "Norwich Terrier", "Parson Russell Terrier", "Patterdale Terr", "Rat Terrier", "Scottish Terrier", "Sealyham Terr", "Skye Terrier", "Smooth Fox Terrier"],
        "Toy": ["Affenpinscher", "Bruss Griffon", "Cavalier Span", "Chihuahua Longhair", "Chihuahua Shorthair", "Chinese Crested", "Havanese", "Italian Greyhound", "Japanese Chin", "Maltese", "Miniature Pinscher", "Papillon", "Pekingese", "Pomeranian", "Pug", "Shih Tzu", "Silky Terrier", "Toy Fox Terrier", "Toy Poodle", "Yorkshire", "Yorkshire Terrier"],
        "Working": ["Akita", "Alaskan Malamute", "Australian Kelpie", "Bernese Mountain Dog", "Boerboel", "Boxer", "Bullmastiff", "Canaan Dog", "Cane Corso", "Doberman Pinsch", "Dogue De Bordeaux", "German Pinscher", "Great Dane", "Great Pyrenees", "Greater Swiss Mountain Dog", "Kuvasz", "Leonberger", "Mastiff", "Neapolitan Mastiff", "Newfoundland", "Port Water Dog", "Rottweiler", "Samoyed", "Schnauzer Giant", "Siberian Husky"]
    }
    # For cat breeds
    cat_breed_group_dict = {
        "Domestic Longhair": ["Domestic Longhair"],
        "Domestic Mediumhair": ["Domestic Medium Hair"],
        "Domestic Shorthair": ["Domestic Shorthair", "British Shorthair", "American Shorthair"],
        "Pixiebob": ["Pixiebob Shorthair"]
    }

    # Replace certain values in the 'Breed' column for consistency
    replacements = [
        (r'\s+', ' '),  # replace multiple spaces with a single space
        (r'/unknown', r' Mix'),  # replace '/Unknown' with 'Mix'
        (r'unknown', ''),  # replace 'Unknown' with ''
        (r'Devon Rex', r'Rex'),  # replace "Devon Rex" with "Rex"
        (r'Cornish Rex', r'Rex'),  # replace "Cornish Rex" with "Rex"
        (r'Wirehair', ''),  # remove "Wirehair"
        (r'Smooth Coat', ''),  # remove "Smooth Coat"
        (r'Smooth', ''),  # remove "Smooth"
        (r'Flat Coat', ''),   # remove "Flat Coat"
        (r'Exotic Shorthair', r'American Shorthair/Persian')   # replace 'Exotic Shorthair' with 'American Shorthair/Persian'
    ]
    for pattern, repl in replacements:
        df['Breed'] = df['Breed'].str.replace(pattern, repl, regex=True, flags=re.IGNORECASE).str.strip()

    # split the column into two columns
    df['Mix'] = df['Breed'].str.contains('Mix', case=False).astype(float)
    df['Breed'] = df['Breed'].str.split(' Mix').str[0]
    # replace rows containing 'Mix' with nan in "Breed" column
    df['Breed'] = df['Breed'].str.replace(r'^Mix$', '', regex=True, flags=re.IGNORECASE).replace('', np.nan)

    # Seperate the 'Breed' column by '/' and create multiple rows for each breed
    breed_list = df['Breed'].str.split('/')
    breed_list = breed_list.explode()
    # Create a seperate breed dataframe
    breed = pd.merge(
        left=df[[AnimalID, "AnimalType", "Breed", "Mix"]],
        right=breed_list.to_frame(name='Breed_broken'),
        left_index=True,
        right_index=True,
        how='left'
    ).reset_index(drop=True)
    breed = breed.drop_duplicates().reset_index(drop=True)
    breed_list = breed[[AnimalID, "Breed_broken"]]

    # Create a combined reverse mapping dictionary
    reverse_breed_group_map = {}
    for group, breeds in dog_breed_group_dict.items():
        for b in breeds:
            reverse_breed_group_map[b] = (group, "Dog")
    for group, breeds in cat_breed_group_dict.items():
        for b in breeds:
            reverse_breed_group_map[b] = (group, "Cat")
    
    # Function to get the breed type
    def get_breed_type(breed_name, animal_type):
        if breed_name in reverse_breed_group_map:
            return reverse_breed_group_map[breed_name][0]
        elif animal_type == "Dog":
            return "Unknown"
        else:  # For cats, retain the original breed name if no mapping is found
            return breed_name

    # Apply the function to create a new column 'BreedType'
    breed['BreedType'] = breed.apply(lambda row: get_breed_type(row['Breed_broken'], row['AnimalType']), axis=1)
    breed['BreedType'] = breed['BreedType'].replace("Unknown", np.nan)

    breed.drop(columns=['AnimalType'], inplace=True)
    breed = breed.drop_duplicates().reset_index(drop=True)


    # For breed mix
    ## Calculate frequency of each AnimalID in breed data
    breed_freq = breed_list[AnimalID].value_counts().reset_index(name='count')
    ## Merge the frequency counts back into the original dataframe
    df = pd.merge(
        left=df,
        right=breed_freq.rename(columns={"index": AnimalID}),
        left_on=AnimalID,
        right_on=AnimalID,
        how='left'
    )
    ## Assign 'Mix' where there are multiple breeds for an AnimalID
    df.loc[df['count'] > 1, 'Mix'] = 'Mix'
    ## Assign 'Pure breed' or keep NaN based on the presence of a Breed entry
    df['Mix'] = df['Mix'].fillna(value='Pure breed')
    ## Clean up by dropping the auxiliary frequency column
    df.drop(columns=['count'], inplace=True)
    del breed_freq

    breed.drop(columns=['Mix'], inplace=True)

    breed_mix = df[[AnimalID, "Breed", "Mix"]]
    breed_mix = breed_mix.loc[:, :]  # Ensures you have the original DataFrame
    breed_mix = breed_mix.drop_duplicates().reset_index(drop=True)


    return df, breed, breed_mix
    

def replace_colors(row: pd.Series) -> str:
    """
    Modify color names based on predefined rules and mappings.

    This function processes a single row from a DataFrame containing animal records.
    It adjusts the 'Color' attribute according to the animal type ('Dog', 'Cat') and applies specific transformations for consistency in color naming.

    Parameters:
    - row (pandas.Series): A pandas Series representing a single record with at least two columns: 'AnimalType' and 'Color'. 'AnimalType' indicates whether the animal is a 'Dog' or 'Cat', and 'Color' describes one or more colors associated with the animal.

    Returns:
    - str: The modified color name. If no applicable changes are found, returns the original color string.
    
    Notes:
    - This function uses the pandas library.
    - The `change_colors` mapping can be modified or extended as needed for additional transformations.
    """
    
    change_colors = pd.DataFrame(
        {
            "Color": ["Buff", "Pink", "Tan", "Silver", "Apricot", "Flame", "Gold", "Blue"],
            "NewColor": ["Cream", "White", "Cream", "White", "Cream", "Orange", "Yellow", "Gray"]
        }
    )

    if row['AnimalType'] == "Dog" and 'Orange' in row['Color']:
        return row['Color'].replace('Orange', 'Red')
    elif row['AnimalType'] == "Cat" and 'Yellow' in row['Color']:
        return row['Color'].replace('Yellow', 'Orange')
    elif row['AnimalType'] == "Cat" and 'Tricolor' in row['Color']:
        return row['Color'].replace('Tricolor', 'Calico')
    else:
        for old, new in change_colors.set_index('Color')['NewColor'].to_dict().items():
            if old in row['Color']:
                return row['Color'].replace(old, new)
    return row['Color']


def extract_coat_pattern(
    color_str: str,
    coat_patterns: list
) -> str:
    """
    Extracts and returns the coat pattern from a given color string.

    This function scans through a provided color description to identify if it contains any predefined coat patterns. If found, it returns the first matching pattern. The search is case-insensitive. If no patterns are detected, it returns NaN (Not a Number).

    Parameters:
    - color_str (str): A string describing the color and potentially the coat pattern of an animal.
    - coat_patterns (list): A list of predefined coat patterns to look for within the color string.

    Returns:
    - str: The name of the first matching coat pattern if found; otherwise, returns "".

    Notes:
    - The function utilizes the `re` module from Python's standard library for regular expression operations.
    - It returns an empty string when no patterns are matched, which can be useful in data processing and analysis workflows.
    """

    for pattern in coat_patterns:  # Fix indentation
        if re.search(pattern, color_str, re.IGNORECASE):  # Add missing 'color_str' variable
            return pattern
        else:
            return ""


def process_coat_colors(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID"
) -> tuple:
    """
    Processes the coat color and pattern information from animal data.

    This function handles the cleaning and extraction of coat colors and patterns from an input DataFrame. It removes unwanted spaces, standardizes color names, extracts specific coat patterns, and restructures the data to provide detailed insights into each animal's coat characteristics. The processed data is then split into separate DataFrames for further use.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the animal dataset with a 'Color' column and an identifier specified by AnimalID.
    - AnimalID (str, optional): The name of the column in `df` that uniquely identifies each animal. Defaults to "AnimalID".

    Returns:
    - tuple: A tuple containing multiple DataFrames representing different aspects of coat data.
        1. df (pd.DataFrame): The original DataFrame passed as input with potential modifications.
        2. coat_color (pd.DataFrame): DataFrame containing detailed information about each animal's coat colors.
        3. coat_patterns (pd.DataFrame): DataFrame listing the identified coat patterns for each animal.

    Processing Steps:
    1. Space Removal: Cleans the 'Color' column by removing multiple spaces between words.
    2. Coat Color Standardization: Applies a function `replace_colors` to standardize color names in the 'Color' column.
    3. Pattern Extraction: Identifies and extracts coat patterns from colors using a predefined list of patterns.
    4. Pattern Removal: Strips out recognized pattern indicators from the 'Color' string.
    5. Data Merging: Combines the original data with processed color information into `coat_color`.
    6. List Separation: Splits combined coat colors separated by '/' and creates individual rows for each color.

    Example usage:
    updated_df, coat_color, coat_patterns = process_coat_colors(animal_data)

    Notes:
    - The function assumes that helper functions `replace_colors` and `extract_coat_pattern` are defined elsewhere.
    - It also uses regular expressions (via the `re` module) to manipulate text data.
    """

    ## remove multiple spaces
    df['Color'] = df['Color'].str.replace('  ', ' ').str.strip()

    coatcolor = df.copy()

    ## For coat colors
    coatcolor['Color'] = coatcolor.apply(replace_colors, axis=1)

    ## For coat patterns
    coat_patterns = ["Brindle", "Merle", "Point", "Smoke", "Tabby", "Tick", "Tiger"]
    coatcolor['CoatPattern'] = coatcolor['Color'].apply(lambda x: extract_coat_pattern(x, coat_patterns))
    coatcolor['Color'] = coatcolor.apply(
        lambda row: re.sub('|'.join(coat_patterns), '', row['Color'], flags=re.IGNORECASE).strip(), axis=1)

    coat_color = pd.merge(
        left=df[[AnimalID, 'Color']],
        right=coatcolor[[AnimalID, 'Color']].rename(columns={'Color': 'CoatColor'}),
        left_on=AnimalID,
        right_on=AnimalID,
        how='left'
    ).drop_duplicates().reset_index(drop=True)
    coat_color["CoatColor"] = coat_color["CoatColor"].str.replace(r' /', r'/').str.replace(r'/ ', r'/').str.strip().str.replace(r' ', r'/')

    coat_patterns = coatcolor[[AnimalID, 'Color', 'CoatPattern']].drop_duplicates().reset_index(drop=True)

    ## Seperate the 'Color' column by '/' and create multiple rows for each breed
    coatcolor_list = coat_color['CoatColor'].str.split('/')
    coatcolor_list = coatcolor_list.explode()
    ## The final coat color dataframe
    coat_color = pd.merge(
        left=coat_color[[AnimalID, "Color"]],
        right=coatcolor_list.to_frame(name='CoatColor'),
        left_index=True,
        right_index=True,
        how='left'
    ).drop_duplicates().reset_index(drop=True)
    coat_color["CoatColor"] = coat_color["CoatColor"].replace("Unknown", np.nan)
    coat_color["CoatColor"] = coat_color["CoatColor"].replace('', np.nan)


    return df, coat_color, coat_patterns


def preprocess_data(
    df: pd.DataFrame,
    AnimalID: str=r"AnimalID",
    dep_var: str=r"OutcomeType"
) -> tuple:
    """
    Preprocesses animal data to clean and organize key attributes.

    This function performs several preprocessing steps on the input DataFrame to handle various aspects of animal data such as age, sex, breed, and coat color. The transformations include cleaning text fields, converting age representations into days, splitting columns for detailed categorization, and merging processed data back into a comprehensive DataFrame.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the animal dataset with required columns.Expected columns include 'AgeuponOutcome', 'SexuponOutcome', 'AnimalType', and optionally 'OutcomeType'.
    - AnimalID (str, optional): The name of the column in `df` that uniquely identifies each animal. Defaults to "AnimalID".
    - dep_var (str, optional): The name of the dependent variable column, which is the target for prediction. Defaults to 'OutcomeType'.

    Returns:
    - tuple: A tuple containing multiple DataFrames representing different aspects of processed data.
        1. df (pd.DataFrame): Merged DataFrame including cleaned and organized attributes.
        2. animal_data (pd.DataFrame): Subset of the original data with key columns after initial cleaning.
        3. breed (pd.DataFrame): Processed data related to the breeds of animals.
        4. breed_mix (pd.DataFrame): Additional processed data for mixed/ pure breeds.
        5. coat_color (pd.DataFrame): Data containing information about animals' coat colors.
        6. coat_patterns (pd.DataFrame): Data detailing patterns found in animals' coats.

    Processing Steps:
    1. Age Preprocessing: Cleans the 'AgeuponOutcome' column, converts age to days, and groups ages into categories.
    2. Sex Preprocessing: Cleans the 'SexuponOutcome' column by removing unwanted spaces and unknown values, then splits it into two columns for detailed categorization.
    3. Breed Processing: Utilizes an external function `process_breed_data` to handle breed-specific data transformations.
    4. Coat Processing: Uses another function `process_coat_colors` to manage coat color information and patterns.
    5. Data Merging: Merges all processed components into a single comprehensive DataFrame.

    Notes:
    - This function assumes the input DataFrame has specific columns like 'AnimalID', 'Breed', and 'Color'. If your dataset differs, you may need to adjust column names accordingly.
    - The function assumes that the helper functions `convert_to_days`, `group_age`, `process_breed_data`, and `process_coat_colors` are defined elsewhere in your codebase.
    """

    # Dependent Variable
    if dep_var in df.columns:
        ## Drop all missing values
        df = df.dropna(subset=dep_var).reset_index(drop=True)
        ## Standardize "Return to owner" labels
        pattern = re.compile(r'^(return\s*to\s*owner|Return\s*To\s*Owner|RETURN\s+TO\s+OWNER|return_to_owner)$', re.IGNORECASE)
        df[dep_var] = df[dep_var].str.replace(pattern, r'Return_to_owner', regex=True)
    else:
        pass


    # Sort data by AnimalID and DateTime
    df.sort_values(
        by=[
            AnimalID,
            "DateTime"
        ],
        ascending=[
            True,
            True
        ],
        ignore_index=True,
        inplace=True
    )

    # Age of animals
    df['AgeuponOutcome'] = df['AgeuponOutcome'].str.replace('  ', ' ')
    ## Convert age to days
    df['AgeuponOutcome'] = df['AgeuponOutcome'].apply(convert_to_days)
    ## Group ages into categories
    df['AgeuponOutcome'] = df['AgeuponOutcome'].apply(group_age)


    # Sex of animals
    ## remove multiple spaces
    df['SexuponOutcome'] = df['SexuponOutcome'].str.replace('  ', ' ')
    ## replace 'Unknown' with NaN
    df['SexuponOutcome'] = df['SexuponOutcome'].str.replace(r'unknown', '', regex=True, flags=re.IGNORECASE).str.strip().replace('', np.nan)
    ## split the column into two columns
    df['Sterilization'] = df['SexuponOutcome'].str.split(' ').str[0]
    df['SexuponOutcome'] = df['SexuponOutcome'].str.split(' ').str[1]
    ## combine "Spayed" and "Neutered" into "Sterilized"
    df['Sterilization'] = df['Sterilization'].replace({'Spayed': 'Sterilized', 'Neutered': 'Sterilized'})


    # Breed of animals
    df, breed, breed_mix = process_breed_data(df, AnimalID=AnimalID)


    # Coat of animals
    df, coat_color, coat_patterns = process_coat_colors(df, AnimalID=AnimalID)


    if dep_var in df.columns:
        animal_data = df[[AnimalID, dep_var, 'Name', 'DateTime', 'AnimalType', 'AgeuponOutcome', 'SexuponOutcome', 'Sterilization']].drop_duplicates().reset_index(drop=True)
    else:
        animal_data = df[[AnimalID, 'Name', 'DateTime', 'AnimalType', 'AgeuponOutcome', 'SexuponOutcome', 'Sterilization']].drop_duplicates().reset_index(drop=True)

    # Merge all the dataframes
    df = pd.merge(  # merge animal data with the breed and color related information
        left=animal_data,
        right=pd.merge(
            left=pd.merge(  # merge breed and breed mix
                left=breed.drop(columns='Breed'),
                right=breed_mix.drop(columns='Breed'),
                left_on=AnimalID,
                right_on=AnimalID,
                how='left'
            ),
            right=pd.merge(  # merge coat color and coat patterns
                left=coat_color.drop(columns='Color'),
                right=coat_patterns.drop(columns='Color'),
                left_on=AnimalID,
                right_on=AnimalID,
                how='left'
            ),
            left_on=AnimalID,
            right_on=AnimalID,
            how='outer'
        ),
        left_on=AnimalID,
        right_on=AnimalID,
        how='left'
    )


    return (df, animal_data, breed, breed_mix, coat_color, coat_patterns)


def process_data(
    raw_data_path: str,
    AnimalID: str="AnimalID",
    dep_var:str ="OutcomeType"
) -> pd.DataFrame:
    """
    Processes data from a specified file path by loading, preprocessing, and encoding categorical variables in sequence to prepare it for analysis or modeling.

    The function performs the following steps:
    1. Loads the data from the given file path. Ensure the file at `file_path` is accessible and in CSV format.
    2. Preprocesses the loaded DataFrame using specific rules.

    Parameters:
    - data_file (str): The name of the CSV file to load, excluding the `.csv` extension. It assumes that the actual file has a `.csv` extension appended.
    - AnimalID (str, optional): The name of the column in the DataFrame used as an identifier for individual animals. Defaults to "AnimalID".
    - dep_var (str, optional): The name of the dependent variable column, which is the target for prediction. Defaults to 'OutcomeType'.

    Returns:
    pandas.DataFrame: A processed DataFrame with loaded data that has been preprocessed.

    Example usage:
    processed_df = process_data("path/to/your/data.csv", AnimalID="UniqueID")
    """

    # Load data from the specified file path
    df = load_data(raw_data_path=raw_data_path, dep_var=dep_var)
    
    # Return preprocessed dataFrames
    return preprocess_data(df=df, AnimalID=AnimalID, dep_var=dep_var)
