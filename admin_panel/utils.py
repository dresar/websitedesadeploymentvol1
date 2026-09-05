"""
Utility Helper Functions untuk Admin Panel
Functions untuk memudahkan logging, tracking, dan notifikasi
"""

from functools import wraps
from django.contrib.contenttypes.models import ContentType
from .models import AdminActivityLog, DataExportHistory, AdminNotification
import os


# ============================================================================
# ACTIVITY LOGGING HELPERS
# ============================================================================

def log_activity(action, module, description=None, obj=None):
    """
    Decorator untuk auto-log activity
    
    Usage:
        @log_activity('create', 'references', 'Menambahkan data penduduk')
        def create_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Execute view
            response = view_func(request, *args, **kwargs)
            
            # Log activity
            if request.user.is_authenticated:
                try:
                    create_activity_log(
                        user=request.user,
                        action=action,
                        module=module,
                        description=description or f"{request.user.username} melakukan {action} di {module}",
                        obj=obj,
                        request=request
                    )
                except:
                    pass  # Don't break view if logging fails
            
            return response
        return wrapper
    return decorator


def create_activity_log(user, action, module, description, obj=None, request=None, old_value=None, new_value=None):
    """
    Helper function untuk create activity log
    
    Args:
        user: User yang melakukan aktivitas
        action: Jenis aksi (create, update, delete, dll)
        module: Module/app name
        description: Deskripsi aktivitas
        obj: Object yang dimodifikasi (optional)
        request: Request object untuk get IP dan user agent (optional)
        old_value: Nilai lama (untuk update)
        new_value: Nilai baru (untuk update/create)
    """
    
    # Get content type and object info
    content_type = None
    object_id = None
    object_repr = None
    
    if obj:
        content_type = ContentType.objects.get_for_model(obj)
        object_id = obj.pk
        object_repr = str(obj)[:255]
    
    # Get IP and user agent
    ip_address = None
    user_agent = None
    
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    
    # Create log
    return AdminActivityLog.objects.create(
        user=user,
        action=action,
        module=module,
        description=description,
        content_type=content_type,
        object_id=object_id,
        object_repr=object_repr,
        ip_address=ip_address,
        user_agent=user_agent,
        old_value=old_value,
        new_value=new_value,
    )


# ============================================================================
# EXPORT TRACKING HELPERS
# ============================================================================

def track_export(user, module, export_format, file_path, record_count, filters=None, request=None):
    """
    Helper function untuk track export data
    
    Args:
        user: User yang melakukan export
        module: Module/app name
        export_format: Format export (excel, csv, pdf, json)
        file_path: Path ke file yang di-export
        record_count: Jumlah records yang di-export
        filters: Dictionary filter yang digunakan (optional)
        request: Request object untuk get IP (optional)
    
    Returns:
        DataExportHistory object
    """
    
    # Get file info
    file_name = os.path.basename(file_path) if file_path else 'export_file'
    file_size = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0
    
    # Get IP
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    # Create export history
    export_history = DataExportHistory.objects.create(
        user=user,
        module=module,
        export_format=export_format,
        file_name=file_name,
        file_size=file_size,
        record_count=record_count,
        filters=filters,
        is_successful=True,
        ip_address=ip_address,
    )
    
    # Also log as activity
    create_activity_log(
        user=user,
        action='export',
        module=module,
        description=f"{user.username} mengexport {record_count} data {module} ke {export_format.upper()}",
        request=request
    )
    
    return export_history


def track_export_error(user, module, export_format, error_message, request=None):
    """
    Helper function untuk track failed export
    """
    
    # Get IP
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    return DataExportHistory.objects.create(
        user=user,
        module=module,
        export_format=export_format,
        file_name='export_failed',
        is_successful=False,
        error_message=error_message,
        ip_address=ip_address,
    )


# ============================================================================
# NOTIFICATION HELPERS
# ============================================================================

def create_notification(title, message, recipient=None, notification_type='info', priority='medium', 
                       action_url=None, action_text=None, expires_at=None):
    """
    Helper function untuk create notification
    
    Args:
        title: Judul notification
        message: Isi pesan
        recipient: User penerima (None = broadcast ke semua)
        notification_type: info, warning, success, danger, reminder
        priority: low, medium, high, urgent
        action_url: URL untuk action button (optional)
        action_text: Text untuk action button (optional)
        expires_at: Datetime kapan notification expire (optional)
    
    Returns:
        AdminNotification object
    """
    
    return AdminNotification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        type=notification_type,
        priority=priority,
        action_url=action_url,
        action_text=action_text,
        expires_at=expires_at,
    )


def notify_admins(title, message, notification_type='info', priority='medium', action_url=None, action_text=None):
    """
    Helper function untuk broadcast notification ke semua admin
    """
    return create_notification(
        title=title,
        message=message,
        recipient=None,  # Broadcast
        notification_type=notification_type,
        priority=priority,
        action_url=action_url,
        action_text=action_text
    )


def notify_user(user, title, message, notification_type='info', action_url=None, action_text=None):
    """
    Helper function untuk notify specific user
    """
    return create_notification(
        title=title,
        message=message,
        recipient=user,
        notification_type=notification_type,
        action_url=action_url,
        action_text=action_text
    )


# ============================================================================
# PREFERENCE HELPERS
# ============================================================================

def get_user_items_per_page(user, default=25):
    """
    Get user's preferred items per page
    """
    try:
        from .models import AdminPreference
        preference = AdminPreference.objects.get(user=user)
        return preference.items_per_page
    except:
        return default


def get_user_theme(user):
    """
    Get user's preferred theme
    """
    try:
        from .models import AdminPreference
        preference = AdminPreference.objects.get(user=user)
        return preference.theme
    except:
        return 'light'

