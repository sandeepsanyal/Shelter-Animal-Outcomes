import time
import re

def calculate_elapsed_time(start_time):
    """
    Calculate elapsed time since a given start time.

    Args:
        start_time (float): Unix timestamp of the start time

    Returns:
        str: Formatted elapsed time in appropriate units
            (seconds, minutes, hours, days, or weeks)
    """
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
    elif elapsed_seconds < 86400:
        elapsed_hours = elapsed_seconds / 3600
        return f"{elapsed_hours:.2f} hours"
    elif elapsed_seconds < 604800:
        elapsed_days = elapsed_seconds / 86400
        return f"{elapsed_days:.2f} days"
    else:
        elapsed_weeks = elapsed_seconds / 604800
        return f"{elapsed_weeks:.2f} weeks"


def format_y_tick(value, tick_number):
    """
    Format numerical values for y-axis ticks with appropriate units.

    Args:
        value (int/float): Numeric value to format
        tick_number (int): Tick position index (unused in this implementation)

    Returns:
        str: Formatted value with unit suffix (K, M, B)
    """
    if value >= 1_000_000_000:
        return f'{value / 1_000_000_000:,.0f}B'
    elif value >= 1_000_000:
        return f'{value / 1_000_000:,.0f}M'
    elif value >= 1_000:
        return f'{value / 1_000:,.1f}K'
    else:
        return value
    

def clean_feature_name(name):
    """
    Clean feature names by replacing problematic characters.

    Args:
        name (str): Original feature name

    Returns:
        str: Cleaned feature name with special characters replaced
    """
    # Replace problematic characters with underscores or remove them
    cleaned_name = re.sub(r'[,\[\]<]', '_', name)
    
    return cleaned_name

