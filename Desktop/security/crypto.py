"""
Security Module: Cryptographic Utilities
PBKDF2-SHA256 password hashing (compatible with Django 6.0 default)
"""
import hashlib
import secrets
import hmac
from typing import Tuple

# Django 6.0 default: 600,000 iterations of PBKDF2-SHA256
PBKDF2_ITERATIONS = 600000
HASH_ALGORITHM = 'sha256'
SALT_LENGTH = 16

# Format: pbkdf2_sha256$iterations$salt$hash
HASH_PREFIX = 'pbkdf2_sha256$'


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-SHA256 with 600,000 iterations.
    Returns a Django-compatible hash string: pbkdf2_sha256$iterations$salt$hash
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Generate random salt
    salt = secrets.token_bytes(SALT_LENGTH)

    # Derive key using PBKDF2
    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode('utf-8'),
        salt,
        PBKDF2_ITERATIONS
    )

    # Encode salt and hash as hex strings
    salt_hex = salt.hex()
    hash_hex = hash_bytes.hex()

    # Return Django-compatible format
    return f"{HASH_PREFIX}{PBKDF2_ITERATIONS}${salt_hex}${hash_hex}"


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a stored hash.
    Supports Django-compatible format: pbkdf2_sha256$iterations$salt$hash
    """
    if not password or not hashed:
        return False

    try:
        # Parse the hash string
        if not hashed.startswith(HASH_PREFIX):
            # Legacy format or unsupported - reject
            return False

        parts = hashed.split('$')
        if len(parts) != 4:
            return False

        _, iterations_str, salt_hex, hash_hex = parts
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        # Compute hash with provided password
        computed_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            password.encode('utf-8'),
            salt,
            iterations
        )

        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(computed_hash, expected_hash)

    except (ValueError, IndexError, TypeError):
        return False


def hash_needs_rehash(hashed: str) -> bool:
    """
    Check if a hash needs to be upgraded (e.g., old iteration count).
    """
    try:
        if not hashed.startswith(HASH_PREFIX):
            return True

        parts = hashed.split('$')
        if len(parts) != 4:
            return True

        iterations = int(parts[1])
        return iterations < PBKDF2_ITERATIONS
    except Exception:
        return True


def constant_time_compare(val1: str, val2: str) -> bool:
    """
    Constant-time string comparison to prevent timing attacks.
    """
    return hmac.compare_digest(val1.encode('utf-8'), val2.encode('utf-8'))


# --- Testing ---
if __name__ == "__main__":
    # Test basic functionality
    pwd = "MinhaSenh@123"

    # Hash
    hashed = hash_password(pwd)
    print(f"Hash: {hashed}")

    # Verify correct
    assert verify_password(pwd, hashed), "Correct password should verify"
    print("✅ Correct password verifies")

    # Verify incorrect
    assert not verify_password("WrongPassword", hashed), "Wrong password should fail"
    print("✅ Wrong password rejected")

    # Test empty password
    try:
        hash_password("")
        assert False, "Should raise ValueError"
    except ValueError:
        print("✅ Empty password rejected")

    # Test rehash detection
    old_hash = "pbkdf2_sha256$100000$salt$hash"
    assert hash_needs_rehash(old_hash), "Old iterations should need rehash"
    print("✅ Rehash detection works")

    # Test constant time compare
    assert constant_time_compare("test", "test"), "Equal strings should match"
    assert not constant_time_compare("test", "wrong"), "Different strings should not match"
    print("✅ Constant time compare works")

    print("\n✅ All crypto tests passed!")