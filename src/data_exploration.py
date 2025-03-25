import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns


home_dir = r"/Users/wrngnfreeman/Library/CloudStorage/OneDrive-Personal/shared_projects/Shelter Animal Outcomes/Shelter-Animal-Outcomes-by-kaggle.com"
data_file = r"train"
AnimalID=r"AnimalID"
dep_var=r"OutcomeType"


# import required modules
sys.path.append(home_dir + r"/src")
import data_processing, utils

# Load and process training data
processed_df = data_processing.process_data(
    home_dir=home_dir,
    data_file=data_file,
    AnimalID=AnimalID,
    dep_var=dep_var
)


# Data exploration

## Visualize the distribution of the dependent variable

# Define the order and colors for OutcomeType
order = ["Adoption", "Return_to_owner", "Transfer", "Euthanasia", "Died"]
colors = ["#76C7C0", "#6495ED", "#DA70D6", "#FFA07A", "#FF4500"]
# Count the occurrences of each OutcomeType
outcome_counts = processed_df['OutcomeType'].value_counts().reindex(order, fill_value=0)
# Calculate the total number of animals
total_animals = outcome_counts.sum()
# Calculate the percentage of each OutcomeType
percentages = (outcome_counts / total_animals) * 100
# Create a custom palette dictionary
custom_palette = dict(zip(order, colors))
# Create a DataFrame from the counts for plotting
plot_df = pd.DataFrame({
    'OutcomeType': outcome_counts.index,
    'Count': outcome_counts.values
})
# Create the bar chart using the pre-calculated data
plt.figure(figsize=(6, 6))
ax = sns.barplot(
    x='OutcomeType',
    y='Count',
    data=plot_df,
    palette=custom_palette,
    hue='OutcomeType',  # Assigning 'OutcomeType' to hue
    legend=False        # Setting legend to False as we don't need it
)
# Set the main title and subtitle
plt.suptitle('Distribution of OutcomeType', fontsize=18)
plt.title('Dependent Variable "OutcomeType" is imbalanced with\n<6% as "Euthanasia", and <1% as "Died"', fontsize=12)
# Set the labels
plt.xlabel('Outcome Type', fontsize=10)
plt.ylabel('Number of Animals (Total: {:,})'.format(total_animals), fontsize=10)
# Format axis ticks
plt.tick_params(axis='x', labelsize=9)  # Size for x-axis ticks
plt.tick_params(axis='y', labelsize=9)  # Size for y-axis ticks
ax.yaxis.set_major_formatter(plt.FuncFormatter(utils.format_y_tick))  # Custom formatter for y-axis ticks
# Add percentage labels on top of each bar
for i, count in enumerate(outcome_counts.values):
    ax.text(i, count + 0.005 * max(outcome_counts), f'{percentages.iloc[i]:.1f}%', ha='center', va='bottom', fontsize=9)
# Show the plot
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()



# Simlarly, show bar chart for 'Animal Type'. But with horizontal bars.
# Define the order and colors for AnimalType
order = ["Dog", "Cat"]
colors = ["#8E9498", "#2D3033"]
# Count the occurrences of each AnimalType
animal_counts = processed_df['AnimalType'].value_counts().reindex(order, fill_value=0)
# Calculate the total number of animals
total_animals = animal_counts.sum()
# Calculate the percentage of each AnimalType
percentages = (animal_counts / total_animals) * 100
# Create a custom palette dictionary
custom_palette = dict(zip(order, colors))
# Create a DataFrame from the counts for plotting
plot_df = pd.DataFrame({
    'AnimalType': animal_counts.index,
    'Count': animal_counts.values
})
# Create the horizontal bar chart using the pre-calculated data
plt.figure(figsize=(9, 2))
ax = sns.barplot(
    x='Count',
    y='AnimalType',
    data=plot_df,
    palette=custom_palette,
    hue='AnimalType',  # Assigning 'AnimalType' to hue
    legend=False       # Setting legend to False as we don't need it
)
# Set the main title and subtitle
plt.suptitle('Distribution of AnimalType', fontsize=18)
plt.title('Shelter has twice the number of Dogs than Cats', fontsize=12)
# Set the labels
plt.xlabel('Number of Animals (Total: {:,})'.format(total_animals), fontsize=10)
plt.ylabel('Animal Type', fontsize=10)
# Format axis ticks
plt.tick_params(axis='x', labelsize=9)  # Size for x-axis ticks
plt.tick_params(axis='y', labelsize=9)  # Size for y-axis ticks
ax.xaxis.set_major_formatter(plt.FuncFormatter(utils.format_y_tick))  # Custom formatter for y-axis ticks
# Add percentage labels on the right side of each bar
for i, count in enumerate(animal_counts.values):
    ax.text(count + 0.005 * max(animal_counts), i, f'{percentages.iloc[i]:.1f}%', ha='left', va='center', fontsize=9)
# Show the plot
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()



# Same with AgeuponOutcome
# Define the order and colors for AgeuponOutcome
order = ['<1 week', '<1 month', '<6 months', '<1 year', '<5 years', '<10 years', '<15 years', '15+ years']
colors = ['#0C85EE' for i in order]
# Count the occurrences of each AgeuponOutcome
outcome_counts = processed_df.loc[processed_df["AgeuponOutcome"].notna(), 'AgeuponOutcome'].value_counts().reindex(order, fill_value=0)
# Calculate the total number of animals
total_animals = outcome_counts.sum()
# Calculate the percentage of each AgeuponOutcome
percentages = (outcome_counts / total_animals) * 100
# Create a custom palette dictionary
custom_palette = dict(zip(order, colors))
# Create a DataFrame from the counts for plotting
plot_df = pd.DataFrame({
    'AgeuponOutcome': outcome_counts.index,
    'Count': outcome_counts.values
})
# Create the bar chart using the pre-calculated data
plt.figure(figsize=(6, 6))
ax = sns.barplot(
    x='AgeuponOutcome',
    y='Count',
    data=plot_df,
    palette=custom_palette,
    hue='AgeuponOutcome',  # Assigning 'AgeuponOutcome' to hue
    legend=False           # Setting legend to False as we don't need it
)
# Set the main title and subtitle
plt.suptitle('Distribution of Age Groups', fontsize=18)
plt.title('Almost 70% of the animals are\nbetween 1-6 months or between 1-5 years of age', fontsize=12)
# Set the labels
plt.xlabel('Age Group', fontsize=10)
plt.ylabel('Number of Animals (Total: {:,})'.format(total_animals), fontsize=10)
# Format axis ticks
plt.tick_params(axis='x', labelsize=9)  # Size for x-axis ticks
plt.tick_params(axis='y', labelsize=9)  # Size for y-axis ticks
ax.yaxis.set_major_formatter(plt.FuncFormatter(utils.format_y_tick))  # Custom formatter for y-axis ticks
# Add percentage labels on top of each bar
for i, count in enumerate(outcome_counts.values):
    ax.text(i, count + 0.005 * max(outcome_counts), f'{percentages.iloc[i]:.1f}%', ha='center', va='bottom', fontsize=9)
# Show the plot
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()





# Function to filter top 5 coat colors for a given animal type
def get_top_coat_colors(df, animal_type, top_n=5):
    # Filter data for the given animal type
    filtered_df = df[df['AnimalType'] == animal_type]
    # Calculate the value counts for CoatColor
    total_counts = filtered_df['CoatColor'].count()
    coat_color_counts = filtered_df['CoatColor'].value_counts().head(top_n)
    # Get the index (coat colors) of the top 5 most common coat colors
    top_coat_colors = coat_color_counts.index.tolist()
    return top_coat_colors, coat_color_counts, total_counts

# Get top 5 coat colors and their counts for Cats and Dogs
top_cats, cat_counts, total_cats = get_top_coat_colors(processed_df, 'Cat')
top_dogs, dog_counts, total_dogs = get_top_coat_colors(processed_df, 'Dog')

# Determine the maximum count from both datasets
max_count = ((max(cat_counts.max(), dog_counts.max()) // 1000) + 1) * 1000

# Set up the matplotlib figure
plt.figure(figsize=(14, 6))
plt.suptitle('White, Black and Brown are most common coat colors for both Cats and Dogs', fontsize=18)

# Create a subplot for Cats
ax1 = plt.subplot(1, 2, 1)
sns.countplot(x='CoatColor', data=processed_df[processed_df['AnimalType'] == 'Cat'], order=top_cats)
plt.title('Distribution of Coat Color for Cats')
plt.xlabel('Coat Color')
plt.ylabel('Number of Cats (Total: {:,})'.format(total_cats), fontsize=10)
plt.ylim(0, max_count)  # Set the y-axis limit to the maximum count
# Format axis ticks
plt.tick_params(axis='x', labelsize=9)  # Size for x-axis ticks
plt.tick_params(axis='y', labelsize=9)  # Size for y-axis ticks
# Annotate bars with percentages for Cats
for p in ax1.patches:
    height = p.get_height()
    percentage = (height / total_cats) * 100
    ax1.annotate(f'{percentage:.2f}%', 
                 (p.get_x() + p.get_width() / 2., height), 
                 ha='center', va='bottom', fontsize=9, color='black')

# Create a subplot for Dogs
ax2 = plt.subplot(1, 2, 2)
sns.countplot(x='CoatColor', data=processed_df[processed_df['AnimalType'] == 'Dog'], order=top_dogs)
plt.title('Distribution of Coat Color for Dogs', fontsize=12)
plt.xlabel('Coat Color')
plt.ylabel('Number of Dogs (Total: {:,})'.format(total_dogs), fontsize=10)
plt.ylim(0, max_count)  # Set the y-axis limit to the maximum count
# Format axis ticks
plt.tick_params(axis='x', labelsize=9)  # Size for x-axis ticks
plt.tick_params(axis='y', labelsize=9)  # Size for y-axis ticks
# Annotate bars with percentages for Dogs
for p in ax2.patches:
    height = p.get_height()
    percentage = (height / total_dogs) * 100
    ax2.annotate(f'{percentage:.2f}%', 
                 (p.get_x() + p.get_width() / 2., height), 
                 ha='center', va='bottom', fontsize=9, color='black')
# Apply the custom y-axis formatter to both subplots
formatter = FuncFormatter(utils.format_y_tick)
plt.gca().yaxis.set_major_formatter(formatter)  # This applies to the last subplot by default
# Get all axes and apply the formatter to each
axes = plt.gcf().get_axes()
for ax in axes:
    ax.yaxis.set_major_formatter(formatter)

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
