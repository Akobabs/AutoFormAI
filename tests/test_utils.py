import unittest
from app.utils.validators import validate_email, validate_name, validate_suggestion

class TestUtils(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))

    def test_validate_name(self):
        self.assertTrue(validate_name("John Doe"))
        self.assertFalse(validate_name("John123"))

    def test_validate_suggestion(self):
        self.assertTrue(validate_suggestion("test@example.com"))
        self.assertTrue(validate_suggestion("John Doe"))
        self.assertFalse(validate_suggestion("<script>"))

if __name__ == '__main__':
    unittest.main()