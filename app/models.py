import sqlite3
import pickle
import os

MODEL_PATH = 'models/trie_model.pkl'

class Trie:
    def __init__(self):
        self.root = {}
        self.end = '*'

    def insert(self, word):
        node = self.root
        for char in word.lower():
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end] = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node:
                return []
            node = node[char]
        return self._collect_words(node, prefix.lower())

    def _collect_words(self, node, prefix):
        words = []
        if self.end in node:
            words.append(prefix)
        for char, child in node.items():
            if char != self.end:
                words.extend(self._collect_words(child, prefix + char))
        return words

def get_db_connection():
    conn = sqlite3.connect('app/data/autocomplete.db')
    conn.row_factory = sqlite3.Row
    return conn

def load_suggestions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM suggestions')
    suggestions = [row['text'] for row in cursor.fetchall()]
    conn.close()
    return suggestions

def add_suggestion(text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO suggestions (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()

def load_trie_from_pickle():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    else:
        return Trie()
