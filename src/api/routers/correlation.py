"""
Router for temperature-precipitation correlation endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

from ..models.schemas import TempPrecipCorrelation
from ..dependencies.file_handler import load_csv_data
from ..config import settings

router = APIRouter(
    prefix="/temp-precipitation",
    tags=["Temperature-Precipitation Correlation"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=List[TempPrecipCorrelation],
    summary="Get temperature-precipitation correlation",
    description="Retrieve monthly correlation between temperature and precipitation"
)
async def get_temp_precipitation():
    """
    Get temperature-precipitation correlation results from MapReduce job
    
    Returns monthly data including:
    - Pearson correlation coefficient
    - Average temperature
    - Average precipitation
    - Number of rainy days
    - Total precipitation
    """
    try:
        # Load data from MapReduce output
        df = load_csv_data(
            settings.temp_precip_file,
            column_names=['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']
        )
        
        # Handle cases where data is in a single column
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['correlation'] = pd.to_numeric(split_data[0], errors='coerce')
            df['avg_temp'] = pd.to_numeric(split_data[1], errors='coerce')
            df['avg_precip'] = pd.to_numeric(split_data[2], errors='coerce')
            df['rainy_days'] = pd.to_numeric(split_data[3], errors='coerce').astype(int)
            df['total_precip'] = pd.to_numeric(split_data[4], errors='coerce')
            df = df[['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']]
        
        # Convert to list of dictionaries
        return df.to_dict('records')
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing correlation data: {str(e)}"
        )


@router.get(
    "/wettest-month",
    summary="Get wettest month",
    description="Find the month with the highest precipitation"
)
async def get_wettest_month():
    """
    Get the month with the highest total precipitation
    """
    try:
        df = load_csv_data(
            settings.temp_precip_file,
            column_names=['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']
        )
        
        # Handle data format
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['correlation'] = pd.to_numeric(split_data[0], errors='coerce')
            df['avg_temp'] = pd.to_numeric(split_data[1], errors='coerce')
            df['avg_precip'] = pd.to_numeric(split_data[2], errors='coerce')
            df['rainy_days'] = pd.to_numeric(split_data[3], errors='coerce').astype(int)
            df['total_precip'] = pd.to_numeric(split_data[4], errors='coerce')
            df = df[['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']]
        
        # Find wettest month
        wettest = df.loc[df['total_precip'].idxmax()]
        
        return wettest.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding wettest month: {str(e)}"
        )


@router.get(
    "/driest-month",
    summary="Get driest month",
    description="Find the month with the lowest precipitation"
)
async def get_driest_month():
    """
    Get the month with the lowest total precipitation
    """
    try:
        df = load_csv_data(
            settings.temp_precip_file,
            column_names=['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']
        )
        
        # Handle data format
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['correlation'] = pd.to_numeric(split_data[0], errors='coerce')
            df['avg_temp'] = pd.to_numeric(split_data[1], errors='coerce')
            df['avg_precip'] = pd.to_numeric(split_data[2], errors='coerce')
            df['rainy_days'] = pd.to_numeric(split_data[3], errors='coerce').astype(int)
            df['total_precip'] = pd.to_numeric(split_data[4], errors='coerce')
            df = df[['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']]
        
        # Find driest month
        driest = df.loc[df['total_precip'].idxmin()]
        
        return driest.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding driest month: {str(e)}"
        )


@router.get(
    "/correlation-strength",
    summary="Interpret correlation strength",
    description="Get interpretation of correlation strength for each month"
)
async def get_correlation_interpretation():
    """
    Interpret the strength of temperature-precipitation correlation
    """
    try:
        df = load_csv_data(
            settings.temp_precip_file,
            column_names=['month', 'correlation', 'avg_temp', 'avg_precip', 'rainy_days', 'total_precip']
        )
        
        # Handle data format
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['correlation'] = pd.to_numeric(split_data[0], errors='coerce')
            df = df[['month', 'correlation']]
        
        def interpret_correlation(corr):
            """Interpret correlation coefficient"""
            abs_corr = abs(corr)
            if abs_corr >= 0.7:
                strength = "strong"
            elif abs_corr >= 0.4:
                strength = "moderate"
            elif abs_corr >= 0.2:
                strength = "weak"
            else:
                strength = "very weak"
            
            direction = "negative" if corr < 0 else "positive"
            return f"{strength} {direction}"
        
        results = []
        for _, row in df.iterrows():
            results.append({
                "month": row['month'],
                "correlation": float(row['correlation']),
                "interpretation": interpret_correlation(row['correlation'])
            })
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interpreting correlation: {str(e)}"
        )
