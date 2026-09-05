# Error URLs Configuration untuk Django Production
# File: core/error_urls.py

from django.urls import path
from . import error_views

app_name = 'errors'

urlpatterns = [
    # Error pages
    path('404/', error_views.custom_404, name='404'),
    path('500/', error_views.custom_500, name='500'),
    path('403/', error_views.custom_403, name='403'),
    path('400/', error_views.custom_400, name='400'),
    path('405/', error_views.custom_405, name='405'),
    path('410/', error_views.custom_410, name='410'),
    path('429/', error_views.custom_429, name='429'),
    path('503/', error_views.custom_503, name='503'),
    
    # Special error pages
    path('maintenance/', error_views.maintenance_mode, name='maintenance'),
    path('security-violation/', error_views.security_violation, name='security_violation'),
    path('blocked-ip/', error_views.blocked_ip, name='blocked_ip'),
    path('suspicious-activity/', error_views.suspicious_activity, name='suspicious_activity'),
]
