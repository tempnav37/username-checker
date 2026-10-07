# Username Availability Checker Requirements

## Purpose

Demonstrate username availability checking with an independently implemented hash table. The hash table, rather than a built-in set or dictionary, is the primary lookup store.

## Behavior

- Accept usernames of 1 to 24 ASCII letters, digits, or underscores.
- Normalize usernames to lowercase before lookup, registration, and deletion.
- Support check, add, delete, sample loading, reset, statistics, and bucket inspection.
- Return dynamically generated alternatives only when they are valid and absent from the hash table.
- Include at least 100 unique sample usernames.

## Data Structure

- Use a deterministic polynomial string hash and modulo table size for the bucket index.
- Resolve collisions with separate chaining.
- Calculate size, count, occupied buckets, collisions, load factor, and maximum chain length from current table contents.
- Keep Flask concerns outside the hash table implementation.

## Interface and Quality

- Use Python, Flask, HTML, CSS, and vanilla JavaScript.
- Expose JSON endpoints and provide a responsive browser interface without page reloads for normal operations.
- Test the hash table independently from the manager and API.
- Document installation, operation, architecture, hashing, collision handling, and complexity.
- This educational project does not implement authentication or store sensitive information.