# Security Middleware untuk Django Production
# File: core/security_middleware.py

import logging
import time
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
import re

logger = logging.getLogger(__name__)

class SecurityMiddleware(MiddlewareMixin):
    """
    Security middleware untuk production
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Process request untuk security checks
        """
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Check blocked IPs
        if self.is_ip_blocked(client_ip):
            logger.warning(f"Blocked IP access attempt: {client_ip} - {request.path}")
            return HttpResponseForbidden("Access denied")
        
        # Check suspicious activity
        if self.is_suspicious_request(request):
            logger.warning(f"Suspicious request detected: {client_ip} - {request.path} - {request.META.get('HTTP_USER_AGENT')}")
            return HttpResponseForbidden("Suspicious activity detected")
        
        # Rate limiting
        if self.is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded: {client_ip} - {request.path}")
            return HttpResponseForbidden("Rate limit exceeded")
        
        # SQL injection protection
        if self.has_sql_injection(request):
            logger.warning(f"SQL injection attempt: {client_ip} - {request.path} - {request.GET}")
            return HttpResponseForbidden("Invalid request")
        
        # XSS protection
        if self.has_xss_attempt(request):
            logger.warning(f"XSS attempt detected: {client_ip} - {request.path}")
            return HttpResponseForbidden("Invalid request")
        
        # Path traversal protection
        if self.has_path_traversal(request):
            logger.warning(f"Path traversal attempt: {client_ip} - {request.path}")
            return HttpResponseForbidden("Invalid request")
        
        return None
    
    def process_response(self, request, response):
        """
        Add security headers to response
        """
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp
        
        # HSTS header (hanya jika HTTPS)
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    def get_client_ip(self, request):
        """
        Get client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_blocked(self, ip):
        """
        Check if IP is blocked
        """
        # Check cache untuk blocked IPs
        blocked_ips = cache.get('blocked_ips', [])
        return ip in blocked_ips
    
    def is_suspicious_request(self, request):
        """
        Check for suspicious request patterns
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        path = request.path.lower()
        
        # Suspicious user agents
        suspicious_agents = [
            'sqlmap', 'nikto', 'nmap', 'masscan', 'zap',
            'burp', 'w3af', 'acunetix', 'nessus', 'openvas',
            'curl', 'wget', 'python-requests', 'scrapy',
            'bot', 'crawler', 'spider'
        ]
        
        for agent in suspicious_agents:
            if agent in user_agent:
                return True
        
        # Suspicious paths
        suspicious_paths = [
            '/admin/', '/wp-admin/', '/phpmyadmin/', '/.env',
            '/config/', '/backup/', '/.git/', '/.svn/',
            '/shell.php', '/cmd.php', '/eval.php'
        ]
        
        for path_pattern in suspicious_paths:
            if path_pattern in path:
                return True
        
        return False
    
    def is_rate_limited(self, ip):
        """
        Check rate limiting
        """
        cache_key = f'rate_limit_{ip}'
        requests = cache.get(cache_key, 0)
        
        # Max 100 requests per minute
        if requests > 100:
            return True
        
        # Increment counter
        cache.set(cache_key, requests + 1, 60)
        return False
    
    def has_sql_injection(self, request):
        """
        Check for SQL injection attempts
        """
        sql_patterns = [
            r'union\s+select',
            r'drop\s+table',
            r'delete\s+from',
            r'insert\s+into',
            r'update\s+set',
            r'exec\s*\(',
            r'sp_',
            r'xp_',
            r'--',
            r'/\*',
            r'\*/',
            r'waitfor\s+delay',
            r'benchmark\s*\(',
            r'sleep\s*\(',
        ]
        
        # Check GET parameters
        for key, value in request.GET.items():
            if isinstance(value, str):
                for pattern in sql_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return True
        
        # Check POST data
        if request.method == 'POST':
            for key, value in request.POST.items():
                if isinstance(value, str):
                    for pattern in sql_patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            return True
        
        return False
    
    def has_xss_attempt(self, request):
        """
        Check for XSS attempts
        """
        xss_patterns = [
            r'<script',
            r'javascript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'onclick\s*=',
            r'onmouseover\s*=',
            r'<iframe',
            r'<object',
            r'<embed',
            r'<link',
            r'<meta',
            r'<style',
            r'expression\s*\(',
            r'vbscript:',
            r'data:text/html',
        ]
        
        # Check GET parameters
        for key, value in request.GET.items():
            if isinstance(value, str):
                for pattern in xss_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return True
        
        # Check POST data
        if request.method == 'POST':
            for key, value in request.POST.items():
                if isinstance(value, str):
                    for pattern in xss_patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            return True
        
        return False
    
    def has_path_traversal(self, request):
        """
        Check for path traversal attempts
        """
        path_traversal_patterns = [
            r'\.\./',
            r'\.\.\\',
            r'%2e%2e%2f',
            r'%2e%2e%5c',
            r'%252e%252e%252f',
            r'%252e%252e%255c',
        ]
        
        path = request.path
        for pattern in path_traversal_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                return True
        
        return False


class IPBlockingMiddleware(MiddlewareMixin):
    """
    Middleware untuk blocking IP addresses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Check if IP should be blocked
        """
        client_ip = self.get_client_ip(request)
        
        # Check if IP is in blocked list
        if self.is_ip_blocked(client_ip):
            logger.warning(f"Blocked IP access: {client_ip}")
            return HttpResponseForbidden("Your IP address has been blocked")
        
        return None
    
    def get_client_ip(self, request):
        """
        Get client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_blocked(self, ip):
        """
        Check if IP is blocked
        """
        # Get blocked IPs from cache or database
        blocked_ips = cache.get('blocked_ips', [])
        return ip in blocked_ips


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware untuk logging requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Log request information
        """
        # Log request
        logger.info(
            f"Request: {request.method} {request.path} - "
            f"IP: {self.get_client_ip(request)} - "
            f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
        )
        
        return None
    
    def process_response(self, request, response):
        """
        Log response information
        """
        # Log response
        logger.info(
            f"Response: {response.status_code} - "
            f"Path: {request.path} - "
            f"IP: {self.get_client_ip(request)}"
        )
        
        return response
    
    def get_client_ip(self, request):
        """
        Get client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# Utility functions untuk security
def block_ip(ip_address, reason="Manual block"):
    """
    Block an IP address
    """
    blocked_ips = cache.get('blocked_ips', [])
    if ip_address not in blocked_ips:
        blocked_ips.append(ip_address)
        cache.set('blocked_ips', blocked_ips, 86400)  # 24 hours
        logger.warning(f"IP blocked: {ip_address} - Reason: {reason}")

def unblock_ip(ip_address):
    """
    Unblock an IP address
    """
    blocked_ips = cache.get('blocked_ips', [])
    if ip_address in blocked_ips:
        blocked_ips.remove(ip_address)
        cache.set('blocked_ips', blocked_ips, 86400)
        logger.info(f"IP unblocked: {ip_address}")

def get_blocked_ips():
    """
    Get list of blocked IPs
    """
    return cache.get('blocked_ips', [])

def is_ip_blocked(ip_address):
    """
    Check if IP is blocked
    """
    blocked_ips = cache.get('blocked_ips', [])
    return ip_address in blocked_ips