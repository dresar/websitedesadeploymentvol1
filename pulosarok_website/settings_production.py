# Django Production Settings untuk Website Desa Pulosarok
# Mode: Production dengan HTTP (tanpa auto HTTPS redirect)

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts untuk production
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'pulosarok.desa.id',
    'www.pulosarok.desa.id',
    'your-domain.com',  # Ganti dengan domain Anda
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'django_summernote',
    
    # Local apps
    'core',
    'admin_panel',
    'beneficiaries',
    'business',
    'complaints',
    'documents',
    'layanan',
    'letters',
    'news',
    'organization',
    'posyandu',
    'references',
    'tourism',
    'village_profile',
]

MIDDLEWARE = [
    # Security middleware (harus di urutan atas)
    'django.middleware.security.SecurityMiddleware',
    'core.security_middleware.SecurityMiddleware',
    
    # Session dan CSRF
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Messages
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Custom middleware
    'core.maintenance_middleware.MaintenanceModeMiddleware',
    'core.activity_logging.ActivityLoggingMiddleware',
    'core.login_tracking.LoginTrackingMiddleware',
    
    # Security headers
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pulosarok_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.website_settings',
                'admin_panel.context_processors.admin_context',
                'news.context_processors.news_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'pulosarok_website.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'pulosarok_db'),
        'USER': os.environ.get('DB_USER', 'pulosarok_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-db-password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'prefer',
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== SECURITY SETTINGS ====================

# Security settings untuk production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = False  # Set True jika menggunakan HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 jam
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CSRF security
CSRF_COOKIE_SECURE = False  # Set True jika menggunakan HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_AGE = 3600

# Password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ==================== CACHE SETTINGS ====================

# Redis cache untuk production
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'pulosarok',
        'TIMEOUT': 300,
    }
}

# Session cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ==================== LOGGING SETTINGS ====================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ==================== EMAIL SETTINGS ====================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-app-password')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@pulosarok.desa.id')

# ==================== SUMMERNOTE SETTINGS ====================

SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '400',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    }
}

# ==================== CUSTOM SETTINGS ====================

# Website settings
WEBSITE_NAME = 'Website Desa Pulosarok'
WEBSITE_DESCRIPTION = 'Website resmi Desa Pulosarok'
WEBSITE_URL = 'http://pulosarok.desa.id'  # HTTP untuk sekarang

# Security settings
SECURITY_LEVEL = 'high'
MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT = 15
ENABLE_2FA = True
ENABLE_CAPTCHA = True

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644

# ==================== PRODUCTION SPECIFIC ====================

# Disable admin interface untuk security tambahan
# ADMIN_ENABLED = False

# Error pages
DEBUG_PROPAGATE_EXCEPTIONS = False

# Disable Django debug toolbar
INTERNAL_IPS = []

# ==================== BACKUP SETTINGS ====================

# Database backup settings
DB_BACKUP_ENABLED = True
DB_BACKUP_SCHEDULE = 'daily'
DB_BACKUP_RETENTION_DAYS = 30

# File backup settings
FILE_BACKUP_ENABLED = True
FILE_BACKUP_SCHEDULE = 'weekly'
FILE_BACKUP_RETENTION_DAYS = 90

# ==================== MONITORING SETTINGS ====================

# Performance monitoring
ENABLE_PERFORMANCE_MONITORING = True
PERFORMANCE_LOG_THRESHOLD = 2.0  # seconds

# Security monitoring
ENABLE_SECURITY_MONITORING = True
SECURITY_LOG_FAILED_LOGINS = True
SECURITY_LOG_SUSPICIOUS_ACTIVITY = True

# ==================== CORS SETTINGS ====================

# CORS settings untuk API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://pulosarok.desa.id",
]

CORS_ALLOW_CREDENTIALS = True

# ==================== CELERY SETTINGS ====================

# Celery untuk background tasks
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# ==================== ENVIRONMENT VARIABLES ====================

# Load environment variables dari .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ==================== FINAL SECURITY CHECKS ====================

# Pastikan tidak ada debug mode di production
if DEBUG:
    raise ValueError("DEBUG must be False in production!")

# Pastikan secret key tidak default
if SECRET_KEY == 'your-secret-key-here-change-in-production':
    raise ValueError("SECRET_KEY must be changed in production!")

# Pastikan database password tidak default
if DATABASES['default']['PASSWORD'] == 'your-db-password':
    raise ValueError("Database password must be changed in production!")

print("✅ Production settings loaded successfully!")
print("🔒 Security settings enabled")
print("📊 Logging configured")
print("💾 Cache configured")
print("📧 Email configured")
print("⚠️  Remember to set up HTTPS in the future!")
