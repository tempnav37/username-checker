import unittest

from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "LOAD_SAMPLE_DATA": False})
        self.client = self.app.test_client()

    def test_checker_registers_and_deletes_username(self):
        available = self.client.post("/api/check", json={"username": "new_user"})
        self.assertTrue(available.get_json()["available"])
        registered = self.client.post("/api/add", json={"username": "new_user"})
        self.assertTrue(registered.get_json()["added"])
        taken = self.client.post("/api/check", json={"username": "NEW_USER"})
        self.assertFalse(taken.get_json()["available"])
        deleted = self.client.delete("/api/delete", json={"username": "NEW_USER"})
        self.assertTrue(deleted.get_json()["deleted"])

    def test_invalid_username_returns_json_error(self):
        response = self.client.post("/api/check", json={"username": "bad name"})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["success"])

    def test_statistics_buckets_sample_and_reset(self):
        sample = self.client.post("/api/sample").get_json()
        self.assertGreaterEqual(sample["loaded"], 100)
        self.assertEqual(self.client.get("/api/stats").get_json()["total_usernames"], sample["loaded"])
        self.assertTrue(self.client.get("/api/buckets").get_json()["buckets"])
        self.assertEqual(self.client.post("/api/reset").get_json()["stats"]["total_usernames"], 0)

    def test_bucket_bounds_return_not_found(self):
        response = self.client.get("/api/bucket/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()