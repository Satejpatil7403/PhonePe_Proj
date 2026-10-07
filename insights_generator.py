"""
Insights Generator Module
Generates detailed analytics and insights from transactions
NO LLM - All processing done locally for privacy
"""

from typing import List, Dict
from datetime import datetime
from collections import defaultdict


class InsightsGenerator:
    """Generate financial insights from transactions"""
    
    def __init__(self):
        pass  # No LLM client needed
    
    def generate_insights(self, transactions: List[Dict]) -> Dict:
        """
        Generate comprehensive insights using local calculations
        
        Args:
            transactions: List of categorized transactions
            
        Returns:
            Dictionary of insights
        """
        return self.calculate_insights_manually(transactions)
    
    def calculate_insights_manually(self, transactions: List[Dict]) -> Dict:
        """
        Calculate insights without LLM (fallback)
        
        Args:
            transactions: List of transactions
            
        Returns:
            Dictionary of calculated insights
        """
        if not transactions:
            return self._empty_insights()
        
        # Basic totals
        total_debit = sum(t['amount'] for t in transactions if t['direction'] == 'debit')
        total_credit = sum(t['amount'] for t in transactions if t['direction'] == 'credit')
        net_flow = total_credit - total_debit
        
        # Top categories
        category_totals = defaultdict(float)
        for t in transactions:
            if t['direction'] == 'debit':
                category_totals[t.get('category', 'other')] += t['amount']
        
        top_categories = [
            {'category': cat, 'total_amount': round(amt, 2)}
            for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Top merchants
        merchant_totals = defaultdict(float)
        for t in transactions:
            if t['direction'] == 'debit':
                merchant_totals[t.get('merchant', 'Unknown')] += t['amount']
        
        top_merchants = [
            {'merchant': merch, 'total_amount': round(amt, 2)}
            for merch, amt in sorted(merchant_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # Daily spend trend
        daily_spend = defaultdict(float)
        for t in transactions:
            if t['direction'] == 'debit' and t.get('date'):
                try:
                    # Try to parse the date - handle multiple formats
                    date_str = t['date']
                    date_obj = None
                    
                    # Try ISO format first
                    try:
                        date_obj = datetime.fromisoformat(date_str)
                    except:
                        # Try other common formats
                        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y', '%d-%m-%y', '%d/%m/%y']:
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                break
                            except:
                                continue
                    
                    if date_obj:
                        day_key = date_obj.strftime('%Y-%m-%d')
                        daily_spend[day_key] += t['amount']
                except Exception as e:
                    print(f"Error parsing date '{t.get('date')}': {e}")
                    pass
        
        daily_spend_trend = [
            {'day': day, 'total_amount': round(amt, 2)}
            for day, amt in sorted(daily_spend.items())
        ]
        
        # Monthly spend trend
        monthly_spend = defaultdict(float)
        for t in transactions:
            if t['direction'] == 'debit' and t.get('date'):
                try:
                    # Try to parse the date - handle multiple formats
                    date_str = t['date']
                    date_obj = None
                    
                    # Try ISO format first
                    try:
                        date_obj = datetime.fromisoformat(date_str)
                    except:
                        # Try other common formats
                        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y', '%d-%m-%y', '%d/%m/%y']:
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                break
                            except:
                                continue
                    
                    if date_obj:
                        month_key = date_obj.strftime('%Y-%m')
                        monthly_spend[month_key] += t['amount']
                except:
                    pass
        
        monthly_spend_trend = [
            {'month': month, 'total_amount': round(amt, 2)}
            for month, amt in sorted(monthly_spend.items())
        ]
        
        # Anomalies (transactions > 2x average)
        debit_amounts = [t['amount'] for t in transactions if t['direction'] == 'debit']
        avg_debit = sum(debit_amounts) / len(debit_amounts) if debit_amounts else 0
        threshold = avg_debit * 2
        
        anomalies = [
            {
                'date': t.get('date'),
                'merchant': t.get('merchant'),
                'amount': t['amount'],
                'reason': f'Amount {round(t["amount"] / avg_debit, 1)}x higher than average'
            }
            for t in transactions
            if t['direction'] == 'debit' and t['amount'] > threshold
        ]
        
        return {
            'total_debit': round(total_debit, 2),
            'total_credit': round(total_credit, 2),
            'net_flow': round(net_flow, 2),
            'top_categories': top_categories,
            'top_merchants': top_merchants,
            'daily_spend_trend': daily_spend_trend,
            'monthly_spend_trend': monthly_spend_trend,
            'anomalies': anomalies,
            'transaction_count': len(transactions),
            'debit_count': sum(1 for t in transactions if t['direction'] == 'debit'),
            'credit_count': sum(1 for t in transactions if t['direction'] == 'credit'),
            'average_debit': round(avg_debit, 2) if avg_debit > 0 else 0,
        }
    
    def _empty_insights(self) -> Dict:
        """Return empty insights structure"""
        return {
            'total_debit': 0.0,
            'total_credit': 0.0,
            'net_flow': 0.0,
            'top_categories': [],
            'top_merchants': [],
            'daily_spend_trend': [],
            'monthly_spend_trend': [],
            'anomalies': [],
            'transaction_count': 0,
            'debit_count': 0,
            'credit_count': 0,
            'average_debit': 0.0,
        }
    
    def get_category_breakdown(self, transactions: List[Dict]) -> List[Dict]:
        """Get detailed breakdown by category"""
        category_data = defaultdict(lambda: {'total': 0.0, 'count': 0, 'transactions': []})
        
        for t in transactions:
            if t['direction'] == 'debit':
                cat = t.get('category', 'other')
                category_data[cat]['total'] += t['amount']
                category_data[cat]['count'] += 1
                category_data[cat]['transactions'].append(t)
        
        return [
            {
                'category': cat,
                'total_amount': round(data['total'], 2),
                'transaction_count': data['count'],
                'average_amount': round(data['total'] / data['count'], 2) if data['count'] > 0 else 0,
            }
            for cat, data in sorted(category_data.items(), key=lambda x: x[1]['total'], reverse=True)
        ]
