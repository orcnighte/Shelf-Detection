#!/bin/bash
# Quick start script for backend

echo "Starting Inventory Management Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Create storage directory
mkdir -p backend/storage/images
mkdir -p backend/models

# Start the server
echo "Starting FastAPI server..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000




