"""
Custom Django Password Hashers
Supports BOTH Django format (base64 salt string as UTF-8 bytes)
AND legacy format (decoded salt bytes) for backward compatibility
"""
import base64
import hashlib
import hmac
import binascii

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.encoding import force_bytes, force_str


class DualFormatPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    PBKDF2-SHA256 hasher that verifies BOTH formats:
    1. Django format: base64 salt string used as UTF-8 bytes for PBKDF2 (standard Django 6.0+)
    2. Legacy format: decoded salt bytes used for PBKDF2 (old hashes in database)

    This matches Desktop/security/crypto.py verify_password() behavior exactly.
    """

    algorithm = "pbkdf2_sha256"
    iterations = 1_200_000  # Django 6.0 default

    def verify(self, password, encoded, preferred=None):
        """
        Verify a password against a hash, trying both formats.

        Args:
            password: Plain text password
            encoded: Stored hash string
            preferred: Not used, kept for compatibility

        Returns:
            bool: True if password matches
        """
        if not password or not encoded:
            return False

        if not encoded.startswith(self.algorithm):
            return False

        try:
            # Parse: algorithm$iterations$salt$hash
            parts = encoded.split('$', 3)
            if len(parts) != 4:
                return False

            _, iterations_str, salt_b64, hash_b64 = parts
            iterations = int(iterations_str)

            # Decode expected hash (base64)
            expected_hash = self._decode_base64(hash_b64)

            password_bytes = force_bytes(password)

            # METHOD 1: Django format - base64 salt STRING as UTF-8 bytes
            salt_django = force_bytes(salt_b64)
            computed = hashlib.pbkdf2_hmac(
                'sha256',
                password_bytes,
                salt_django,
                iterations,
                dklen=len(expected_hash)
            )
            if hmac.compare_digest(computed, expected_hash):
                return True

            # METHOD 2: Legacy format - DECODED salt bytes
            try:
                salt_legacy = self._decode_base64(salt_b64)
                computed_legacy = hashlib.pbkdf2_hmac(
                    'sha256',
                    password_bytes,
                    salt_legacy,
                    iterations,
                    dklen=len(expected_hash)
                )
                if hmac.compare_digest(computed_legacy, expected_hash):
                    return True
            except (binascii.Error, ValueError):
                pass

            return False

        except (ValueError, IndexError, TypeError):
            return False

    def _decode_base64(self, data):
        """Decode base64 with automatic padding."""
        padding = '=' * (-len(data) % 4)
        return base64.b64decode(data + padding)

    def encode(self, password, salt, iterations=None):
        """
        Encode password using Django standard format (base64 salt string as UTF-8 bytes).
        This ensures NEW hashes are created in Django format.
        """
        iterations = iterations or self.iterations
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            force_bytes(password),
            force_bytes(salt),  # Django uses base64 salt STRING as UTF-8 bytes
            iterations,
            dklen=32
        )
        salt_b64 = base64.b64encode(force_bytes(salt)).decode('ascii').rstrip('=')
        hash_b64 = base64.b64encode(hash_bytes).decode('ascii').rstrip('=')
        return f"{self.algorithm}${iterations}${salt_b64}${hash_b64}"

    def safe_summary(self, encoded):
        """Return a safe summary of the hash for logging."""
        return super().safe_summary(encoded)


class LegacyOnlyPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    Fallback hasher for legacy format ONLY (decoded salt bytes).
    Use this if you ONLY want to support old hashes without Django format.
    """

    algorithm = "pbkdf2_sha256_legacy"
    iterations = 600_000

    def verify(self, password, encoded, preferred=None):
        if not password or not encoded:
            return False

        if not encoded.startswith("pbkdf2_sha256$"):
            return False

        try:
            parts = encoded.split('$', 3)
            if len(parts) != 4:
                return False

            _, iterations_str, salt_b64, hash_b64 = parts
            iterations = int(iterations_str)

            # Decode hash
            expected_hash = self._decode_base64(hash_b64)
            password_bytes = force_bytes(password)

            # ONLY legacy method: decoded salt bytes
            salt_legacy = self._decode_base64(salt_b64)
            computed = hashlib.pbkdf2_hmac(
                'sha256',
                password_bytes,
                salt_legacy,
                iterations,
                dklen=len(expected_hash)
            )
            return hmac.compare_digest(computed, expected_hash)

        except (ValueError, IndexError, TypeError, binascii.Error):
            return False

    def _decode_base64(self, data):
        padding = '=' * (-len(data) % 4)
        return base64.b64decode(data + padding)

    def encode(self, password, salt, iterations=None):
        # Always encode in standard Django format (not legacy)
        return DualFormatPBKDF2PasswordHasher().encode(password, salt, iterations)