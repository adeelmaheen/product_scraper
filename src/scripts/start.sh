#!/bin/bash

echo "🚀 Starting Product Review Sentiment Scraper..."

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Function to cleanup processes
cleanup() {
    echo "🛑 Stopping servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if required ports are available
if ! check_port 8000; then
    echo "❌ Backend port 8000 is in use. Please stop the process using this port."
    exit 1
fi

if ! check_port 3000; then
    echo "❌ Frontend port 3000 is in use. Please stop the process using this port."
    exit 1
fi

# Start backend
echo "🐍 Starting FastAPI backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start backend server
echo "🚀 Starting backend server on port 8000..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend failed to start"
    cleanup
    exit 1
fi

echo "✅ Backend started successfully"

# Start frontend
echo "⚛️  Starting Next.js frontend..."
cd ..

# Install frontend dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Start frontend server
echo "🚀 Starting frontend server on port 3000..."
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

echo "✅ Both servers are running!"
echo ""
echo "🌐 Backend API: http://localhost:8000"
echo "🌐 Frontend App: http://localhost:3000"
echo "📊 API Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for user input
wait
