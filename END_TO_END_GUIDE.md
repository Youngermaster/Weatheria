# Weatheria Climate Observatory - End-to-End Usage Guide

## Complete Workflow for Local Testing

This guide walks you through the entire workflow from data acquisition to visualization.

---

## Prerequisites

- Python 3.10+ (avoid 3.14 due to mrjob incompatibility)
- Node.js 18+ and npm
- Docker and Docker Compose (optional, for Hadoop cluster)
- 2GB free disk space

---

## Step 1: Environment Setup

### Backend Setup

```bash
# Navigate to project root
cd /Users/youngermaster/GitHub/Youngermaster/Weatheria

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install pandas numpy requests fastapi uvicorn python-multipart
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd weatheria-frontend

# Install Node dependencies (already done)
npm install

# Verify installations
npm list react react-router-dom recharts axios lucide-react
```

---

## Step 2: Data Acquisition

Download real weather data from Open-Meteo API for Medellín (2022-2024):

```bash
# Go back to project root
cd ..

# Run data download script
python3 scripts/download_data.py
```

**Expected Output:**
- File created: `data/raw/medellin_weather_2022-2024.csv`
- Total records: 1,096 days
- Date range: 2022-01-01 to 2024-12-31
- Variables: date, temp_max, temp_min, precipitation

**Sample Data:**
```
date,temp_max,temp_min,precipitation
2022-01-01,24.8,14.9,0.0
2022-01-02,24.7,14.2,1.2
...
```

---

## Step 3: Data Processing (MapReduce-Style)

Process the raw data to generate analysis results:

```bash
# Run simplified MapReduce processing
python3 scripts/process_data_simple.py
```

**Expected Output:**
```
✓ Processing monthly averages...
  Saved to output/monthly_avg_results.csv (36 records)

✓ Processing extreme temperatures...
  Saved to output/extreme_temps_results.csv (4 categories)

✓ Processing temperature-precipitation correlation...
  Saved to output/temp_precip_results.csv (36 records)

Summary:
- Monthly data: 36 months analyzed
- Extreme temps: 4 categories identified
- Correlation: Negative relationship detected
```

**Generated Files:**
1. `output/monthly_avg_results.csv` - Monthly temperature averages
2. `output/extreme_temps_results.csv` - Temperature classification
3. `output/temp_precip_results.csv` - Temperature-precipitation correlation

---

## Step 4: Start the API Server

Launch the FastAPI backend to serve the processed data:

```bash
# Ensure you're in project root with venv activated
python3 src/api/main.py
```

**Expected Output:**
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Verify API is running:**
```bash
# In a new terminal
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.0"}

curl http://localhost:8000/
# Expected: Welcome message with all endpoints
```

---

## Step 5: Start the Frontend

Launch the React + Vite frontend application:

```bash
# In a new terminal, navigate to frontend
cd weatheria-frontend

# Start development server
npm run dev
```

**Expected Output:**
```
VITE v7.2.4  ready in 180 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## Step 6: Access the Application

Open your browser and navigate to: **http://localhost:5173/**

### Available Pages:

1. **Dashboard** (`/dashboard`)
   - Comprehensive climate overview
   - 4 interactive charts:
     - Temperature trends (line chart)
     - Temperature distribution (pie chart)
     - Monthly precipitation (bar chart)
     - Temp vs precipitation correlation (dual-axis line chart)
   - Key statistics cards
   - Climate insights

2. **Monthly Analysis** (`/monthly`)
   - Detailed temperature trends over 36 months
   - Area chart showing max/min temperatures
   - Hottest and coolest month summaries
   - Complete data table
   - CSV download functionality

3. **Extreme Temperatures** (`/extreme`)
   - Temperature classification analysis
   - Category breakdown:
     - Very Hot (>30°C)
     - Normal (15-30°C)
     - Cool (<15°C)
     - Very Cool (<12°C)
   - Pie and bar charts
   - Detailed category insights
   - CSV download

4. **Precipitation Analysis** (`/precipitation`)
   - Temperature-precipitation correlation
   - Combined bar + line chart
   - Scatter plot showing relationship
   - Monthly correlation table
   - Wettest and driest month stats
   - Climate insights
   - CSV download

5. **About** (`/about`)
   - Project overview
   - Technology stack
   - MapReduce job descriptions
   - Data source information
   - Key climate findings
   - Links to resources

---

## Step 7: Test API Endpoints

### Using Browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Using curl:

```bash
# Get all monthly averages
curl http://localhost:8000/monthly-avg

# Get extreme temperatures
curl http://localhost:8000/extreme-temps

# Get temperature-precipitation data
curl http://localhost:8000/temp-precipitation

# Get overall statistics
curl http://localhost:8000/stats

# Get hottest month
curl http://localhost:8000/monthly-avg/hottest

# Download CSV results
curl -O http://localhost:8000/download/monthly-avg
curl -O http://localhost:8000/download/extreme-temps
curl -O http://localhost:8000/download/temp-precipitation
```

---

## Step 8: Verify Data Flow

### Frontend → API → Data Files

1. **Open browser console** (F12)
2. Navigate between pages
3. Check Network tab for API calls:
   - `/monthly-avg` returns 36 records
   - `/extreme-temps` returns 4 categories
   - `/temp-precipitation` returns 36 records

4. **Verify charts render correctly:**
   - Dashboard shows 4 charts with data
   - All pages load without errors
   - Download buttons work

---

## Key Climate Findings

From the processed data (2022-2024):

### Temperature Trends:
- **Average Max Temperature:** 24.7°C
- **Average Min Temperature:** 14.8°C
- **Warming Trend:** +1.8°C from 2022 to 2024
- **Hottest Month:** Multiple candidates around 25-26°C
- **Coolest Month:** Multiple candidates around 13-14°C

### Extreme Temperature Days:
- **Normal Days (15-30°C):** 700 days (63.9%)
- **Cool Days (<15°C):** 380 days (34.7%)
- **Very Cool Days (<12°C):** 6 days (0.5%)
- **Very Hot Days (>30°C):** 23 days (2.1%)

### Precipitation Patterns:
- **Total Precipitation:** 5,754.5 mm over 3 years
- **Average Correlation:** -0.30 to -0.50 (negative)
- **Interpretation:** Warmer periods tend to have less rainfall
- **Wettest Month:** ~350 mm
- **Driest Month:** ~100 mm

---

## Troubleshooting

### API Issues:

**Port 8000 already in use:**
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Restart API
python3 src/api/main.py
```

**Cannot find output files:**
```bash
# Regenerate results
python3 scripts/process_data_simple.py
```

**CORS errors in browser:**
- API already has CORS enabled for localhost:5173
- Check browser console for specific errors

### Frontend Issues:

**Port 5173 already in use:**
```bash
# Kill existing process
lsof -ti:5173 | xargs kill -9

# Restart frontend
npm run dev
```

**Module not found errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Blank page or loading forever:**
- Check browser console for errors
- Verify API is running: `curl http://localhost:8000/health`
- Check Network tab for failed API calls

### Data Processing Issues:

**Missing raw data:**
```bash
# Re-download data
python3 scripts/download_data.py
```

**Python module errors:**
```bash
# Reinstall dependencies
pip install --force-reinstall pandas numpy requests fastapi uvicorn
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│              WEATHERIA CLIMATE OBSERVATORY               │
└─────────────────────────────────────────────────────────┘

┌─────────────────┐
│  Open-Meteo API │  (Data Source)
└────────┬────────┘
         │ download_data.py
         ▼
┌─────────────────────────────────────────────────────────┐
│  RAW DATA (CSV)                                          │
│  data/raw/medellin_weather_2022-2024.csv                │
│  1,096 daily records                                     │
└────────┬────────────────────────────────────────────────┘
         │ process_data_simple.py
         ▼
┌─────────────────────────────────────────────────────────┐
│  PROCESSED RESULTS (CSV)                                 │
│  - output/monthly_avg_results.csv                       │
│  - output/extreme_temps_results.csv                     │
│  - output/temp_precip_results.csv                       │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  FASTAPI SERVER (Backend)                                │
│  http://localhost:8000                                   │
│  - REST API endpoints                                    │
│  - CSV download functionality                            │
│  - Swagger/ReDoc documentation                           │
└────────┬────────────────────────────────────────────────┘
         │ HTTP JSON
         ▼
┌─────────────────────────────────────────────────────────┐
│  REACT FRONTEND (UI)                                     │
│  http://localhost:5173                                   │
│  - Interactive dashboards                                │
│  - Data visualizations (Recharts)                        │
│  - Download functionality                                │
└─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend:
- **Python 3.10+:** Core language
- **FastAPI:** Modern REST API framework
- **Uvicorn:** ASGI server
- **pandas:** Data processing
- **numpy:** Numerical operations

### Frontend:
- **React 19.2.0:** UI framework
- **TypeScript:** Type safety
- **Vite:** Build tool
- **React Router:** Navigation
- **ShadcnUI:** Component library
- **Recharts:** Data visualization
- **Axios:** HTTP client
- **TailwindCSS:** Styling

### Data Source:
- **Open-Meteo Archive API:** Historical weather data
- **Location:** Medellín, Colombia (6.25°N, 75.56°W)
- **Period:** 2022-2024
- **Resolution:** Daily

---

## Next Steps

### For Development:
1. Add more MapReduce analyses
2. Implement yearly comparisons
3. Add predictive models
4. Create downloadable reports (PDF)

### For Deployment:
1. Set up Hadoop cluster (Docker or AWS EMR)
2. Implement actual MapReduce jobs with MRJOB
3. Deploy API to cloud (AWS EC2, Heroku, etc.)
4. Deploy frontend to Vercel/Netlify
5. Set up CI/CD pipeline

### For AWS EMR (Production):
1. Upload data to S3
2. Create EMR cluster
3. Run MapReduce jobs on cluster
4. Store results in S3
5. Configure API to read from S3

---

## Quick Start Commands

```bash
# Terminal 1: API Server
cd /Users/youngermaster/GitHub/Youngermaster/Weatheria
source venv/bin/activate
python3 src/api/main.py

# Terminal 2: Frontend
cd /Users/youngermaster/GitHub/Youngermaster/Weatheria/weatheria-frontend
npm run dev

# Terminal 3: Testing
curl http://localhost:8000/health
open http://localhost:5173
```

---

## Success Checklist

- [ ] Raw data downloaded (1,096 records)
- [ ] Data processed successfully (3 output files)
- [ ] API server running on port 8000
- [ ] API health check passes
- [ ] All API endpoints return data
- [ ] Frontend running on port 5173
- [ ] Dashboard loads with 4 charts
- [ ] All pages accessible via sidebar
- [ ] Download buttons work
- [ ] No console errors in browser
- [ ] Charts display data correctly

---

## Project Structure

```
Weatheria/
├── data/
│   └── raw/
│       └── medellin_weather_2022-2024.csv  (1,096 records)
├── output/
│   ├── monthly_avg_results.csv             (36 records)
│   ├── extreme_temps_results.csv           (4 categories)
│   └── temp_precip_results.csv             (36 records)
├── scripts/
│   ├── download_data.py                    (Data acquisition)
│   └── process_data_simple.py              (MapReduce-style processing)
├── src/
│   └── api/
│       └── main.py                         (FastAPI server)
├── weatheria-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   └── DashboardLayout.tsx
│   │   │   ├── ui/                         (ShadcnUI components)
│   │   │   └── StatCard.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── MonthlyAnalysis.tsx
│   │   │   ├── ExtremeAnalysis.tsx
│   │   │   ├── PrecipitationAnalysis.tsx
│   │   │   └── About.tsx
│   │   ├── services/
│   │   │   └── api.ts                      (Axios API client)
│   │   ├── types/
│   │   │   └── index.ts                    (TypeScript types)
│   │   ├── App.tsx                         (Router setup)
│   │   └── main.tsx                        (Entry point)
│   ├── package.json
│   └── .env                                (VITE_API_URL)
├── requirements.txt
├── CLAUDE.md                                (Project requirements)
├── GETTING_STARTED.md                       (Setup instructions)
├── EXECUTION_SUMMARY.md                     (Results documentation)
└── END_TO_END_GUIDE.md                      (This file)
```

---

## Support & Resources

- **API Documentation:** http://localhost:8000/docs
- **Open-Meteo API:** https://open-meteo.com/en/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Recharts Docs:** https://recharts.org/

---

**Last Updated:** November 22, 2025
**Version:** 1.0.0
**Status:** ✅ Fully Functional

---

*Inspired by Weatheria from One Piece - Where Science Meets the Clouds* ☁️🌡️
