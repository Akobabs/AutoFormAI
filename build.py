from app.models import Trie
import pickle
import pandas as pd
import os

MODEL_PATH = 'models/trie_model.pkl'

# Load your CSV or data here
df = pd.read_csv('data/autocomplete_dataset.csv')  # Adjust to your CSV path and name
names = df['name'].dropna().unique()
emails = df['email'].dropna().unique()

# Build Trie
trie = Trie()
for item in list(names) + list(emails):
    trie.insert(str(item).strip())

# Save to pickle
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(trie, f)

print("✅ Trie saved to", MODEL_PATH)
