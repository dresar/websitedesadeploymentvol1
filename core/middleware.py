from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
import time
import threading

# Thread local storage untuk menyimpan current user
_thread_locals = threading.local()


def get_current_user():
    """
    Retrieve current user from thread local storage
    """
    return getattr(_thread_locals, 'user', None)


def set_current_user(user):
    """
    Store current user in thread local storage
    """
    _thread_locals.user = user

class RoleBasedAccessMiddleware:
    """
    Middleware untuk role-based access control
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Simple role check - allow all for now
        response = self.get_response(request)
        return response

class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware untuk menyimpan current user di thread local
    Diperlukan untuk activity logging
    """
    
    def process_request(self, request):
        set_current_user(getattr(request, 'user', None))
    
    def process_response(self, request, response):
        set_current_user(None)
        return response


class AutoCacheClearMiddleware(MiddlewareMixin):
    """
    Middleware untuk auto clear cache setiap request dalam development mode
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_cache_clear = 0
        self.cache_clear_interval = 5  # Clear cache every 5 seconds
        
    def __call__(self, request):
        # Clear cache every 5 seconds
        current_time = time.time()
        if current_time - self.last_cache_clear > self.cache_clear_interval:
            try:
                cache.clear()
                self.last_cache_clear = current_time
                print(f"[{time.strftime('%H:%M:%S')}] Auto cache cleared")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Error auto clearing cache: {e}")
        
        response = self.get_response(request)
        return response


class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware untuk menerapkan pengaturan keamanan
    """
    
    def process_request(self, request):
        try:
            from django.conf import settings as django_settings
            from .models import WebsiteSettings
            settings_obj = WebsiteSettings.get_settings()
            
            # SSL Redirect - hanya aktif di production atau jika DEBUG=False
            if (settings_obj.enable_ssl_redirect and 
                not request.is_secure() and 
                not django_settings.DEBUG):
                # Skip redirect for admin panel login to avoid redirect loops
                if not request.path.startswith('/admin-panel/login/'):
                    return HttpResponseRedirect('https://' + request.get_host() + request.get_full_path())
        except Exception as e:
            # If there's an error, continue without security checks
            pass
        
        return None
    
    def process_response(self, request, response):
        try:
            from django.conf import settings as django_settings
            from .models import WebsiteSettings
            settings_obj = WebsiteSettings.get_settings()
            
            # HSTS Header - hanya aktif di production atau jika DEBUG=False
            if (settings_obj.enable_hsts and 
                request.is_secure() and 
                not django_settings.DEBUG):
                response['Strict-Transport-Security'] = f'max-age={settings_obj.hsts_max_age}; includeSubDomains'
            
            # Security Headers - selalu aktif
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
        except Exception as e:
            # If there's an error, continue without security headers
            pass
        
        return response