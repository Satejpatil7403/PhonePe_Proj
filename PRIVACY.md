# 🔒 Privacy & Security

## Complete Data Privacy

**PhonePe Insights Analyzer is designed with privacy as the #1 priority.**

Your financial data is extremely sensitive. That's why this application:
- ✅ **Never sends your data to any external service**
- ✅ **No API keys or cloud services required**
- ✅ **All processing happens on your local machine**
- ✅ **No tracking, logging, or data collection**
- ✅ **Files are deleted immediately after processing**
- ✅ **No database - session storage only**

## How We Protect Your Data

### 1. No External Services
Unlike many modern apps that use cloud AI services (OpenAI, Anthropic, etc.), we use:
- **Rule-based pattern matching** instead of LLM APIs
- **Keyword matching** for categorization
- **Local calculations** for insights

### 2. No Network Calls
The application:
- ❌ Does NOT send data to OpenAI
- ❌ Does NOT send data to Anthropic
- ❌ Does NOT send data to any cloud service
- ❌ Does NOT phone home
- ✅ Works completely offline (after dependencies are installed)

### 3. Temporary File Storage
- PDF files are saved to `uploads/` folder temporarily
- Files are **deleted immediately** after text extraction
- No permanent storage of your PDFs

### 4. Session-Only Data
- Transaction data lives only in your browser session
- Data is cleared when you close the browser
- No database writes
- No persistent storage

### 5. Local Processing
All operations happen on your machine:
```
Your Computer
    ↓
1. Upload PDF → Saved temporarily
    ↓
2. Extract text → Pattern matching locally
    ↓
3. Parse transactions → Regex on your CPU
    ↓
4. Categorize → Keyword matching locally
    ↓
5. Generate insights → Math on your machine
    ↓
6. Display → Rendered in your browser
    ↓
7. Delete PDF → File removed from disk
```

**NO step involves external services!**

## What Data Is Stored?

### Temporarily (During Upload)
- PDF file in `uploads/` folder
- Deleted within seconds after processing

### In Session (While Using App)
- Extracted transaction data
- Generated insights
- Cleared when you close browser

### Permanently
- **NOTHING!**

## Can Anyone Access My Data?

**No!** Unless someone:
1. Has physical access to your computer
2. While you have the app open
3. And looks at your browser

The application:
- Has no user accounts
- Has no database
- Has no logging
- Has no remote access
- Cannot be accessed over the internet (runs on localhost only)

## Security Best Practices

### For Maximum Security:
1. **Run locally only** - Don't deploy to a public server
2. **Close browser** when done - Clears session data
3. **Secure your computer** - Standard OS security
4. **Use password-protected PDFs** - If available
5. **Don't screenshot** sensitive data

### If You Want to Deploy:
If you need to deploy this for multiple users:
1. Use HTTPS (SSL/TLS)
2. Add user authentication
3. Implement proper session management
4. Add database with encryption
5. Follow OWASP security guidelines

## Comparison: LLM vs Local Processing

### Original Design (LLM-based)
```
Your PDF → Upload → OpenAI API → Transaction Data
          ⚠️ Data sent to external server
          ⚠️ API key required
          ⚠️ Costs money per request
          ⚠️ Subject to OpenAI privacy policy
```

### Current Design (Privacy-First)
```
Your PDF → Upload → Local Pattern Matching → Transaction Data
          ✅ Everything on your machine
          ✅ No API keys needed
          ✅ Completely free
          ✅ You control the data 100%
```

## Source Code Transparency

This is an open-source project. You can:
- ✅ Review all source code
- ✅ Verify no external calls are made
- ✅ See exactly how your data is processed
- ✅ Modify for your own needs
- ✅ Audit for security

Key files to review:
- `transaction_parser.py` - No LLM imports
- `insights_generator.py` - Pure math calculations
- `app.py` - No external API calls
- `requirements.txt` - No OpenAI/Anthropic packages

## Limitations of Privacy-First Approach

### Trade-offs:
1. **Accuracy** - Pattern matching may miss some transactions that LLM would catch
2. **Flexibility** - Works best with standard PhonePe PDF formats
3. **Categorization** - Keyword-based, not context-aware like AI
4. **Languages** - English keywords only (can be extended)

### Worth It Because:
- ✅ Your financial data stays private
- ✅ No subscription costs
- ✅ Works offline
- ✅ No rate limits
- ✅ Instant processing
- ✅ Peace of mind

## Questions?

### "Can I trust this app?"
- Check the source code - it's all visible
- No network calls except during initial setup (pip install)
- Run offline after dependencies are installed

### "What about Flask secret key?"
- Used only for session cookies in your browser
- Doesn't leave your machine
- Can be any random string

### "Is the PDF password secure?"
- Only used to decrypt PDF locally
- Never stored or transmitted
- Cleared from memory after use

### "Can this be hacked?"
- If someone has access to your computer, yes
- Same as any local application
- Use standard OS security practices

### "What about browser history?"
- Session data only, not in history
- Clear on browser close
- Use incognito/private mode if concerned

## Bottom Line

**Your financial data is YOUR data.**

We built this tool to help you analyze your spending **without sacrificing privacy**. Every design decision prioritizes keeping your data on your machine, under your control.

If you're not comfortable with cloud AI services accessing your financial transactions, this tool is for you.

---

**Questions or concerns?** Review the source code or ask!
