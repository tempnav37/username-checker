"""Business rules that connect usernames to the custom hash table."""

import csv
from pathlib import Path
from typing import Optional

from src.hash_table import HashTable
from src.validators import DEFAULT_MAX_LENGTH, normalize_username


class UsernameManager:
    """Validate and manage usernames using a custom HashTable."""

    def __init__(self, table_size: int = 151, max_length: int = DEFAULT_MAX_LENGTH) -> None:
        self.hash_table = HashTable(table_size)
        self.max_length = max_length

    def _normalize(self, username: str) -> str:
        return normalize_username(username, self.max_length)

    def check(self, username: str) -> dict:
        """Search for a username and return the hashing trace and suggestions."""
        normalized = self._normalize(username)
        location = self.hash_table.locate(normalized)
        found = self.hash_table.search(normalized)
        return {
            "success": True,
            "username": normalized,
            "available": not found,
            "found": found,
            "hash_value": location.hash_value,
            "bucket_index": location.bucket_index,
            "bucket_contents": self.hash_table.bucket_contents(location.bucket_index),
            "suggestions": self._suggestions(normalized) if found else [],
        }

    def add(self, username: str) -> dict:
        """Register a username if its normalized form is available."""
        result = self.check(username)
        if not result["available"]:
            return {**result, "added": False, "message": "Username is already taken."}
        self.hash_table.insert(result["username"])
        result["bucket_contents"] = self.hash_table.bucket_contents(result["bucket_index"])
        return {**result, "added": True, "message": "Username successfully registered."}

    def delete(self, username: str) -> dict:
        """Delete a registered username using its normalized form."""
        normalized = self._normalize(username)
        location = self.hash_table.locate(normalized)
        deleted = self.hash_table.delete(normalized)
        return {
            "success": True,
            "deleted": deleted,
            "username": normalized,
            "hash_value": location.hash_value,
            "bucket_index": location.bucket_index,
            "bucket_contents": self.hash_table.bucket_contents(location.bucket_index),
            "message": "Username deleted." if deleted else "Username was not found.",
        }

    def _suggestions(self, username: str, limit: int = 5) -> list:
        """Build available alternatives from a small set of username patterns."""
        candidates = (
            f"{username}4",
            f"{username}_1",
            f"{username}_dev",
            f"{username}2026",
            f"the_{username}",
            f"{username}_app",
            f"{username}7",
        )
        suggestions = []
        for candidate in candidates:
            try:
                normalized = self._normalize(candidate)
            except ValueError:
                continue
            if not self.hash_table.search(normalized) and normalized not in suggestions:
                suggestions.append(normalized)
            if len(suggestions) == limit:
                break
        return suggestions

    def load_sample_data(self, path: Optional[Path] = None) -> int:
        """Replace current contents with usernames from the sample CSV."""
        sample_path = path or Path(__file__).resolve().parent.parent / "data" / "usernames.csv"
        self.hash_table = HashTable(self.hash_table.get_statistics()["table_size"])
        with sample_path.open(newline="", encoding="utf-8") as sample_file:
            reader = csv.DictReader(sample_file)
            for row in reader:
                self.hash_table.insert(self._normalize(row["username"]))
        return len(self.hash_table)

    def reset(self) -> None:
        """Clear all usernames while retaining the table size."""
        table_size = self.hash_table.get_statistics()["table_size"]
        self.hash_table = HashTable(table_size)

    def statistics(self) -> dict:
        return self.hash_table.get_statistics()