"""A small educational hash table using separate chaining."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EntryLocation:
    """Hash details for a key, whether or not it is stored."""

    hash_value: int
    bucket_index: int


class HashTable:
    """Store strings in buckets with a deterministic polynomial hash."""

    def __init__(self, size: int = 151) -> None:
        if size <= 0:
            raise ValueError("Table size must be greater than zero.")
        self._buckets: List[List[str]] = [[] for _ in range(size)]
        self._size = size
        self._count = 0

    def hash_value(self, username: str) -> int:
        """Calculate a stable polynomial hash for a username."""
        value = 0
        for character in username:
            value = value * 31 + ord(character)
        return value

    def locate(self, username: str) -> EntryLocation:
        """Return the deterministic hash and corresponding bucket index."""
        value = self.hash_value(username)
        return EntryLocation(value, value % self._size)

    def insert(self, username: str) -> bool:
        """Insert a username, returning false if it is already present."""
        index = self.locate(username).bucket_index
        bucket = self._buckets[index]
        if username in bucket:
            return False
        bucket.append(username)
        self._count += 1
        return True

    def search(self, username: str) -> bool:
        """Return whether a username exists in its bucket chain."""
        index = self.locate(username).bucket_index
        return username in self._buckets[index]

    def delete(self, username: str) -> bool:
        """Remove a username, returning false when it is not stored."""
        index = self.locate(username).bucket_index
        bucket = self._buckets[index]
        try:
            bucket.remove(username)
        except ValueError:
            return False
        self._count -= 1
        return True

    def bucket_contents(self, index: int) -> List[str]:
        """Return a copy of the contents of a bucket."""
        if not 0 <= index < self._size:
            raise IndexError("Bucket index is outside the table.")
        return list(self._buckets[index])

    def occupied_buckets(self) -> List[dict]:
        """Return non-empty buckets and their entries for visualization."""
        return [
            {"index": index, "usernames": list(bucket)}
            for index, bucket in enumerate(self._buckets)
            if bucket
        ]

    def get_statistics(self) -> dict:
        """Calculate current table statistics from the bucket chains."""
        occupied = sum(bool(bucket) for bucket in self._buckets)
        collisions = sum(max(0, len(bucket) - 1) for bucket in self._buckets)
        maximum_bucket_size = max((len(bucket) for bucket in self._buckets), default=0)
        return {
            "total_usernames": self._count,
            "table_size": self._size,
            "occupied_buckets": occupied,
            "collisions": collisions,
            "load_factor": self._count / self._size,
            "maximum_bucket_size": maximum_bucket_size,
        }

    def __len__(self) -> int:
        return self._count