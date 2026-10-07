"""
Transaction Parser Module
Handles transaction extraction and categorization using rule-based logic
NO LLM - All processing done locally for privacy
"""

import json
import re
from typing import List, Dict
from datetime import datetime


class TransactionParser:
    """Parse and categorize transactions from raw text using pattern matching"""
    
    def __init__(self):
        # Category keywords mapping
        self.category_keywords = {
            'fuel': ['petrol', 'pump', 'diesel', 'fuel', 'gas', 'bharat petroleum', 'indian oil', 'hp', 'shell', 'essar'],
            'groceries': ['grocery', 'kirana', 'supermarket', 'store', 'mart', 'market', 'vegetable', 'fruit', 'food', 'provisions'],
            'dining': ['restaurant', 'cafe', 'hotel', 'swiggy', 'zomato', 'domino', 'pizza', 'mcdonald', 'kfc', 'food', 'dining'],
            'shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'shopping', 'mall', 'store', 'shop', 'retail', 'meesho'],
            'recharge': ['recharge', 'mobile', 'prepaid', 'airtel', 'jio', 'vodafone', 'vi', 'bsnl', 'dth', 'broadband'],
            'education': ['school', 'college', 'university', 'education', 'course', 'exam', 'fee', 'tuition', 'learning'],
            'government': ['government', 'tax', 'challan', 'municipal', 'electricity', 'water', 'bill', 'lic', 'insurance'],
            'personal_transfer': ['transfer', 'upi', 'sent to', 'received from', 'wallet'],
        }
    
    def extract_transactions(self, raw_text: str) -> List[Dict]:
        """
        Extract structured transactions from raw text using pattern matching
        
        Args:
            raw_text: Raw OCR text from PDF
            
        Returns:
            List of transaction dictionaries
        """
        transactions = []
        lines = raw_text.split('\n')
        
        # Filter out page numbers and irrelevant lines
        filtered_lines = []
        page_pattern = r'(?:page|pg)\s+\d+\s+of\s+\d+|^\d+\s+of\s+\d+$'
        for line in lines:
            line_stripped = line.strip()
            # Skip empty lines, page numbers, and header/footer noise
            if (not line_stripped or 
                re.search(page_pattern, line_stripped, re.IGNORECASE) or
                line_stripped.lower() in ['phonepe', 'statement', 'transaction history', 'page']):
                continue
            filtered_lines.append(line)
        
        lines = filtered_lines
        
        # Debug: Print first 20 lines to see what we're working with
        print("\n=== DEBUG: First 20 lines of PDF text (after filtering) ===")
        for idx, line in enumerate(lines[:20]):
            print(f"{idx}: {line.strip()}")
        print("=" * 50)
        
        # Enhanced transaction patterns
        date_pattern = r'\b(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}|\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b'
        time_pattern = r'\b(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\b'
        # More flexible amount pattern
        amount_pattern = r'(?:Rs\.?|INR|₹|Amount[:\s]*)\s*([0-9,]+(?:\.[0-9]{1,2})?)|([0-9,]+(?:\.[0-9]{1,2})?)\s*(?:Rs\.?|INR|₹)'
        
        i = 0
        found_count = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Try to extract a transaction from current position
            transaction = self._extract_single_transaction(lines, i, date_pattern, time_pattern, amount_pattern)
            if transaction:
                found_count += 1
                print(f"\n✓ Found transaction #{found_count}: {transaction.get('merchant', 'Unknown')} - ₹{transaction.get('amount', 0)}")
                transactions.append(self._validate_transaction(transaction))
                i += 5  # Skip ahead to avoid duplicates
            else:
                i += 1
        
        print(f"\n=== Total transactions found: {len(transactions)} ===\n")
        return transactions
    
    def categorize_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """
        Add category field to transactions using keyword matching
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Transactions with added 'category' field
        """
        if not transactions:
            return []
        
        for transaction in transactions:
            merchant = transaction.get('merchant', '').lower()
            category = self._categorize_merchant(merchant)
            transaction['category'] = category
        
        return transactions
    
    def _categorize_merchant(self, merchant: str) -> str:
        """Categorize merchant based on keywords"""
        merchant_lower = merchant.lower()
        
        # Check each category's keywords
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in merchant_lower:
                    return category
        
        return 'other'
    
    def process_full_pipeline(self, raw_text: str) -> Dict:
        """
        Run full extraction, categorization, and insights pipeline
        
        Args:
            raw_text: Raw OCR text from PDF
            
        Returns:
            Dictionary with 'transactions' and 'insights' keys
        """
        # Extract transactions
        transactions = self.extract_transactions(raw_text)
        
        # Categorize transactions
        categorized = self.categorize_transactions(transactions)
        
        return {
            'transactions': categorized,
            'insights': None  # Will be generated separately
        }
    
    def _extract_single_transaction(self, lines: List[str], start_idx: int, 
                                    date_pattern: str, time_pattern: str, 
                                    amount_pattern: str) -> Dict:
        """Extract a single transaction from lines starting at index"""
        transaction = {
            'date': None,
            'time': None,
            'merchant': None,
            'direction': 'debit',
            'amount': 0.0,
            'transaction_id': None,
            'utr_number': None,
            'account_reference': None
        }
        
        # Look ahead up to 10 lines for transaction data
        end_idx = min(start_idx + 10, len(lines))
        context_lines = lines[start_idx:end_idx]
        context_text = ' '.join(context_lines)
        
        # Extract date
        date_match = re.search(date_pattern, context_text)
        if date_match:
            transaction['date'] = self._normalize_date(date_match.group(1))
        
        # Extract time
        time_match = re.search(time_pattern, context_text)
        if time_match:
            transaction['time'] = self._normalize_time(time_match.group(1))
        
        # Extract amount
        amount_match = re.search(amount_pattern, context_text, re.IGNORECASE)
        if amount_match:
            amount_str = amount_match.group(1) or amount_match.group(2)
            transaction['amount'] = self._parse_amount(amount_str)
        else:
            return None  # No amount, probably not a transaction
        
        # Extract merchant/recipient
        merchant = self._extract_merchant(context_lines)
        if merchant:
            transaction['merchant'] = merchant
        else:
            return None  # No merchant, probably not a transaction
        
        # Detect direction (credit or debit)
        transaction['direction'] = self._detect_direction(context_text)
        
        # Extract transaction ID
        txn_id = self._extract_pattern(context_text, r'(?:transaction|txn|trans|ref)\s*(?:id|no|number)?\s*[:=#]?\s*([A-Z0-9]{10,})', 1)
        if txn_id:
            transaction['transaction_id'] = txn_id
        
        # Extract UTR
        utr = self._extract_pattern(context_text, r'(?:utr|ref\s*no)?\s*[:=#]?\s*([0-9]{12,})', 1)
        if utr:
            transaction['utr_number'] = utr
        
        # Extract account reference
        account = self._extract_pattern(context_text, r'(?:account|a/c)?\s*(?:xxxx|x{4})?(\d{4})', 1)
        if account:
            transaction['account_reference'] = account
        
        return transaction if transaction['date'] and transaction['amount'] > 0 else None
    
    def _validate_transaction(self, transaction: Dict) -> Dict:
        """Validate and clean a transaction object"""
        # Ensure required fields
        required_fields = ['date', 'merchant', 'direction', 'amount']
        for field in required_fields:
            if field not in transaction or transaction[field] is None:
                if field == 'direction':
                    transaction[field] = 'debit'
                elif field == 'amount':
                    transaction[field] = 0.0
                else:
                    transaction[field] = ''
        
        # Ensure numeric amount
        try:
            transaction['amount'] = float(transaction['amount'])
        except (ValueError, TypeError):
            transaction['amount'] = 0.0
        
        # Ensure category exists
        if 'category' not in transaction:
            transaction['category'] = 'other'
        
        # Add optional fields as null if missing
        optional_fields = ['time', 'transaction_id', 'utr_number', 'account_reference']
        for field in optional_fields:
            if field not in transaction:
                transaction[field] = None
        
        return transaction
    
    def _normalize_date(self, date_str: str) -> str:
        """Convert date to ISO format (yyyy-mm-dd)"""
        try:
            # Try different date formats
            for fmt in ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%y', '%d/%m/%y']:
                try:
                    dt = datetime.strptime(date_str.strip(), fmt)
                    return dt.strftime('%Y-%m-%d')
                except:
                    continue
            return date_str
        except:
            return date_str
    
    def _normalize_time(self, time_str: str) -> str:
        """Convert time to 24-hour format (HH:MM)"""
        try:
            time_str = time_str.strip().upper()
            # Handle 12-hour format with AM/PM
            if 'AM' in time_str or 'PM' in time_str:
                for fmt in ['%I:%M %p', '%I:%M:%S %p']:
                    try:
                        dt = datetime.strptime(time_str, fmt)
                        return dt.strftime('%H:%M')
                    except:
                        continue
            # Already 24-hour format
            else:
                for fmt in ['%H:%M', '%H:%M:%S']:
                    try:
                        dt = datetime.strptime(time_str, fmt)
                        return dt.strftime('%H:%M')
                    except:
                        continue
            return time_str
        except:
            return time_str
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float"""
        try:
            # Remove commas and any non-numeric characters except decimal point
            clean_amount = re.sub(r'[^\d.]', '', amount_str)
            return float(clean_amount)
        except:
            return 0.0
    
    def _extract_merchant(self, lines: List[str]) -> str:
        """Extract merchant/recipient name from lines"""
        # Keywords that indicate merchant name (expanded list)
        merchant_indicators = [
            'to:', 'to ', 'merchant:', 'from:', 'recipient:', 'payee:', 
            'paid to:', 'sent to:', 'received from:', 'transfer to:',
            'payment to:', 'money sent to:'
        ]
        
        # Invalid merchant patterns to skip
        invalid_patterns = [
            r'^\d{1,2}:\d{2}\s*(am|pm)',  # Time stamps like "10:21 PM"
            r'^(transaction|txn|trans)\s*(id|no|number)',  # "Transaction ID"
            r'^(utr|ref)\s*(no|number)',  # "UTR No"
            r'^(debited|credited)\s*(from|to)',  # "Debited from"
            r'^xx\d+',  # Account numbers like "XX7875"
            r'^\d+$',  # Just numbers
            r'^[a-z]{1,3}$',  # Single short words
        ]
        
        for line in lines:
            line_stripped = line.strip()
            line_lower = line_stripped.lower()
            
            # Skip if line matches invalid patterns
            skip_line = False
            for pattern in invalid_patterns:
                if re.match(pattern, line_lower, re.IGNORECASE):
                    skip_line = True
                    break
            
            if skip_line:
                continue
            
            # Check for merchant indicators
            for indicator in merchant_indicators:
                if indicator in line_lower:
                    # Extract text after indicator
                    idx = line_lower.find(indicator)
                    merchant = line_stripped[idx + len(indicator):].strip()
                    # Remove common suffixes
                    merchant = re.sub(r'\s*(success|completed|failed|pending).*$', '', merchant, flags=re.IGNORECASE)
                    merchant = re.sub(r'\s+', ' ', merchant)
                    if len(merchant) > 2 and not any(re.match(p, merchant.lower()) for p in invalid_patterns):
                        return merchant[:100]
            
            # If line looks like a merchant name (not a label or number)
            if line_stripped and len(line_stripped) > 3:
                if not line_lower.startswith(('date', 'time', 'amount', 'status', 'transaction', 'upi', 'ref', 'utr', 'debited', 'credited')):
                    if not re.match(r'^[\d\s:/-]+$', line_stripped):  # Not just numbers/dates
                        # Check if it's not just a single word label
                        if ' ' in line_stripped or len(line_stripped) > 10:
                            # Final validation - must contain at least one letter
                            if re.search(r'[a-zA-Z]{3,}', line_stripped):
                                return line_stripped[:100]
        
        return 'Unknown Merchant'
    
    def _detect_direction(self, text: str) -> str:
        """Detect if transaction is debit or credit"""
        text_lower = text.lower()
        
        # Credit indicators
        credit_keywords = ['received', 'credit', 'credited', 'from', 'refund', 'cashback']
        # Debit indicators
        debit_keywords = ['paid', 'debit', 'debited', 'payment', 'sent', 'transfer to']
        
        credit_count = sum(1 for keyword in credit_keywords if keyword in text_lower)
        debit_count = sum(1 for keyword in debit_keywords if keyword in text_lower)
        
        if credit_count > debit_count:
            return 'credit'
        else:
            return 'debit'
    
    def _extract_pattern(self, text: str, pattern: str, group: int) -> str:
        """Extract text using regex pattern"""
        try:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(group).strip()
        except:
            pass
        return None
