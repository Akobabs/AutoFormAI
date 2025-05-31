import os
from flask import Flask
from app import create_app, db
from app.models.database import Suggestion, SearchLog, UserInteraction
from app.models.suggestions import SuggestionManager
import pandas as pd
from faker import Faker

def init_database():
    """Initialize database with sample data"""
    app = create_app('development')

    # Use app context for all database operations
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")

        # Initialize suggestion manager
        suggestion_manager = SuggestionManager(load_trie_on_init=False)

        # Import names dataset if available
        names_file = 'data/raw/NationalNames.csv'
        if os.path.exists(names_file):
            print("📊 Importing names dataset...")
            imported_names = suggestion_manager.import_names_dataset(names_file)
            print(f"✓ Imported {imported_names} names")
        else:
            print("⚠️ Names dataset not found. Add NationalNames.csv to data/raw/")

            # Add some sample names
            sample_names = [
                'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma',
                'Christopher', 'Emily', 'Matthew', 'Jessica', 'Andrew', 'Ashley',
                'Joshua', 'Amanda', 'Daniel', 'Brittany', 'James', 'Samantha'
            ]

            for name in sample_names:
                suggestion_manager.add_suggestion(name, 'name')
            print(f"✓ Added {len(sample_names)} sample names")

        # Generate synthetic emails
        print("📧 Generating synthetic emails...")
        imported_emails = suggestion_manager.generate_synthetic_emails(500)
        print(f"✓ Generated {imported_emails} synthetic emails")

        # Add some common email domains for autocomplete
        common_domains = [
            '@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com',
            '@aol.com', '@icloud.com', '@protonmail.com', '@zoho.com'
        ]

        for domain in common_domains:
            suggestion_manager.add_suggestion(f'user{domain}', 'email')

        # Explicitly rebuild and save the trie
        print("🔄 Rebuilding and saving trie...")
        suggestion_manager.rebuild_trie()
        try:
            suggestion_manager.save_trie()
            print("✓ Trie saved successfully")
        except Exception as e:
            print(f"⚠️ Error saving trie: {e}")

        print("✓ Database initialization completed")
        print(f"\n📈 Statistics:")
        analytics = suggestion_manager.get_analytics()
        print(f"  - Total suggestions: {analytics['database']['total_suggestions']}")
        print(f"  - Active suggestions: {analytics['database']['active_suggestions']}")
        print(f"  - Words in trie: {analytics['trie']['total_words']}")

if __name__ == '__main__':
    init_database()