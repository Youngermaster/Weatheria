"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional


class MonthlyAverage(BaseModel):
    """Monthly average temperature model"""
    month: str = Field(..., description="Year-month (YYYY-MM)")
    avg_max: float = Field(..., description="Average maximum temperature (°C)")
    avg_min: float = Field(..., description="Average minimum temperature (°C)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "month": "2022-01",
                "avg_max": 28.5,
                "avg_min": 17.2
            }
        }


class ExtremeTemperature(BaseModel):
    """Extreme temperature detection model"""
    category: str = Field(..., description="Temperature category")
    count: int = Field(..., description="Number of days in this category")
    avg_temp: float = Field(..., description="Average temperature for this category (°C)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "very_hot",
                "count": 45,
                "avg_temp": 31.2
            }
        }


class TempPrecipCorrelation(BaseModel):
    """Temperature-precipitation correlation model"""
    month: str = Field(..., description="Year-month (YYYY-MM)")
    correlation: float = Field(..., description="Pearson correlation coefficient")
    avg_temp: float = Field(..., description="Average temperature (°C)")
    avg_precip: float = Field(..., description="Average precipitation (mm)")
    rainy_days: int = Field(..., description="Number of days with precipitation")
    total_precip: float = Field(..., description="Total precipitation (mm)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "month": "2022-04",
                "correlation": -0.6234,
                "avg_temp": 23.5,
                "avg_precip": 12.8,
                "rainy_days": 18,
                "total_precip": 384.5
            }
        }


class Statistics(BaseModel):
    """Overall statistics model"""
    total_months_analyzed: int = Field(..., description="Total number of months")
    max_temperature: float = Field(..., description="Highest temperature recorded (°C)")
    min_temperature: float = Field(..., description="Lowest temperature recorded (°C)")
    overall_avg_max: float = Field(..., description="Overall average maximum temperature (°C)")
    overall_avg_min: float = Field(..., description="Overall average minimum temperature (°C)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_months_analyzed": 36,
                "max_temperature": 32.5,
                "min_temperature": 14.2,
                "overall_avg_max": 28.7,
                "overall_avg_min": 17.8
            }
        }


class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "FileNotFoundError",
                "message": "Results file not found",
                "detail": "monthly_avg_results.csv does not exist"
            }
        }
