import unittest

from src.hash_table import HashTable


class HashTableTests(unittest.TestCase):
    def test_insert_search_and_missing_key(self):
        table = HashTable(7)
        self.assertTrue(table.insert("nav123"))
        self.assertTrue(table.search("nav123"))
        self.assertFalse(table.search("missing"))

    def test_duplicate_insert_does_not_duplicate_entry(self):
        table = HashTable(7)
        self.assertTrue(table.insert("same"))
        self.assertFalse(table.insert("same"))
        self.assertEqual(len(table), 1)

    def test_collision_chaining_and_deletion(self):
        table = HashTable(3)
        colliding = ["a", "d"]
        self.assertEqual(table.locate(colliding[0]).bucket_index, table.locate(colliding[1]).bucket_index)
        for username in colliding:
            self.assertTrue(table.insert(username))
        self.assertTrue(all(table.search(username) for username in colliding))
        self.assertTrue(table.delete("a"))
        self.assertFalse(table.search("a"))
        self.assertTrue(table.search("d"))

    def test_delete_and_empty_table(self):
        table = HashTable()
        self.assertFalse(table.search("any"))
        self.assertTrue(table.insert("any"))
        self.assertTrue(table.delete("any"))
        self.assertFalse(table.delete("any"))
        self.assertEqual(len(table), 0)

    def test_statistics_are_calculated_from_chains(self):
        table = HashTable(3)
        table.insert("a")
        table.insert("d")
        table.insert("b")
        stats = table.get_statistics()
        self.assertEqual(stats["total_usernames"], 3)
        self.assertEqual(stats["table_size"], 3)
        self.assertEqual(stats["occupied_buckets"], 2)
        self.assertEqual(stats["collisions"], 1)
        self.assertEqual(stats["load_factor"], 1.0)
        self.assertEqual(stats["maximum_bucket_size"], 2)

    def test_stable_hash_and_bucket_bounds(self):
        table = HashTable(17)
        self.assertEqual(table.hash_value("nav123"), table.hash_value("nav123"))
        self.assertGreaterEqual(table.locate("nav123").bucket_index, 0)
        self.assertLess(table.locate("nav123").bucket_index, 17)


if __name__ == "__main__":
    unittest.main()