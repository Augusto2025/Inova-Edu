"""
Security Module: Input Validation
Validators for user input sanitization and validation.
"""
import re
import html
from typing import Tuple, Optional

# Try to import optional dependencies
try:
    from email_validator import validate_email, EmailNotValidError
    HAS_EMAIL_VALIDATOR = True
except ImportError:
    HAS_EMAIL_VALIDATOR = False
    validate_email = None
    EmailNotValidError = None

try:
    import bleach
    HAS_BLEACH = True
except ImportError:
    HAS_BLEACH = False
    bleach = None

# Password policy
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL = True
SPECIAL_CHARS = r"!@#$%^&*()_+-=[]{}|;:,.<>?"

# Name validation
NAME_MAX_LENGTH = 100
# Unicode letters + spaces, hyphens, apostrophes
# Python's re doesn't support \p{L}, so we use \w and exclude digits in validate_name()
NAME_PATTERN = re.compile(r"^[\w\s'-]+$", re.UNICODE)

# Bio/description
BIO_MAX_LENGTH = 1000

# Email
EMAIL_MAX_LENGTH = 254
# Simple RFC 5322 compliant regex (fallback when email-validator not available)
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$'
)


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password against policy.

    Returns:
        (is_valid, error_message)
    """
    if not password:
        return False, "Senha é obrigatória"

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Senha deve ter pelo menos {MIN_PASSWORD_LENGTH} caracteres"

    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Senha muito longa (máx. {MAX_PASSWORD_LENGTH} caracteres)"

    if REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"

    if REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        return False, "Senha deve conter pelo menos uma letra minúscula"

    if REQUIRE_DIGIT and not re.search(r'\d', password):
        return False, "Senha deve conter pelo menos um número"

    if REQUIRE_SPECIAL and not re.search(rf'[{re.escape(SPECIAL_CHARS)}]', password):
        return False, f"Senha deve conter pelo menos um caractere especial ({SPECIAL_CHARS})"

    # Check for common weak patterns
    if re.search(r'(.)\1{3,}', password):  # 4+ repeated chars
        return False, "Senha não pode ter 4 caracteres iguais em sequência"

    if password.lower() in ['senha123', '12345678', 'password', 'admin123', 'qwerty']:
        return False, "Senha muito comum, escolha outra"

    return True, None


def validate_email_address(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format.
    Uses email-validator if available, falls back to regex.
    """
    if not email:
        return False, "E-mail é obrigatório"

    if len(email) > EMAIL_MAX_LENGTH:
        return False, f"E-mail muito longo (máx. {EMAIL_MAX_LENGTH} caracteres)"

    if HAS_EMAIL_VALIDATOR:
        try:
            # Use email-validator library for RFC-compliant validation
            valid = validate_email(email, check_deliverability=False)
            return True, None
        except EmailNotValidError as e:
            return False, f"E-mail inválido: {str(e)}"
    else:
        # Fallback: regex validation
        if EMAIL_REGEX.match(email):
            return True, None
        return False, "E-mail inválido (formato incorreto)"


def validate_name(name: str, field_name: str = "Nome") -> Tuple[bool, Optional[str]]:
    """
    Validate name (first name, last name).
    """
    if not name or not name.strip():
        return False, f"{field_name} é obrigatório"

    name = name.strip()

    if len(name) > NAME_MAX_LENGTH:
        return False, f"{field_name} muito longo (máx. {NAME_MAX_LENGTH} caracteres)"

    # Reject digits (names shouldn't contain numbers)
    if re.search(r'\d', name):
        return False, f"{field_name} não pode conter números"

    # Allow letters, spaces, hyphens, apostrophes (Unicode)
    if not NAME_PATTERN.match(name):
        return False, f"{field_name} contém caracteres inválidos. Use apenas letras, espaços, hífens e apóstrofos"

    return True, None


def validate_bio(bio: str) -> Tuple[bool, Optional[str]]:
    """
    Validate biography/description text.
    """
    if bio is None:
        return True, None

    if len(bio) > BIO_MAX_LENGTH:
        return False, f"Descrição muito longa (máx. {BIO_MAX_LENGTH} caracteres)"

    return True, None


def sanitize_html(text: str) -> str:
    """
    Sanitize text to prevent XSS.
    Uses bleach if available, falls back to html.escape.
    """
    if not text:
        return ""

    if HAS_BLEACH:
        # bleach.clean removes dangerous tags/attributes, keeps safe ones
        return bleach.clean(
            text,
            tags=[],  # No HTML tags allowed
            attributes={},
            strip=True
        )
    else:
        # Fallback: escape all HTML entities
        return html.escape(text)


def sanitize_sql_input(text: str) -> str:
    """
    Basic SQL injection prevention (use parameterized queries instead!).
    This is a safety net, NOT a replacement for parameterized queries.
    """
    if not text:
        return ""

    # Remove SQL comment sequences and dangerous patterns
    dangerous = [
        '--', ';', '/*', '*/', 'xp_', 'sp_',
        'union select', 'drop table', 'delete from',
        'insert into', 'update set', 'alter table',
        'create table', 'exec ', 'execute ',
    ]

    result = text
    for pattern in dangerous:
        # Case insensitive replace
        result = re.sub(re.escape(pattern), '', result, flags=re.IGNORECASE)

    return result


def validate_cpf(cpf: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Brazilian CPF (optional, for future use).
    """
    if not cpf:
        return True, None  # Optional field

    # Remove formatting
    cpf = re.sub(r'[.\-]', '', cpf)

    if len(cpf) != 11 or not cpf.isdigit():
        return False, "CPF deve ter 11 dígitos numéricos"

    # Check for all same digits (invalid)
    if cpf == cpf[0] * 11:
        return False, "CPF inválido"

    # Calculate check digits
    def calc_digit(cpf_partial: str, weights: list) -> int:
        total = sum(int(d) * w for d, w in zip(cpf_partial, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    first_digit = calc_digit(cpf[:9], [10, 9, 8, 7, 6, 5, 4, 3, 2])
    second_digit = calc_digit(cpf[:10], [11, 10, 9, 8, 7, 6, 5, 4, 3, 2])

    if int(cpf[9]) != first_digit or int(cpf[10]) != second_digit:
        return False, "CPF inválido (dígitos verificadores incorretos)"

    return True, None


# --- Testing ---
if __name__ == "__main__":
    # Test password validation
    assert validate_password("Senh@123")[0], "Valid password should pass"
    assert not validate_password("senha")[0], "Short password should fail"
    assert not validate_password("SENHA123")[0], "No lowercase should fail"
    assert not validate_password("senha123")[0], "No uppercase should fail"
    assert not validate_password("SenhaAbc")[0], "No digit should fail"
    assert not validate_password("Senha123")[0], "No special char should fail"
    assert not validate_password("aaaa123@")[0], "Repeated chars should fail"
    print("[OK] Password validation tests passed")

    # Test email validation
    assert validate_email_address("test@example.com")[0], "Valid email should pass"
    assert not validate_email_address("invalid")[0], "Invalid email should fail"
    assert not validate_email_address("@nodomain")[0], "No local part should fail"
    print("[OK] Email validation tests passed")

    # Test name validation
    assert validate_name("João")[0], "Valid name should pass"
    assert validate_name("Maria Silva")[0], "Name with space should pass"
    assert validate_name("Jean-Pierre")[0], "Hyphenated name should pass"
    assert validate_name("D'Angelo")[0], "Apostrophe should pass"
    assert not validate_name("João123")[0], "Numbers in name should fail"
    assert not validate_name("")[0], "Empty name should fail"
    print("[OK] Name validation tests passed")

    # Test bio validation
    assert validate_bio("A" * 500)[0], "Short bio should pass"
    assert not validate_bio("A" * 1500)[0], "Long bio should fail"
    print("[OK] Bio validation tests passed")

    # Test sanitization
    escaped = sanitize_html("<script>alert('xss')</script>")
    # html.escape converts < to < and > to >
    assert "<script>" not in escaped and "</script>" not in escaped, "HTML should be escaped"
    # sanitize_sql_input removes dangerous patterns
    sql_result = sanitize_sql_input("test; DROP TABLE users; --")
    assert "DROP" not in sql_result and ";" not in sql_result and "--" not in sql_result
    print("[OK] Sanitization tests passed")

    # Test CPF
    assert validate_cpf("111.444.777-35")[0], "Valid CPF should pass"
    assert not validate_cpf("111.111.111-11")[0], "All same digits should fail"
    assert not validate_cpf("123.456.789-00")[0], "Invalid check digits should fail"
    print("[OK] CPF validation tests passed")

    print("\n[OK] All validator tests passed!")