"""
Context Processors untuk Admin Panel
Menyediakan data utility models ke semua templates
"""

from django.db.models import Q
from django.utils import timezone
from .models import AdminNotification, SystemMessage, QuickAccess, AdminPreference


def admin_utilities(request):
    """
    Context processor untuk utility data
    - Notifications (unread count dan latest)
    - System Messages (active)
    - Quick Access (user's shortcuts)
    - User Preferences
    """
    
    # Check if user is authenticated and has user attribute
    if not hasattr(request, 'user') or not request.user.is_authenticated or not request.user.is_staff:
        return {}
    
    # ========================================================================
    # NOTIFICATIONS
    # ========================================================================
    from django.db.models import Case, When, IntegerField
    
    notifications = AdminNotification.objects.filter(
        Q(recipient=request.user) | Q(recipient__isnull=True),
        is_read=False
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    ).annotate(
        priority_order=Case(
            When(priority='urgent', then=4),
            When(priority='high', then=3),
            When(priority='medium', then=2),
            When(priority='low', then=1),
            default=0,
            output_field=IntegerField()
        )
    ).order_by('-priority_order', '-created_at')
    
    unread_notifications = notifications[:10]  # Latest 10
    unread_count = notifications.count()
    urgent_count = notifications.filter(priority='urgent').count()
    
    # ========================================================================
    # SYSTEM MESSAGES
    # ========================================================================
    now = timezone.now()
    
    # Get active system messages berdasarkan current page
    current_path = request.path
    
    # Dashboard messages
    dashboard_messages = []
    if '/admin-panel/' in current_path:
        dashboard_messages = SystemMessage.objects.filter(
            is_active=True,
            start_date__lte=now,
            display_location__in=['dashboard', 'all_pages']
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        ).order_by('-priority')[:3]
    
    # All pages messages
    global_messages = SystemMessage.objects.filter(
        is_active=True,
        start_date__lte=now,
        display_location='all_pages'
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    ).order_by('-priority')[:2]
    
    # ========================================================================
    # QUICK ACCESS
    # ========================================================================
    quick_access_items = QuickAccess.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('position')[:8]  # Max 8 items
    
    # ========================================================================
    # USER PREFERENCES
    # ========================================================================
    try:
        user_preference = AdminPreference.objects.get(user=request.user)
    except AdminPreference.DoesNotExist:
        # Default preference
        user_preference = AdminPreference(
            user=request.user,
            theme='light',
            sidebar_state='expanded',
            items_per_page=25
        )
    
    return {
        # Notifications
        'unread_notifications': unread_notifications,
        'unread_notification_count': unread_count,
        'urgent_notification_count': urgent_count,
        
        # System Messages
        'dashboard_messages': dashboard_messages,
        'global_messages': global_messages,
        
        # Quick Access
        'quick_access_items': quick_access_items,
        
        # User Preference
        'user_preference': user_preference,
    }


def notification_count(request):
    """
    Simple context processor untuk notification count saja
    Lebih ringan untuk pages yang tidak perlu full data
    """
    
    # Check if user is authenticated and has user attribute
    if not hasattr(request, 'user') or not request.user.is_authenticated or not request.user.is_staff:
        return {'notification_count': 0}
    
    count = AdminNotification.objects.filter(
        Q(recipient=request.user) | Q(recipient__isnull=True),
        is_read=False
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    ).count()
    
    return {'notification_count': count}

