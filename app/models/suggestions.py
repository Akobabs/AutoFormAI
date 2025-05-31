from app.models.database import Suggestion, SearchLog, UserInteraction
from app.models.trie import EnhancedTrie
from app import db
from typing import List, Dict, Optional
import pandas as pd
from faker import Faker
import os

# Compute the base directory (same as in config/__init__.py)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
TRIE_DIR = os.path.join(BASE_DIR, 'app', 'data')
os.makedirs(TRIE_DIR, exist_ok=True)

class SuggestionManager:
    def __init__(self, load_trie_on_init=True):
        self.trie = EnhancedTrie()
        self.trie_path = os.path.join(TRIE_DIR, 'enhanced_trie.pkl')
        self.load_trie_on_init = load_trie_on_init
        if self.load_trie_on_init:
            self.load_trie()

    def load_trie(self) -> None:
        """Load or create trie"""
        if os.path.exists(self.trie_path) and os.path.getsize(self.trie_path) > 0:
            try:
                self.trie = EnhancedTrie.load(self.trie_path)
            except Exception as e:
                print(f"⚠️ Error loading trie from {self.trie_path}: {e}. Rebuilding trie...")
                self.rebuild_trie()
        else:
            print(f"⚠️ Trie file not found or empty at {self.trie_path}. Rebuilding trie...")
            self.rebuild_trie()

    def rebuild_trie(self) -> None:
        """Rebuild trie from database"""
        suggestions = Suggestion.query.filter_by(is_active=True).all()
        self.trie = EnhancedTrie()

        for suggestion in suggestions:
            self.trie.insert(suggestion.text, suggestion.frequency)

        self.save_trie()

    def save_trie(self) -> None:
        """Save trie to disk"""
        try:
            self.trie.save(self.trie_path)
        except Exception as e:
            raise Exception(f"Failed to save trie to {self.trie_path}: {e}")

    def get_suggestions(self, prefix: str, limit: int = 10) -> List[Dict]:
        """Get autocomplete suggestions"""
        suggestions = self.trie.search_prefix(prefix, limit)
        return [{'text': text, 'frequency': freq} for text, freq in suggestions]

    def add_suggestion(self, text: str, category: str = 'general') -> bool:
        """Add new suggestion"""
        try:
            suggestion = Suggestion.query.filter_by(text=text).first()

            if suggestion:
                suggestion.frequency += 1
                suggestion.updated_at = db.func.now()
            else:
                suggestion = Suggestion(text=text, category=category)
                db.session.add(suggestion)

            db.session.commit()

            # Update trie
            self.trie.insert(text, suggestion.frequency)
            self.save_trie()

            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding suggestion: {e}")
            return False

    def log_search(self, query: str, results_count: int,
                   user_agent: str = None, ip_address: str = None) -> None:
        """Log search query"""
        try:
            log = SearchLog(
                query=query,
                results_count=results_count,
                user_agent=user_agent,
                ip_address=ip_address
            )
            db.session.add(log)
            db.session.commit()

            self.trie.add_search(query)
        except Exception as e:
            db.session.rollback()
            print(f"Error logging search: {e}")

    def log_interaction(self, suggestion_text: str, action: str) -> None:
        """Log user interaction"""
        try:
            suggestion = Suggestion.query.filter_by(text=suggestion_text).first()
            if suggestion:
                interaction = UserInteraction(
                    suggestion_id=suggestion.id,
                    action=action
                )
                db.session.add(interaction)

                # Increase frequency for popular suggestions
                if action in ['select', 'submit']:
                    suggestion.frequency += 1

                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error logging interaction: {e}")

    def get_analytics(self) -> Dict:
        """Get comprehensive analytics"""
        trie_analytics = self.trie.get_analytics()

        # Database analytics using db.session.query
        total_suggestions = db.session.query(Suggestion).count()
        active_suggestions = db.session.query(Suggestion).filter_by(is_active=True).count()
        total_searches = db.session.query(SearchLog).count()

        # Popular suggestions from DB
        popular_db = db.session.query(
            Suggestion.text,
            Suggestion.frequency
        ).order_by(Suggestion.frequency.desc()).limit(20).all()

        return {
            'trie': trie_analytics,
            'database': {
                'total_suggestions': total_suggestions,
                'active_suggestions': active_suggestions,
                'total_searches': total_searches,
                'popular_suggestions': [
                    {'text': text, 'frequency': freq}
                    for text, freq in popular_db
                ]
            }
        }

    def import_names_dataset(self, filepath: str) -> int:
        """Import names from CSV dataset"""
        try:
            df = pd.read_csv(filepath)
            imported = 0

            # Group by name and sum counts
            name_counts = df.groupby('Name')['Count'].sum().to_dict()

            for name, count in name_counts.items():
                if self.add_suggestion(name, 'name'):
                    # Update frequency based on historical data
                    suggestion = Suggestion.query.filter_by(text=name).first()
                    if suggestion:
                        suggestion.frequency = max(count // 1000, 1)  # Scale down
                        db.session.commit()
                    imported += 1

            self.rebuild_trie()
            return imported

        except Exception as e:
            print(f"Error importing dataset: {e}")
            return 0

    def generate_synthetic_emails(self, count: int = 1000) -> int:
        """Generate synthetic email data"""
        fake = Faker()
        imported = 0

        try:
            for _ in range(count):
                email = fake.email()
                if self.add_suggestion(email, 'email'):
                    imported += 1

            return imported

        except Exception as e:
            print(f"Error generating emails: {e}")
            return 0