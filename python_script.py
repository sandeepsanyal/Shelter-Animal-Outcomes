# importing modules
import pandas as pd

# folder paths
raw_data_folder_path = r"C:\Users\sande\OneDrive\Github\Shelter-Animal-Outcomes-by-kaggle.com\raw_datasets" # folder containing raw_datasets
intermediate_results_folder_path = r"C:\Users\sande\OneDrive\Github\Shelter-Animal-Outcomes-by-kaggle.com\rintermediate_results" # folder containing intermediate results
temp_folder_path = r"C:\Users\sande\OneDrive\Github\Shelter-Animal-Outcomes-by-kaggle.com\temp" # folder containing temp_files

# importing datasets
train = pd.read_csv(filepath_or_buffer=raw_data_folder_path+r"\train.csv",
                    sep=',',
                    encoding='latin-1')
score = pd.read_csv(filepath_or_buffer=raw_data_folder_path+r"\test.csv",
                    sep=',',
                    encoding='latin-1')

