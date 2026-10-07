"""Username validation and normalization rules."""

import re


USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
DEFAULT_MAX_LENGTH = 24


def normalize_username(username: str, max_length: int = DEFAULT_MAX_LENGTH) -> str:
    """Validate a username and return its case-insensitive canonical form."""
    if not isinstance(username, str) or not username:
        raise ValueError("Enter a username to continue.")
    if len(username) > max_length:
        raise ValueError(f"Username must be {max_length} characters or fewer.")
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError("Use letters, numbers, and underscores only, with no spaces.")
    return username.casefold()