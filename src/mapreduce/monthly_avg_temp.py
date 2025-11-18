#!/usr/bin/env python3
"""
Monthly Average Temperature MapReduce Job
Calculates average max and min temperatures per month

Usage:
    # Local mode
    python src/mapreduce/monthly_avg_temp.py data/raw/test_weather_data.csv
    
    # Hadoop mode
    python src/mapreduce/monthly_avg_temp.py -r hadoop hdfs:///input/weather_data.csv
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime


class MonthlyAvgTemperature(MRJob):
    """
    MapReduce job to calculate monthly average temperatures
    
    Input: CSV with date, temp_max, temp_min, precipitation
    Output: year-month\tavg_temp_max\tavg_temp_min
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
        Parse CSV line and emit (year-month, (temp_max, temp_min, 1))
        
        Args:
            _: Line number (ignored)
            line: CSV line
            
        Yields:
            (year_month, (temp_max, temp_min, 1))
        """
        # Skip header line
        if line.startswith('date'):
            return
        
        try:
            # Parse CSV line
            parts = line.strip().split(',')
            if len(parts) < 3:
                return
            
            date_str = parts[0]
            temp_max = float(parts[1])
            temp_min = float(parts[2])
            
            # Extract year-month
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            year_month = date_obj.strftime('%Y-%m')
            
            # Emit (year_month, (temp_max, temp_min, count))
            yield year_month, (temp_max, temp_min, 1)
            
        except (ValueError, IndexError) as e:
            # Skip malformed lines
            pass
    
    def reducer(self, year_month, values):
        """
        Calculate average temperatures for each month
        
        Args:
            year_month: Year-month string (e.g., "2022-01")
            values: Iterator of (temp_max, temp_min, count) tuples
            
        Yields:
            (year_month, (avg_temp_max, avg_temp_min))
        """
        total_max = 0.0
        total_min = 0.0
        count = 0
        
        # Sum all temperatures and counts
        for temp_max, temp_min, cnt in values:
            total_max += temp_max
            total_min += temp_min
            count += cnt
        
        # Calculate averages
        if count > 0:
            avg_max = round(total_max / count, 2)
            avg_min = round(total_min / count, 2)
            
            # Emit result as tab-separated values
            yield year_month, f"{avg_max}\t{avg_min}"


if __name__ == '__main__':
    MonthlyAvgTemperature.run()
