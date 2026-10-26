# Security Audit Report - Inova Edu Web System

## Executive Summary
**Critical Vulnerabilities Found: 7** | **High: 5** | **Medium: 8** | **Low: 4**

The system has **critical security flaws** including plain-text password storage, hardcoded API keys, and insecure authentication mechanisms.

---

## CRITICAL Vulnerabilities

### 1. Plain-Text Password Storage (CWE-256)
**Location:** `InovaEdu/models.py:83`, `InovaEdu/views.py:48-51`
**Impact:** All user passwords stored in plain text in database
**Evidence:**
```python
# models.py
senha = models.CharField(db_column='Senha', max_length=128)

# views.py - Login compares plain text
usuario = Usuario.objects.filter(email__iexact=Email, senha=Senha).first()
```
**Fix:** Use Django's `make_password`/`check_password` with PBKDF2.

### 2. Hardcoded API Key in Source Code (CWE-798)
**Location:** `InovaEdu/views.py:119`
**Impact:** Resend API key exposed in repository
```python
resend.api_key = "re_Dn9Qt4mm_6cxkqsovJ3uhe3rWSX79rY9w"
```
**Fix:** Move to environment variable.

### 3. Insecure Password Reset Token (CWE-326)
**Location:** `InovaEdu/tokens.py`
**Impact:** Token based on SHA256(user_id + plain_password) - reversible if password known, predictable
```python
def make_token(self, usuario):
    valor = f"{usuario.idusuario}{usuario.senha}"  # Uses plain password!
    return hashlib.sha256(valor.encode()).hexdigest()
```
**Fix:** Use Django's `default_token_generator` (HMAC + timestamp).

### 4. Missing CSRF Protection on State-Changing Endpoints (CWE-352)
**Location:** `InovaEdu/views.py:23` - `@csrf_exempt` imported and potentially used
**Impact:** CSRF attacks on profile updates, file uploads, deletions
**Fix:** Remove `@csrf_exempt`, enforce CSRF on all POST/PUT/DELETE.

### 5. Session Fixation / Weak Session Management (CWE-384)
**Location:** `InovaEdu/views.py:56`, `InovaEdu/context_processors.py:9`
**Impact:** Session only stores email, no rotation on login, no secure flags in dev
**Fix:** Use Django's auth system, rotate session on login.

### 6. Open Redirect via HTTP_REFERER (CWE-601)
**Location:** `InovaEdu/views.py:1801, 1880, 1511, 1530`
**Impact:** Attackers can redirect users to malicious sites
```python
return redirect(request.META.get("HTTP_REFERER", "CursoCoord"))
```
**Fix:** Validate redirect URLs against allowed hosts.

### 7. Debug Information Exposure (CWE-497)
**Location:** Multiple `print()` statements in production views
**Impact:** Sensitive data leaked to logs (user info, tokens, SQL queries)
**Fix:** Remove all debug prints, use proper logging.

---

## HIGH Vulnerabilities

### 8. Insecure Direct Object References (IDOR) (CWE-639)
**Location:** Multiple views (repositorio, projetos, certificados)
**Impact:** Users can access objects by ID without authorization checks
**Fix:** Consistent authorization checks on all object access.

### 9. Missing Rate Limiting (CWE-307)
**Location:** Login, password reset, API endpoints
**Impact:** Brute force attacks on credentials
**Fix:** Implement django-ratelimit or similar.

### 10. Weak Content Security Policy (CWE-693)
**Location:** `config/settings.py:62-66`
**Impact:** `'unsafe-inline'` allows XSS via injected scripts
```python
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", ...)
```
**Fix:** Use nonces/hashes for inline scripts, remove unsafe-inline.

### 11. File Upload Without Validation (CWE-434)
**Location:** `InovaEdu/views.py:854-928` (upload_arquivo, upload_pasta)
**Impact:** Malicious file upload, potential RCE
**Fix:** Validate MIME type, extension, scan for malware.

### 12. Duplicate View Functions (Maintenance/Security Risk)
**Location:** `InovaEdu/views.py:1133-1154` and `1188-1240` (criar_evento x2)
**Impact:** Confusion, potential bypass of security checks
**Fix:** Consolidate, remove duplicates.

---

## MEDIUM Vulnerabilities

13. **Missing Security Headers in Development** - SECURE_HSTS not set when DEBUG=True
14. **Inconsistent Authorization Patterns** - Some views check `is_professor`, others check session email
15. **No Password Complexity Enforcement** - Only Django validators, no custom rules
16. **Information Disclosure in Error Messages** - Stack traces exposed to users
17. **Missing HTTPS Enforcement in Development** - SECURE_SSL_REDIRECT = not DEBUG
18. **Weak CORS Configuration** - Not explicitly configured
19. **No Audit Logging** - No tracking of sensitive actions
20. **Template Variable Exposure** - `{{ usuario.senha }}` could be exposed in templates

---

## LOW Vulnerabilities

21. **Outdated Dependencies** - Need to check requirements.txt
22. **Missing Security.txt** - No responsible disclosure contact
23. **Verbose Error Pages** - DEBUG=True shows detailed errors
24. **No Automated Security Testing** - No SAST/DAST in CI/CD

---

## Recommended Fix Priority

1. **Immediate (Today):** #1, #2, #3, #4, #7
2. **This Week:** #5, #6, #8, #9, #10, #11, #12
3. **This Sprint:** #13-20
4. **Backlog:** #21-24