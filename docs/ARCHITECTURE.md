# Weatheria Climate Observatory - Technical Documentation

## System Architecture

[Add detailed architecture diagrams and explanations]

## MapReduce Algorithm Details

### Monthly Average Temperature

**Mapper Phase:**

- Input: CSV lines with date, temp_max, temp_min
- Process: Extract year-month, emit (year-month, (temp_max, temp_min, 1))
- Output: Key-value pairs grouped by month

**Reducer Phase:**

- Input: (year-month, list of (temp_max, temp_min, 1))
- Process: Sum temperatures and counts, calculate averages
- Output: (year-month, (avg_max, avg_min))

[Continue with more details...]
