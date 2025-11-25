import os
from .settings import *

# Production settings override
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Secret key from environment (must be set). Fallback is unsafe.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'UNSAFE_DEFAULT_CHANGE_ME')

# Security hardening
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Assume behind HTTPS proxy
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# DRF throttling to mitigate abuse
REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
})

# In production collectstatic will place files in STATIC_ROOT
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
