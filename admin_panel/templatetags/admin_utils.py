"""
Template Tags untuk Admin Panel Utilities
"""

from django import template
from django.db.models import Q
from django.utils import timezone
from admin_panel.models import (
    AdminNotification, SystemMessage, QuickAccess, 
    AdminActivityLog, DashboardWidget
)

register = template.Library()


# ============================================================================
# NOTIFICATION TAGS
# ============================================================================

@register.simple_tag
def get_unread_notifications(user, limit=10):
    """Get unread notifications untuk user"""
    if not user.is_authenticated:
        return []
    
    return AdminNotification.objects.filter(
        Q(recipient=user) | Q(recipient__isnull=True),
        is_read=False
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    ).order_by('-priority', '-created_at')[:limit]


@register.simple_tag
def get_notification_count(user):
    """Get count of unread notifications"""
    if not user.is_authenticated:
        return 0
    
    return AdminNotification.objects.filter(
        Q(recipient=user) | Q(recipient__isnull=True),
        is_read=False
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    ).count()


@register.simple_tag
def get_urgent_notification_count(user):
    """Get count of urgent unread notifications"""
    if not user.is_authenticated:
        return 0
    
    return AdminNotification.objects.filter(
        Q(recipient=user) | Q(recipient__isnull=True),
        is_read=False,
        priority='urgent'
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    ).count()


# ============================================================================
# SYSTEM MESSAGE TAGS
# ============================================================================

@register.simple_tag
def get_system_messages(location='dashboard', limit=3):
    """Get active system messages untuk location tertentu"""
    now = timezone.now()
    
    return SystemMessage.objects.filter(
        is_active=True,
        start_date__lte=now,
        display_location__in=[location, 'all_pages']
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    ).order_by('-priority')[:limit]


@register.simple_tag
def has_active_system_messages(location='dashboard'):
    """Check apakah ada system messages aktif"""
    now = timezone.now()
    
    count = SystemMessage.objects.filter(
        is_active=True,
        start_date__lte=now,
        display_location__in=[location, 'all_pages']
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    ).count()
    
    return count > 0


# ============================================================================
# QUICK ACCESS TAGS
# ============================================================================

@register.simple_tag
def get_quick_access(user, limit=8):
    """Get quick access items untuk user"""
    if not user.is_authenticated:
        return []
    
    return QuickAccess.objects.filter(
        user=user,
        is_active=True
    ).order_by('position')[:limit]


@register.simple_tag
def has_quick_access(user):
    """Check apakah user punya quick access"""
    if not user.is_authenticated:
        return False
    
    return QuickAccess.objects.filter(user=user, is_active=True).exists()


# ============================================================================
# ACTIVITY LOG TAGS
# ============================================================================

@register.simple_tag
def get_recent_activities(user=None, module=None, limit=10):
    """Get recent activities"""
    logs = AdminActivityLog.objects.select_related('user').all()
    
    if user:
        logs = logs.filter(user=user)
    
    if module:
        logs = logs.filter(module=module)
    
    return logs.order_by('-created_at')[:limit]


@register.simple_tag
def get_user_activity_count(user, days=30):
    """Get activity count untuk user dalam X hari terakhir"""
    if not user:
        return 0
    
    from datetime import timedelta
    since = timezone.now() - timedelta(days=days)
    
    return AdminActivityLog.objects.filter(
        user=user,
        created_at__gte=since
    ).count()


# ============================================================================
# DASHBOARD WIDGET TAGS
# ============================================================================

@register.simple_tag
def get_dashboard_widgets(user):
    """Get dashboard widgets untuk user"""
    if not user.is_authenticated:
        return []
    
    return DashboardWidget.objects.filter(
        user=user,
        is_visible=True
    ).order_by('position')


@register.simple_tag
def has_dashboard_widgets(user):
    """Check apakah user punya dashboard widgets"""
    if not user.is_authenticated:
        return False
    
    return DashboardWidget.objects.filter(
        user=user,
        is_visible=True
    ).exists()


# ============================================================================
# UTILITY FILTERS
# ============================================================================

@register.filter
def notification_icon(notification_type):
    """Get icon class untuk notification type"""
    icons = {
        'info': 'fa-info-circle text-info',
        'warning': 'fa-exclamation-triangle text-warning',
        'success': 'fa-check-circle text-success',
        'danger': 'fa-times-circle text-danger',
        'reminder': 'fa-clock text-primary',
    }
    return icons.get(notification_type, 'fa-info-circle')


@register.filter
def priority_badge(priority):
    """Get badge class untuk priority"""
    badges = {
        'low': 'badge bg-secondary',
        'medium': 'badge bg-primary',
        'high': 'badge bg-warning',
        'urgent': 'badge bg-danger',
    }
    return badges.get(priority, 'badge bg-secondary')


@register.filter
def action_badge(action):
    """Get badge class untuk action type"""
    badges = {
        'create': 'badge bg-success',
        'update': 'badge bg-info',
        'delete': 'badge bg-danger',
        'view': 'badge bg-secondary',
        'export': 'badge bg-primary',
        'import': 'badge bg-warning',
        'approve': 'badge bg-success',
        'reject': 'badge bg-danger',
        'publish': 'badge bg-info',
        'unpublish': 'badge bg-secondary',
    }
    return badges.get(action, 'badge bg-secondary')


@register.filter
def system_message_class(message_type):
    """Get alert class untuk system message type"""
    classes = {
        'announcement': 'alert-info',
        'maintenance': 'alert-warning',
        'update': 'alert-success',
        'warning': 'alert-danger',
        'info': 'alert-info',
    }
    return classes.get(message_type, 'alert-info')

