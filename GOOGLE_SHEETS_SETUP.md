# Google Sheets API Setup Guide

This guide will help you set up Google Sheets API integration to save scraped review data.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select existing project
3. Give your project a name (e.g., "Review Scraper")
4. Click "Create"

## Step 2: Enable Google Sheets API

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on "Google Sheets API"
4. Click "Enable"

## Step 3: Enable Google Drive API

1. Search for "Google Drive API" in the API Library
2. Click on "Google Drive API"
3. Click "Enable"

## Step 4: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - **Service account name**: `review-scraper-service`
   - **Service account ID**: `review-scraper-service`
   - **Description**: `Service account for review scraper application`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

## Step 5: Create and Download Credentials

1. In the "Credentials" page, find your service account
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create New Key"
5. Select "JSON" format
6. Click "Create"
7. The JSON file will be downloaded automatically

## Step 6: Setup Credentials in Your Project

1. **Rename the downloaded file** to `credentials.json`
2. **Move the file** to your `backend/` directory:
   \`\`\`
   backend/
   ├── main.py
   ├── requirements.txt
   ├── credentials.json  ← Place your file here
   └── .env
   \`\`\`

## Step 7: Configure Environment Variables

1. Copy the example environment file:
   \`\`\`bash
   cp backend/.env.example backend/.env
   \`\`\`

2. Edit `backend/.env` with your details:
   \`\`\`env
   GOOGLE_CREDENTIALS_FILE=credentials.json
   GOOGLE_SHEET_NAME=Product Reviews Sentiment Analysis
   USER_EMAIL=your-email@gmail.com
   \`\`\`

## Step 8: Test the Integration

1. Start your backend server:
   \`\`\`bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   \`\`\`

2. Check the health endpoint:
   \`\`\`bash
   curl http://localhost:8000/health
   \`\`\`

   You should see:
   \`\`\`json
   {
     "status": "healthy",
     "google_sheets": "configured"
   }
   \`\`\`

3. Test scraping with Google Sheets save:
   \`\`\`bash
   curl -X POST http://localhost:8000/scrape \
        -H "Content-Type: application/json" \
        -d '{"product_url": "https://www.daraz.pk/products/test"}'
   \`\`\`

## Step 9: Access Your Google Sheet

After running a scrape, you should:

1. **Check your Google Drive** - A new spreadsheet will be created
2. **Look for the sheet name** you specified in the environment variables
3. **Open the spreadsheet** to see your scraped data

## 📊 What Gets Saved to Google Sheets

The following data is saved for each review:

| Column | Description |
|--------|-------------|
| Timestamp | When the review was processed |
| Product Name | Name of the product |
| Review Text | The actual review content |
| Rating | Star rating (1-5) |
| Sentiment Score | Numerical sentiment score (-1 to 1) |
| Sentiment Label | Positive/Negative/Neutral |
| Review Length | Character count of review |
| Date Scraped | When the scraping was performed |

## 🔒 Security Best Practices

1. **Never commit credentials.json to version control**
   \`\`\`bash
   echo "credentials.json" >> .gitignore
   echo ".env" >> .gitignore
   \`\`\`

2. **Restrict service account permissions**
   - Only give necessary permissions
   - Regularly rotate credentials

3. **Use environment variables for sensitive data**
   - Never hardcode credentials in source code
   - Use the .env file for configuration

## 🛠 Troubleshooting

### Common Issues

**1. "Credentials file not found"**
- Make sure `credentials.json` is in the `backend/` directory
- Check the file path in your `.env` file

**2. "Permission denied" errors**
- Ensure Google Sheets API is enabled
- Ensure Google Drive API is enabled
- Check service account has proper permissions

**3. "Spreadsheet not found"**
- The app will create a new spreadsheet automatically
- Make sure the service account has Drive access

**4. "Authentication failed"**
- Verify your credentials.json file is valid
- Try downloading new credentials from Google Cloud Console

### Testing Commands

Test Google Sheets connection:
\`\`\`python
# Run this in Python to test your setup
import gspread
from google.oauth2.service_account import Credentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
client = gspread.authorize(credentials)

print("✅ Google Sheets connection successful!")
\`\`\`

## 🎉 Success!

Once configured, your application will:
- ✅ Automatically save all scraped reviews to Google Sheets
- ✅ Create formatted spreadsheets with headers
- ✅ Provide direct links to the created sheets
- ✅ Handle errors gracefully if Sheets API is unavailable

Your scraped data will now be permanently stored and easily accessible via Google Sheets!
\`\`\`

Let's create a setup script that handles Google Sheets configuration:

```python file="scripts/setup_google_sheets.py"
#!/usr/bin/env python3

import os
import json
import sys
from pathlib import Path

def setup_google_sheets():
    """Interactive setup for Google Sheets API"""
    print("🔧 Google Sheets API Setup")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Check for credentials file
    credentials_path = backend_dir / "credentials.json"
    
    if not credentials_path.exists():
        print("📋 Google Sheets API Setup Required")
        print("\n📖 Follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Google Sheets API and Google Drive API")
        print("4. Create a Service Account")
        print("5. Download the JSON credentials file")
        print("6. Rename it to 'credentials.json'")
        print("7. Place it in the 'backend/' directory")
        print("\n📚 Detailed guide: See GOOGLE_SHEETS_SETUP.md")
        
        # Ask if user wants to continue without Google Sheets
        response = input("\n❓ Continue without Google Sheets integration? (y/n): ").lower()
        if response != 'y':
            print("⏸️  Setup paused. Please configure Google Sheets first.")
            return False
        else:
            print("⚠️  Continuing without Google Sheets - data won't be saved to sheets")
            return True
    
    # Validate credentials file
    try:
        with open(credentials_path, 'r') as f:
            credentials_data = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in credentials_data]
        
        if missing_fields:
            print(f"❌ Invalid credentials file. Missing fields: {missing_fields}")
            return False
        
        print("✅ Valid credentials.json found")
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in credentials.json")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False
    
    # Setup environment file
    env_path = backend_dir / ".env"
    env_example_path = backend_dir / ".env.example"
    
    if not env_path.exists():
        if env_example_path.exists():
            print("📝 Creating .env file from template...")
            
            # Get user input for configuration
            sheet_name = input("📊 Enter Google Sheet name (default: 'Product Reviews Sentiment Analysis'): ").strip()
            if not sheet_name:
                sheet_name = "Product Reviews Sentiment Analysis"
            
            user_email = input("📧 Enter your email to share the sheet with (optional): ").strip()
            
            # Create .env file
            env_content = f"""# Google Sheets Configuration
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME={sheet_name}
USER_EMAIL={user_email}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
"""
            
            with open(env_path, 'w') as f:
                f.write(env_content)
            
            print("✅ .env file created")
        else:
            print("⚠️  .env.example not found, creating basic .env")
            with open(env_path, 'w') as f:
                f.write("GOOGLE_CREDENTIALS_FILE=credentials.json\n")
    else:
        print("✅ .env file already exists")
    
    # Test the connection
    print("\n🧪 Testing Google Sheets connection...")
    
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(str(credentials_path), scopes=scope)
        client = gspread.authorize(credentials)
        
        print("✅ Google Sheets connection successful!")
        
        # Try to create a test sheet
        try:
            test_sheet_name = "Test Sheet - Delete Me"
            test_sheet = client.create(test_sheet_name)
            print(f"✅ Test sheet created: {test_sheet.url}")
            
            # Delete the test sheet
            client.del_spreadsheet_by_key(test_sheet.id)
            print("✅ Test sheet deleted")
            
        except Exception as e:
            print(f"⚠️  Could not create test sheet: {e}")
            print("   (This might be due to permissions, but basic connection works)")
        
        return True
        
    except ImportError:
        print("❌ Google Sheets libraries not installed")
        print("   Run: pip install gspread google-auth")
        return False
    except Exception as e:
        print(f"❌ Google Sheets connection failed: {e}")
        print("   Please check your credentials and API permissions")
        return False

def main():
    """Main setup function"""
    print("🚀 Product Review Scraper - Google Sheets Setup")
    
    if setup_google_sheets():
        print("\n🎉 Google Sheets setup completed!")
        print("\n📋 Next steps:")
        print("1. Run: python scripts/run_complete_setup.py")
        print("2. Test scraping - data will be saved to Google Sheets")
        print("3. Check your Google Drive for the created spreadsheet")
        return True
    else:
        print("\n❌ Google Sheets setup failed!")
        print("📚 See GOOGLE_SHEETS_SETUP.md for detailed instructions")
        return False

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
