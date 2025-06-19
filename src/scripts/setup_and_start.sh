#!/bin/bash

echo "🚀 Product Review Sentiment Scraper - Setup and Start"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Found Python: $($PYTHON_CMD --version)"

# Check Node.js
if command_exists node; then
    echo "✅ Found Node.js: $(node --version)"
else
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Step 1: Check and install Python requirements
echo ""
echo "📋 Step 1: Checking Python requirements..."
$PYTHON_CMD scripts/check_requirements.py

if [ $? -ne 0 ]; then
    echo "❌ Python requirements check failed!"
    exit 1
fi

# Step 2: Setup backend
echo ""
echo "📋 Step 2: Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ Could not find virtual environment activation script"
    exit 1
fi

# Install requirements
echo "📦 Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Start backend
echo ""
echo "📋 Step 3: Starting backend server..."
echo "🚀 Starting FastAPI on http://localhost:8000"

# Start backend in background
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 10

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend started successfully!"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Step 4: Setup frontend
echo ""
echo "📋 Step 4: Setting up frontend..."
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Step 5: Start frontend
echo ""
echo "📋 Step 5: Starting frontend server..."
echo "🚀 Starting Next.js on http://localhost:3000"

# Start frontend in background
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 15

echo ""
echo "🎉 Setup complete!"
echo "================================"
echo "🌐 Backend API: http://localhost:8000"
echo "🌐 Frontend App: http://localhost:3000"
echo "📊 API Health: http://localhost:8000/health"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handler
trap cleanup SIGINT SIGTERM

# Wait for user input
wait
