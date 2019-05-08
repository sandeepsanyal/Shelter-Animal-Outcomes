# importing modules
import numpy as np
import pandas as pd

# folder path
directory = r"C:\Users\sande\OneDrive\Github\Shelter-Animal-Outcomes-by-kaggle.com"

# importing datasets
train = pd.read_csv(filepath_or_buffer=directory+r"\raw_datasets\train.csv",
                    sep=',',
                    encoding='latin-1')
score = pd.read_csv(filepath_or_buffer=directory+r"\raw_datasets\test.csv",
                    sep=',',
                    encoding='latin-1')

################################# working with Breed variable #################################
# grouping dog breeds using AKC grouping system
dog_breed = pd.read_excel(io=directory+r"\intermediate_results\Animal Breeds.xlsx",
                          sheet_name="Dog Breeds").replace(to_replace=np.nan, value='')
cat_breed = pd.read_excel(io=directory+r"\intermediate_results\Animal Breeds.xlsx",
                          sheet_name="Cat Breeds").replace(to_replace=np.nan, value='')
t=0
for i in train.index:
    t=t+1
    if train.loc[i, 'AnimalType'] == 'Dog':
        for j in dog_breed.index:
            train.loc[i, 'Breed1'] = train.loc[i, 'Breed'].replace(dog_breed.loc[j, 'Breed'],
                                                                   dog_breed.loc[j, 'BreedType'])
    else:
        for j in cat_breed.index:
            train.loc[i, 'Breed1'] = train.loc[i, 'Breed'].replace(cat_breed.loc[j, 'Breed'],
                                                                   cat_breed.loc[j, 'BreedType'])
    print(str(round(((t/train.shape[0])*100),2))+"% done")
