"""
Activity Logging System
Auto-log semua aktivitas CRUD di seluruh aplikasi
"""
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import logging

logger = logging.getLogger('admin_panel')

# Daftar model yang dikecualikan dari logging
EXCLUDE_MODELS = [
    'LogEntry',
    'AdminActivityLog',
    'Session',
    'ContentType',
    'Permission',
    'Group',
]


def get_module_from_model(model_name):
    """Tentukan module berdasarkan nama model"""
    module_mapping = {
        'penduduk': 'references',
        'dusun': 'references',
        'lorong': 'references',
        'rw': 'references',
        'rt': 'references',
        'disabilitas': 'references',
        'pelajar': 'references',
        'keluarga': 'references',
        'beneficiary': 'beneficiaries',
        'usaha': 'business',
        'umkm': 'business',
        'koperasi': 'business',
        'bumgdes': 'business',
        'complaint': 'complaints',
        'document': 'documents',
        'tourism': 'tourism',
        'posyandu': 'posyandu',
        'news': 'news',
        'layanan': 'layanan',
        'villageofficials': 'organization',
        'villagestructure': 'organization',
        'customuser': 'users',
    }
    return module_mapping.get(model_name.lower(), 'system')


def log_activity(user, obj, action, description=''):
    """
    Log aktivitas user ke AdminActivityLog
    """
    if not user or not user.is_authenticated:
        return
    
    try:
        from admin_panel.models import AdminActivityLog
        
        content_type = ContentType.objects.get_for_model(obj)
        
        # Skip model yang dikecualikan
        if content_type.model in [m.lower() for m in EXCLUDE_MODELS]:
            return
        
        # Dapatkan module dari model
        module = get_module_from_model(content_type.model)
        
        # Buat object repr yang readable
        object_repr = str(obj)[:255]
        if not object_repr or object_repr == 'None':
            object_repr = f"{content_type.model} #{obj.pk}"
        
        # Buat log
        AdminActivityLog.objects.create(
            user=user,
            action=action,
            module=module,
            description=description or f"{action.upper()} {content_type.model}",
            content_type=content_type,
            object_id=obj.pk,
            object_repr=object_repr,
        )
        
        logger.info(
            f"Activity Log: {user.username} - {action.upper()} - "
            f"{module} - {object_repr}"
        )
    except Exception as e:
        logger.error(f"Error creating activity log: {str(e)}")


def get_request_user():
    """
    Get current request user from thread local
    """
    from core.middleware import get_current_user
    return get_current_user()


@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    """
    Auto-log ketika model di-save
    """
    # Skip jika AUDIT_LOGGING dimatikan
    if not getattr(settings, 'AUDIT_LOGGING', True):
        return
    
    # Skip model yang dikecualikan
    if sender.__name__ in EXCLUDE_MODELS:
        return
    
    try:
        user = get_request_user()
        if user and user.is_authenticated:
            action = 'create' if created else 'update'
            action_msg = 'Dibuat' if created else 'Diubah'
            description = f'{action_msg} {sender._meta.verbose_name or sender.__name__}: {str(instance)}'
            log_activity(user, instance, action, description)
    except Exception as e:
        logger.error(f"Error in log_model_save: {str(e)}")


@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    """
    Auto-log ketika model di-delete
    """
    # Skip jika AUDIT_LOGGING dimatikan
    if not getattr(settings, 'AUDIT_LOGGING', True):
        return
    
    # Skip model yang dikecualikan
    if sender.__name__ in EXCLUDE_MODELS:
        return
    
    try:
        user = get_request_user()
        if user and user.is_authenticated:
            description = f'Dihapus {sender._meta.verbose_name or sender.__name__}: {str(instance)}'
            log_activity(user, instance, 'delete', description)
    except Exception as e:
        logger.error(f"Error in log_model_delete: {str(e)}")


def manual_log(user, obj, action, message):
    """
    Manual logging untuk aktivitas khusus
    action: 'create', 'update', 'delete', 'view', 'export', 'import', 'login', 'logout', etc
    """
    log_activity(user, obj, action, message)

