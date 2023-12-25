# importing modules
import numpy as np
import pandas as pd
from tqdm import tqdm

# folder path
directory = r"/Users/wrngnfreeman/Library/CloudStorage/OneDrive-Personal/shared_projects/Shelter Animal Outcomes"

# importing datasets
train = pd.read_csv(
    filepath_or_buffer=directory+r"/train.csv",
    sep=",",
    usecols=[
        "AnimalID",
        "DateTime",
        "OutcomeType",
        "AnimalType",
        "SexuponOutcome",
        "AgeuponOutcome",
        "Breed",
        "Color"
    ],
    encoding="latin-1"
)

# Data preparation
cats = train.loc[train["AnimalType"]=="Cat", "AnimalID"].values.tolist()
dogs = train.loc[train["AnimalType"]=="Dog", "AnimalID"].values.tolist()


## Date Time
train["DateTime"] = pd.to_datetime(
    arg=train["DateTime"],
    infer_datetime_format=True
)

## Sex upon outcome
train["SexuponOutcome"] = [
    train.loc[i, "SexuponOutcome"] if train.loc[i, "SexuponOutcome"] != "Unknown"\
    else np.NaN\
    for i in train.index
]
train[["SterilizationType", "Sex"]] = train["SexuponOutcome"].str.split(pat=" ", expand=True)
train["SterilizationType"] = [
    "Sterilized" if train.loc[i, "SterilizationType"] in ["Neutered", "Spayed"]\
    else train.loc[i, "SterilizationType"]\
    for i in train.index
]

## Age upon outcome
train = pd.merge(
    left=train,
    right=pd.read_excel(
        io=directory+r"/animal_type.xlsx",
        sheet_name=r"age_group",
        engine="openpyxl"
    ),
    how="left",
    left_on=["AgeuponOutcome"],
    right_on=["AgeuponOutcome"]
)

with pd.ExcelWriter(
    path=directory+r"/animal_data.xlsx",
    engine='openpyxl',
    mode='w',
    date_format='DD-MMM-YYYY',
    datetime_format='DD-MMM-YYYY HH:MM:SS'
) as writer:
    train[
        [
            "AnimalID",
            "DateTime",
            "OutcomeType",
            "AnimalType",
            "Age group",
            "Sex",
            "SterilizationType"
        ]
    ].to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='train'
    )

## Color
color_list = pd.read_excel(
    io=directory+r"/animal_type.xlsx",
    sheet_name=r"color",
    engine="openpyxl"
)["Color"].values.tolist()
coat_pattern_list = [
    i for i in pd.read_excel(
        io=directory+r"/animal_type.xlsx",
        sheet_name=r"color",
        engine="openpyxl"
    )["Coat pattern"].values.tolist() if str(i) != 'nan'
]

coat_color = pd.DataFrame(
    {
        "AnimalID": [],
        "CoatColor": []
    }
)
for i in tqdm(color_list):
    for j in train.index:
        if i in train.loc[j, "Color"]:
            coat_color = pd.concat(
                [
                    coat_color,
                    pd.DataFrame(
                        {
                            "AnimalID": [train.loc[j, "AnimalID"]],
                            "CoatColor": [i]
                        }
                    )
                ],
                axis=0
            )

coat_color.loc[(coat_color["AnimalID"].isin(dogs)) & (coat_color["CoatColor"]=="Orange"), "CoatColor"] = "Red"
coat_color.loc[(coat_color["AnimalID"].isin(cats)) & (coat_color["CoatColor"]=="Yellow"), "CoatColor"] = "Orange"
coat_color.loc[(coat_color["AnimalID"].isin(cats)) & (coat_color["CoatColor"]=="Tricolor"), "CoatColor"] = "Calico"
coat_color.loc[coat_color["CoatColor"]=="Buff", "CoatColor"] = "Cream"
coat_color.loc[coat_color["CoatColor"]=="Pink", "CoatColor"] = "White"
coat_color.loc[coat_color["CoatColor"]=="Tan", "CoatColor"] = "Cream"
coat_color.loc[coat_color["CoatColor"]=="Silver", "CoatColor"] = "White"
coat_color.loc[coat_color["CoatColor"]=="Apricot", "CoatColor"] = "Cream"
coat_color.loc[coat_color["CoatColor"]=="Flame", "CoatColor"] = "Orange"
coat_color.loc[coat_color["CoatColor"]=="Gold", "CoatColor"] = "Yellow"
coat_color.drop_duplicates(inplace=True)

coat_pattern = pd.DataFrame(
    {
        "AnimalID": [],
        "CoatPattern": []
    }
)
for i in tqdm(coat_pattern_list):
    for j in train.index:
        if i in train.loc[j, "Color"]:
            coat_pattern = pd.concat(
                [
                    coat_pattern,
                    pd.DataFrame(
                        {
                            "AnimalID": [train.loc[j, "AnimalID"]],
                            "CoatPattern": [i]
                        }
                    )
                ],
                axis=0
            )
with pd.ExcelWriter(
    path=directory+r"/coat.xlsx",
    engine='openpyxl',
    mode='w',
    date_format='DD-MMM-YYYY',
    datetime_format='DD-MMM-YYYY'
) as writer:
    coat_color.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='Coat Color'
    )
    coat_pattern.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='Coat Pattern'
    )

## Breed
dog_breed_list = pd.read_excel(
    io=directory+r"/dog_breed_type.xlsx",
    sheet_name=r"Breed Type",
    engine="openpyxl"
)["AnimalType"].values.tolist()
cat_breed_list = pd.read_excel(
    io=directory+r"/animal_type.xlsx",
    sheet_name=r"cat_breeds",
    engine="openpyxl"
)["AnimalType"].values.tolist()
breed_type = pd.DataFrame(
    {
        "AnimalID": [],
        "BreedType": []
    }
)
for i in tqdm(dog_breed_list+cat_breed_list):
    for j in train.index:
        if i in train.loc[j, "Breed"]:
            breed_type = pd.concat(
                [
                    breed_type,
                    pd.DataFrame(
                        {
                            "AnimalID": [train.loc[j, "AnimalID"]],
                            "BreedType": [i]
                        }
                    )
                ],
                axis=0
            ).reset_index(drop=True)
for i in breed_type.index:
    if breed_type.loc[i, "BreedType"] == "Pit Bull":
        breed_type.loc[i, "BreedType"] = "Bull Terrier"
    elif breed_type.loc[i, "BreedType"] == "Yorkshire":
        breed_type.loc[i, "BreedType"] = "Yorkshire Terrier"
    else:
        pass
breed_type.drop_duplicates(inplace=True)

mixed_breed = pd.DataFrame(
    {
        "AnimalID": train["AnimalID"],
        "MixType": [
            "Mix" if "Mix" in train.loc[i, "Breed"]\
            else np.NaN\
            for i in train.index
        ]
    }
)
temp = pd.DataFrame(
    data=breed_type['AnimalID'].value_counts()
).reset_index(drop=False).rename(
    columns={
        "index": "AnimalID",
        "AnimalID": "Frequency"
    }
)
for i in tqdm(mixed_breed.index):
    if mixed_breed.loc[i, "AnimalID"] in temp.drop(temp[temp["Frequency"] < 2].index)["AnimalID"].values.tolist():
        mixed_breed.loc[i, "MixType"] = "Mix"
    if str(mixed_breed.loc[i, "MixType"]) == "nan":
        mixed_breed.loc[i, "MixType"] = "Pure breed"

with pd.ExcelWriter(
    path=directory+r"/breed.xlsx",
    engine='openpyxl',
    mode='w',
    date_format='DD-MMM-YYYY',
    datetime_format='DD-MMM-YYYY'
) as writer:
    breed_type.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='Breed Type'
    )
    mixed_breed.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='Mixed or Pure Breed'
    )

