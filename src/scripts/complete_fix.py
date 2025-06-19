#!/usr/bin/env python3

import os
import shutil
import json
from pathlib import Path

def fix_project_structure():
    """Fix the project structure and imports"""
    print("🔧 Fixing project structure and imports...")
    
    # Create necessary directories
    os.makedirs("components/ui", exist_ok=True)
    os.makedirs("lib", exist_ok=True)
    
    # Check if src directory exists
    src_dir = Path("src")
    if src_dir.exists():
        print("📁 Found src directory - moving files to root...")
        
        # Move app directory contents
        src_app = src_dir / "app"
        if src_app.exists():
            app_dir = Path("app")
            if not app_dir.exists():
                os.makedirs("app", exist_ok=True)
            
            # Copy all files from src/app to app
            for item in src_app.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(src_app)
                    dest_path = app_dir / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
                    print(f"   Moved: {item} -> {dest_path}")
        
        print("✅ Files moved from src to root")
    else:
        print("📁 No src directory found - files are in correct location")
    
    # Update tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "lib": ["dom", "dom.iterable", "es6"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "baseUrl": ".",
            "paths": {"@/*": ["./*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }
    
    with open("tsconfig.json", "w") as f:
        json.dump(tsconfig, f, indent=2)
    
    print("✅ tsconfig.json updated")
    
    # Check if all required files exist
    required_files = [
        "components/ui/badge.tsx",
        "components/ui/button.tsx",
        "components/ui/card.tsx",
        "components/ui/input.tsx",
        "components/ui/table.tsx",
        "components/ui/alert.tsx",
        "lib/utils.ts"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"⚠️  Missing files: {missing_files}")
        print("   These files should be created by the v0 code blocks above")
    else:
        print("✅ All required UI components exist")
    
    print("\n🎉 Project structure fixed!")
    print("📋 Next steps:")
    print("1. Stop the dev server (Ctrl+C)")
    print("2. Run: npm run dev")
    print("3. Open: http://localhost:3000")

if __name__ == "__main__":
    fix_project_structure()
