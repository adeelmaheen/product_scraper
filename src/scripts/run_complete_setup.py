#!/usr/bin/env python3

import subprocess
import sys
import os
import time
import requests
import json
from pathlib import Path
import threading
import signal

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    print(f"{color}{message}{Colors.END}")

def print_header(message):
    print_colored(f"\n{'='*60}", Colors.CYAN)
    print_colored(f"{message}", Colors.CYAN + Colors.BOLD)
    print_colored(f"{'='*60}", Colors.CYAN)

def run_command(command, cwd=None, shell=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def check_google_sheets_setup():
    """Check if Google Sheets is configured"""
    print_colored("📊 Checking Google Sheets configuration...", Colors.BLUE)
    
    backend_dir = Path("backend")
    credentials_path = backend_dir / "credentials.json"
    env_path = backend_dir / ".env"
    
    if not credentials_path.exists():
        print_colored("⚠️  Google Sheets not configured (credentials.json missing)", Colors.YELLOW)
        print_colored("   Data will be processed but not saved to Google Sheets", Colors.YELLOW)
        print_colored("   Run: python scripts/setup_google_sheets.py", Colors.YELLOW)
        return False
    
    if not env_path.exists():
        print_colored("⚠️  Environment file missing (.env)", Colors.YELLOW)
        print_colored("   Run: python scripts/setup_google_sheets.py", Colors.YELLOW)
        return False
    
    print_colored("✅ Google Sheets configuration found", Colors.GREEN)
    return True

def check_python():
    """Check Python installation"""
    print_colored("🐍 Checking Python installation...", Colors.BLUE)
    
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print_colored(f"✅ {version}", Colors.GREEN)
        return True
    except Exception as e:
        print_colored(f"❌ Python check failed: {e}", Colors.RED)
        return False

def check_node():
    """Check Node.js installation"""
    print_colored("📦 Checking Node.js installation...", Colors.BLUE)
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print_colored(f"✅ Node.js {version}", Colors.GREEN)
        return True
    except Exception as e:
        print_colored(f"❌ Node.js not found. Please install Node.js 18+", Colors.RED)
        return False

def setup_backend():
    """Setup and start backend"""
    print_header("BACKEND SETUP")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_colored("❌ Backend directory not found!", Colors.RED)
        return False, None
    
    os.chdir(backend_dir)
    
    # Create virtual environment
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print_colored("📦 Creating virtual environment...", Colors.BLUE)
        success, output = run_command(f"{sys.executable} -m venv venv")
        if not success:
            print_colored(f"❌ Failed to create venv: {output}", Colors.RED)
            return False, None
        print_colored("✅ Virtual environment created", Colors.GREEN)
    
    # Determine paths
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    # Install requirements
    print_colored("📦 Installing Python dependencies (including Google Sheets API)...", Colors.BLUE)
    success, output = run_command(f"{pip_exe} install --upgrade pip")
    if not success:
        print_colored(f"❌ Failed to upgrade pip: {output}", Colors.RED)
        return False, None
    
    success, output = run_command(f"{pip_exe} install -r requirements.txt")
    if not success:
        print_colored(f"❌ Failed to install requirements: {output}", Colors.RED)
        return False, None
    
    print_colored("✅ Dependencies installed (including Google Sheets support)", Colors.GREEN)
    
    # Start backend server
    print_colored("🚀 Starting FastAPI server with Google Sheets integration...", Colors.BLUE)
    
    try:
        process = subprocess.Popen([
            str(python_exe), "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print_colored("⏳ Waiting for backend to start...", Colors.YELLOW)
        for i in range(30):
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    health_data = response.json()
                    print_colored("✅ Backend server started successfully!", Colors.GREEN)
                    print_colored("🌐 Backend API: http://localhost:8000", Colors.CYAN)
                    
                    # Check Google Sheets status
                    sheets_status = health_data.get('google_sheets', 'unknown')
                    if sheets_status == 'configured':
                        print_colored("✅ Google Sheets integration: ACTIVE", Colors.GREEN)
                    else:
                        print_colored("⚠️  Google Sheets integration: NOT CONFIGURED", Colors.YELLOW)
                        print_colored("   Data will be processed but not saved to sheets", Colors.YELLOW)
                    
                    return True, process
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        print_colored("❌ Backend failed to start within 30 seconds", Colors.RED)
        process.terminate()
        return False, None
        
    except Exception as e:
        print_colored(f"❌ Failed to start backend: {e}", Colors.RED)
        return False, None

def test_backend():
    """Test backend API including Google Sheets"""
    print_header("BACKEND TESTING")
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        print_colored("🧪 Testing health endpoint...", Colors.BLUE)
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_colored("✅ Health check passed", Colors.GREEN)
            print_colored(f"   Status: {data.get('status')}", Colors.WHITE)
            print_colored(f"   Google Sheets: {data.get('google_sheets', 'unknown')}", Colors.WHITE)
        else:
            print_colored(f"❌ Health check failed: {response.status_code}", Colors.RED)
            return False
    except Exception as e:
        print_colored(f"❌ Health check error: {e}", Colors.RED)
        return False
    
    # Test scrape endpoint with Google Sheets
    try:
        print_colored("🧪 Testing scrape endpoint with Google Sheets integration...", Colors.BLUE)
        payload = {"product_url": "https://www.daraz.pk/products/test"}
        response = requests.post(f"{base_url}/scrape", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print_colored("✅ Scrape endpoint passed", Colors.GREEN)
            print_colored(f"   Reviews processed: {data.get('total_reviews', 0)}", Colors.WHITE)
            print_colored(f"   Google Sheets saved: {data.get('google_sheets_saved', False)}", Colors.WHITE)
            
            if data.get('sheet_url'):
                print_colored(f"   Sheet URL: {data.get('sheet_url')}", Colors.CYAN)
            
            # Check sentiment distribution
            reviews = data.get('data', [])
            if reviews:
                sentiments = {}
                for review in reviews:
                    sentiment = review.get('sentiment_label', 'Unknown')
                    sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
                
                print_colored("   Sentiment distribution:", Colors.WHITE)
                for sentiment, count in sentiments.items():
                    print_colored(f"     {sentiment}: {count}", Colors.WHITE)
            
            return True
        else:
            print_colored(f"❌ Scrape endpoint failed: {response.status_code}", Colors.RED)
            return False
    except Exception as e:
        print_colored(f"❌ Scrape endpoint error: {e}", Colors.RED)
        return False

def setup_frontend():
    """Setup and start frontend"""
    print_header("FRONTEND SETUP")
    
    # Go back to root directory
    os.chdir("..")
    
    # Install dependencies
    print_colored("📦 Installing Node.js dependencies...", Colors.BLUE)
    success, output = run_command("npm install")
    if not success:
        print_colored(f"❌ Failed to install npm dependencies: {output}", Colors.RED)
        return False, None
    
    print_colored("✅ Frontend dependencies installed", Colors.GREEN)
    
    # Start frontend server
    print_colored("🚀 Starting Next.js server...", Colors.BLUE)
    
    try:
        process = subprocess.Popen(["npm", "run", "dev"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for frontend to start
        print_colored("⏳ Waiting for frontend to start...", Colors.YELLOW)
        time.sleep(15)  # Give Next.js more time to start
        
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print_colored("✅ Frontend server started successfully!", Colors.GREEN)
                print_colored("🌐 Frontend App: http://localhost:3000", Colors.CYAN)
                return True, process
        except requests.exceptions.RequestException:
            pass
        
        print_colored("⚠️  Frontend may still be starting...", Colors.YELLOW)
        return True, process  # Return success even if we can't verify immediately
        
    except Exception as e:
        print_colored(f"❌ Failed to start frontend: {e}", Colors.RED)
        return False, None

def main():
    """Main function"""
    print_header("PRODUCT REVIEW SENTIMENT SCRAPER - COMPLETE SETUP WITH GOOGLE SHEETS")
    
    # Store process references for cleanup
    backend_process = None
    frontend_process = None
    
    def cleanup():
        print_colored("\n🛑 Shutting down servers...", Colors.YELLOW)
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print_colored("✅ Cleanup completed", Colors.GREEN)
    
    def signal_handler(sig, frame):
        cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Check prerequisites
        if not check_python():
            return False
        
        if not check_node():
            return False
        
        # Check Google Sheets setup
        google_sheets_configured = check_google_sheets_setup()
        
        # Setup backend
        backend_success, backend_process = setup_backend()
        if not backend_success:
            return False
        
        # Test backend
        if not test_backend():
            return False
        
        # Setup frontend
        frontend_success, frontend_process = setup_frontend()
        if not frontend_success:
            return False
        
        # Success message
        print_header("🎉 SETUP COMPLETE!")
        print_colored("Both servers are running successfully!", Colors.GREEN + Colors.BOLD)
        print_colored("\n📍 Access Points:", Colors.CYAN + Colors.BOLD)
        print_colored("   🌐 Frontend App: http://localhost:3000", Colors.WHITE)
        print_colored("   🔧 Backend API: http://localhost:8000", Colors.WHITE)
        print_colored("   📊 API Health: http://localhost:8000/health", Colors.WHITE)
        print_colored("   📖 API Docs: http://localhost:8000/docs", Colors.WHITE)
        
        print_colored("\n📊 Google Sheets Integration:", Colors.CYAN + Colors.BOLD)
        if google_sheets_configured:
            print_colored("   ✅ CONFIGURED - Data will be saved to Google Sheets", Colors.GREEN)
            print_colored("   📋 Check your Google Drive for created spreadsheets", Colors.WHITE)
        else:
            print_colored("   ⚠️  NOT CONFIGURED - Data will be processed but not saved", Colors.YELLOW)
            print_colored("   🔧 Run: python scripts/setup_google_sheets.py", Colors.WHITE)
        
        print_colored("\n🎯 How to use:", Colors.CYAN + Colors.BOLD)
        print_colored("   1. Open http://localhost:3000 in your browser", Colors.WHITE)
        print_colored("   2. Enter any product URL (demo mode)", Colors.WHITE)
        print_colored("   3. Click 'Scrape Reviews' button", Colors.WHITE)
        print_colored("   4. View sentiment analysis results", Colors.WHITE)
        if google_sheets_configured:
            print_colored("   5. Check Google Sheets link in the results", Colors.WHITE)
        
        print_colored(f"\n{Colors.YELLOW}Press Ctrl+C to stop both servers...{Colors.END}")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        cleanup()
        return True
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", Colors.RED)
        cleanup()
        return False

if __name__ == "__main__":
    if main():
        print_colored("✅ Application stopped successfully!", Colors.GREEN)
    else:
        print_colored("❌ Setup failed!", Colors.RED)
        sys.exit(1)
