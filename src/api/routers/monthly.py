"""
Router for monthly average temperature endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

from ..models.schemas import MonthlyAverage
from ..dependencies.file_handler import load_csv_data
from ..config import settings

router = APIRouter(
    prefix="/monthly-avg",
    tags=["Monthly Averages"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=List[MonthlyAverage],
    summary="Get monthly average temperatures",
    description="Retrieve monthly average maximum and minimum temperatures for Medellín"
)
async def get_monthly_averages():
    """
    Get monthly average temperature results from MapReduce job
    
    Returns a list of monthly averages with:
    - Month (YYYY-MM format)
    - Average maximum temperature
    - Average minimum temperature
    """
    try:
        # Load data from MapReduce output
        df = load_csv_data(
            settings.monthly_avg_file,
            column_names=['month', 'avg_max', 'avg_min']
        )
        
        # Handle cases where avg_max and avg_min are in a single column
        if len(df.columns) == 2:
            # Split the second column by tab
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['avg_max'] = pd.to_numeric(split_data[0], errors='coerce')
            df['avg_min'] = pd.to_numeric(split_data[1], errors='coerce')
            df = df[['month', 'avg_max', 'avg_min']]
        
        # Convert to list of dictionaries
        return df.to_dict('records')
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing monthly averages: {str(e)}"
        )


@router.get(
    "/hottest",
    response_model=MonthlyAverage,
    summary="Get hottest month",
    description="Find the month with the highest average maximum temperature"
)
async def get_hottest_month():
    """
    Get the hottest month based on average maximum temperature
    """
    try:
        df = load_csv_data(
            settings.monthly_avg_file,
            column_names=['month', 'avg_max', 'avg_min']
        )
        
        # Handle data format
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['avg_max'] = pd.to_numeric(split_data[0], errors='coerce')
            df['avg_min'] = pd.to_numeric(split_data[1], errors='coerce')
            df = df[['month', 'avg_max', 'avg_min']]
        
        # Find hottest month
        hottest = df.loc[df['avg_max'].idxmax()]
        
        return hottest.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding hottest month: {str(e)}"
        )


@router.get(
    "/coolest",
    response_model=MonthlyAverage,
    summary="Get coolest month",
    description="Find the month with the lowest average minimum temperature"
)
async def get_coolest_month():
    """
    Get the coolest month based on average minimum temperature
    """
    try:
        df = load_csv_data(
            settings.monthly_avg_file,
            column_names=['month', 'avg_max', 'avg_min']
        )
        
        # Handle data format
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['avg_max'] = pd.to_numeric(split_data[0], errors='coerce')
            df['avg_min'] = pd.to_numeric(split_data[1], errors='coerce')
            df = df[['month', 'avg_max', 'avg_min']]
        
        # Find coolest month
        coolest = df.loc[df['avg_min'].idxmin()]
        
        return coolest.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding coolest month: {str(e)}"
        )
