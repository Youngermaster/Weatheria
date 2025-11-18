#!/usr/bin/env python3
"""
Temperature-Precipitation Correlation MapReduce Job
Analyzes relationship between temperature and rainfall by month

Usage:
    # Local mode
    python src/mapreduce/temp_precipitation.py data/raw/test_weather_data.csv
    
    # Hadoop mode
    python src/mapreduce/temp_precipitation.py -r hadoop hdfs:///input/weather_data.csv
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import math


class TempPrecipitationCorrelation(MRJob):
    """
    Analyze correlation between temperature and precipitation
    
    Input: CSV with date, temp_max, temp_min, precipitation
    Output: year-month\tcorrelation\tavg_temp\tavg_precip\tdays_with_rain
    """
    
    def steps(self):
        """Define the MapReduce steps"""
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer
            )
        ]
    
    def mapper(self, _, line):
        """
        Emit monthly temperature and precipitation data
        
        Args:
            _: Line number (ignored)
            line: CSV line
            
        Yields:
            (year_month, (avg_temp, precipitation))
        """
        # Skip header line
        if line.startswith('date'):
            return
        
        try:
            # Parse CSV line
            parts = line.strip().split(',')
            if len(parts) < 4:
                return
            
            date_str = parts[0]
            temp_max = float(parts[1])
            temp_min = float(parts[2])
            precipitation = float(parts[3])
            
            # Calculate average temperature
            avg_temp = (temp_max + temp_min) / 2
            
            # Extract year-month
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            year_month = date_obj.strftime('%Y-%m')
            
            # Emit (year_month, (avg_temp, precipitation))
            yield year_month, (avg_temp, precipitation)
            
        except (ValueError, IndexError):
            # Skip malformed lines
            pass
    
    def reducer(self, year_month, values):
        """
        Calculate correlation coefficient and statistics
        
        Args:
            year_month: Year-month string
            values: Iterator of (avg_temp, precipitation) tuples
            
        Yields:
            (year_month, statistics)
        """
        temps = []
        precips = []
        
        # Collect all values
        for temp, precip in values:
            temps.append(temp)
            precips.append(precip)
        
        n = len(temps)
        
        if n < 2:
            # Not enough data for correlation
            return
        
        # Calculate means
        mean_temp = sum(temps) / n
        mean_precip = sum(precips) / n
        
        # Calculate correlation coefficient (Pearson)
        numerator = sum((t - mean_temp) * (p - mean_precip) 
                       for t, p in zip(temps, precips))
        
        temp_variance = sum((t - mean_temp) ** 2 for t in temps)
        precip_variance = sum((p - mean_precip) ** 2 for p in precips)
        
        denominator = math.sqrt(temp_variance * precip_variance)
        
        if denominator == 0:
            correlation = 0.0
        else:
            correlation = round(numerator / denominator, 4)
        
        # Count rainy days (precipitation > 0)
        rainy_days = sum(1 for p in precips if p > 0)
        
        # Calculate total precipitation
        total_precip = sum(precips)
        
        # Format output
        avg_temp = round(mean_temp, 2)
        avg_precip = round(mean_precip, 2)
        total_precip = round(total_precip, 2)
        
        # Emit result as tab-separated values
        yield year_month, f"{correlation}\t{avg_temp}\t{avg_precip}\t{rainy_days}\t{total_precip}"


if __name__ == '__main__':
    TempPrecipitationCorrelation.run()
