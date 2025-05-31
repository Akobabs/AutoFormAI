import pickle
import os
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import json

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_word: bool = False
        self.frequency: int = 0
        self.suggestions: Set[str] = set()

class EnhancedTrie:
    def __init__(self):
        self.root = TrieNode()
        self.word_frequency: Dict[str, int] = defaultdict(int)
        self.recent_searches: List[str] = []
        self.max_recent = 100
        
    def insert(self, word: str, frequency: int = 1) -> None:
        """Insert word with frequency weighting"""
        if not word:
            return
            
        word = word.lower().strip()
        self.word_frequency[word] += frequency
        
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.suggestions.add(word)
            
        node.is_end_word = True
        node.frequency = self.word_frequency[word]
    
    def search_prefix(self, prefix: str, limit: int = 10) -> List[Tuple[str, int]]:
        """Search with frequency-based ranking"""
        if not prefix:
            return self._get_popular_suggestions(limit)
            
        prefix = prefix.lower().strip()
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Get suggestions with frequencies
        suggestions = []
        for word in node.suggestions:
            if word.startswith(prefix):
                freq = self.word_frequency[word]
                suggestions.append((word, freq))
        
        # Sort by frequency (descending) and alphabetically
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        return suggestions[:limit]
    
    def _get_popular_suggestions(self, limit: int) -> List[Tuple[str, int]]:
        """Get most popular suggestions when no prefix"""
        popular = sorted(
            self.word_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return popular[:limit]
    
    def add_search(self, query: str) -> None:
        """Track recent searches for analytics"""
        if query and query not in self.recent_searches:
            self.recent_searches.insert(0, query)
            if len(self.recent_searches) > self.max_recent:
                self.recent_searches.pop()
    
    def get_analytics(self) -> Dict:
        """Get usage analytics"""
        return {
            'total_words': len(self.word_frequency),
            'recent_searches': self.recent_searches[:20],
            'top_searches': sorted(
                self.word_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:20]
        }
    
    def save(self, filepath: str) -> None:
        """Save trie to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, filepath: str) -> 'EnhancedTrie':
        """Load trie from file"""
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()