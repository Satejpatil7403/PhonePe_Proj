# PhonePe Insights Analyzer - Setup Guide

## Quick Setup (Windows PowerShell)

Follow these steps to get your application running:

### 1. Install Python
Make sure you have Python 3.8 or higher installed. Check with:
```powershell
python --version
```

### 2. Create Virtual Environment
```powershell
cd "c:\Users\Lenovo\OneDrive\Desktop\ats"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file from the example:
```powershell
Copy-Item .env.example .env
```

Edit `.env` with your text editor and add your API keys:
- Get OpenAI API key from: https://platform.openai.com/api-keys
- Or get Anthropic API key from: https://console.anthropic.com/

Minimum required configuration in `.env`:
```
OPENAI_API_KEY=sk-your-key-here
FLASK_SECRET_KEY=your-random-secret-key
```

### 5. Create Uploads Directory
```powershell
New-Item -ItemType Directory -Path "uploads" -Force
```

### 6. Run the Application
```powershell
python app.py
```

The app will start on: http://localhost:5000

### 7. Open in Browser
Navigate to: http://localhost:5000

## Testing the Application

### Sample PhonePe Transaction Format
Create a test PDF with transactions in this format:
```
Date: 09-11-2024
Time: 14:30
To: Amazon Pay
Amount: ₹1,299.00
Status: Success
Transaction ID: T2024110900001
UPI Ref: 432198765012

Date: 08-11-2024
Time: 10:15
To: Shell Petrol Pump
Amount: ₹2,500.00
Status: Success
```

## Troubleshooting

### Issue: Module not found
**Solution:** Make sure virtual environment is activated
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: API key error
**Solution:** Check `.env` file has correct API key format

### Issue: PDF extraction fails
**Solution:** Ensure PDF is not corrupted and password (if any) is correct

### Issue: Port already in use
**Solution:** Stop other Flask apps or change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Features Demo

1. **Upload Screen**: Drag and drop your PhonePe PDF
2. **Dashboard**: View comprehensive analytics
3. **Transaction Details**: Click any transaction for details
4. **Category Update**: Modify transaction categories
5. **Export Data**: Download JSON with all insights

## API Endpoints

- `GET /` - Home (redirects to upload)
- `GET /upload` - Upload screen
- `POST /upload` - Process PDF file
- `GET /dashboard` - View insights dashboard
- `GET /transaction/<index>` - Transaction details
- `POST /api/update_category` - Update transaction category
- `GET /api/export` - Export data as JSON
- `GET /api/data` - Get current session data

## System Architecture

```
User uploads PDF
    ↓
PDF Processor extracts raw text
    ↓
LLM extracts structured transactions
    ↓
LLM categorizes transactions
    ↓
Insights Generator creates analytics
    ↓
Dashboard displays results
```

## Next Steps

- Add user authentication
- Implement database (SQLite/PostgreSQL)
- Add transaction search and filtering
- Create CSV export option
- Add budget tracking features
- Implement recurring transaction detection
- Add email report generation

## Support

For issues or questions:
- Check the logs in the terminal
- Verify all dependencies are installed
- Ensure API keys are valid
- Check PDF file is readable
