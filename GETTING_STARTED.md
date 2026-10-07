# 🚀 GETTING STARTED - PhonePe Insights Analyzer

## 📦 What You Have

A complete, production-ready web application that:
- ✅ Analyzes PhonePe transaction PDFs using pattern matching
- ✅ Auto-categorizes spending into 9 categories
- ✅ Generates visual analytics and insights
- ✅ Detects unusual spending patterns
- ✅ Exports data as JSON
- ✅ Modern, responsive UI
- ✅ **100% PRIVATE** - No data sent to external services!

## 🔒 Privacy Guarantee

**Your financial data NEVER leaves your computer:**
- ❌ No API keys required
- ❌ No cloud services used
- ❌ No external LLM calls
- ✅ All processing done locally
- ✅ Files deleted after processing
- ✅ Session-only storage

## ⚡ Quick Start (3 Minutes)

### Step 1: Open PowerShell in Project Directory
```powershell
cd "c:\Users\Lenovo\OneDrive\Desktop\ats"
```

### Step 2: Run Automated Setup
```powershell
.\setup.ps1
```

This will:
- ✓ Check Python installation
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Create configuration files
- ✓ Set up directory structure
- ✓ Run validation tests

### Step 3: Configure Secret Key (Optional)

Edit `.env` file and set a random secret key:
```
FLASK_SECRET_KEY=your-random-secret-key-12345
```

**No API keys needed!** This is just for session security.

### Step 4: Start the Application
```powershell
.\run.ps1
```

Or manually:
```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

## 📋 What Each File Does

### Core Application Files
- `app.py` - Main Flask server with all routes
- `prompts.py` - AI system prompts for extraction/categorization
- `pdf_processor.py` - Extracts text from PDF files
- `llm_client.py` - Communicates with OpenAI/Anthropic
- `transaction_parser.py` - AI-powered transaction extraction
- `insights_generator.py` - Calculates analytics

### Frontend Files
- `templates/upload.html` - File upload page
- `templates/dashboard.html` - Main analytics dashboard
- `templates/transaction_detail.html` - Individual transaction view
- `static/css/style.css` - All styling
- `static/js/main.js` - Client-side interactions

### Configuration & Setup
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `setup.ps1` - Automated setup script
- `run.ps1` - Quick run script
- `test_setup.py` - Verify installation

### Documentation
- `README.md` - Main documentation
- `SETUP.md` - Detailed setup guide
- `PROJECT_OVERVIEW.md` - Architecture & features
- `SAMPLE_DATA.md` - Test data examples

## 🎯 How to Use

### 1. Upload PDF
- Drag and drop your PhonePe PDF statement
- Or click to browse and select
- Enter password if PDF is protected
- Click "Generate Insights"

### 2. View Dashboard
- See total spent, received, and net flow
- View spending by category (bar chart)
- See spending trend over time (line chart)
- Browse all transactions in table
- Check unusual transactions

### 3. Transaction Details
- Click any transaction to see full details
- Update category if needed
- View all transaction IDs and references

### 4. Export Data
- Click "Export Data" to download JSON
- Contains all transactions and insights
- Can be imported into other tools

## 🏗️ System Flow

```
1. USER UPLOADS PDF
   ↓
2. PDF PROCESSOR extracts raw text
   ↓
3. PATTERN MATCHER extracts structured transactions
   (using regex and rule-based logic)
   {date, time, merchant, amount, direction}
   ↓
4. KEYWORD MATCHER categorizes each transaction
   (based on merchant name patterns)
   {fuel, groceries, dining, shopping, etc.}
   ↓
5. INSIGHTS GENERATOR calculates analytics
   (local computations only)
   {totals, trends, anomalies, top categories}
   ↓
6. DASHBOARD displays visualizations
   (Charts, tables, statistics)
```

## 🔧 How It Works (No LLM!)

### Transaction Extraction
Uses regex patterns to find:
- Dates: `09-11-2024`, `2024-11-09`
- Times: `14:30`, `2:30 PM`
- Amounts: `₹1,299.00`, `Rs. 500`
- Merchants: Names after "To:", "Merchant:", etc.
- IDs: Transaction IDs, UTR numbers

### Categorization
Keyword-based matching:
- "petrol", "pump" → **fuel**
- "grocery", "kirana" → **groceries**
- "amazon", "flipkart" → **shopping**
- "restaurant", "zomato" → **dining**
- etc.

### Analytics
Pure mathematical calculations:
- Sum, average, count
- Group by category/month
- Detect anomalies (>2x average)
- No external services needed!

## 🔑 No API Keys Required!

Unlike the original design, this version:
- ❌ Doesn't use OpenAI
- ❌ Doesn't use Anthropic
- ❌ Doesn't send data anywhere
- ✅ Works completely offline
- ✅ Costs nothing to run
- ✅ 100% private and secure

## 🛠️ Customization

### Change Port
Edit `app.py`, line 144:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Change Colors
Edit `static/css/style.css`, lines 2-11:
```css
:root {
    --primary-color: #1d1f21;
    --accent-color: #ffd65b;
    /* ... modify as needed ... */
}
```

### Add Categories
Edit `prompts.py`, line 23-32:
```python
Category rules:
- Your new category → your_category
```

### Modify Analysis
Edit `insights_generator.py` to add custom metrics.

## 📊 Sample Output

After processing a PDF with 50 transactions:

```json
{
  "insights": {
    "total_debit": 25000.00,
    "total_credit": 30000.00,
    "net_flow": 5000.00,
    "transaction_count": 50,
    "top_categories": [
      {"category": "groceries", "total_amount": 8000},
      {"category": "fuel", "total_amount": 5000},
      ...
    ]
  },
  "transactions": [...]
}
```

## ⚠️ Important Notes

### Security
- Files are deleted after processing
- No data stored in database (session only)
- Add authentication for production use

### Performance
- Large PDFs (>50 pages) may take 30-60 seconds
- API rate limits apply
- Process one PDF at a time

### Accuracy
- Depends on PDF text quality
- Works best with digital PDFs (not scanned images)
- May need category corrections for unusual merchants

## 🐛 Troubleshooting

### "Module not found"
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Secret key not configured"
- Edit `.env` file
- Set FLASK_SECRET_KEY to any random string
- Example: `FLASK_SECRET_KEY=my-secret-key-123`

### "PDF extraction failed"
- Ensure PDF is not corrupted
- Check if password is required
- Try with a different PDF
- Make sure PDF has actual text (not scanned images)

### "Port already in use"
- Close other Flask apps
- Change port in `app.py`
- Check with: `netstat -ano | findstr :5000`

### "No transactions found"
- PDF format may not be recognized
- Try a different PhonePe statement
- Check that PDF contains transaction-like text
- Verify date/amount patterns exist

## 📱 Browser Compatibility

✅ Chrome 90+
✅ Firefox 88+
✅ Edge 90+
✅ Safari 14+

## 💡 Pro Tips

1. **Batch Processing**: Upload statements one at a time for best results
2. **Category Training**: Review and correct categories to improve future results
3. **Export Regular**: Download JSON backups monthly
4. **Budget Tracking**: Use insights to set category-based budgets
5. **Anomaly Review**: Check unusual transactions for errors or fraud

## 📚 Learn More

- **Full Documentation**: See README.md
- **Setup Guide**: See SETUP.md
- **Architecture**: See PROJECT_OVERVIEW.md
- **Test Data**: See SAMPLE_DATA.md

## 🎉 Success!

If everything is working:
1. You should see the upload page at http://localhost:5000
2. Upload a PhonePe PDF
3. See analytics dashboard with charts
4. Browse and search transactions
5. Export data as JSON

## 🤝 Need Help?

Common commands:
```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_setup.py

# Start app
python app.py

# Stop app
Ctrl + C
```

## 🚀 Next Steps

After getting it working:
1. ✅ Test with your actual PhonePe PDF
2. ✅ Review and correct any miscategorized transactions
3. ✅ Export your data
4. ⬜ Add database for persistence (see PROJECT_OVERVIEW.md)
5. ⬜ Customize categories for your spending habits
6. ⬜ Add authentication for multi-user access

---

**Ready to start?** Run `.\setup.ps1` now!
