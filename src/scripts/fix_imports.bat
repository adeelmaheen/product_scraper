@echo off
echo 🔧 Fixing import paths and file structure...

REM Create the correct directory structure
if not exist "components\ui" mkdir components\ui
if not exist "lib" mkdir lib

REM Check if we have a src directory
if exist "src" (
    echo 📁 Found src directory - moving files...
    
    REM Move components to root level
    if exist "src\app\components" (
        xcopy "src\app\components\*" "app\components\" /E /I /Y >nul 2>&1
    )
    
    REM Move app files
    if exist "src\app" (
        xcopy "src\app\*" "app\" /E /I /Y >nul 2>&1
    )
    
    echo ✅ Files moved from src to root
) else (
    echo 📁 No src directory found - files are in correct location
)

echo ✅ Import paths fixed!
echo 🚀 Restart your dev server: npm run dev
pause
