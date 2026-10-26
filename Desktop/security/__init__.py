"""
Security Package for Inova Edu Desktop
Provides cryptographic, rate limiting, validation, and logging utilities.
"""
from .crypto import (
    hash_password,
    verify_password,
    hash_needs_rehash,
    constant_time_compare,
    PBKDF2_ITERATIONS,
)

from .rate_limiter import (
    RateLimiter,
    login_limiter,
)

from .file_validator import (
    validate_image_upload,
    sanitize_filename,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    MAX_FILE_SIZE,
)

from .validators import (
    validate_password,
    validate_email_address,
    validate_name,
    validate_bio,
    sanitize_html,
    sanitize_sql_input,
    validate_cpf,
    MIN_PASSWORD_LENGTH,
)

from .logger import (
    SecureLogger,
    get_logger,
    security_logger,
    SensitiveDataFilter,
)

__all__ = [
    # Crypto
    'hash_password',
    'verify_password',
    'hash_needs_rehash',
    'constant_time_compare',
    'PBKDF2_ITERATIONS',

    # Rate Limiter
    'RateLimiter',
    'login_limiter',

    # File Validator
    'validate_image_upload',
    'sanitize_filename',
    'ALLOWED_IMAGE_EXTENSIONS',
    'ALLOWED_MIME_TYPES',
    'MAX_FILE_SIZE',

    # Validators
    'validate_password',
    'validate_email_address',
    'validate_name',
    'validate_bio',
    'sanitize_html',
    'sanitize_sql_input',
    'validate_cpf',
    'MIN_PASSWORD_LENGTH',

    # Logger
    'SecureLogger',
    'get_logger',
    'security_logger',
    'SensitiveDataFilter',
]