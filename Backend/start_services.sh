#!/bin/bash

# Function to check if a service is running
check_service() {
    if ! pgrep -f "$1" > /dev/null; then
        echo "Starting $1..."
        return 1
    else
        echo "$1 is already running."
        return 0
    fi
}

# Function to wait for a service to be available
wait_for_service() {
    echo "Waiting for $1 to be ready..."
    while ! curl -s "$2" > /dev/null; do
        sleep 1
    done
    echo "$1 is ready!"
}

# Start Ollama service if not running
check_service "ollama"
if [ $? -eq 1 ]; then
    # Start Ollama in the background
    ollama serve &
    # Wait for Ollama to be ready
    wait_for_service "Ollama" "http://localhost:11434"
fi

# Start FastAPI server if not running
check_service "api.py"
if [ $? -eq 1 ]; then
    # Start FastAPI server in the background
    python api.py &
    # Wait for FastAPI to be ready
    wait_for_service "FastAPI" "http://localhost:8000/docs"
fi

# Start React frontend
echo "Starting React frontend..."
cd ..
cd Frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install --legacy-peer-deps
fi

# Start the React development server
echo "Starting React development server..."
npm run dev 