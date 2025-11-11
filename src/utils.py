"""
Utility functions for the NL Query System
"""
import pandas as pd
from datetime import datetime
from typing import Any


def format_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format a DataFrame for better display in Streamlit.
    
    Args:
        df: DataFrame to format
        
    Returns:
        pd.DataFrame: Formatted DataFrame
    """
    if df.empty:
        return df
    
    # Format date columns
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].dt.strftime('%Y-%m-%d')
    
    # Replace NaN/None with empty string for better display
    df = df.fillna('')
    
    return df


def parse_date_string(date_str: str) -> datetime:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        datetime: Parsed datetime object
    """
    formats = [
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%m/%d/%Y',
        '%d/%m/%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'


def format_percentage(value: float) -> str:
    """
    Format a percentage value.
    
    Args:
        value: Percentage value (0-100)
        
    Returns:
        str: Formatted percentage string
    """
    return f"{value:.1f}%"


def safe_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary.
    
    Args:
        dictionary: Dictionary to get value from
        key: Key to look up
        default: Default value if key not found
        
    Returns:
        Any: Value from dictionary or default
    """
    return dictionary.get(key, default)
