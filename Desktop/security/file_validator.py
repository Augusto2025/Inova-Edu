"""
Security Module: File Upload Validation
Validates file uploads for type, size, and content safety.
"""
import os
from typing import Tuple, Optional, Set
from pathlib import Path

# Try to import python-magic (requires libmagic C library)
# On Windows, use: pip install python-magic-bin
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False
    magic = None

# Allowed file extensions for profile images
ALLOWED_IMAGE_EXTENSIONS: Set[str] = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'
}

# Allowed MIME types
ALLOWED_MIME_TYPES: Set[str] = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/bmp',
}

# Blocked MIME types (dangerous)
BLOCKED_MIME_TYPES: Set[str] = {
    'application/x-msdownload',      # .exe
    'application/x-msdos-program',   # .com
    'application/x-sh',              # .sh
    'application/x-python-code',     # .pyc
    'application/x-php',             # .php
    'text/x-php',                    # .php
    'application/javascript',        # .js
    'text/html',                     # .html
    'application/xml',               # .xml
    'application/x-httpd-php',       # .php
}

# Maximum file size (5MB for profile images)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image_upload(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an uploaded image file.

    Args:
        file_path: Path to the uploaded file

    Returns:
        (is_valid, error_message)
    """
    # Check file exists
    if not os.path.exists(file_path):
        return False, "Arquivo não encontrado"

    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        return False, f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB"

    if file_size == 0:
        return False, "Arquivo vazio"

    # Check extension
    ext = Path(file_path).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Extensão não permitida: {ext}. Permitidas: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"

    # Check MIME type using python-magic (libmagic) if available
    mime_type = None
    if HAS_MAGIC:
        try:
            mime_type = magic.from_file(file_path, mime=True)
        except Exception:
            mime_type = _guess_mime_from_extension(ext)
    else:
        # Fallback: guess from extension
        mime_type = _guess_mime_from_extension(ext)

    if mime_type in BLOCKED_MIME_TYPES:
        return False, f"Tipo de arquivo perigoso detectado: {mime_type}"

    if mime_type not in ALLOWED_MIME_TYPES:
        return False, f"Tipo de arquivo não suportado: {mime_type}"

    # Additional: Verify it's actually a valid image by trying to open with PIL
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            img.verify()  # Verify it's a valid image
            # Check dimensions (max 4000x4000)
            if img.width > 4000 or img.height > 4000:
                return False, "Imagem muito grande (máx. 4000x4000 pixels)"
    except Exception as e:
        return False, f"Arquivo de imagem inválido ou corrompido: {str(e)}"

    return True, None


def _guess_mime_from_extension(ext: str) -> str:
    """Guess MIME type from extension (fallback)."""
    mime_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
    }
    return mime_map.get(ext, 'application/octet-stream')


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and injection.
    """
    # Get just the filename (no path)
    filename = os.path.basename(filename)

    # Replace dangerous characters
    filename = "".join(c for c in filename if c.isalnum() or c in "._- ")

    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]

    return name + ext.lower()


# --- Testing ---
if __name__ == "__main__":
    import tempfile

    # Create a test image
    from PIL import Image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        img = Image.new('RGB', (100, 100), color='red')
        img.save(f.name, 'PNG')
        test_file = f.name

    try:
        # Test valid image
        valid, err = validate_image_upload(test_file)
        assert valid, f"Valid image should pass: {err}"
        print("[OK] Valid image accepted")

        # Test non-existent file
        valid, err = validate_image_upload("/nonexistent/file.png")
        assert not valid, "Non-existent file should fail"
        print("[OK] Non-existent file rejected")

        # Test sanitize
        assert sanitize_filename("test.jpg") == "test.jpg"
        assert sanitize_filename("../evil.exe") == "evil.exe"
        assert sanitize_filename("file with spaces.png") == "file with spaces.png"
        print("[OK] Filename sanitization works")

    finally:
        os.unlink(test_file)

    print("\n[OK] All file validator tests passed!")