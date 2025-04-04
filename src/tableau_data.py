import sys
import pandas as pd


home_dir = r"/Users/wrngnfreeman/Github/Shelter-Animal-Outcomes"
data_file = r"Austin_Animal_Center_Outcomes_20250318"
AnimalID=r"AnimalID"
dep_var=r"OutcomeType"
export_location=r"/Users/wrngnfreeman/Library/CloudStorage/OneDrive-Personal/shared_projects/Shelter Animal Outcomes/intermediate_data"

# import required modules
sys.path.append(home_dir + r"/src")
import data_processing

# Load data from the specified file path
df = data_processing.load_data(home_dir=home_dir, data_file=data_file)

# Preprocess the loaded DataFrame
_, animal_data, breed, breed_mix, coat_color, coat_patterns = data_processing.preprocess_data(df=df, AnimalID=AnimalID, dep_var=dep_var)


# Finishing touches
## base animal info
animal_data.drop(columns=["Name", "DateTime"], inplace=True)
animal_data.rename(columns={
    "AgeuponOutcome": "AgeGroup",
    "SexuponOutcome": "Sex"
}, inplace=True)
## breed info
breed.drop(columns="Breed", inplace=True)
breed.rename(columns={"Breed_broken": "Breed"}, inplace=True)
breed.dropna(subset=["Breed"], inplace=True)
breed_mix.drop(columns=["Breed"], inplace=True)
breed_mix.rename(columns={"Mix": "BreedMix"}, inplace=True)
breed_mix["BreedMix"] = breed_mix["BreedMix"].str.replace("Mix", "Mixed Breed")
breed_mix["BreedMix"] = breed_mix["BreedMix"].str.replace("Pure breed", "Pure Breed")

breed_mix.rename(columns={"Mix": "BreedMix"}, inplace=True)
breed_mix.dropna(how="any", inplace=True)
# coat info
coat_color.drop(columns=["Color"], inplace=True)
coat_color.dropna(how="any", inplace=True)
coat_patterns.drop(columns=["Color"], inplace=True)
coat_patterns.dropna(how="any", inplace=True)

# Export animal_data Excel file
with pd.ExcelWriter(
    path=export_location + r"/animal_data.xlsx",
    mode="w",
    date_format="YYYY-MM-DD",
    datetime_format="YYYY-MM-DD"
) as writer:
    animal_data.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name=r"animal_data",
        engine="openpyxl"
    )
# Export breed Excel file
with pd.ExcelWriter(
    path=export_location + r"/breed.xlsx",
    mode="w",
    date_format="YYYY-MM-DD",
    datetime_format="YYYY-MM-DD"
) as writer:
    breed.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name=r"breed_type",
        engine="openpyxl"
    )
    breed_mix.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name=r"breed_mix",
        engine="openpyxl"
    )
# Export breed Excel file
with pd.ExcelWriter(
    path=export_location + r"/coat.xlsx",
    mode="w",
    date_format="YYYY-MM-DD",
    datetime_format="YYYY-MM-DD"
) as writer:
    coat_color.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name=r"coat_color",
        engine="openpyxl"
    )
    coat_patterns.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name=r"coat_pattern",
        engine="openpyxl"
    )
