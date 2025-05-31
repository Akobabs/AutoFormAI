from flask import Request
from typing import Tuple, Dict, Any
import json
from datetime import datetime

def get_client_info(request: Request) -> Tuple[str, str]:
    """Extract client information from request"""
    user_agent = request.headers.get('User-Agent', '')
    
    # Try to get real IP (considering proxies)
    ip_address = (
        request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or
        request.headers.get('X-Real-IP', '') or
        request.remote_addr or
        'unknown'
    )
    
    return user_agent[:500], ip_address  # Limit length

def format_analytics_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format analytics data for display"""
    formatted = {}
    
    if 'trie' in data:
        trie_data = data['trie']
        formatted['trie'] = {
            'total_words': trie_data.get('total_words', 0),
            'recent_searches': trie_data.get('recent_searches', [])[:10],
            'top_searches': trie_data.get('top_searches', [])[:10]
        }
    
    if 'database' in data:
        db_data = data['database']
        formatted['database'] = {
            'total_suggestions': db_data.get('total_suggestions', 0),
            'active_suggestions': db_data.get('active_suggestions', 0),
            'total_searches': db_data.get('total_searches', 0),
            'popular_suggestions': db_data.get('popular_suggestions', [])[:10]
        }
    
    return formatted

def export_data_to_json(data: Dict[str, Any], filename: str = None) -> str:
    """Export data to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'export_{timestamp}.json'
    
    filepath = f'data/exports/{filename}'
    
    try:
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filepath
    except Exception as e:
        print(f"Error exporting data: {e}")
        return ""

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using Levenshtein distance"""
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    max_len = max(len(text1), len(text2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein_distance(text1.lower(), text2.lower())
    return 1.0 - (distance / max_len)