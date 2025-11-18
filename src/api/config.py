"""
Configuration settings for the API
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = "Weatheria Climate Observatory API"
    api_description: str = "MapReduce-based weather analysis for Medellín (2022-2024)"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Results directory
    results_dir: str = "./output"
    
    # CORS
    cors_origins: list = ["*"]
    
    # File names
    monthly_avg_file: str = "monthly_avg_results.csv"
    extreme_temps_file: str = "extreme_temps_results.csv"
    temp_precip_file: str = "temp_precip_results.csv"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
