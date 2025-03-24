import time
import re

def calculate_elapsed_time(start_time):
    # Get the current time
    end_time = time.time()
    
    # Calculate elapsed time in seconds
    elapsed_seconds = end_time - start_time
    
    # Determine appropriate unit and format for display
    if elapsed_seconds < 60:
        return f"{elapsed_seconds:.2f} seconds"
    elif elapsed_seconds < 3600:
        elapsed_minutes = elapsed_seconds / 60
        return f"{elapsed_minutes:.2f} minutes"
    elif elapsed_hours < elapsed_seconds / 3600:
        elapsed_minutes = elapsed_seconds / 3600
        return f"{elapsed_hours:.2f} hours"
    elif elapsed_hours < elapsed_seconds / 86400:
        elapsed_minutes = elapsed_seconds / 86400
        return f"{elapsed_hours:.2f} days"
    else:
        elapsed_hours = elapsed_seconds / 604800
        return f"{elapsed_hours:.2f} weeks"


# Function to format y-axis ticks as "#,##0 K", "#,##0 M", "#,##0 B"
def format_y_tick(value, tick_number):
    if value >= 1_000_000_000:
        return f'{value / 1_000_000_000:,.0f}B'
    elif value >= 1_000_000:
        return f'{value / 1_000_000:,.0f}M'
    elif value >= 1_000:
        return f'{value / 1_000:,.1f}K'
    else:
        return value
    

# Function to clean feature names
def clean_feature_name(name):
    # Replace problematic characters with underscores or remove them
    cleaned_name = re.sub(r'[,\[\]<]', '_', name)
    
    return cleaned_name
