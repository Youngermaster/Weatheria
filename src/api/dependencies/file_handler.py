"""
Dependency injection functions
"""

import os
import pandas as pd
from fastapi import HTTPException
from ..config import settings


def get_results_file_path(filename: str) -> str:
    """
    Get the full path to a results file
    
    Args:
        filename: Name of the results file
        
    Returns:
        Full path to the file
        
    Raises:
        HTTPException: If file doesn't exist
    """
    file_path = os.path.join(settings.results_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Results file not found: {filename}"
        )
    
    return file_path


def load_csv_data(filename: str, column_names: list) -> pd.DataFrame:
    """
    Load CSV data from results file
    
    Args:
        filename: Name of the results file
        column_names: List of column names for the DataFrame
        
    Returns:
        DataFrame with the data
        
    Raises:
        HTTPException: If file cannot be loaded
    """
    try:
        file_path = get_results_file_path(filename)
        
        # Read tab-separated values (MapReduce output format)
        df = pd.read_csv(file_path, sep='\t', names=column_names, header=None)
        
        return df
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=500,
            detail=f"Results file is empty: {filename}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading results: {str(e)}"
        )


def ensure_results_directory():
    """
    Ensure the results directory exists
    
    Raises:
        HTTPException: If directory cannot be created or accessed
    """
    try:
        os.makedirs(settings.results_dir, exist_ok=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cannot access results directory: {str(e)}"
        )
