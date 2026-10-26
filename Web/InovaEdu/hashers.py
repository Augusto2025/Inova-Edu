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
        import logging
        logger = logging.getLogger('InovaEdu.hashers')

        if not password or not encoded:
            logger.debug(f"[HASHER] Empty password or encoded: password={bool(password)}, encoded={bool(encoded)}")
            return False

        if not encoded.startswith(self.algorithm):
            logger.debug(f"[HASHER] Algorithm mismatch: expected {self.algorithm}, got {encoded[:20]}...")
            return False

        try:
            # Parse: algorithm$iterations$salt$hash
            parts = encoded.split('$', 3)
            if len(parts) != 4:
                logger.debug(f"[HASHER] Invalid hash format (parts != 4): {parts}")
                return False

            _, iterations_str, salt_b64, hash_b64 = parts
            iterations = int(iterations_str)

            # Decode expected hash (base64)
            expected_hash = self._decode_base64(hash_b64)

            password_bytes = force_bytes(password)

            logger.debug(f"[HASHER] Verifying: iterations={iterations}, salt_b64={salt_b64}, hash_len={len(expected_hash)}")

            # METHOD 1: Django format - base64 salt STRING as UTF-8 bytes
            salt_django = force_bytes(salt_b64)
            computed = hashlib.pbkdf2_hmac(
                'sha256',
                password_bytes,
                salt_django,
                iterations,
                dklen=len(expected_hash)
            )
            match1 = hmac.compare_digest(computed, expected_hash)
            logger.debug(f"[HASHER] Method 1 (Django format): match={match1}, salt_bytes_len={len(salt_django)}")
            if match1:
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
                match2 = hmac.compare_digest(computed_legacy, expected_hash)
                logger.debug(f"[HASHER] Method 2 (Legacy format): match={match2}, salt_legacy_len={len(salt_legacy)}")
                if match2:
                    return True
            except (binascii.Error, ValueError) as e:
                logger.debug(f"[HASHER] Legacy decode error: {e}")

            logger.debug(f"[HASHER] Both methods failed for hash: {encoded[:50]}...")
            return False

        except (ValueError, IndexError, TypeError) as e:
            logger.debug(f"[HASHER] Parse error: {e}")
            return False

    def _decode_base64(self, data):
        """Decode base64 with automatic padding."""
        padding = '=' * (-len(data) % 4)
        return base64.b64decode(data + padding)

    def encode(self, password, salt, iterations=None):
        """
        Encode password using Django standard format.
        The salt parameter can be either:
        - Raw bytes (when creating new hash)
        - Base64 string (when called from verify() for comparison)
        """
        import logging
        logger = logging.getLogger('InovaEdu.hashers')

        iterations = iterations or self.iterations

        # Check if salt is already a base64 string (from verify())
        # Django's verify() passes the base64 salt string from the hash
        if isinstance(salt, str):
            # Try to decode as base64 to see if it's already base64
            try:
                # If it decodes to 12 or 16 bytes, it's likely a base64 salt
                decoded = base64.b64decode(salt + '=' * (-len(salt) % 4))
                if len(decoded) in (12, 16):
                    # It's already a base64 salt string - use as-is
                    salt_for_pbkdf2 = force_bytes(salt)
                    salt_b64 = salt
                    logger.debug(f"[HASHER] encode: salt is base64 string (len={len(salt)}), using as-is")
                else:
                    # It's a regular string - encode to bytes
                    salt_for_pbkdf2 = force_bytes(salt)
                    salt_b64 = base64.b64encode(salt_for_pbkdf2).decode('ascii').rstrip('=')
                    logger.debug(f"[HASHER] encode: salt is regular string, encoded to base64")
            except (binascii.Error, ValueError):
                # Not valid base64 - treat as string
                salt_for_pbkdf2 = force_bytes(salt)
                salt_b64 = base64.b64encode(salt_for_pbkdf2).decode('ascii').rstrip('=')
                logger.debug(f"[HASHER] encode: salt not valid base64, treated as string")
        else:
            # It's bytes - base64 encode for storage
            salt_for_pbkdf2 = salt
            salt_b64 = base64.b64encode(salt).decode('ascii').rstrip('=')
            logger.debug(f"[HASHER] encode: salt is bytes (len={len(salt)}), base64 encoded")

        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            force_bytes(password),
            salt_for_pbkdf2,
            iterations,
            dklen=32
        )
        hash_b64 = base64.b64encode(hash_bytes).decode('ascii').rstrip('=')
        result = f"{self.algorithm}${iterations}${salt_b64}${hash_b64}"
        logger.debug(f"[HASHER] encode result: {result[:60]}...")
        return result

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