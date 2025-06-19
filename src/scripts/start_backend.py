#!/usr/bin/env python3

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def setup_backend():
    """Setup and start the backend server"""
    print("🐍 Setting up FastAPI backend...")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    # Determine activation script path
    if sys.platform == "win32":
        activate_script = venv_dir / "Scripts" / "activate"
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    # Install requirements
    print("📦 Installing Python dependencies...")
    try:
        # Upgrade pip first
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Start the server
    print("🚀 Starting FastAPI server...")
    try:
        # Start uvicorn server
        process = subprocess.Popen([
            str(python_exe), "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend server started successfully!")
                    print("🌐 Backend API: http://localhost:8000")
                    print("📊 API Health: http://localhost:8000/health")
                    print("📖 API Docs: http://localhost:8000/docs")
                    return True
            except requests.exceptions.RequestException:
                time.sleep(1)
                print(f"   Waiting... ({i+1}/30)")
        
        print("❌ Server failed to start within 30 seconds")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    print("🚀 Starting Product Review Sentiment Scraper Backend...")
    
    if not check_python():
        return False
    
    if not setup_backend():
        return False
    
    print("\n🎉 Backend is ready!")
    print("Now you can run the test script in another terminal:")
    print("python scripts/test_api.py")
    
    # Keep the script running
    try:
        print("\nPress Ctrl+C to stop the server...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        return True

if __name__ == "__main__":
    if main():
        print("✅ Backend stopped successfully!")
    else:
        print("❌ Backend setup failed!")
        sys.exit(1)
