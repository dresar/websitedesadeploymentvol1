# Konfigurasi Error Pages untuk Django Production
# File: pulosarok_website/urls_production.py

from django.conf import settings
from django.conf.urls import handler404, handler500, handler403, handler400
from django.urls import path, include
from core import error_views

# Error handlers untuk production
handler404 = error_views.custom_404
handler500 = error_views.custom_500
handler403 = error_views.custom_403
handler400 = error_views.custom_400

# URL patterns untuk production
urlpatterns = [
    # Core URLs
    path('', include('core.urls')),
    
    # Admin Panel URLs
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    
    # App URLs
    path('beneficiaries/', include('beneficiaries.urls')),
    path('business/', include('business.urls')),
    path('complaints/', include('complaints.urls')),
    path('documents/', include('documents.urls')),
    path('layanan/', include('layanan.urls')),
    path('letters/', include('letters.urls')),
    path('news/', include('news.urls')),
    path('organization/', include('organization.urls')),
    path('posyandu/', include('posyandu.urls')),
    path('references/', include('references.urls')),
    path('tourism/', include('tourism.urls')),
    path('village-profile/', include('village_profile.urls')),
    
    # Error URLs
    path('errors/', include('core.error_urls')),
    
    # API URLs (with different namespaces)
    path('api/', include('core.urls', namespace='api_core')),
    path('api/beneficiaries/', include('beneficiaries.urls', namespace='api_beneficiaries')),
    path('api/business/', include('business.urls', namespace='api_business')),
    path('api/complaints/', include('complaints.urls', namespace='api_complaints')),
    path('api/documents/', include('documents.urls', namespace='api_documents')),
    path('api/layanan/', include('layanan.urls', namespace='api_layanan')),
    path('api/letters/', include('letters.urls', namespace='api_letters')),
    path('api/news/', include('news.urls', namespace='api_news')),
    path('api/organization/', include('organization.urls', namespace='api_organization')),
    path('api/posyandu/', include('posyandu.urls', namespace='api_posyandu')),
    path('api/references/', include('references.urls', namespace='api_references')),
    path('api/tourism/', include('tourism.urls', namespace='api_tourism')),
    path('api/village-profile/', include('village_profile.urls', namespace='api_village_profile')),
]

# Security settings untuk production
if not settings.DEBUG:
    # Disable admin interface untuk security tambahan
    # urlpatterns = [path('admin/', lambda request: HttpResponseForbidden("Admin disabled in production"))] + urlpatterns
    
    # Add security middleware
    from django.middleware.security import SecurityMiddleware
    from core.security_middleware import SecurityMiddleware as CustomSecurityMiddleware
    
    # Custom error handlers
    handler404 = error_views.custom_404
    handler500 = error_views.custom_500
    handler403 = error_views.custom_403
    handler400 = error_views.custom_400
