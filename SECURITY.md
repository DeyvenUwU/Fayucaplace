# Aspectos de seguridad implementados en FayucaPlace

## 1. CSRF (Cross-Site Request Forgery)
**Implementación:**
- Middleware `CsrfViewMiddleware` habilitado por defecto
- Tokens CSRF en todos los formularios (`{% csrf_token %}`)
- `CSRF_COOKIE_HTTPONLY = True` (previene lectura por JS)
- `CSRF_COOKIE_SECURE = True` en producción (solo HTTPS)
- `CSRF_TRUSTED_ORIGINS` configurable por entorno

**Protección:**
- Formularios POST/PUT/DELETE requieren token válido
- API REST usa CSRF token o autenticación por token
- Previene ataques donde sitios maliciosos envían peticiones en nombre del usuario

## 2. XSS (Cross-Site Scripting)
**Implementación:**
- Templates Django escapan automáticamente HTML
- `SECURE_BROWSER_XSS_FILTER = True` (header X-XSS-Protection)
- `SECURE_CONTENT_TYPE_NOSNIFF = True` (previene MIME sniffing)
- `X_FRAME_OPTIONS = 'DENY'` (previene clickjacking)

**Protección:**
- Variables en templates se escapan: `{{ user.username }}` es seguro
- Uso de `|safe` solo cuando es necesario y validado
- Headers de seguridad configurados

## 3. CORS (Cross-Origin Resource Sharing)
**Implementación:**
- Por defecto, sin CORS habilitado (solo same-origin)
- Si se necesita API pública, instalar `django-cors-headers`
- Configurar `CORS_ALLOWED_ORIGINS` explícitamente

**Protección:**
- API solo accesible desde mismo dominio por defecto
- Si se habilita CORS, whitelist de orígenes permitidos
- Previene acceso no autorizado desde otros dominios

## 4. SQL Injection
**Implementación:**
- ORM Django con queries parametrizadas
- Nunca se construyen queries SQL directamente con f-strings
- Uso de `.filter()`, `.get()`, `.exclude()` del ORM

**Ejemplos seguros:**
```python
# SEGURO (parametrizado)
Publicacion.objects.filter(titulo__icontains=search)

# INSEGURO (si se usara, pero NO usamos esto)
# cursor.execute(f"SELECT * FROM publicacion WHERE titulo LIKE '%{search}%'")
```

**Protección:**
- ORM escapa automáticamente parámetros
- Previene inyección de código SQL malicioso

## 5. Host Header Attack
**Implementación:**
- `ALLOWED_HOSTS` configurado explícitamente
- `USE_X_FORWARDED_HOST = False` (solo confía en Host header validado)
- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`

**Protección:**
- Django rechaza peticiones con Host header no permitido
- Previene cache poisoning y password reset attacks
- Solo acepta dominios en whitelist

## 6. Referer/Origin validation
**Implementación:**
- CSRF middleware valida Referer/Origin headers
- `CSRF_TRUSTED_ORIGINS` define orígenes válidos para peticiones cross-origin

**Protección:**
- Peticiones POST/PUT/DELETE verifican origen
- Previene ataques desde sitios no autorizados

## Aspectos adicionales de seguridad

### Session Security
- `SESSION_COOKIE_SECURE = True` (solo HTTPS en producción)
- `SESSION_COOKIE_HTTPONLY = True` (no accesible por JavaScript)
- `SESSION_COOKIE_SAMESITE = 'Lax'` (protección contra CSRF)

### HTTPS/SSL (producción)
- `SECURE_SSL_REDIRECT = True` (redirect HTTP → HTTPS)
- `SECURE_HSTS_SECONDS = 31536000` (1 año de HSTS)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`

### Password Security
- Validators: UserAttributeSimilarity, MinimumLength, CommonPassword, Numeric
- Hashing con PBKDF2 (default Django)

### API Security
- Token authentication (DRF)
- Permissions por objeto (IsOwnerOrReadOnly)
- Throttling: 100/día anónimos, 1000/día usuarios
- HTTPS requerido en producción

### Logging
- Log de warnings a archivo `django.log`
- Log de eventos de seguridad (django.security logger)
- Formato verboso con timestamp y módulo

## Testing de seguridad

```bash
# Check deployment
python manage.py check --deploy

# Verificar settings
python manage.py diffsettings

# Security headers test
curl -I https://tu-dominio.com
```

## Recomendaciones adicionales

1. **Rate Limiting**: Implementar en login (django-ratelimit)
2. **2FA**: Considerar django-otp para admin
3. **CSP**: Implementar Content-Security-Policy (django-csp)
4. **Security Scans**: Usar Bandit, Safety, OWASP ZAP
5. **Updates**: Mantener Django y dependencias actualizadas
6. **Secrets**: Usar variables de entorno, nunca commitear secrets
7. **Backups**: Automatizar backups de BD
8. **Monitoring**: Configurar Sentry para errores en producción
