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
    
    # Results directory (can be overridden with env var RESULTS_DIR)
    results_dir: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output")
    
    # CORS
    cors_origins: list = ["*"]
    
    # File names
    monthly_avg_file: str = "monthly_avg_fixed.csv"
    extreme_temps_file: str = "extreme_temps_fixed.csv"
    temp_precip_file: str = "temp_precip_fixed.csv"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
