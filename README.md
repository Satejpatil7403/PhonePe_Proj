# PhonePe Insights Analyzer

A modern web application that analyzes PhonePe transaction PDFs to provide categorized insights, spending patterns, and financial analytics. **100% privacy-focused - all processing is done locally without any external API calls or LLM services.**

## Features

- 📄 PDF Upload with password protection support
- 🔒 **Complete Privacy** - No data sent to external services
- 🏷️ Automatic transaction categorization using pattern matching
- 📊 Visual analytics and insights
- 📈 Spending trends and patterns
- 🔍 Transaction search and filtering
- 💾 Data export capabilities

## Tech Stack

- **Backend**: Flask (Python)
- **PDF Processing**: PyPDF2, pdfplumber
- **Transaction Extraction**: Rule-based pattern matching (NO LLM)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Charts**: Chart.js
- **Database**: In-memory session storage (no external database)

## Privacy First

**Your financial data never leaves your computer!**
- ✅ No API keys required
- ✅ No external service calls
- ✅ No data tracking or logging
- ✅ All processing done locally
- ✅ Files deleted immediately after processing
- ✅ Session-only storage

## Installation

1. Clone or navigate to the project directory
2. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```powershell
   cp .env.example .env
   ```
   Edit `.env` and set FLASK_SECRET_KEY (no API keys needed!)

5. Run the application:
   ```powershell
   python app.py
   ```

6. Open your browser to `http://localhost:5000`

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask sessions (required)
- `UPLOAD_FOLDER`: Directory for temporary file uploads (optional)
- `DEBUG`: Enable debug mode (optional)

**Note**: No API keys needed!

## Usage

1. Upload your PhonePe transaction PDF
2. Enter the PDF password if required
3. Click "Generate Insights"
4. View categorized transactions and analytics
5. Export data or modify categories as needed

## Project Structure

```
ats/
├── app.py                 # Main Flask application
├── prompts.py            # AI system prompts
├── pdf_processor.py      # PDF extraction logic
├── transaction_parser.py # Transaction parsing and categorization
├── insights_generator.py # Analytics and insights generation
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── static/              # Static assets
│   ├── css/
│   ├── js/
│   └── images/
└── templates/           # HTML templates
    ├── upload.html
    ├── dashboard.html
    └── transaction_detail.html
```

## License

MIT License
