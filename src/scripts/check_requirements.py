#!/usr/bin/env python3

import subprocess
import sys
import importlib.util

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            print(f"✅ {package_name} is installed")
            return True
        else:
            print(f"❌ {package_name} is NOT installed")
            return False
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def main():
    print("🔍 Checking Python requirements...")
    
    # Required packages for the backend
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("textblob", "textblob"),
        ("pydantic", "pydantic"),
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        for package in missing_packages:
            if not install_package(package):
                print(f"❌ Failed to install {package}")
                return False
        
        print("\n🔄 Re-checking packages...")
        for package_name, import_name in required_packages:
            check_package(package_name, import_name)
    
    # Download TextBlob corpora if needed
    try:
        import nltk
        print("📚 Downloading TextBlob corpora...")
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        print("✅ TextBlob corpora downloaded")
    except:
        print("⚠️  TextBlob corpora download failed (will try during runtime)")
    
    print("\n🎉 All requirements checked!")
    return True

if __name__ == "__main__":
    if main():
        print("✅ Requirements check completed!")
    else:
        print("❌ Requirements check failed!")
        sys.exit(1)
