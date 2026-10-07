import unittest

from src.username_manager import UsernameManager


class UsernameManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = UsernameManager(table_size=7)

    def test_case_insensitive_check_and_add(self):
        added = self.manager.add("Nav123")
        self.assertTrue(added["added"])
        self.assertFalse(self.manager.check("NAV123")["available"])
        self.assertFalse(self.manager.add("nav123")["added"])

    def test_suggestions_are_available_and_valid(self):
        self.manager.add("alex")
        suggestions = self.manager.check("ALEX")["suggestions"]
        self.assertTrue(suggestions)
        self.assertTrue(all(self.manager.check(name)["available"] for name in suggestions))

    def test_delete_uses_normalized_username(self):
        self.manager.add("DeleteMe")
        self.assertTrue(self.manager.delete("DELETEME")["deleted"])
        self.assertTrue(self.manager.check("deleteme")["available"])

    def test_reset_clears_table(self):
        self.manager.add("known")
        self.manager.reset()
        self.assertEqual(self.manager.statistics()["total_usernames"], 0)

    def test_sample_data_contains_at_least_one_hundred_names(self):
        count = self.manager.load_sample_data()
        self.assertGreaterEqual(count, 100)
        self.assertFalse(self.manager.check("admin")["available"])


if __name__ == "__main__":
    unittest.main()