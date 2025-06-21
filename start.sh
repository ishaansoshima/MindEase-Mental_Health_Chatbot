#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" >/dev/null 2>&1
}

# Function to start a service in the background
start_service() {
    local name=$1
    local command=$2
    local log_file=$3
    
    echo -e "${YELLOW}Starting ${name}...${NC}"
    if is_process_running "$command"; then
        echo -e "${YELLOW}${name} is already running${NC}"
    else
        eval "nohup $command >> "$log_file" 2>&1 &"
        echo -e "${GREEN}${name} started${NC}"
        echo -e "Logs: $log_file"
    fi
    echo ""
}

# Create logs directory if it doesn't exist
mkdir -p logs

# 1. Start Ollama (if not already running)
if ! is_process_running "ollama serve"; then
    echo -e "${YELLOW}Ollama is not running. Please start it manually with:${NC}"
    echo -e "  ollama serve"
    echo -e "${YELLOW}Or install it from: https://ollama.ai/download${NC}"
    echo ""
else
    echo -e "${GREEN}✓ Ollama is running${NC}"
    echo ""
fi

# 2. Activate virtual environment
if [ ! -d "myenv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv myenv
    source myenv/bin/activate
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -r requirements-minimal.txt
else
    source myenv/bin/activate
fi

# 3. Start FastAPI backend
start_service "FastAPI Backend" \
    "uvicorn main:app --host 0.0.0.0 --port 8001" \
    "logs/backend.log"

# 4. Start React frontend
cd frontend
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
fi

start_service "React Frontend" \
    "npm run dev" \
    "../logs/frontend.log"
cd ..

# 5. Open the application in the default browser
sleep 3  # Give the servers a moment to start
if command_exists xdg-open; then
    xdg-open "http://localhost:5173"
elif command_exists open; then
    open "http://localhost:5173"
fi

echo -e "${GREEN}✓ Application is starting up!${NC}"
echo -e "${YELLOW}Frontend:${NC} http://localhost:5173"
echo -e "${YELLOW}Backend API:${NC} http://localhost:8001"
echo -e "${YELLOW}API Docs:${NC} http://localhost:8001/docs"
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for all background processes
wait

# Make the script executable
chmod +x start.sh
