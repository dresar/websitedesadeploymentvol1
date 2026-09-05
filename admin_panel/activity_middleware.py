"""
Activity Logging Middleware
Auto-log semua aktivitas admin di sistem
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from .models import AdminActivityLog
import json


class ActivityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware untuk auto-logging aktivitas admin
    Log create, update, delete operations
    """
    
    # Skip logging untuk URL ini
    SKIP_URLS = [
        '/static/',
        '/media/',
        '/admin/jsi18n/',
        '/favicon.ico',
        '__debug__',
        '/api/notifications/',
        '/utilities/activity-logs/',  # Prevent infinite loop
    ]
    
    # Module mapping berdasarkan URL path
    MODULE_MAP = {
        '/admin-panel/references/': 'references',
        '/admin-panel/beneficiaries/': 'beneficiaries',
        '/admin-panel/business/': 'business',
        '/admin-panel/complaints/': 'complaints',
        '/admin-panel/documents/': 'documents',
        '/admin-panel/tourism/': 'tourism',
        '/admin-panel/posyandu/': 'posyandu',
        '/admin-panel/news/': 'news',
        '/admin-panel/village-profile/': 'village_profile',
        '/admin-panel/organization/': 'organization',
        '/admin-panel/layanan/': 'layanan',
        '/admin-panel/letters/': 'letters',
        '/admin-panel/settings/': 'settings',
        '/admin-panel/users/': 'users',
        '/admin-panel/': 'dashboard',
    }
    
    def process_response(self, request, response):
        """Process response untuk logging"""
        
        # Skip jika bukan user yang login atau bukan staff
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return response
        
        if not request.user.is_staff:
            return response
        
        # Skip URL tertentu
        path = request.path
        if any(skip in path for skip in self.SKIP_URLS):
            return response
        
        # Skip jika bukan method yang perlu di-log
        if request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return response
        
        # Skip jika response error
        if response.status_code >= 400:
            return response
        
        # Tentukan action berdasarkan method dan path
        action = self._determine_action(request)
        if not action:
            return response
        
        # Tentukan module
        module = self._determine_module(path)
        
        # Create log
        try:
            self._create_log(request, action, module)
        except Exception as e:
            # Jangan break request jika logging gagal
            pass
        
        return response
    
    def _determine_action(self, request):
        """Tentukan action berdasarkan request"""
        path = request.path.lower()
        method = request.method
        
        # DELETE method
        if method == 'DELETE':
            return 'delete'
        
        # Check path patterns
        if '/delete/' in path or '/hapus/' in path:
            return 'delete'
        elif '/create/' in path or '/add/' in path or '/tambah/' in path:
            return 'create'
        elif '/edit/' in path or '/update/' in path or '/ubah/' in path:
            return 'update'
        elif '/export/' in path:
            return 'export'
        elif '/import/' in path:
            return 'import'
        elif '/approve/' in path:
            return 'approve'
        elif '/reject/' in path:
            return 'reject'
        elif '/publish/' in path:
            return 'publish'
        elif '/unpublish/' in path:
            return 'unpublish'
        elif method == 'POST':
            return 'create'
        elif method in ['PUT', 'PATCH']:
            return 'update'
        
        return None
    
    def _determine_module(self, path):
        """Tentukan module berdasarkan path"""
        for url_pattern, module_name in self.MODULE_MAP.items():
            if path.startswith(url_pattern):
                return module_name
        return 'system'
    
    def _create_log(self, request, action, module):
        """Create activity log entry"""
        
        # Get IP address
        ip_address = self._get_client_ip(request)
        
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        # Build description
        description = self._build_description(request, action, module)
        
        # Get object info if available
        content_type = None
        object_id = None
        object_repr = None
        
        # Try to extract object ID from URL
        if hasattr(request, 'resolver_match') and request.resolver_match:
            kwargs = request.resolver_match.kwargs
            if 'pk' in kwargs:
                object_id = kwargs['pk']
            elif 'id' in kwargs:
                object_id = kwargs['id']
        
        # Create log
        AdminActivityLog.objects.create(
            user=request.user,
            action=action,
            module=module,
            description=description,
            content_type=content_type,
            object_id=object_id,
            object_repr=object_repr,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _build_description(self, request, action, module):
        """Build description for log"""
        action_text = {
            'create': 'menambahkan',
            'update': 'mengubah',
            'delete': 'menghapus',
            'export': 'mengexport',
            'import': 'mengimport',
            'approve': 'menyetujui',
            'reject': 'menolak',
            'publish': 'mempublikasi',
            'unpublish': 'membatalkan publikasi',
        }.get(action, 'melakukan aksi')
        
        module_text = {
            'references': 'Data Referensi',
            'beneficiaries': 'Penerima Bantuan',
            'business': 'Usaha',
            'complaints': 'Keluhan',
            'documents': 'Dokumen',
            'tourism': 'Wisata',
            'posyandu': 'Posyandu',
            'news': 'Berita',
            'village_profile': 'Profil Desa',
            'organization': 'Organisasi',
            'layanan': 'Layanan',
            'letters': 'Surat',
            'settings': 'Pengaturan',
            'users': 'Pengguna',
            'dashboard': 'Dashboard',
            'system': 'Sistem',
        }.get(module, module)
        
        return f"{request.user.username} {action_text} data {module_text}"

