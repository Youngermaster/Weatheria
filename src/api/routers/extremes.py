"""
Router for extreme temperature endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

from ..models.schemas import ExtremeTemperature
from ..dependencies.file_handler import load_csv_data
from ..config import settings

router = APIRouter(
    prefix="/extreme-temps",
    tags=["Extreme Temperatures"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=List[ExtremeTemperature],
    summary="Get extreme temperature statistics",
    description="Retrieve counts of days with extreme temperature conditions"
)
async def get_extreme_temperatures():
    """
    Get extreme temperature detection results from MapReduce job
    
    Categories:
    - very_hot: Maximum temperature > 30°C
    - cool: Minimum temperature < 15°C
    - very_cool: Minimum temperature < 12°C
    - normal: All other days
    """
    try:
        # Load data from MapReduce output
        df = load_csv_data(
            settings.extreme_temps_file,
            column_names=['category', 'count', 'avg_temp']
        )
        
        # Handle cases where count and avg_temp are in a single column
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['count'] = pd.to_numeric(split_data[0], errors='coerce').astype(int)
            df['avg_temp'] = pd.to_numeric(split_data[1], errors='coerce')
            df = df[['category', 'count', 'avg_temp']]
        
        # Convert to list of dictionaries
        return df.to_dict('records')
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing extreme temperatures: {str(e)}"
        )


@router.get(
    "/summary",
    summary="Get extreme temperature summary",
    description="Get a summary of extreme temperature occurrences"
)
async def get_extreme_summary():
    """
    Get a summary of extreme temperature events
    """
    try:
        df = load_csv_data(
            settings.extreme_temps_file,
            column_names=['category', 'count', 'avg_temp']
        )
        
        # Handle data format
        if len(df.columns) == 2:
            split_data = df.iloc[:, 1].str.split('\t', expand=True)
            df['count'] = pd.to_numeric(split_data[0], errors='coerce').astype(int)
            df['avg_temp'] = pd.to_numeric(split_data[1], errors='coerce')
            df = df[['category', 'count', 'avg_temp']]
        
        total_days = df['count'].sum()
        
        summary = {
            "total_days_analyzed": int(total_days),
            "categories": {}
        }
        
        for _, row in df.iterrows():
            category = row['category']
            count = int(row['count'])
            percentage = round((count / total_days * 100), 2) if total_days > 0 else 0
            
            summary["categories"][category] = {
                "count": count,
                "percentage": percentage,
                "avg_temp": float(row['avg_temp'])
            }
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {str(e)}"
        )
