import unittest
from app.models.trie import EnhancedTrie
from app.models.suggestions import SuggestionManager

class TestModels(unittest.TestCase):
    def setUp(self):
        self.trie = EnhancedTrie()
        self.manager = SuggestionManager()

    def test_trie_insert_search(self):
        self.trie.insert("John", 5)
        self.trie.insert("Jane", 3)
        suggestions = self.trie.search_prefix("Jo")
        self.assertEqual(len(suggestions), 2)
        self.assertEqual(suggestions[0][0], "John")  # Higher frequency first

    def test_suggestion_manager(self):
        self.manager.add_suggestion("Test", "general")
        suggestions = self.manager.get_suggestions("Te")
        self.assertTrue(any(s['text'] == "Test" for s in suggestions))

if __name__ == '__main__':
    unittest.main()