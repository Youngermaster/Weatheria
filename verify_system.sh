#!/bin/bash

echo "============================================"
echo "  Weatheria Climate Observatory - System Check"
echo "============================================"
echo ""

# Check if API is running
echo "1. Checking API Server (port 8000)..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✓ API Server is running"
    API_STATUS=$(curl -s http://localhost:8000/health | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
    echo "   ✓ Health Status: $API_STATUS"
else
    echo "   ✗ API Server is NOT running"
    echo "   → Start with: python3 src/api/main.py"
fi

echo ""

# Check if Frontend is running
echo "2. Checking Frontend Server (port 5173)..."
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "   ✓ Frontend Server is running"
    echo "   ✓ URL: http://localhost:5173"
else
    echo "   ✗ Frontend Server is NOT running"
    echo "   → Start with: cd weatheria-frontend && npm run dev"
fi

echo ""

# Check data files
echo "3. Checking Data Files..."
if [ -f "data/raw/medellin_weather_2022-2024.csv" ]; then
    LINES=$(wc -l < data/raw/medellin_weather_2022-2024.csv)
    echo "   ✓ Raw data exists: $LINES lines"
else
    echo "   ✗ Raw data missing"
    echo "   → Download with: python3 scripts/download_data.py"
fi

echo ""

# Check output files
echo "4. Checking Processed Results..."
if [ -f "output/monthly_avg_results.csv" ]; then
    echo "   ✓ Monthly averages: $(wc -l < output/monthly_avg_results.csv) records"
else
    echo "   ✗ Monthly averages missing"
fi

if [ -f "output/extreme_temps_results.csv" ]; then
    echo "   ✓ Extreme temps: $(wc -l < output/extreme_temps_results.csv) records"
else
    echo "   ✗ Extreme temps missing"
fi

if [ -f "output/temp_precip_results.csv" ]; then
    echo "   ✓ Temp-precipitation: $(wc -l < output/temp_precip_results.csv) records"
else
    echo "   ✗ Temp-precipitation missing"
fi

if [ ! -f "output/monthly_avg_results.csv" ] || [ ! -f "output/extreme_temps_results.csv" ] || [ ! -f "output/temp_precip_results.csv" ]; then
    echo "   → Generate with: python3 scripts/process_data_simple.py"
fi

echo ""

# Test API endpoints
echo "5. Testing API Endpoints..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    MONTHLY_COUNT=$(curl -s http://localhost:8000/monthly-avg | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    EXTREME_COUNT=$(curl -s http://localhost:8000/extreme-temps | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    PRECIP_COUNT=$(curl -s http://localhost:8000/temp-precipitation | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)

    if [ ! -z "$MONTHLY_COUNT" ]; then
        echo "   ✓ /monthly-avg returns $MONTHLY_COUNT records"
    fi
    if [ ! -z "$EXTREME_COUNT" ]; then
        echo "   ✓ /extreme-temps returns $EXTREME_COUNT categories"
    fi
    if [ ! -z "$PRECIP_COUNT" ]; then
        echo "   ✓ /temp-precipitation returns $PRECIP_COUNT records"
    fi
else
    echo "   ✗ Cannot test endpoints (API not running)"
fi

echo ""
echo "============================================"
echo "  System Status Summary"
echo "============================================"

# Overall status
if curl -s http://localhost:8000/health > /dev/null 2>&1 && lsof -ti:5173 > /dev/null 2>&1; then
    echo "✓ All systems operational!"
    echo ""
    echo "Access the application:"
    echo "  • Frontend: http://localhost:5173"
    echo "  • API Docs: http://localhost:8000/docs"
    echo ""
else
    echo "⚠ Some services are not running"
    echo ""
    echo "Quick start commands:"
    echo ""
    echo "# Terminal 1 - API"
    echo "source venv/bin/activate"
    echo "python3 src/api/main.py"
    echo ""
    echo "# Terminal 2 - Frontend"
    echo "cd weatheria-frontend"
    echo "npm run dev"
    echo ""
fi
