# Quick Start Guide

Follow these steps to get the Product Review Sentiment Scraper running:

## Option 1: Automatic Setup (Recommended)

### Step 1: Run the setup script
\`\`\`bash
chmod +x scripts/setup_and_start.sh
./scripts/setup_and_start.sh
\`\`\`

## Option 2: Manual Setup

### Step 1: Start Backend Server

1. **Check Python requirements:**
   \`\`\`bash
   python3 scripts/check_requirements.py
   \`\`\`

2. **Start backend server:**
   \`\`\`bash
   python3 scripts/start_backend.py
   \`\`\`

   Wait until you see:
   \`\`\`
   ✅ Backend server started successfully!
   🌐 Backend API: http://localhost:8000
   \`\`\`

### Step 2: Test Backend (Optional)

In a new terminal:
\`\`\`bash
python3 scripts/test_api.py
\`\`\`

### Step 3: Start Frontend

In a new terminal:
\`\`\`bash
npm install
npm run dev
\`\`\`

### Step 4: Access Application

Open your browser and go to: http://localhost:3000

## Troubleshooting

### Backend won't start?
1. Check if Python 3.8+ is installed: \`python3 --version\`
2. Check if port 8000 is free: \`lsof -i :8000\`
3. Install missing packages: \`pip install fastapi uvicorn requests beautifulsoup4 textblob pydantic\`

### Frontend won't start?
1. Check if Node.js 18+ is installed: \`node --version\`
2. Check if port 3000 is free: \`lsof -i :3000\`
3. Clear cache and reinstall: \`rm -rf node_modules package-lock.json && npm install\`

### Connection errors?
1. Make sure backend is running on port 8000
2. Test backend health: \`curl http://localhost:8000/health\`
3. Check firewall settings

## What to expect

1. **Backend**: FastAPI server with sample review data
2. **Frontend**: Next.js app with sentiment analysis dashboard
3. **Features**: 
   - Scrape product reviews (demo mode)
   - Sentiment analysis with TextBlob
   - Interactive charts and tables
   - Responsive design

## Demo Usage

1. Enter any product URL (e.g., \`https://www.daraz.pk/products/sample\`)
2. Click "Scrape Reviews"
3. View sentiment analysis results in charts and tables
4. Explore the interactive dashboard

The application uses sample data for demonstration. In production, you would implement actual web scraping.
