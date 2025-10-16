#!/bin/bash
##############################################################################
# Deprecated: Use `docker-compose up` or `make start` instead for easier     #
# management of services.                                                    #
##############################################################################
# This script starts the proxy server, backend, and frontend for the Finance 
# Manager application. It also ensures that any existing instances of these 
# services are terminated before starting new ones.

echo "Starting Finance Manager Application..."

lsof -ti:8000 | xargs kill -9 2>/dev/null 
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8001 | xargs kill -9 2>/dev/null

# Start proxy server
echo "Starting exchange rate proxy server..."
source .venv/bin/activate
python ./proxy/server.py &
PROXY_PID=$!

# Start backend
echo "Starting backend server..."
source .venv/bin/activate
which python
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Proxy server running on http://localhost:8001"
echo "Backend running on http://localhost:8000"
echo "Frontend running on http://localhost:3000"
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill -3 $PROXY_PID 2>/dev/null
    kill -3 $BACKEND_PID 2>/dev/null
    kill -3 $FRONTEND_PID 2>/dev/null
    printf "\n"
    exit
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for any background process to finish
wait