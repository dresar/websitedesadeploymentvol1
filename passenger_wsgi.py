# passenger_wsgi.py untuk Mode Deployment - Tidak Ketat
# Konfigurasi khusus untuk shared hosting dengan pengaturan fleksibel
# Mode: Development/Testing - Bukan Production

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
sys.path.insert(0, '/home/expedien/public_html/pulosarok.my.id')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')

# ==================== BASIC SETTINGS ====================
# BASIC settings untuk mode deployment yang tidak ketat
os.environ['DEBUG'] = 'True'  # ENABLED untuk mode deployment
os.environ['SECRET_KEY'] = 'django-insecure-deployment-key-not-for-production'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,pulosarok.my.id,www.pulosarok.my.id,expedien.my.id,*'

# ==================== DATABASE CONFIGURATION ====================
# PostgreSQL untuk mode deployment
os.environ['DATABASE_ENGINE'] = 'django.db.backends.postgresql'
os.environ['DATABASE_NAME'] = 'postgres'
os.environ['DATABASE_USER'] = 'postgres'
os.environ['DATABASE_PASSWORD'] = 'root'
os.environ['DATABASE_HOST'] = 'localhost'
os.environ['DATABASE_PORT'] = '5432'

# ==================== SSL/HTTPS SETTINGS - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['SECURE_SSL_REDIRECT'] = 'False'          # DISABLED - Tidak redirect ke HTTPS
os.environ['SECURE_HSTS_SECONDS'] = '0'              # DISABLED - Tidak ada HSTS
os.environ['SECURE_HSTS_INCLUDE_SUBDOMAINS'] = 'False'  # DISABLED
os.environ['SECURE_HSTS_PRELOAD'] = 'False'          # DISABLED
os.environ['SECURE_PROXY_SSL_HEADER'] = ''          # DISABLED

# ==================== SECURITY SETTINGS - RELAXED ====================
# RELAXED untuk mode deployment yang tidak ketat
os.environ['SECURE_BROWSER_XSS_FILTER'] = 'True'     # ENABLED - Basic XSS protection
os.environ['SECURE_CONTENT_TYPE_NOSNIFF'] = 'True'   # ENABLED - Basic content type protection
os.environ['X_FRAME_OPTIONS'] = 'SAMEORIGIN'         # RELAXED - Allow same origin
os.environ['SECURE_REFERRER_POLICY'] = 'strict-origin-when-cross-origin'  # RELAXED
os.environ['SECURE_CROSS_ORIGIN_OPENER_POLICY'] = 'same-origin'  # RELAXED

# ==================== COOKIE SETTINGS - FLEKSIBEL ====================
# FLEKSIBEL untuk mode deployment yang tidak ketat
os.environ['CSRF_COOKIE_SECURE'] = 'False'           # DISABLED - Tidak secure cookies
os.environ['SESSION_COOKIE_SECURE'] = 'False'        # DISABLED - Tidak secure cookies
os.environ['CSRF_COOKIE_HTTPONLY'] = 'True'          # ENABLED - Basic security
os.environ['SESSION_COOKIE_HTTPONLY'] = 'True'       # ENABLED - Basic security
os.environ['CSRF_COOKIE_SAMESITE'] = 'Lax'           # FLEKSIBEL - Lax same site
os.environ['SESSION_COOKIE_SAMESITE'] = 'Lax'        # FLEKSIBEL - Lax same site
os.environ['SESSION_COOKIE_AGE'] = '3600'            # 1 hour
os.environ['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = 'False'  # FLEKSIBEL - Tidak expire saat close

# ==================== CORS SETTINGS - FLEKSIBEL ====================
# FLEKSIBEL untuk mode deployment yang tidak ketat
os.environ['CORS_ALLOW_ALL_ORIGINS'] = 'True'        # ENABLED - Allow semua origin
os.environ['CORS_ALLOW_CREDENTIALS'] = 'True'       # ENABLED - Allow credentials
os.environ['CORS_ALLOWED_ORIGINS'] = 'http://localhost:8000,http://127.0.0.1:8000,http://pulosarok.my.id,https://pulosarok.my.id,http://www.pulosarok.my.id,https://www.pulosarok.my.id,http://expedien.my.id,https://expedien.my.id'

# ==================== CACHE SETTINGS - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['CACHE_BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'  # DISABLED
os.environ['CACHE_MIDDLEWARE_SECONDS'] = '0'         # DISABLED - Tidak ada cache
os.environ['CACHE_MIDDLEWARE_KEY_PREFIX'] = ''       # DISABLED
os.environ['CACHE_MIDDLEWARE_ALIAS'] = 'default'     # DISABLED

# ==================== LOGGING SETTINGS - SEDERHANA ====================
# SEDERHANA untuk mode deployment yang tidak ketat
os.environ['LOG_LEVEL'] = 'INFO'                     # SEDERHANA - Level INFO
os.environ['LOG_FILE'] = '/home/expedien/public_html/pulosarok.my.id/logs/django.log'

# ==================== STATIC & MEDIA FILES ====================
# Django serving untuk mode deployment yang tidak ketat
os.environ['STATIC_URL'] = '/static/'
os.environ['STATIC_ROOT'] = '/home/expedien/public_html/pulosarok.my.id/staticfiles/'
os.environ['MEDIA_URL'] = '/media/'
os.environ['MEDIA_ROOT'] = '/home/expedien/public_html/pulosarok.my.id/media/'

# ==================== PERFORMANCE SETTINGS - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['CONN_MAX_AGE'] = '0'                     # DISABLED - Tidak ada connection pooling
os.environ['CONN_MAX_AGE_OPTIONS'] = '0'             # DISABLED

# ==================== SECURITY MONITORING - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['SECURITY_MONITORING'] = 'False'          # DISABLED
os.environ['INTRUSION_DETECTION'] = 'False'          # DISABLED
os.environ['MALWARE_SCANNING'] = 'False'             # DISABLED
os.environ['VULNERABILITY_SCANNING'] = 'False'       # DISABLED

# ==================== COMPLIANCE & AUDITING - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['AUDIT_LOGGING'] = 'False'                # DISABLED
os.environ['COMPLIANCE_MODE'] = 'False'              # DISABLED
os.environ['PRIVACY_MODE'] = 'False'                 # DISABLED
os.environ['DATA_RETENTION_DAYS'] = '0'              # DISABLED

# ==================== RATE LIMITING - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['RATE_LIMIT_ENABLED'] = 'False'           # DISABLED
os.environ['RATE_LIMIT_REQUESTS'] = '1000'           # FLEKSIBEL - 1000 requests
os.environ['RATE_LIMIT_WINDOW'] = '3600'             # FLEKSIBEL - 1 hour window

# ==================== ERROR REPORTING - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['ERROR_REPORTING'] = 'False'              # DISABLED
os.environ['SENTRY_DSN'] = ''                        # DISABLED

# ==================== MAINTENANCE MODE - DISABLED ====================
# DISABLED untuk mode deployment yang tidak ketat
os.environ['MAINTENANCE_MODE'] = 'False'             # DISABLED
os.environ['MAINTENANCE_MODE_IGNORE_ADMIN'] = 'True' # ENABLED - Admin tetap bisa akses
os.environ['MAINTENANCE_MODE_IGNORE_STAFF'] = 'True' # ENABLED - Staff tetap bisa akses

# ==================== FILE UPLOAD SETTINGS - FLEKSIBEL ====================
# FLEKSIBEL untuk mode deployment yang tidak ketat
os.environ['FILE_UPLOAD_MAX_MEMORY_SIZE'] = '10485760'  # 10MB - FLEKSIBEL
os.environ['DATA_UPLOAD_MAX_MEMORY_SIZE'] = '10485760'   # 10MB - FLEKSIBEL
os.environ['FILE_UPLOAD_PERMISSIONS'] = '0o644'         # FLEKSIBEL
os.environ['FILE_UPLOAD_DIRECTORY_PERMISSIONS'] = '0o755'  # FLEKSIBEL

# ==================== SESSION SETTINGS - FLEKSIBEL ====================
# FLEKSIBEL untuk mode deployment yang tidak ketat
os.environ['SESSION_ENGINE'] = 'django.contrib.sessions.backends.db'  # Database sessions
os.environ['SESSION_COOKIE_AGE'] = '3600'            # 1 hour - FLEKSIBEL
os.environ['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = 'False'  # FLEKSIBEL - Tidak expire saat close
os.environ['SESSION_SAVE_EVERY_REQUEST'] = 'False'   # FLEKSIBEL - Tidak save setiap request

# ==================== CSRF SETTINGS - FLEKSIBEL ====================
# FLEKSIBEL untuk mode deployment yang tidak ketat
os.environ['CSRF_TRUSTED_ORIGINS'] = 'http://localhost:8000,http://127.0.0.1:8000,http://pulosarok.my.id,https://pulosarok.my.id,http://www.pulosarok.my.id,https://www.pulosarok.my.id,http://expedien.my.id,https://expedien.my.id'
os.environ['CSRF_COOKIE_AGE'] = '31449600'           # 1 year - FLEKSIBEL

# ==================== ADMIN SETTINGS ====================
# Admin settings untuk mode deployment yang tidak ketat
os.environ['ADMIN_URL'] = 'admin-panel/'             # Custom admin URL
os.environ['LOGIN_URL'] = '/custom-login-redirect/'
os.environ['LOGIN_REDIRECT_URL'] = '/admin-panel/'
os.environ['LOGOUT_REDIRECT_URL'] = '/admin-panel/login/'

# ==================== RESOURCE LIMITS ====================
# Resource limits untuk cPanel - FLEKSIBEL
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
os.environ['NUMBA_NUM_THREADS'] = '1'

# ==================== ENVIRONMENT SETTINGS ====================
# Environment settings untuk mode deployment yang tidak ketat
os.environ['ENVIRONMENT'] = 'development'            # Development mode
os.environ['DEPLOYMENT_MODE'] = 'hosting'            # Hosting mode

# ==================== DEPLOYMENT NOTES ====================
# 1. SSL/HTTPS: DISABLED - Gunakan HTTP saja
# 2. Security: RELAXED - Tidak terlalu ketat
# 3. CORS: FLEKSIBEL - Allow semua origin
# 4. Session: FLEKSIBEL - Tidak secure cookies
# 5. Cache: DISABLED - Tidak ada caching
# 6. Logging: SEDERHANA - Level INFO
# 7. Database: SQLite3 - File-based
# 8. Static Files: Django serving
# 9. Media Files: Django serving
# 10. Performance: DISABLED - Tidak ada optimasi

# ==================== DEPLOYMENT CHECKLIST ====================
# ✅ SSL/HTTPS: Disabled
# ✅ Security: Relaxed
# ✅ CORS: Flexible
# ✅ Session: Flexible
# ✅ Cache: Disabled
# ✅ Logging: Simple
# ✅ Database: SQLite3
# ✅ Static Files: Django serving
# ✅ Media Files: Django serving
# ✅ Performance: Disabled

# Get WSGI application
application = get_wsgi_application()
