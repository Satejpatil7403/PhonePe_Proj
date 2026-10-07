# PhonePe Insights Analyzer - Setup Script
# Run this script to automatically set up the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PhonePe Insights Analyzer - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "1. Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "2. Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   → Virtual environment already exists" -ForegroundColor Cyan
} else {
    python -m venv venv
    if ($?) {
        Write-Host "   ✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host ""
Write-Host "3. Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "   ✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ Could not activate. You may need to run:" -ForegroundColor Yellow
    Write-Host "     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Then run this script again." -ForegroundColor Yellow
    exit 1
}

# Upgrade pip
Write-Host ""
Write-Host "4. Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   ✓ Pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "5. Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($?) {
    Write-Host "   ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "   ✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create .env file
Write-Host ""
Write-Host "6. Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   → .env file already exists" -ForegroundColor Cyan
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "   ✓ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "   ⚠ IMPORTANT: Edit .env and add your API keys!" -ForegroundColor Yellow
    Write-Host "     - OPENAI_API_KEY=your_key_here" -ForegroundColor Yellow
}

# Create directories
Write-Host ""
Write-Host "7. Creating required directories..." -ForegroundColor Yellow
$dirs = @("uploads", "static", "static\css", "static\js", "templates")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✓ Created $dir" -ForegroundColor Green
    }
}

# Run tests
Write-Host ""
Write-Host "8. Running setup tests..." -ForegroundColor Yellow
python test_setup.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your OpenAI API key" -ForegroundColor White
Write-Host "2. Run: python app.py" -ForegroundColor White
Write-Host "3. Open: http://localhost:5000" -ForegroundColor White
Write-Host ""
