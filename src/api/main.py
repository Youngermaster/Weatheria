"""
Main FastAPI application for Weatheria Climate Observatory
Best practices implementation with routers, models, and dependency injection
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict
import os
import pandas as pd

from .config import settings
from .models.schemas import Statistics, HealthCheck
from .routers import monthly, extremes, correlation
from .dependencies.file_handler import ensure_results_directory, get_results_file_path

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(monthly.router)
app.include_router(extremes.router)
app.include_router(correlation.router)


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    ensure_results_directory()
    print(f"🚀 Weatheria Climate Observatory API v{settings.api_version}")
    print(f"📂 Results directory: {settings.results_dir}")
    print(f"📊 Access docs at: http://{settings.api_host}:{settings.api_port}/docs")


@app.get(
    "/",
    response_model=Dict,
    summary="API Welcome",
    description="Get API information and available endpoints"
)
async def root():
    """
    Welcome endpoint with API information
    """
    return {
        "message": "Welcome to Weatheria Climate Observatory",
        "description": "MapReduce-based weather analysis for Medellín (2022-2024)",
        "version": settings.api_version,
        "inspiration": "Inspired by Weatheria from One Piece - where science meets the clouds ☁️",
        "endpoints": {
            "/monthly-avg": "Monthly average temperatures",
            "/monthly-avg/hottest": "Hottest month",
            "/monthly-avg/coolest": "Coolest month",
            "/extreme-temps": "Extreme temperature days",
            "/extreme-temps/summary": "Extreme temperature summary",
            "/temp-precipitation": "Temperature-precipitation correlation",
            "/temp-precipitation/wettest-month": "Month with most rain",
            "/temp-precipitation/driest-month": "Month with least rain",
            "/temp-precipitation/correlation-strength": "Correlation interpretation",
            "/stats": "Overall statistics",
            "/health": "Health check",
            "/download/{result_type}": "Download CSV results"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get(
    "/health",
    response_model=HealthCheck,
    summary="Health Check",
    description="Check if the API is running"
)
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.api_version
    }


@app.get(
    "/stats",
    response_model=Statistics,
    summary="Overall Statistics",
    description="Get overall climate statistics for the analyzed period"
)
async def get_statistics():
    """
    Get overall statistics from all MapReduce results
    """
    try:
        # Load monthly averages
        monthly_df = pd.read_csv(
            get_results_file_path(settings.monthly_avg_file),
            sep='\t',
            names=['month', 'data'],
            header=None
        )
        
        # Parse the data column
        split_data = monthly_df['data'].str.split('\t', expand=True)
        monthly_df['avg_max'] = pd.to_numeric(split_data[0], errors='coerce')
        monthly_df['avg_min'] = pd.to_numeric(split_data[1], errors='coerce')
        
        return {
            "total_months_analyzed": len(monthly_df),
            "max_temperature": float(monthly_df['avg_max'].max()),
            "min_temperature": float(monthly_df['avg_min'].min()),
            "overall_avg_max": float(monthly_df['avg_max'].mean()),
            "overall_avg_min": float(monthly_df['avg_min'].mean())
        }
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Statistics not available. Run MapReduce jobs first."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating statistics: {str(e)}"
        )


@app.get(
    "/download/{result_type}",
    summary="Download Results",
    description="Download CSV file of MapReduce results"
)
async def download_results(result_type: str):
    """
    Download CSV file of results
    
    Available result types:
    - monthly-avg: Monthly average temperatures
    - extreme-temps: Extreme temperature detection
    - temp-precipitation: Temperature-precipitation correlation
    """
    file_mapping = {
        "monthly-avg": settings.monthly_avg_file,
        "extreme-temps": settings.extreme_temps_file,
        "temp-precipitation": settings.temp_precip_file
    }
    
    if result_type not in file_mapping:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid result type. Available types: {', '.join(file_mapping.keys())}"
        )
    
    try:
        file_path = get_results_file_path(file_mapping[result_type])
        
        return FileResponse(
            file_path,
            media_type="text/csv",
            filename=file_mapping[result_type]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading file: {str(e)}"
        )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": "The requested resource was not found",
            "detail": str(exc.detail) if hasattr(exc, 'detail') else None
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An internal server error occurred",
            "detail": str(exc.detail) if hasattr(exc, 'detail') else None
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info"
    )
