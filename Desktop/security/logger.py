"""
Security Module: Secure Logging
Logging configuration that prevents sensitive data exposure.
"""
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

# Sensitive field names that should never be logged
SENSITIVE_FIELDS = {
    'password', 'senha', 'passwd', 'pwd', 'secret', 'token',
    'api_key', 'apikey', 'api_secret', 'apisecret', 'access_token',
    'refresh_token', 'authorization', 'auth', 'credential',
    'private_key', 'privatekey', 'ssl_key', 'sslkey'
}

# Sensitive patterns in messages
SENSITIVE_PATTERNS = [
    r'password\s*[=:]\s*\S+',
    r'senha\s*[=:]\s*\S+',
    r'token\s*[=:]\s*\S+',
    r'api[_-]?key\s*[=:]\s*\S+',
    r'api[_-]?secret\s*[=:]\s*\S+',
    r'Bearer\s+\S+',
    r'Authorization:\s*\S+',
]


class SensitiveDataFilter(logging.Filter):
    """
    Filter that removes sensitive data from log records.
    """

    def __init__(self):
        super().__init__()
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in SENSITIVE_PATTERNS]

    def filter(self, record: logging.LogRecord) -> bool:
        # Filter message
        if isinstance(record.msg, str):
            record.msg = self._sanitize_message(record.msg)

        # Filter args
        if record.args:
            record.args = self._sanitize_args(record.args)

        return True

    def _sanitize_message(self, msg: str) -> str:
        """Sanitize log message."""
        for pattern in self._compiled_patterns:
            msg = pattern.sub('[REDACTED]', msg)
        return msg

    def _sanitize_args(self, args: tuple) -> tuple:
        """Sanitize log arguments."""
        sanitized = []
        for arg in args:
            if isinstance(arg, dict):
                sanitized.append(self._sanitize_dict(arg))
            elif isinstance(arg, str):
                sanitized.append(self._sanitize_message(arg))
            else:
                sanitized.append(arg)
        return tuple(sanitized)

    def _sanitize_dict(self, data: dict) -> dict:
        """Sanitize dictionary by redacting sensitive keys."""
        result = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
                result[key] = '[REDACTED]'
            elif isinstance(value, dict):
                result[key] = self._sanitize_dict(value)
            elif isinstance(value, str):
                result[key] = self._sanitize_message(value)
            else:
                result[key] = value
        return result


class SecureLogger:
    """
    Wrapper for secure logging with automatic sensitive data filtering.
    """

    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()

        # Add sensitive data filter
        self.logger.addFilter(SensitiveDataFilter())

    def _setup_handlers(self):
        """Setup console and file handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (if logs directory exists)
        log_dir = Path('logs')
        if log_dir.exists() or not log_dir.exists():
            try:
                log_dir.mkdir(exist_ok=True)
                file_handler = RotatingFileHandler(
                    log_dir / 'security.log',
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.WARNING)
                file_formatter = logging.Formatter(
                    '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
            except Exception:
                # Fallback to console only if file logging fails
                pass

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def log_security_event(self, event_type: str, details: Dict[str, Any], level: int = logging.WARNING):
        """
        Log a security-relevant event with structured data.
        """
        safe_details = {k: v for k, v in details.items()
                       if not any(s in k.lower() for s in SENSITIVE_FIELDS)}
        self.logger.log(level, f"SECURITY_EVENT: {event_type} | {safe_details}")


# Convenience function to get logger
def get_logger(name: str) -> SecureLogger:
    """Get a secure logger instance."""
    return SecureLogger(name)


# Module-level logger for security events
security_logger = SecureLogger('security')


# --- Testing ---
if __name__ == "__main__":
    import re
    from pathlib import Path

    logger = get_logger('test')

    # Test normal logging
    logger.info("User login successful")
    logger.warning("Failed login attempt")

    # Test sensitive data filtering
    logger.info("User login with password=secret123")
    logger.info("API call with api_key=abc123")

    # Test dict sanitization
    logger.info("User data", extra={'user_data': {'email': 'test@test.com', 'password': 'secret'}})

    print("✅ Logger tests completed - check output for [REDACTED]")