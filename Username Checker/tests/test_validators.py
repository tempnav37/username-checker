import unittest

from src.validators import normalize_username


class UsernameValidatorTests(unittest.TestCase):
    def test_normalizes_case(self):
        self.assertEqual(normalize_username("Nav_123"), "nav_123")

    def test_rejects_empty_spaces_and_special_characters(self):
        for username in ("", "two words", "name!", " name"):
            with self.subTest(username=username), self.assertRaises(ValueError):
                normalize_username(username)

    def test_rejects_username_over_maximum_length(self):
        with self.assertRaises(ValueError):
            normalize_username("x" * 25)

    def test_allows_numbers_and_underscores(self):
        self.assertEqual(normalize_username("__007__"), "__007__")


if __name__ == "__main__":
    unittest.main()