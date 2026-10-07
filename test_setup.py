"""
Test script to verify the application setup
Run this after installing dependencies to check if everything is configured correctly
"""

import sys
import os

def test_python_version():
    """Test Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version: OK (Python {}.{}.{})".format(version.major, version.minor, version.micro))
        return True
    else:
        print("✗ Python version: FAIL (Python 3.8+ required)")
        return False

def test_dependencies():
    """Test if all dependencies are installed"""
    required = [
        'flask',
        'PyPDF2',
        'pdfplumber',
        'dotenv',
        'werkzeug',
        'PIL'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"✓ {package}: OK")
        except ImportError:
            print(f"✗ {package}: MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n✗ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies: OK")
        return True

def test_env_file():
    """Test if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("✗ .env file: MISSING")
        print("Copy .env.example to .env and configure it")
        return False
    
    print("✓ .env file: EXISTS")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['FLASK_SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            print(f"✗ {var}: NOT CONFIGURED")
            missing_vars.append(var)
        else:
            print(f"✓ {var}: CONFIGURED")
    
    if missing_vars:
        print(f"\n⚠ Missing configuration: {', '.join(missing_vars)}")
        print("Note: API keys not needed - all processing is done locally!")
        return True  # Not critical, just a warning
    else:
        print("\n✓ Environment configuration: OK")
        return True

def test_folders():
    """Test if required folders exist"""
    folders = ['uploads', 'static', 'static/css', 'static/js', 'templates']
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"✗ {folder}: MISSING")
            os.makedirs(folder, exist_ok=True)
            print(f"  → Created {folder}")
        else:
            print(f"✓ {folder}: EXISTS")
    
    return True

def test_modules():
    """Test if custom modules can be imported"""
    modules = [
        'prompts',
        'pdf_processor',
        'transaction_parser',
        'insights_generator',
        'app'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}: OK")
        except Exception as e:
            print(f"✗ {module}: FAIL - {str(e)}")
            return False
    
    print("\n✓ All modules: OK")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("PhonePe Insights Analyzer - Setup Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Folders", test_folders),
        ("Environment File", test_env_file),
        ("Modules", test_modules),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! You can now run: python app.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
