# Production Settings Track

This guide explains the production-readiness changes made in both Django projects:

- `myproject/myproject/settings.py`
- `portfolio/portfolio/settings.py`

The goal is to keep local development convenient while keeping secrets and deployment behavior outside the source code.

## 1. The Original Development Settings

A new Django project commonly starts with settings like these:

```python
SECRET_KEY = 'django-insecure-generated-development-value'
DEBUG = True
ALLOWED_HOSTS = []
```

The original portfolio project also used a development-only console email backend and did not define secure cookie, HTTPS, or HSTS settings.

These settings are acceptable for learning on a local machine, but they are not appropriate for a public deployment:

- A secret key in source code can be exposed through Git, backups, logs, or screenshots.
- `DEBUG = True` can reveal tracebacks, settings, file paths, and other internal details.
- An empty or wildcard host policy does not describe the real domains allowed to serve the site.
- Plain HTTP and non-secure cookies make session and CSRF theft easier.
- The console email backend prints email instead of sending it.

## 2. Why Environment Variables Are Used

An environment variable is a value supplied by the operating system or deployment platform instead of being written into the application source.

For example, PowerShell can set a value for the current terminal session:

```powershell
$env:DJANGO_DEBUG='False'
$env:DJANGO_SECRET_KEY='a-long-random-secret-value'
```

Python reads it with `os.environ`:

```python
import os

secret_key = os.environ.get('DJANGO_SECRET_KEY')
```

This gives us three benefits:

1. The same code can run locally, in testing, and in production.
2. Secrets do not need to be committed to Git.
3. Deployment configuration can change without editing application code.

`os.environ.get(name, default)` means: use the environment value when it exists; otherwise use the default.

The defaults in this repository are intentionally suitable only for local development. They are not production secrets.

## 3. Secret Key: Before and After

### Before

```python
SECRET_KEY = 'django-insecure-4!wz)uh7ui=@2*vqrk_21p^...'
```

The problem is not only the text itself. The important problem is that the secret is stored in tracked source code.

### After

```python
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'dev-only-change-this-secret-key'
)
```

In production, provide a long, random value:

```powershell
$env:DJANGO_SECRET_KEY='replace-with-a-long-random-production-secret'
```

Never copy a real production secret into `settings.py`, a Markdown file, a notebook, a commit message, or a public issue.

## 4. Debug Mode: Before and After

### Before

```python
DEBUG = True
```

When `DEBUG` is true, Django is optimized for development. Error pages are detailed and static-file behavior is different.

### After

```python
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'
```

This line has several steps:

1. Read `DJANGO_DEBUG` from the environment.
2. Use the string `'True'` if the variable is missing, preserving local behavior.
3. Convert the text to lowercase.
4. Compare it with `'true'` to produce a real Python boolean.

Examples:

```text
DJANGO_DEBUG=True   -> True
DJANGO_DEBUG=true   -> True
DJANGO_DEBUG=False  -> False
DJANGO_DEBUG=false  -> False
```

This is important because environment variables are strings. Do not write `bool(os.environ.get('DJANGO_DEBUG'))`: the string `'False'` is non-empty, so Python would incorrectly treat it as true.

For deployment:

```powershell
$env:DJANGO_DEBUG='False'
```

## 5. Allowed Hosts: Before and After

### Before

```python
ALLOWED_HOSTS = []
```

This may work for local development with Django's test client, but a deployed site needs explicit hostnames.

### After

```python
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'DJANGO_ALLOWED_HOSTS',
        '127.0.0.1,localhost'
    ).split(',')
    if host.strip()
]
```

The environment value is a comma-separated string:

```powershell
$env:DJANGO_ALLOWED_HOSTS='example.com,www.example.com'
```

The code then:

1. Reads the string.
2. Splits it at commas.
3. Removes extra spaces with `strip()`.
4. Ignores empty entries.
5. Produces the list Django expects.

Do not use `ALLOWED_HOSTS = ['*']` for a public deployment unless you fully understand the risk and have another trusted host-validation layer.

## 6. HTTPS and Secure Cookies

The projects now define these controls from environment variables:

```python
SECURE_SSL_REDIRECT = os.environ.get(
    'DJANGO_SECURE_SSL_REDIRECT', 'False'
).lower() == 'true'
SESSION_COOKIE_SECURE = os.environ.get(
    'DJANGO_SESSION_COOKIE_SECURE', 'False'
).lower() == 'true'
CSRF_COOKIE_SECURE = os.environ.get(
    'DJANGO_CSRF_COOKIE_SECURE', 'False'
).lower() == 'true'
```

### `SECURE_SSL_REDIRECT`

When true, Django redirects HTTP requests to HTTPS. Enable it when HTTPS is configured correctly and the site should not serve ordinary HTTP.

### `SESSION_COOKIE_SECURE`

When true, browsers send the login session cookie only over HTTPS. This helps prevent session theft over an insecure connection.

### `CSRF_COOKIE_SECURE`

When true, browsers send the CSRF cookie only over HTTPS. This protects the cookie used by Django's CSRF defense.

For a real HTTPS deployment:

```powershell
$env:DJANGO_SECURE_SSL_REDIRECT='True'
$env:DJANGO_SESSION_COOKIE_SECURE='True'
$env:DJANGO_CSRF_COOKIE_SECURE='True'
```

Do not enable these blindly on a local HTTP-only setup, or login and forms may appear broken because the browser will not send secure cookies over HTTP.

## 7. HSTS Settings

The projects also define:

```python
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False'
).lower() == 'true'
SECURE_HSTS_PRELOAD = os.environ.get(
    'DJANGO_SECURE_HSTS_PRELOAD', 'False'
).lower() == 'true'
```

HSTS tells browsers to use HTTPS for a period of time.

- `SECURE_HSTS_SECONDS` is the duration in seconds.
- `SECURE_HSTS_INCLUDE_SUBDOMAINS` includes subdomains.
- `SECURE_HSTS_PRELOAD` indicates readiness for browser preload lists.

HSTS can be difficult to undo after browsers cache it. Enable it only after every relevant domain and subdomain works reliably over HTTPS.

A strict deployment example is:

```powershell
$env:DJANGO_SECURE_HSTS_SECONDS='31536000'
$env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='True'
$env:DJANGO_SECURE_HSTS_PRELOAD='True'
```

## 8. Email Backend: Before and After

### Development

The main learning project uses:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This prints email messages in the terminal. It is useful for testing password reset or notification code without sending real mail.

### Portfolio deployment setting

The portfolio project uses:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

This selects Django's SMTP backend, but it still requires SMTP host, port, username, password, and TLS settings from the deployment environment before it can send mail.

A future project might add:

```python
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
```

Never commit an email password.

## 9. Local Versus Production Profiles

### Local development

```powershell
$env:DJANGO_DEBUG='True'
$env:DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
$env:DJANGO_SECURE_SSL_REDIRECT='False'
$env:DJANGO_SESSION_COOKIE_SECURE='False'
$env:DJANGO_CSRF_COOKIE_SECURE='False'
$env:DJANGO_SECURE_HSTS_SECONDS='0'
```

### Production

```powershell
$env:DJANGO_DEBUG='False'
$env:DJANGO_SECRET_KEY='replace-with-a-long-random-secret'
$env:DJANGO_ALLOWED_HOSTS='example.com,www.example.com'
$env:DJANGO_SECURE_SSL_REDIRECT='True'
$env:DJANGO_SESSION_COOKIE_SECURE='True'
$env:DJANGO_CSRF_COOKIE_SECURE='True'
$env:DJANGO_SECURE_HSTS_SECONDS='31536000'
$env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='True'
$env:DJANGO_SECURE_HSTS_PRELOAD='True'
```

The exact values depend on the hosting platform, reverse proxy, domain names, and HTTPS certificate setup.

## 10. How to Validate the Configuration

Run the ordinary check during development:

```powershell
python manage.py check
```

Run the deployment check with production-like values:

```powershell
python manage.py check --deploy
```

The deployment check is meaningful only when the production environment variables are actually set. A local default profile should be convenient, while the production profile should be strict.

Also run:

```powershell
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py collectstatic --noinput
```

For both projects, run the commands from the directory containing that project's `manage.py`.

## 11. Repeat This Pattern in a New Project

1. Add `import os` to `settings.py`.
2. Replace hard-coded secrets with `os.environ.get()`.
3. Parse booleans explicitly by normalizing text and comparing with `'true'`.
4. Parse comma-separated lists such as `ALLOWED_HOSTS`.
5. Parse integer settings such as ports and HSTS duration with `int()`.
6. Keep development defaults safe for local work but clearly non-production.
7. Set production values in the hosting platform's environment configuration.
8. Keep `.env` files out of Git if you use them locally.
9. Run `check`, `check --deploy`, migrations, tests, and static collection.
10. Review `git diff` and `git status --short` before committing.

## 12. Important Limitation

Environment variables protect values from being stored in source code, but they do not automatically make an application secure. Production readiness also requires HTTPS, a correct reverse-proxy setup, secure database access, backups, logging, dependency updates, least-privilege accounts, and tested deployment procedures.
