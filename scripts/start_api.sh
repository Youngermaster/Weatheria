#!/bin/bash
# Start the FastAPI application
# Usage: ./scripts/start_api.sh

set -e

echo "============================================================"
echo "Weatheria Climate Observatory - API Server"
echo "============================================================"

# Check if output directory has results
if [ ! -d "output" ] || [ -z "$(ls -A output 2>/dev/null)" ]; then
    echo "⚠️  Warning: No results found in output/ directory"
    echo "   Run MapReduce jobs first: ./scripts/run_mapreduce.sh"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 Starting FastAPI server..."
echo ""

# Check if we should use Docker
if [ -f "/.dockerenv" ]; then
    # Already in Docker
    cd /app
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
    # Check if Docker Compose is running
    if docker ps | grep -q weatheria-api; then
        echo "✓ Using Docker Compose..."
        echo ""
        echo "API running at:"
        echo "  - Swagger UI: http://localhost:8000/docs"
        echo "  - ReDoc: http://localhost:8000/redoc"
        echo "  - API Root: http://localhost:8000"
        echo ""
        echo "Press Ctrl+C to stop"
        docker-compose logs -f api
    else
        # Run locally
        echo "✓ Running locally..."
        echo ""
        
        # Check if virtual environment exists
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        # Activate virtual environment
        source venv/bin/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install -q -r requirements.txt
        
        echo ""
        echo "API starting at:"
        echo "  - Swagger UI: http://localhost:8000/docs"
        echo "  - ReDoc: http://localhost:8000/redoc"
        echo "  - API Root: http://localhost:8000"
        echo ""
        
        # Start the server
        cd src/api
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    fi
fi
