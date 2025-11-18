#!/usr/bin/env python3
"""
Extreme Temperature Detection MapReduce Job
Identifies days with extreme temperature conditions

Usage:
    # Local mode
    python src/mapreduce/extreme_temps.py data/raw/test_weather_data.csv
    
    # Hadoop mode
    python src/mapreduce/extreme_temps.py -r hadoop hdfs:///input/weather_data.csv
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime


class ExtremeTemperatures(MRJob):
    """
    Detect days with extreme temperature conditions
    
    Extreme conditions:
    - Very hot: max temp > 30°C
    - Cool: min temp < 15°C
    - Very cool: min temp < 12°C
    
    Input: CSV with date, temp_max, temp_min, precipitation
    Output: category\tcount\tavg_temp
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
        Classify days by temperature extremes
        
        Args:
            _: Line number (ignored)
            line: CSV line
            
        Yields:
            (category, (date, avg_temp, 1))
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
            
            # Calculate average temperature
            avg_temp = (temp_max + temp_min) / 2
            
            # Classify based on temperature thresholds
            categories = []
            
            if temp_max > 30:
                categories.append('very_hot')
            
            if temp_min < 15:
                categories.append('cool')
            
            if temp_min < 12:
                categories.append('very_cool')
            
            # If no extreme condition, classify as normal
            if not categories:
                categories.append('normal')
            
            # Emit each category
            for category in categories:
                yield category, (date_str, avg_temp, 1)
                
        except (ValueError, IndexError):
            # Skip malformed lines
            pass
    
    def reducer(self, category, values):
        """
        Count extreme days by category and calculate average temperature
        
        Args:
            category: Temperature category
            values: Iterator of (date, avg_temp, count) tuples
            
        Yields:
            (category, (count, avg_temp))
        """
        count = 0
        total_temp = 0.0
        dates = []
        
        # Aggregate data
        for date, avg_temp, cnt in values:
            count += cnt
            total_temp += avg_temp
            dates.append(date)
        
        # Calculate average temperature for this category
        avg_temp_for_category = round(total_temp / count, 2) if count > 0 else 0.0
        
        # Emit result as tab-separated values
        yield category, f"{count}\t{avg_temp_for_category}"


if __name__ == '__main__':
    ExtremeTemperatures.run()
