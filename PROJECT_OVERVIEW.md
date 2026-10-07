# PhonePe Insights Analyzer - Project Overview

## 📋 Project Description

A sophisticated web application that uses AI to analyze PhonePe transaction PDFs, automatically categorize spending, and generate comprehensive financial insights with beautiful visualizations.

## 🎯 Key Features

### 1. PDF Processing
- Password-protected PDF support
- Robust text extraction using multiple methods (pdfplumber + PyPDF2)
- Handles inconsistent formatting and OCR noise

### 2. AI-Powered Transaction Extraction
- Uses GPT-4/Claude to extract structured data from raw text
- Automatic field detection (date, time, merchant, amount, IDs)
- Intelligent parsing of various transaction formats
- ISO date/time standardization

### 3. Smart Categorization
- 9 predefined categories (fuel, groceries, dining, shopping, etc.)
- AI-based merchant name analysis
- Manual category override capability
- Category-based spending analytics

### 4. Advanced Analytics
- Total debit/credit/net flow calculations
- Top spending categories with visualizations
- Top merchants analysis
- Monthly spending trends
- Anomaly detection (unusual transactions)
- Average transaction metrics

### 5. Modern UI/UX
- Clean, minimal design inspired by PhonePe branding
- Responsive charts using Chart.js
- Interactive transaction table with search
- Drag-and-drop file upload
- Real-time processing feedback

### 6. Data Management
- Session-based data storage
- JSON export functionality
- Transaction detail view
- Category update capability

## 🏗️ Architecture

```
┌─────────────────┐
│   User Upload   │
│   (PDF File)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Processor  │ ← pdfplumber/PyPDF2
│  (Extract Text) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Transaction     │ ← OpenAI/Anthropic LLM
│ Parser (AI)     │
│ - Extract       │
│ - Categorize    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Insights      │
│   Generator     │
│ - Analytics     │
│ - Aggregations  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Server   │
│  (API + Views)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │ ← Chart.js
│  (Visualize)    │
└─────────────────┘
```

## 📁 Project Structure

```
ats/
├── app.py                      # Flask application & routes
├── prompts.py                  # AI system prompts
├── pdf_processor.py            # PDF text extraction
├── llm_client.py              # LLM API wrapper
├── transaction_parser.py       # Transaction extraction & categorization
├── insights_generator.py       # Analytics generation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── SETUP.md                   # Setup instructions
├── SAMPLE_DATA.md             # Sample transaction formats
├── test_setup.py              # Setup verification script
├── setup.ps1                  # Automated setup script (Windows)
├── run.ps1                    # Quick run script (Windows)
│
├── static/
│   ├── css/
│   │   └── style.css          # Global styles
│   └── js/
│       └── main.js            # Client-side JavaScript
│
├── templates/
│   ├── upload.html            # File upload page
│   ├── dashboard.html         # Analytics dashboard
│   ├── transaction_detail.html # Single transaction view
│   └── 404.html               # Error page
│
└── uploads/                   # Temporary file storage
```

## 🔧 Technology Stack

### Backend
- **Framework**: Flask 3.0
- **PDF Processing**: PyPDF2, pdfplumber
- **AI/LLM**: OpenAI GPT-4 / Anthropic Claude
- **Environment**: python-dotenv
- **File Handling**: Werkzeug

### Frontend
- **HTML5** with Jinja2 templating
- **CSS3** with custom design system
- **Vanilla JavaScript** (no framework dependencies)
- **Charts**: Chart.js 4.4

### Development
- **Python**: 3.8+
- **Virtual Environment**: venv
- **Package Manager**: pip

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```powershell
cd "c:\Users\Lenovo\OneDrive\Desktop\ats"
.\setup.ps1
```

### Option 2: Manual Setup
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
Copy-Item .env.example .env
# Edit .env and add your API keys

# Run application
python app.py
```

### Option 3: Quick Run (After Setup)
```powershell
.\run.ps1
```

## 🔑 Configuration

### Required Environment Variables
```
OPENAI_API_KEY=sk-...          # OpenAI API key
FLASK_SECRET_KEY=random-key    # Flask session secret
```

### Optional Configuration
```
ANTHROPIC_API_KEY=...          # Alternative LLM provider
LLM_PROVIDER=openai            # openai or anthropic
LLM_MODEL=gpt-4-turbo-preview  # Model to use
DEBUG=True                     # Debug mode
UPLOAD_FOLDER=uploads          # Upload directory
MAX_CONTENT_LENGTH=16777216    # Max file size (16MB)
```

## 📊 AI Prompts

The system uses 4 specialized AI prompts:

1. **Extraction Prompt**: Converts raw PDF text to structured JSON
2. **Categorization Prompt**: Assigns spending categories
3. **Insights Prompt**: Generates analytics and patterns
4. **Pipeline Prompt**: End-to-end processing (combined)

## 🎨 Design System

### Colors
- **Primary**: `#1d1f21` (Dark gray-black)
- **Accent**: `#ffd65b` (Golden yellow)
- **Background**: `#ffffff` (White)
- **Success**: `#10b981` (Green)
- **Error**: `#ef4444` (Red)

### Typography
- **Font**: Inter (sans-serif)
- **Weights**: 400, 500, 600, 700

### Components
- Cards with shadow elevation
- Gradient headers
- Badge system for categories
- Responsive tables
- Chart visualizations

## 📈 Analytics Features

### Summary Metrics
- Total Spent (all debits)
- Total Received (all credits)
- Net Flow (credit - debit)
- Transaction counts
- Average transaction amount

### Visualizations
- Bar chart: Spending by category
- Line chart: Monthly spending trend
- Tables: Top categories, top merchants
- Anomaly highlighting

### Smart Detection
- Transactions > 2x average marked as anomalies
- Category-based aggregations
- Merchant frequency analysis
- Time-based trend analysis

## 🔒 Security Considerations

- Session-based data storage (no database in current version)
- Temporary file cleanup after processing
- Password-protected PDF support
- Input validation and sanitization
- CSRF protection via Flask
- Secure file upload handling

## 🚧 Future Enhancements

### Short-term
- [ ] Add database persistence (SQLite/PostgreSQL)
- [ ] CSV export functionality
- [ ] Advanced filtering and search
- [ ] Multiple PDF batch processing
- [ ] Transaction editing capability

### Medium-term
- [ ] User authentication system
- [ ] Budget tracking and alerts
- [ ] Recurring transaction detection
- [ ] Email report generation
- [ ] Multi-user support
- [ ] Transaction notes/tags

### Long-term
- [ ] Bank statement integration
- [ ] Mobile app (React Native)
- [ ] Predictive spending analytics
- [ ] Bill payment reminders
- [ ] Investment tracking
- [ ] Tax report generation

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Activate virtual environment
2. **API failures**: Check API key in `.env`
3. **PDF extraction fails**: Verify PDF integrity
4. **Port in use**: Change port in `app.py`
5. **LLM timeout**: Reduce PDF size or retry

### Debug Mode
Set `DEBUG=True` in `.env` for detailed error messages.

## 📝 License

MIT License - Feel free to use and modify for your projects.

## 👥 Contributing

Contributions welcome! Areas for improvement:
- Additional transaction formats
- New visualization types
- Performance optimizations
- UI/UX enhancements
- Bug fixes

## 📞 Support

For issues or questions:
1. Check SETUP.md for configuration help
2. Review logs in terminal output
3. Verify all dependencies installed
4. Test with sample data (SAMPLE_DATA.md)

## 🎉 Acknowledgments

- OpenAI/Anthropic for LLM APIs
- Chart.js for visualizations
- Flask community
- PhonePe for design inspiration
