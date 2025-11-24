"""
Dependency injection functions
"""

import os
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from ..config import settings
import io


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


def load_csv_from_s3(s3_prefix: str, column_names: list) -> pd.DataFrame:
    """
    Load CSV data from S3 MapReduce output (combines all part files)
    
    Args:
        s3_prefix: S3 prefix/folder containing MapReduce output parts
        column_names: List of column names for the DataFrame
        
    Returns:
        DataFrame with the data
        
    Raises:
        HTTPException: If files cannot be loaded from S3
    """
    try:
        s3_client = boto3.client('s3', region_name=settings.aws_region)
        
        # List all part files in the S3 prefix
        response = s3_client.list_objects_v2(
            Bucket=settings.s3_bucket,
            Prefix=s3_prefix
        )
        
        if 'Contents' not in response:
            raise HTTPException(
                status_code=404,
                detail=f"No files found in S3 at: {s3_prefix}"
            )
        
        # Filter for part files (exclude _SUCCESS and directory markers)
        part_files = [
            obj['Key'] for obj in response['Contents']
            if 'part-' in obj['Key'] and obj['Size'] > 0
        ]
        
        if not part_files:
            raise HTTPException(
                status_code=404,
                detail=f"No part files found in S3 at: {s3_prefix}"
            )
        
        # Download and combine all part files
        dfs = []
        for part_file in sorted(part_files):
            obj = s3_client.get_object(Bucket=settings.s3_bucket, Key=part_file)
            content = obj['Body'].read().decode('utf-8')
            
            # Read tab-separated values (MapReduce output format)
            # Note: Hadoop output has quoted strings and embedded tabs
            df_part = pd.read_csv(
                io.StringIO(content),
                sep='\t',
                header=None,
                quotechar='"',
                skipinitialspace=True
            )
            
            # Handle cases where multiple values are in a single column (from Hadoop reducer)
            # Example: "2022-01"\t"24.75\t14.52" where second column has embedded tab
            if len(df_part.columns) == 2 and len(column_names) > 2:
                # Split the second column - note that Hadoop outputs literal \t not actual tabs
                split_cols = df_part.iloc[:, 1].str.replace('\\t', '\t').str.split('\t', expand=True)
                
                # Create DataFrame with proper column names
                data = {column_names[0]: df_part.iloc[:, 0].str.strip('"')}
                for i, col_name in enumerate(column_names[1:]):
                    data[col_name] = pd.to_numeric(split_cols[i], errors='coerce')
                
                df_part = pd.DataFrame(data)
            else:
                # Assign column names if dimensions match
                df_part.columns = column_names
            
            dfs.append(df_part)
        
        # Combine all parts
        df = pd.concat(dfs, ignore_index=True)
        
        return df
        
    except ClientError as e:
        import traceback
        error_detail = f"S3 access error: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )
    except pd.errors.EmptyDataError as e:
        import traceback
        error_detail = f"Results files are empty at: {s3_prefix}\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )
    except Exception as e:
        import traceback
        error_detail = f"Error loading results from S3: {str(e)}\nTraceback:\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )


def load_csv_data(filename: str, column_names: list) -> pd.DataFrame:
    """
    Load CSV data from results file (tries S3 first, then local)
    
    Args:
        filename: Name of the results file or S3 prefix
        column_names: List of column names for the DataFrame
        
    Returns:
        DataFrame with the data
        
    Raises:
        HTTPException: If file cannot be loaded
    """
    # Try loading from S3 first if S3 is configured
    if settings.use_s3:
        # Map filename to S3 prefix
        s3_prefix_map = {
            settings.monthly_avg_file: "output/monthly_avg/",
            settings.extreme_temps_file: "output/extreme_temps/",
            settings.temp_precip_file: "output/temp_precip/"
        }
        
        s3_prefix = s3_prefix_map.get(filename)
        if s3_prefix:
            try:
                return load_csv_from_s3(s3_prefix, column_names)
            except HTTPException:
                # If S3 fails, fall back to local files
                pass
    
    # Fall back to local file loading
    try:
        file_path = get_results_file_path(filename)
        
        # Read tab-separated values (MapReduce output format)
        df = pd.read_csv(
            file_path, 
            sep='\t', 
            header=None,
            quotechar='"',
            skipinitialspace=True
        )
        
        # Handle cases where multiple values are in a single column (from Hadoop reducer)
        if len(df.columns) == 2 and len(column_names) > 2:
            # Split the second column - note that Hadoop outputs literal \t not actual tabs
            split_cols = df.iloc[:, 1].str.replace('\\t', '\t').str.split('\t', expand=True)
            
            # Create DataFrame with proper column names
            data = {column_names[0]: df.iloc[:, 0].str.strip('"')}
            # split_cols has indices 0, 1, 2... for the values from the second column
            for i, col_name in enumerate(column_names[1:]):
                data[col_name] = pd.to_numeric(split_cols[i], errors='coerce')
            
            df = pd.DataFrame(data)
        else:
            # Assign column names if dimensions match
            df.columns = column_names
        
        return df
        
    except pd.errors.EmptyDataError as e:
        import traceback
        error_detail = f"Results file is empty: {filename}\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )
    except Exception as e:
        import traceback
        error_detail = f"Error loading results: {str(e)}\nTraceback:\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=500,
            detail=error_detail
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
