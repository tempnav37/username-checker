# Username Availability Checker

An educational Flask application that demonstrates how a custom hash table can quickly check whether a username is available. The lookup data is stored in a hand-built table using separate chaining, not in Python's built-in set or dictionary.

## Problem Statement

Username registration needs to identify existing names quickly. A linear list scan can take $O(n)$ time. This project uses a deterministic hash function to locate one bucket and searches only that bucket's chain.

## Objectives

- Implement and test a custom hash table with insert, search, and delete operations.
- Demonstrate deterministic hashing, bucket indexing, and collision handling.
- Show the lookup trace, live table statistics, and occupied bucket chains.
- Validate usernames consistently and provide available alternatives for taken names.

## Features

- Case-insensitive username lookup; input is normalized to lowercase.
- Username rules: 1-24 ASCII letters, numbers, or underscores. Spaces and other symbols are rejected.
- Check, register, and delete usernames without reloading the page.
- Dynamically generated suggestions, checked against the hash table.
- More than 100 unique sample usernames, loaded on startup or with **Load sample**.
- Live total, table size, occupied bucket, collision, and load-factor statistics.
- Bucket explorer with a collision-only filter.
- Reset control and JSON API.

## Technologies and Data Structures

- Python 3 and Flask
- HTML5, CSS3, and vanilla JavaScript
- A custom fixed-size array of bucket lists (separate chaining)
- A CSV file for the sample usernames

## Hashing Explanation

For each character, the hash value is updated as `value = value * 31 + ord(character)`. This polynomial calculation is deterministic, unlike Python's randomized built-in `hash()`. The bucket index is `hash_value % table_size`; modulo maps the integer hash into the valid index range from zero to `table_size - 1`.

When distinct usernames map to one bucket, separate chaining stores both in that bucket's list. Search and deletion calculate the same bucket and inspect its chain. The collision count is the number of entries beyond the first in all non-empty chains. The load factor is `stored usernames / table size`.

## Architecture

- `app.py`: Flask routes, JSON responses, and application factory.
- `src/hash_table.py`: independent deterministic hash table implementation.
- `src/validators.py`: username validation and normalization.
- `src/username_manager.py`: application rules and hash table operations.
- `data/usernames.csv`: sample usernames.
- `templates/index.html`: dashboard structure.
- `static/css/style.css`: responsive presentation.
- `static/js/app.js`: asynchronous API calls and dashboard updates.
- `tests/`: unit tests for the table, validator, manager, and API.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── PROJECT_REQUIREMENTS.md
├── README.md
├── data/
│   └── usernames.csv
├── src/
│   ├── hash_table.py
│   ├── username_manager.py
│   └── validators.py
├── static/
│   ├── css/style.css
│   └── js/app.js
├── templates/index.html
└── tests/
    ├── test_api.py
    ├── test_hash_table.py
    ├── test_username_manager.py
    └── test_validators.py
```

## Installation

Python 3.9 or newer is recommended.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open `http://127.0.0.1:5000`. The sample dataset is loaded when the app starts. The Flask development server is for local educational use, not production deployment.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/stats` | Current table statistics |
| `POST` | `/api/check` | Check a username and return hash trace/suggestions |
| `POST` | `/api/add` | Register an available username |
| `DELETE` | `/api/delete` | Remove a username |
| `POST` | `/api/sample` | Reload sample data |
| `POST` | `/api/reset` | Clear the table |
| `GET` | `/api/buckets` | List occupied buckets |
| `GET` | `/api/bucket/<index>` | Read a single bucket |

POST and DELETE requests use JSON such as `{"username": "nav123"}`. Invalid usernames return HTTP 400 with a JSON error.

## Testing

Run the independent data structure, manager, validator, and API tests:

```powershell
python -m unittest discover -s tests -v
```

## Complexity Analysis

- Average search: $O(1)$, assuming a well-distributed hash and a reasonable load factor.
- Average insertion: $O(1)$, including the expected constant-time bucket lookup.
- Average deletion: $O(1)$ under the same assumptions.
- Worst-case search, insertion, or deletion: $O(n)$ when all keys occupy one chain.
- Statistics and occupied-bucket listing: $O(m + n)$, where $m$ is the table size and $n$ the number of stored usernames.

Actual performance depends on the hash distribution, chain lengths, and load factor. The table uses 151 fixed buckets so these values and collisions remain visible for demonstration.

## Screenshots

_Add screenshots of the checker, lookup trace, and collision explorer here._

## Future Scope

- Allow table size selection and compare hash distributions.
- Add dynamic resizing and rehashing as a separate lesson.
- Persist registrations between application restarts.
- Add additional visualizations for chain length and lookup comparisons.

## Academic Notes

Hashing maps a key to an index through a hash function. A collision occurs when different keys map to the same bucket. Separate chaining keeps these keys together without overwriting them. A normal list needs a linear scan; a hash table offers average constant-time lookup when the hash function distributes keys well. The dashboard visualizes each of these steps for a viva demonstration.

No passwords, authentication tokens, or sensitive personal information are requested or stored.