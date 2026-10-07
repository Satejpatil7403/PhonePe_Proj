# PhonePe Transaction Analyzer

🔒 **100% Privacy-Focused** | 🚀 **No LLM/AI** | ⚡ **Local Processing**

A privacy-first web application that analyzes PhonePe transaction PDF statements locally without any cloud processing or LLM access.

## 🌟 Features

- **Complete Privacy**: All processing happens locally - no data sent to external servers
- **No LLM Required**: Uses regex pattern matching instead of AI models
- **Instant Analysis**: Fast transaction parsing and insights generation
- **Beautiful UI**: Modern, responsive design with mobile hamburger menu
- **Secure**: PDFs are deleted immediately after processing
- **Category Detection**: Automatically categorizes transactions
- **Visual Dashboard**: Clean insights with color-coded transaction display

## 🚀 Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/CrazAr374/phonepe-proj)

### Deployment Steps:

1. Click the "Deploy to Vercel" button above
2. Connect your GitHub account
3. Select this repository
4. Click "Deploy"
5. Wait for deployment to complete
6. Your app will be live! 🎉

### Environment Variables (Optional):

No environment variables are required for basic functionality. The app works out of the box!

## 🛡️ Privacy & Security

- **No Cloud Storage**: PDFs are processed in-memory and deleted immediately
- **No Database**: Transaction data stored only in session (cleared on browser close)
- **No LLM/AI**: Pure pattern matching - your data never reaches any AI service
- **No Sign-ups**: Completely anonymous usage
- **HTTPS Only**: All connections encrypted (Vercel provides SSL by default)

## 🔧 Local Development

### Prerequisites:
- Python 3.8+
- pip

### Installation:

```bash
# Clone the repository
git clone https://github.com/CrazAr374/phonepe-proj.git
cd phonepe-proj

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000`

## 📦 Tech Stack

- **Backend**: Flask 3.0
- **PDF Processing**: PyPDF2 + pdfplumber
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Typography**: Inter font family
- **Deployment**: Vercel

## 📝 How It Works

1. **Upload**: User uploads PhonePe PDF statement (with optional password)
2. **Extract**: PDF text is extracted using PyPDF2/pdfplumber
3. **Parse**: Regex patterns identify transactions, dates, amounts, merchants
4. **Categorize**: Transactions are auto-categorized (Food, Shopping, Transport, etc.)
5. **Analyze**: Insights calculated (spending by category, top merchants, etc.)
6. **Display**: Beautiful dashboard shows results
7. **Delete**: PDF is immediately deleted from server

## 🔒 Data Privacy Statement

This application:
- ✅ Does NOT store your PDF files
- ✅ Does NOT send data to any external API
- ✅ Does NOT use LLM or AI models
- ✅ Does NOT require sign-up or login
- ✅ Does NOT track users
- ✅ Processes everything locally on the server
- ✅ Clears all data when you close the browser

## 📄 License

MIT License - Feel free to use for personal or commercial projects

## 🙏 Acknowledgments

Built with privacy and simplicity in mind. No fancy AI, just reliable pattern matching.

---

Made with ❤️ for privacy-conscious users
