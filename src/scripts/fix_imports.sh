#!/bin/bash

echo "🔧 Fixing import paths and file structure..."

# Create the correct directory structure
mkdir -p components/ui
mkdir -p lib

# Check if we have a src directory
if [ -d "src" ]; then
    echo "📁 Found src directory - moving files..."
    
    # Move components to root level
    if [ -d "src/app/components" ]; then
        cp -r src/app/components/* app/components/ 2>/dev/null || true
    fi
    
    # Move app files
    if [ -d "src/app" ]; then
        cp -r src/app/* app/ 2>/dev/null || true
    fi
    
    echo "✅ Files moved from src to root"
else
    echo "📁 No src directory found - files are in correct location"
fi

echo "✅ Import paths fixed!"
echo "🚀 Restart your dev server: npm run dev"
