# Error Pages Configuration untuk Django Production
# File: core/error_views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def custom_404(request, exception=None):
    """
    Custom 404 error page untuk production
    """
    # Log 404 error untuk monitoring
    logger.warning(f"404 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - User-Agent: {request.META.get('HTTP_USER_AGENT')}")
    
    # Render custom 404 template
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """
    Custom 500 error page untuk production
    """
    # Log 500 error untuk monitoring
    logger.error(f"500 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - User-Agent: {request.META.get('HTTP_USER_AGENT')}")
    
    # Render custom 500 template
    return render(request, 'errors/500.html', status=500)

def custom_403(request, exception=None):
    """
    Custom 403 error page untuk production
    """
    # Log 403 error untuk monitoring
    logger.warning(f"403 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - User-Agent: {request.META.get('HTTP_USER_AGENT')}")
    
    # Render custom 403 template
    return render(request, 'errors/403.html', status=403)

def custom_400(request, exception=None):
    """
    Custom 400 error page untuk production
    """
    # Log 400 error untuk monitoring
    logger.warning(f"400 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - User-Agent: {request.META.get('HTTP_USER_AGENT')}")
    
    # Render custom 400 template
    return render(request, 'errors/400.html', status=400)

def custom_405(request, exception=None):
    """
    Custom 405 error page untuk production
    """
    # Log 405 error untuk monitoring
    logger.warning(f"405 Error: {request.path} - Method: {request.method} - IP: {request.META.get('REMOTE_ADDR')}")
    
    # Render custom 405 template
    return render(request, 'errors/405.html', status=405)

def custom_410(request, exception=None):
    """
    Custom 410 error page untuk production
    """
    # Log 410 error untuk monitoring
    logger.warning(f"410 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')}")
    
    # Render custom 410 template
    return render(request, 'errors/410.html', status=410)

def custom_429(request, exception=None):
    """
    Custom 429 error page untuk production (Rate Limited)
    """
    # Log 429 error untuk monitoring
    logger.warning(f"429 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - Rate Limited")
    
    # Render custom 429 template
    return render(request, 'errors/429.html', status=429)

def custom_503(request, exception=None):
    """
    Custom 503 error page untuk production (Service Unavailable)
    """
    # Log 503 error untuk monitoring
    logger.error(f"503 Error: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - Service Unavailable")
    
    # Render custom 503 template
    return render(request, 'errors/503.html', status=503)

def maintenance_mode(request):
    """
    Maintenance mode page
    """
    return render(request, 'errors/maintenance.html', status=503)

def security_violation(request):
    """
    Security violation page untuk akses yang tidak sah
    """
    # Log security violation
    logger.critical(f"Security Violation: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - User-Agent: {request.META.get('HTTP_USER_AGENT')}")
    
    # Render security violation template
    return render(request, 'errors/security_violation.html', status=403)

def blocked_ip(request):
    """
    Blocked IP page
    """
    # Log blocked IP attempt
    logger.warning(f"Blocked IP Access: {request.path} - IP: {request.META.get('REMOTE_ADDR')}")
    
    # Render blocked IP template
    return render(request, 'errors/blocked_ip.html', status=403)

def suspicious_activity(request):
    """
    Suspicious activity page
    """
    # Log suspicious activity
    logger.warning(f"Suspicious Activity: {request.path} - IP: {request.META.get('REMOTE_ADDR')} - User-Agent: {request.META.get('HTTP_USER_AGENT')}")
    
    # Render suspicious activity template
    return render(request, 'errors/suspicious_activity.html', status=403)

# Error handler untuk AJAX requests
def ajax_error_handler(request, error_code, error_message):
    """
    Error handler khusus untuk AJAX requests
    """
    return HttpResponse(
        f'{{"error": true, "code": {error_code}, "message": "{error_message}"}}',
        content_type='application/json',
        status=error_code
    )

# Error handler untuk API requests
def api_error_handler(request, error_code, error_message):
    """
    Error handler khusus untuk API requests
    """
    return HttpResponse(
        f'{{"error": true, "code": {error_code}, "message": "{error_message}", "timestamp": "{timezone.now().isoformat()}"}}',
        content_type='application/json',
        status=error_code
    )

# Utility functions untuk error handling
def log_error(request, error_type, error_message, status_code=500):
    """
    Utility function untuk logging error
    """
    logger.error(
        f"{error_type}: {error_message} - "
        f"Path: {request.path} - "
        f"Method: {request.method} - "
        f"IP: {request.META.get('REMOTE_ADDR')} - "
        f"User-Agent: {request.META.get('HTTP_USER_AGENT')} - "
        f"Status: {status_code}"
    )

def get_client_ip(request):
    """
    Get client IP address dari request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_suspicious_request(request):
    """
    Check apakah request mencurigakan
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    suspicious_patterns = [
        'sqlmap', 'nikto', 'nmap', 'masscan', 'zap',
        'burp', 'w3af', 'acunetix', 'nessus', 'openvas',
        'curl', 'wget', 'python-requests', 'scrapy'
    ]
    
    for pattern in suspicious_patterns:
        if pattern in user_agent:
            return True
    
    return False

def rate_limit_exceeded(request):
    """
    Check apakah rate limit exceeded
    """
    # Implementasi rate limiting logic di sini
    # Untuk sekarang return False
    return False

# Error context untuk templates
def get_error_context(request, error_code):
    """
    Get context data untuk error templates
    """
    context = {
        'error_code': error_code,
        'request_path': request.path,
        'client_ip': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'timestamp': timezone.now(),
        'website_name': getattr(settings, 'WEBSITE_NAME', 'Website Desa Pulosarok'),
        'website_url': getattr(settings, 'WEBSITE_URL', 'http://pulosarok.desa.id'),
    }
    
    return context
