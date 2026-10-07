
"""
Flask Application - PhonePe Insights Analyzer
Main application file with routes and business logic
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from pdf_processor import extract_text_from_pdf
from transaction_parser import TransactionParser
from insights_generator import InsightsGenerator

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production-vercel-deployment')

# Use /tmp for Vercel serverless functions (writable directory)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure /tmp exists (it should on Vercel)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize processors
transaction_parser = TransactionParser()
insights_generator = InsightsGenerator()

# In-memory storage (replace with database in production)
sessions_data = {}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/upload')
def upload():
    """Upload screen"""
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Debug: log request info to help diagnose upload issues (kept concise)
        app.logger.debug('Upload request content_type: %s', request.content_type)
        try:
            app.logger.debug('request.files keys: %s', list(request.files.keys()))
        except Exception:
            app.logger.debug('Could not read request.files')
        try:
            app.logger.debug('request.form keys: %s', list(request.form.keys()))
        except Exception:
            app.logger.debug('Could not read request.form')

        # Check if file is present
        if 'pdf_file' not in request.files:
            # If the client used a different field name, accept the first file found as a fallback.
            if len(request.files) == 0:
                # Return helpful debug info to client (non-sensitive)
                return jsonify({
                    'error': 'No file uploaded',
                    'debug': {
                        'content_type': request.content_type,
                        'files': list(request.files.keys()),
                        'form_keys': list(request.form.keys())
                    }
                }), 400
            else:
                # Use the first available file field as a fallback
                first_key = next(iter(request.files))
                file = request.files[first_key]
        else:
            file = request.files['pdf_file']
        # Log filename and content type for debugging
        try:
            app.logger.debug('Uploaded file -> filename: %s, content_type: %s', file.filename, getattr(file, 'content_type', None))
        except Exception:
            app.logger.debug('Could not read uploaded file metadata')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400
        
        # Get password if provided
        password = request.form.get('password', None)
        if password == '':
            password = None
        
        # Save file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Extract text from PDF
        try:
            # Log file path and size to help debug extraction failures
            try:
                file_size = os.path.getsize(filepath)
            except Exception:
                file_size = None
            app.logger.debug('Saved file path: %s (size=%s bytes)', filepath, file_size)

            raw_text = extract_text_from_pdf(filepath, password)
        except Exception as e:
            # Log full exception with traceback for diagnosis
            app.logger.exception('PDF extraction failed for %s', filepath)
            try:
                os.remove(filepath)
            except Exception:
                app.logger.debug('Failed to remove file during error cleanup: %s', filepath)
            return jsonify({'error': f'Failed to extract text from PDF: {str(e)}'}), 400
        
        # Process transactions
        try:
            result = transaction_parser.process_full_pipeline(raw_text)
            transactions = result.get('transactions', [])
            
            # Generate insights
            if 'insights' not in result or not result['insights']:
                insights = insights_generator.calculate_insights_manually(transactions)
            else:
                insights = result['insights']
            
        except Exception as e:
            app.logger.exception('Transaction processing failed')
            try:
                os.remove(filepath)
            except Exception:
                app.logger.debug('Failed to remove file during error cleanup after processing error: %s', filepath)
            return jsonify({'error': f'Failed to process transactions: {str(e)}'}), 500
        
        # Store in session
        session_id = str(uuid.uuid4())
        sessions_data[session_id] = {
            'transactions': transactions,
            'insights': insights,
            'filename': filename,
            'upload_time': datetime.now().isoformat()
        }
        
        # Clean up file
        os.remove(filepath)
        
        # Store session ID
        session['session_id'] = session_id
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'redirect': url_for('dashboard')
        })
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/dashboard')
def dashboard():
    """Dashboard screen with insights"""
    session_id = session.get('session_id')
    
    if not session_id or session_id not in sessions_data:
        return redirect(url_for('upload'))
    
    data = sessions_data[session_id]
    return render_template(
        'dashboard.html',
        insights=data['insights'],
        transactions=data['transactions'],
        filename=data['filename']
    )


@app.route('/transaction/<int:index>')
def transaction_detail(index):
    """Transaction detail screen"""
    session_id = session.get('session_id')
    
    if not session_id or session_id not in sessions_data:
        return redirect(url_for('upload'))
    
    data = sessions_data[session_id]
    transactions = data['transactions']
    
    if index < 0 or index >= len(transactions):
        return "Transaction not found", 404
    
    transaction = transactions[index]
    
    # Get available categories
    categories = [
        'fuel', 'groceries', 'personal_transfer', 'education',
        'recharge', 'dining', 'shopping', 'government', 'other'
    ]
    
    return render_template(
        'transaction_detail.html',
        transaction=transaction,
        index=index,
        categories=categories
    )


@app.route('/api/update_category', methods=['POST'])
def update_category():
    """Update transaction category"""
    session_id = session.get('session_id')
    
    if not session_id or session_id not in sessions_data:
        return jsonify({'error': 'Session expired'}), 401
    
    data = request.get_json()
    index = data.get('index')
    new_category = data.get('category')
    
    if index is None or new_category is None:
        return jsonify({'error': 'Missing parameters'}), 400
    
    session_data = sessions_data[session_id]
    transactions = session_data['transactions']
    
    if index < 0 or index >= len(transactions):
        return jsonify({'error': 'Invalid transaction index'}), 400
    
    # Update category
    transactions[index]['category'] = new_category
    
    # Regenerate insights
    insights = insights_generator.calculate_insights_manually(transactions)
    session_data['insights'] = insights
    
    return jsonify({'success': True, 'insights': insights})


@app.route('/api/export')
def export_data():
    """Export transactions as JSON"""
    session_id = session.get('session_id')
    
    if not session_id or session_id not in sessions_data:
        return jsonify({'error': 'Session expired'}), 401
    
    data = sessions_data[session_id]
    
    export = {
        'filename': data['filename'],
        'export_time': datetime.now().isoformat(),
        'transactions': data['transactions'],
        'insights': data['insights']
    }
    
    return jsonify(export)


@app.route('/api/data')
def get_data():
    """Get current session data"""
    session_id = session.get('session_id')
    
    if not session_id or session_id not in sessions_data:
        return jsonify({'error': 'Session expired'}), 401
    
    return jsonify(sessions_data[session_id])


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=5000)
