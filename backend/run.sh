#!/bin/bash
# Quick start script for backend

echo "🚀 Starting Smart Knowledge Graph Search Engine Backend"
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
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
fi

# Check if data is ingested
if [ ! -f "faiss_index.bin" ]; then
    echo "⚠️  No vector index found. Running data ingestion..."
    echo "This may take a few minutes..."
    python ingest_data.py "Artificial Intelligence" 20
fi

# Start server
echo ""
echo "Starting FastAPI server..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

