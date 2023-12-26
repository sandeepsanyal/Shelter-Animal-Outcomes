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

## exporting main data
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

### exporting coat data
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
)["Breed"].values.tolist()
cat_breed_list = pd.read_excel(
    io=directory+r"/animal_type.xlsx",
    sheet_name=r"cat_breeds",
    engine="openpyxl"
)["Breed"].values.tolist()
breed = pd.DataFrame(
    {
        "AnimalID": [],
        "Breed": []
    }
)
for i in tqdm(dog_breed_list+cat_breed_list):
    for j in train.index:
        if i in train.loc[j, "Breed"]:
            breed = pd.concat(
                [
                    breed,
                    pd.DataFrame(
                        {
                            "AnimalID": [train.loc[j, "AnimalID"]],
                            "Breed": [i]
                        }
                    )
                ],
                axis=0
            ).reset_index(drop=True)
breed.loc[breed["Breed"]=="Pit Bull", "Breed"] = "Bull Terrier"
breed.loc[breed["Breed"]=="Yorkshire", "Breed"] = "Yorkshire Terrier"
### removing a case where Chihuahua Shorthair got tagged in both Chihuahua Shorthair & Shorthair. There are no just Shirthair dogs in out data
breed.drop(
    breed.loc[((breed["AnimalID"].isin(dogs)) & (breed["Breed"]=="Shorthair")), :].index,
    inplace=True
)
breed.loc[(breed["AnimalID"].isin(cats)) & (breed["Breed"]=="Shorthair"), "Breed"] = "Domestic Shorthair"

breed.drop_duplicates(inplace=True)

breed = pd.merge(
    left=breed,
    right=pd.read_excel(
        io=directory+r"/dog_breed_type.xlsx",
        sheet_name=r"Breed Type",
        engine="openpyxl"
    ),
    how="left",
    left_on="Breed",
    right_on="Breed"
)
breed.loc[breed["BreedType"]=="Unknown", "BreedType"] = np.NaN

mixed_breed = pd.DataFrame(
    {
        "AnimalID": train["AnimalID"],
        "MixType": [
            "Mix" if "Mix" in train.loc[i, "Breed"]\
            else np.NaN\
            for i in train.index
        ]
    }
).dropna()
temp = pd.DataFrame(
    data=breed['AnimalID'].value_counts()
).reset_index(drop=False).rename(
    columns={
        "index": "AnimalID",
        "AnimalID": "MixType"
    }
)
temp.loc[temp["MixType"] == 2, "MixType"] = "Mix"
temp.loc[temp["MixType"] == 1, "MixType"] = "Pure breed"
mixed_breed = pd.concat(
    [
        mixed_breed,
        temp
    ], axis=0
).drop_duplicates()
temp = pd.DataFrame(
    data=mixed_breed['AnimalID'].value_counts()
).reset_index(drop=False).rename(
    columns={
        "index": "AnimalID",
        "AnimalID": "Frequency"
    }
)
temp.loc[temp["Frequency"] == 2, "AnimalID"].values.tolist()
mixed_breed.loc[
    mixed_breed["AnimalID"].isin(temp.loc[temp["Frequency"] == 2, "AnimalID"].values.tolist()),
    "MixType"
] = "Mix"
mixed_breed.drop_duplicates(inplace=True)

### clubbing a couple of breeds with <15 observations
temp = pd.DataFrame(
    data=breed['Breed'].value_counts()
).reset_index(drop=False).rename(
    columns={
        "index": "Breed",
        "Breed": "Frequency"
    }
)
for i in tqdm(breed.index):
    if breed.loc[i, "Breed"] in temp.drop(temp[temp["Frequency"] >= 15].index)["Breed"].values.tolist():
        breed.loc[i, "Breed"] = np.NaN

### exporting breed data
with pd.ExcelWriter(
    path=directory+r"/breed.xlsx",
    engine='openpyxl',
    mode='w',
    date_format='DD-MMM-YYYY',
    datetime_format='DD-MMM-YYYY'
) as writer:
    breed.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='Breed Type'
    )
    mixed_breed.to_excel(
        excel_writer=writer,
        index=False,
        sheet_name='Mixed or Pure Breed'
    )

