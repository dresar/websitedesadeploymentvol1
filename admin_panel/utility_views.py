"""
Utility Views untuk Admin Panel
Mengelola 7 model utility: ActivityLog, Notification, Widget, QuickAccess, SystemMessage, ExportHistory, Preference
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
import json
import os

from .models import (
    AdminActivityLog, AdminNotification, DashboardWidget, QuickAccess,
    SystemMessage, DataExportHistory, AdminPreference
)
from core.models import CustomUser


# ============================================================================
# ADMIN ACTIVITY LOG VIEWS
# ============================================================================

@login_required
def activity_log_list(request):
    """List semua activity logs dengan filter"""
    logs = AdminActivityLog.objects.select_related('user').all()
    
    # Filter by user
    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(user_id=user_id)
    
    # Filter by module
    module = request.GET.get('module')
    if module:
        logs = logs.filter(module=module)
    
    # Filter by action
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(created_at__gte=date_from)
    if date_to:
        logs = logs.filter(created_at__lte=date_to)
    
    # Search
    search = request.GET.get('search')
    if search:
        logs = logs.filter(
            Q(description__icontains=search) |
            Q(object_repr__icontains=search) |
            Q(user__username__icontains=search)
        )
    
    # Statistics
    stats = {
        'total': logs.count(),
        'today': logs.filter(created_at__date=timezone.now().date()).count(),
        'this_week': logs.filter(created_at__gte=timezone.now() - timedelta(days=7)).count(),
        'by_action': logs.values('action').annotate(count=Count('id')).order_by('-count')[:5],
        'by_module': logs.values('module').annotate(count=Count('id')).order_by('-count')[:5],
    }
    
    # Get unique values for filters
    users = CustomUser.objects.filter(id__in=logs.values_list('user_id', flat=True).distinct())
    modules = logs.values_list('module', flat=True).distinct()
    actions = logs.values_list('action', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(logs, 50)
    page = request.GET.get('page', 1)
    logs_page = paginator.get_page(page)
    
    context = {
        'page_title': 'Activity Logs',
        'active_menu': 'utilities',
        'active_submenu': 'activity_logs',
        'logs': logs_page,
        'stats': stats,
        'users': users,
        'modules': sorted(set(modules)),
        'actions': sorted(set(actions)),
        'current_filters': {
            'user': user_id,
            'module': module,
            'action': action,
            'date_from': date_from,
            'date_to': date_to,
            'search': search,
        }
    }
    
    return render(request, 'admin_panel/utilities/activity_log_list.html', context)


@login_required
def activity_log_detail(request, log_id):
    """Detail dari satu activity log"""
    log = get_object_or_404(AdminActivityLog, id=log_id)
    
    context = {
        'page_title': 'Activity Log Detail',
        'active_menu': 'utilities',
        'active_submenu': 'activity_logs',
        'log': log,
    }
    
    return render(request, 'admin_panel/utilities/activity_log_detail.html', context)


@login_required
@require_POST
def activity_log_delete(request, log_id):
    """Delete activity log (soft delete or hard delete)"""
    log = get_object_or_404(AdminActivityLog, id=log_id)
    log.delete()
    
    messages.success(request, 'Log aktivitas berhasil dihapus')
    return redirect('admin_panel:utilities:activity_logs')


@login_required
def activity_log_export(request):
    """Export activity logs ke CSV"""
    import csv
    from django.utils.text import slugify
    
    logs = AdminActivityLog.objects.select_related('user').all()
    
    # Apply same filters as list view
    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(user_id=user_id)
    
    module = request.GET.get('module')
    if module:
        logs = logs.filter(module=module)
    
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)
    
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(timestamp__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__lte=date_to)
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    filename = f'activity_logs_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'User', 'Action', 'Module', 'Object', 'Description', 'IP Address'])
    
    for log in logs:
        writer.writerow([
            log.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            log.user.username if log.user else 'Anonim',
            log.action,
            log.module or '-',
            log.object_repr or '-',
            log.description or '-',
            log.ip_address or '-',
        ])
    
    return response


# ============================================================================
# ADMIN NOTIFICATION VIEWS
# ============================================================================

@login_required
def notification_list(request):
    """List semua notifications untuk user saat ini"""
    from django.db.models import Case, When, IntegerField
    
    # Get notifications for current user or broadcast
    notifications = AdminNotification.objects.filter(
        Q(recipient=request.user) | Q(recipient__isnull=True)
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
    
    # Filter by read status
    status = request.GET.get('status')
    if status == 'unread':
        notifications = notifications.filter(is_read=False)
    elif status == 'read':
        notifications = notifications.filter(is_read=True)
    
    # Filter by type
    notif_type = request.GET.get('type')
    if notif_type:
        notifications = notifications.filter(type=notif_type)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        notifications = notifications.filter(priority=priority)
    
    # Remove expired
    notifications = notifications.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    )
    
    # Statistics
    stats = {
        'total': notifications.count(),
        'unread': notifications.filter(is_read=False).count(),
        'urgent': notifications.filter(priority='urgent', is_read=False).count(),
        'by_type': notifications.values('type').annotate(count=Count('id')),
    }
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page', 1)
    notifications_page = paginator.get_page(page)
    
    context = {
        'page_title': 'Notifications',
        'active_menu': 'utilities',
        'active_submenu': 'notifications',
        'notifications': notifications_page,
        'stats': stats,
        'current_filters': {
            'status': status,
            'type': notif_type,
            'priority': priority,
        }
    }
    
    return render(request, 'admin_panel/utilities/notification_list.html', context)


@login_required
def notification_create(request):
    """Create new notification"""
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notif_type = request.POST.get('type', 'info')
        priority = request.POST.get('priority', 'medium')
        action_text = request.POST.get('action_text')
        action_url = request.POST.get('action_url')
        expires_at = request.POST.get('expires_at')
        is_broadcast = request.POST.get('is_broadcast') == 'on'
        recipient_id = request.POST.get('recipient_id')
        
        notification = AdminNotification.objects.create(
            title=title,
            message=message,
            type=notif_type,
            priority=priority,
            action_text=action_text or None,
            action_url=action_url or None,
            expires_at=expires_at or None,
            recipient=None if is_broadcast else CustomUser.objects.get(id=recipient_id),
            created_by=request.user,
        )
        
        messages.success(request, f'Notifikasi "{title}" berhasil dibuat')
        return redirect('admin_panel:utilities:notifications')
    
    # GET request - show form
    users = CustomUser.objects.filter(is_active=True).order_by('username')
    
    context = {
        'page_title': 'Create Notification',
        'active_menu': 'utilities',
        'active_submenu': 'notifications',
        'users': users,
    }
    
    return render(request, 'admin_panel/utilities/notification_form.html', context)


@login_required
@require_POST
def notification_mark_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(
        AdminNotification,
        id=notification_id,
        recipient__in=[request.user, None]
    )
    
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('admin_panel:utilities:notifications')


@login_required
@require_POST
def notification_mark_all_read(request):
    """Mark all notifications as read for current user"""
    count = AdminNotification.objects.filter(
        Q(recipient=request.user) | Q(recipient__isnull=True),
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    messages.success(request, f'{count} notifikasi ditandai sudah dibaca')
    return redirect('admin_panel:utilities:notifications')


@login_required
@require_POST
def notification_delete(request, notification_id):
    """Delete notification"""
    notification = get_object_or_404(AdminNotification, id=notification_id)
    notification.delete()
    
    messages.success(request, 'Notifikasi berhasil dihapus')
    return redirect('admin_panel:utilities:notifications')


@login_required
def notification_center_api(request):
    """API untuk notification center (untuk AJAX)"""
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
    ).order_by('-priority_order', '-created_at')[:10]
    
    data = {
        'count': notifications.count(),
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.type,
                'priority': n.priority,
                'action_text': n.action_text,
                'action_url': n.action_url,
                'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
                'icon': n.get_icon(),
                'badge_class': n.get_badge_class(),
            }
            for n in notifications
        ]
    }
    
    return JsonResponse(data)


# ============================================================================
# DASHBOARD WIDGET VIEWS
# ============================================================================

@login_required
def dashboard_widget_list(request):
    """List dan manage dashboard widgets untuk user saat ini"""
    widgets = DashboardWidget.objects.filter(user=request.user).order_by('position')
    
    # Calculate stats
    total_widgets = widgets.count()
    visible_widgets = widgets.filter(is_visible=True).count()
    hidden_widgets = widgets.filter(is_visible=False).count()
    # Count unique widget types
    unique_types = widgets.values('widget_type').distinct().count()
    
    context = {
        'page_title': 'Dashboard Widgets',
        'active_menu': 'utilities',
        'active_submenu': 'dashboard_widgets',
        'widgets': widgets,
        'total_widgets': total_widgets,
        'visible_widgets': visible_widgets,
        'hidden_widgets': hidden_widgets,
        'unique_types': unique_types,
    }
    
    return render(request, 'admin_panel/utilities/dashboard_widget_list.html', context)


@login_required
def dashboard_widget_create(request):
    """Create new dashboard widget"""
    if request.method == 'POST':
        title = request.POST.get('title')
        widget_type = request.POST.get('widget_type')
        size = request.POST.get('size', 'medium')
        config = request.POST.get('config', '{}')
        refresh_interval = request.POST.get('refresh_interval')
        
        # Get max position
        max_pos = DashboardWidget.objects.filter(user=request.user).count()
        
        widget = DashboardWidget.objects.create(
            user=request.user,
            title=title,
            widget_type=widget_type,
            size=size,
            config=json.loads(config) if config else {},
            refresh_interval=int(refresh_interval) if refresh_interval else None,
            position=max_pos,
        )
        
        messages.success(request, f'Widget "{title}" berhasil ditambahkan')
        return redirect('admin_panel:utilities:dashboard_widgets')
    
    context = {
        'page_title': 'Create Dashboard Widget',
        'active_menu': 'utilities',
        'active_submenu': 'dashboard_widgets',
    }
    return render(request, 'admin_panel/utilities/dashboard_widget_form.html', context)


@login_required
def dashboard_widget_edit(request, widget_id):
    """Edit dashboard widget"""
    widget = get_object_or_404(DashboardWidget, id=widget_id, user=request.user)
    
    if request.method == 'POST':
        widget.title = request.POST.get('title')
        widget.widget_type = request.POST.get('widget_type')
        widget.size = request.POST.get('size', 'medium')
        config = request.POST.get('config', '{}')
        widget.config = json.loads(config) if config else {}
        refresh_interval = request.POST.get('refresh_interval')
        widget.refresh_interval = int(refresh_interval) if refresh_interval else None
        widget.save()
        
        messages.success(request, f'Widget "{widget.title}" berhasil diupdate')
        return redirect('admin_panel:utilities:dashboard_widgets')
    
    context = {
        'page_title': 'Edit Dashboard Widget',
        'active_menu': 'utilities',
        'active_submenu': 'dashboard_widgets',
        'widget': widget,
        'config_json': json.dumps(widget.config, indent=2),
    }
    return render(request, 'admin_panel/utilities/dashboard_widget_form.html', context)


@login_required
@require_POST
def dashboard_widget_delete(request, widget_id):
    """Delete dashboard widget"""
    widget = get_object_or_404(DashboardWidget, id=widget_id, user=request.user)
    widget.delete()
    
    messages.success(request, 'Widget berhasil dihapus')
    return redirect('admin_panel:utilities:dashboard_widgets')


@login_required
@require_POST
def dashboard_widget_toggle(request, widget_id):
    """Toggle widget visibility"""
    widget = get_object_or_404(DashboardWidget, id=widget_id, user=request.user)
    widget.is_visible = not widget.is_visible
    widget.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'is_visible': widget.is_visible})
    
    return redirect('admin_panel:utilities:dashboard_widgets')


@login_required
@require_POST
def dashboard_widget_reorder(request):
    """Reorder widgets (AJAX)"""
    try:
        data = json.loads(request.body)
        widget_order = data.get('order', [])
        
        for index, widget_id in enumerate(widget_order):
            DashboardWidget.objects.filter(
                id=widget_id,
                user=request.user
            ).update(position=index)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ============================================================================
# QUICK ACCESS VIEWS
# ============================================================================

@login_required
def quick_access_list(request):
    """List dan manage quick access links"""
    links = QuickAccess.objects.filter(user=request.user).order_by('position')
    
    context = {
        'page_title': 'Quick Access',
        'active_menu': 'utilities',
        'active_submenu': 'quick_access',
        'links': links,
    }
    
    return render(request, 'admin_panel/utilities/quick_access_list.html', context)


@login_required
def quick_access_create(request):
    """Create new quick access link"""
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url')
        icon = request.POST.get('icon', 'fas fa-link')
        color = request.POST.get('color', 'primary')
        
        # Get max position
        max_pos = QuickAccess.objects.filter(user=request.user).count()
        
        link = QuickAccess.objects.create(
            user=request.user,
            title=title,
            url=url,
            icon=icon,
            color=color,
            position=max_pos,
        )
        
        messages.success(request, f'Quick access "{title}" berhasil ditambahkan')
        return redirect('admin_panel:utilities:quick_access')
    
    context = {
        'page_title': 'Create Quick Access',
        'active_menu': 'utilities',
        'active_submenu': 'quick_access',
    }
    return render(request, 'admin_panel/utilities/quick_access_form.html', context)


@login_required
def quick_access_edit(request, link_id):
    """Edit quick access link"""
    link = get_object_or_404(QuickAccess, id=link_id, user=request.user)
    
    if request.method == 'POST':
        link.title = request.POST.get('title')
        link.url = request.POST.get('url')
        link.icon = request.POST.get('icon', 'fas fa-link')
        link.color = request.POST.get('color', 'primary')
        link.save()
        
        messages.success(request, f'Quick access "{link.title}" berhasil diupdate')
        return redirect('admin_panel:utilities:quick_access')
    
    context = {
        'page_title': 'Edit Quick Access',
        'active_menu': 'utilities',
        'active_submenu': 'quick_access',
        'link': link,
    }
    return render(request, 'admin_panel/utilities/quick_access_form.html', context)


@login_required
@require_POST
def quick_access_delete(request, link_id):
    """Delete quick access link"""
    link = get_object_or_404(QuickAccess, id=link_id, user=request.user)
    link.delete()
    
    messages.success(request, 'Quick access berhasil dihapus')
    return redirect('admin_panel:utilities:quick_access')


@login_required
@require_POST
def quick_access_reorder(request):
    """Reorder quick access links (AJAX)"""
    try:
        data = json.loads(request.body)
        link_order = data.get('order', [])
        
        for index, link_id in enumerate(link_order):
            QuickAccess.objects.filter(
                id=link_id,
                user=request.user
            ).update(position=index)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def quick_access_track(request, link_id):
    """Track quick access usage"""
    link = get_object_or_404(QuickAccess, id=link_id, user=request.user)
    link.access_count += 1
    link.last_accessed = timezone.now()
    link.save()
    
    return JsonResponse({'success': True})


# ============================================================================
# SYSTEM MESSAGE VIEWS
# ============================================================================

@login_required
def system_message_list(request):
    """List semua system messages (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini')
        return redirect('admin_panel:dashboard')
    
    messages_list = SystemMessage.objects.all().order_by('-priority', '-start_date')
    
    # Filter by active status
    status = request.GET.get('status')
    if status == 'active':
        now = timezone.now()
        messages_list = messages_list.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )
    elif status == 'inactive':
        messages_list = messages_list.filter(is_active=False)
    elif status == 'expired':
        messages_list = messages_list.filter(
            end_date__lt=timezone.now()
        )
    
    # Filter by type
    msg_type = request.GET.get('type')
    if msg_type:
        messages_list = messages_list.filter(type=msg_type)
    
    # Pagination
    paginator = Paginator(messages_list, 20)
    page = request.GET.get('page', 1)
    messages_page = paginator.get_page(page)
    
    context = {
        'page_title': 'System Messages',
        'active_menu': 'utilities',
        'active_submenu': 'system_messages',
        'messages': messages_page,
        'current_filters': {
            'status': status,
            'type': msg_type,
        }
    }
    
    return render(request, 'admin_panel/utilities/system_message_list.html', context)


@login_required
def system_message_create(request):
    """Create new system message"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini')
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        msg_type = request.POST.get('type', 'info')
        display_location = request.POST.get('display_location', 'dashboard')
        priority = request.POST.get('priority', 1)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_dismissible = request.POST.get('is_dismissible') == 'on'
        
        system_message = SystemMessage.objects.create(
            title=title,
            message=message,
            type=msg_type,
            display_location=display_location,
            priority=int(priority),
            start_date=start_date,
            end_date=end_date or None,
            is_dismissible=is_dismissible,
            created_by=request.user,
        )
        
        messages.success(request, f'System message "{title}" berhasil dibuat')
        return redirect('admin_panel:utilities:system_messages')
    
    context = {
        'page_title': 'Create System Message',
        'active_menu': 'utilities',
        'active_submenu': 'system_messages',
    }
    return render(request, 'admin_panel/utilities/system_message_form.html', context)


@login_required
def system_message_edit(request, message_id):
    """Edit system message"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini')
        return redirect('admin_panel:dashboard')
    
    system_message = get_object_or_404(SystemMessage, id=message_id)
    
    if request.method == 'POST':
        system_message.title = request.POST.get('title')
        system_message.message = request.POST.get('message')
        system_message.type = request.POST.get('type', 'info')
        system_message.display_location = request.POST.get('display_location', 'dashboard')
        system_message.priority = int(request.POST.get('priority', 1))
        system_message.start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        system_message.end_date = end_date or None
        system_message.is_dismissible = request.POST.get('is_dismissible') == 'on'
        system_message.save()
        
        messages.success(request, f'System message "{system_message.title}" berhasil diupdate')
        return redirect('admin_panel:utilities:system_messages')
    
    context = {
        'page_title': 'Edit System Message',
        'active_menu': 'utilities',
        'active_submenu': 'system_messages',
        'system_message': system_message,
    }
    return render(request, 'admin_panel/utilities/system_message_form.html', context)


@login_required
@require_POST
def system_message_delete(request, message_id):
    """Delete system message"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    system_message = get_object_or_404(SystemMessage, id=message_id)
    system_message.delete()
    
    messages.success(request, 'System message berhasil dihapus')
    return redirect('admin_panel:utilities:system_messages')


@login_required
@require_POST
def system_message_toggle(request, message_id):
    """Toggle system message active status"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    system_message = get_object_or_404(SystemMessage, id=message_id)
    system_message.is_active = not system_message.is_active
    system_message.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'is_active': system_message.is_active})
    
    return redirect('admin_panel:utilities:system_messages')


# ============================================================================
# DATA EXPORT HISTORY VIEWS
# ============================================================================

@login_required
def export_history_list(request):
    """List semua export history"""
    exports = DataExportHistory.objects.select_related('user').all()
    
    # Filter by user
    user_id = request.GET.get('user')
    if user_id:
        exports = exports.filter(user_id=user_id)
    
    # Filter by module
    module = request.GET.get('module')
    if module:
        exports = exports.filter(module=module)
    
    # Filter by format
    export_format = request.GET.get('format')
    if export_format:
        exports = exports.filter(export_format=export_format)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'success':
        exports = exports.filter(is_successful=True)
    elif status == 'failed':
        exports = exports.filter(is_successful=False)
    
    # Statistics
    stats = {
        'total': exports.count(),
        'success': exports.filter(is_successful=True).count(),
        'failed': exports.filter(is_successful=False).count(),
        'by_format': exports.values('export_format').annotate(count=Count('id')),
        'by_module': exports.values('module').annotate(count=Count('id')).order_by('-count')[:5],
    }
    
    # Get unique values for filters
    users = CustomUser.objects.filter(id__in=exports.values_list('user_id', flat=True).distinct())
    modules = exports.values_list('module', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(exports, 30)
    page = request.GET.get('page', 1)
    exports_page = paginator.get_page(page)
    
    context = {
        'page_title': 'Export History',
        'active_menu': 'utilities',
        'active_submenu': 'export_history',
        'exports': exports_page,
        'stats': stats,
        'users': users,
        'modules': sorted(set(modules)),
        'current_filters': {
            'user': user_id,
            'module': module,
            'format': export_format,
            'status': status,
        }
    }
    
    return render(request, 'admin_panel/utilities/export_history_list.html', context)


@login_required
def export_history_detail(request, export_id):
    """Detail dari satu export history"""
    export = get_object_or_404(DataExportHistory, id=export_id)
    
    context = {
        'page_title': 'Export History Detail',
        'active_menu': 'utilities',
        'active_submenu': 'export_history',
        'export': export,
    }
    
    return render(request, 'admin_panel/utilities/export_history_detail.html', context)


@login_required
def export_history_download(request, export_id):
    """Download exported file"""
    export = get_object_or_404(DataExportHistory, id=export_id)
    
    if not export.file_path or not os.path.exists(export.file_path):
        messages.error(request, 'File tidak ditemukan')
        return redirect('admin_panel:utilities:export_history')
    
    return FileResponse(
        open(export.file_path, 'rb'),
        as_attachment=True,
        filename=export.file_name
    )


@login_required
@require_POST
def export_history_delete(request, export_id):
    """Delete export history dan file nya"""
    export = get_object_or_404(DataExportHistory, id=export_id)
    
    # Delete file if exists
    if export.file_path and os.path.exists(export.file_path):
        try:
            os.remove(export.file_path)
        except:
            pass
    
    export.delete()
    
    messages.success(request, 'Export history berhasil dihapus')
    return redirect('admin_panel:utilities:export_history')


# ============================================================================
# ADMIN PREFERENCE VIEWS
# ============================================================================

@login_required
def admin_preference_view(request):
    """View dan edit admin preferences"""
    preference, created = AdminPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preference.theme = request.POST.get('theme', 'light')
        preference.sidebar_state = request.POST.get('sidebar_state', 'expanded')
        preference.items_per_page = int(request.POST.get('items_per_page', 25))
        preference.notification_sound = request.POST.get('notification_sound') == 'on'
        preference.notification_desktop = request.POST.get('notification_desktop') == 'on'
        preference.notification_email = request.POST.get('notification_email') == 'on'
        preference.default_dashboard_view = request.POST.get('default_dashboard_view', 'overview')
        
        # Custom settings (JSON)
        try:
            custom_settings = request.POST.get('custom_settings', '{}')
            preference.custom_settings = json.loads(custom_settings) if custom_settings else {}
        except:
            pass
        
        preference.save()
        
        messages.success(request, 'Preferensi berhasil disimpan')
        return redirect('admin_panel:utilities:preferences')
    
    context = {
        'page_title': 'Admin Preferences',
        'active_menu': 'utilities',
        'active_submenu': 'preferences',
        'preference': preference,
        'custom_settings_json': json.dumps(preference.custom_settings, indent=2),
    }
    
    return render(request, 'admin_panel/utilities/admin_preference.html', context)


@login_required
@require_POST
def admin_preference_reset(request):
    """Reset preferences to default"""
    try:
        preference = AdminPreference.objects.get(user=request.user)
        preference.delete()
    except AdminPreference.DoesNotExist:
        pass
    
    messages.success(request, 'Preferensi berhasil direset ke default')
    return redirect('admin_panel:utilities:preferences')


@login_required
def admin_preference_api(request):
    """API untuk get user preferences (AJAX)"""
    try:
        preference = AdminPreference.objects.get(user=request.user)
        data = {
            'theme': preference.theme,
            'sidebar_state': preference.sidebar_state,
            'items_per_page': preference.items_per_page,
            'notification_sound': preference.notification_sound,
            'notification_desktop': preference.notification_desktop,
            'notification_email': preference.notification_email,
            'default_dashboard_view': preference.default_dashboard_view,
            'custom_settings': preference.custom_settings,
        }
    except AdminPreference.DoesNotExist:
        data = {
            'theme': 'light',
            'sidebar_state': 'expanded',
            'items_per_page': 25,
            'notification_sound': True,
            'notification_desktop': True,
            'notification_email': False,
            'default_dashboard_view': 'overview',
            'custom_settings': {},
        }
    
    return JsonResponse(data)

