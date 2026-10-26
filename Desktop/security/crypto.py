"""
Security Module: Cryptographic Utilities
PBKDF2-SHA256 password hashing (compatible with Django 6.0 default)
"""
import hashlib
import secrets
import hmac
import base64
from typing import Tuple

# Django 6.0 default: 1,200,000 iterations of PBKDF2-SHA256
PBKDF2_ITERATIONS = 1_200_000
HASH_ALGORITHM = 'sha256'
SALT_LENGTH = 16

# Format: pbkdf2_sha256$iterations$salt$hash
HASH_PREFIX = 'pbkdf2_sha256$'


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-SHA256 with 1,200,000 iterations (Django 6.0 default).
    Returns a Django-compatible hash string: pbkdf2_sha256$iterations$salt$hash
    Uses base64 encoding for salt and hash (Django standard).

    IMPORTANT: The salt is stored as base64 string. During verification, Django uses
    the base64 salt string's UTF-8 bytes as the salt for PBKDF2 (not the decoded bytes).
    This matches Django's PBKDF2PasswordHasher exactly.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Generate random salt (16 bytes)
    salt = secrets.token_bytes(SALT_LENGTH)

    # Derive key using PBKDF2 - Django uses the BASE64 SALT STRING as the salt for PBKDF2!
    salt_b64 = base64.b64encode(salt).decode('ascii').rstrip('=')

    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode('utf-8'),
        salt_b64.encode('utf-8'),  # Django uses base64 salt string as UTF-8 bytes
        PBKDF2_ITERATIONS
    )

    # Encode hash as base64 (Django standard)
    hash_b64 = base64.b64encode(hash_bytes).decode('ascii').rstrip('=')

    # Return Django-compatible format
    return f"{HASH_PREFIX}{PBKDF2_ITERATIONS}${salt_b64}${hash_b64}"


def _decode_hash_part(part: str) -> bytes:
    """
    Decode a hash part (hash) that could be hex or base64.
    Salt is NOT decoded - it's used as base64 string (Django compatibility).
    """
    # Try base64 first (Django format)
    try:
        # Add padding if needed
        padding = '=' * (-len(part) % 4)
        return base64.b64decode(part + padding)
    except Exception:
        pass

    # Fallback: try hex
    try:
        return bytes.fromhex(part)
    except Exception:
        pass

    # If both fail, raise
    raise ValueError(f"Unable to decode hash part: {part}")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a stored hash.
    Fully compatible with Django 6.0 PBKDF2PasswordHasher.

    Django's PBKDF2PasswordHasher uses the BASE64 SALT STRING (UTF-8 bytes)
    as the salt for PBKDF2, not the decoded bytes.
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

        _, iterations_str, salt_b64, hash_b64 = parts
        iterations = int(iterations_str)

        # CRITICAL: Django uses the BASE64 SALT STRING (UTF-8 bytes) as the salt for PBKDF2!
        # NOT the decoded bytes. This matches Django's PBKDF2PasswordHasher exactly.
        salt = salt_b64.encode('utf-8')

        # Decode expected hash (base64)
        expected_hash = _decode_hash_part(hash_b64)

        # Compute hash with provided password using base64 salt string as salt
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
    print("[OK] Correct password verifies")

    # Verify incorrect
    assert not verify_password("WrongPassword", hashed), "Wrong password should fail"
    print("[OK] Wrong password rejected")

    # Test empty password
    try:
        hash_password("")
        assert False, "Should raise ValueError"
    except ValueError:
        print("[OK] Empty password rejected")

    # Test rehash detection
    old_hash = "pbkdf2_sha256$100000$salt$hash"
    assert hash_needs_rehash(old_hash), "Old iterations should need rehash"
    print("[OK] Rehash detection works")

    # Test constant time compare
    assert constant_time_compare("test", "test"), "Equal strings should match"
    assert not constant_time_compare("test", "wrong"), "Different strings should not match"
    print("[OK] Constant time compare works")

    # Test with Django-format hash (1.2M iterations, base64 salt string as salt)
    print("\n--- Testing Django format compatibility ---")
    django_hash = "pbkdf2_sha256$1200000$YBTbJb6ew0tY4tn0dU4u9R$JpTdFeQa7b9ykQgW+w2cqpG7kwzbTfIx/TC9aFJ3RYs="
    assert verify_password("1234", django_hash), "Django hash should verify"
    print("[OK] Django-format hash (1234) verifies")

    # Test our own hash
    our_hash = hash_password("1234")
    assert verify_password("1234", our_hash), "Our hash should verify"
    print("[OK] Our hash (1234) verifies")

    print("\n[OK] All crypto tests passed!")