"""
URL Configuration untuk Admin Panel Utilities
"""

from django.urls import path
from . import utility_views

app_name = 'utilities'

urlpatterns = [
    # ============================================================================
    # ADMIN ACTIVITY LOG URLs
    # ============================================================================
    path('activity-logs/', utility_views.activity_log_list, name='activity_logs'),
    path('activity-logs/<int:log_id>/', utility_views.activity_log_detail, name='activity_log_detail'),
    path('activity-logs/<int:log_id>/delete/', utility_views.activity_log_delete, name='activity_log_delete'),
    path('activity-logs/export/', utility_views.activity_log_export, name='activity_log_export'),
    
    # ============================================================================
    # ADMIN NOTIFICATION URLs
    # ============================================================================
    path('notifications/', utility_views.notification_list, name='notifications'),
    path('notifications/create/', utility_views.notification_create, name='notification_create'),
    path('notifications/<int:notification_id>/mark-read/', utility_views.notification_mark_read, name='notification_mark_read'),
    path('notifications/mark-all-read/', utility_views.notification_mark_all_read, name='notification_mark_all_read'),
    path('notifications/<int:notification_id>/delete/', utility_views.notification_delete, name='notification_delete'),
    path('notifications/api/center/', utility_views.notification_center_api, name='notification_center_api'),
    
    # ============================================================================
    # DASHBOARD WIDGET URLs
    # ============================================================================
    path('dashboard-widgets/', utility_views.dashboard_widget_list, name='dashboard_widgets'),
    path('dashboard-widgets/create/', utility_views.dashboard_widget_create, name='dashboard_widget_create'),
    path('dashboard-widgets/<int:widget_id>/edit/', utility_views.dashboard_widget_edit, name='dashboard_widget_edit'),
    path('dashboard-widgets/<int:widget_id>/delete/', utility_views.dashboard_widget_delete, name='dashboard_widget_delete'),
    path('dashboard-widgets/<int:widget_id>/toggle/', utility_views.dashboard_widget_toggle, name='dashboard_widget_toggle'),
    path('dashboard-widgets/reorder/', utility_views.dashboard_widget_reorder, name='dashboard_widget_reorder'),
    
    # ============================================================================
    # QUICK ACCESS URLs
    # ============================================================================
    path('quick-access/', utility_views.quick_access_list, name='quick_access'),
    path('quick-access/create/', utility_views.quick_access_create, name='quick_access_create'),
    path('quick-access/<int:link_id>/edit/', utility_views.quick_access_edit, name='quick_access_edit'),
    path('quick-access/<int:link_id>/delete/', utility_views.quick_access_delete, name='quick_access_delete'),
    path('quick-access/reorder/', utility_views.quick_access_reorder, name='quick_access_reorder'),
    path('quick-access/<int:link_id>/track/', utility_views.quick_access_track, name='quick_access_track'),
    
    # ============================================================================
    # SYSTEM MESSAGE URLs
    # ============================================================================
    path('system-messages/', utility_views.system_message_list, name='system_messages'),
    path('system-messages/create/', utility_views.system_message_create, name='system_message_create'),
    path('system-messages/<int:message_id>/edit/', utility_views.system_message_edit, name='system_message_edit'),
    path('system-messages/<int:message_id>/delete/', utility_views.system_message_delete, name='system_message_delete'),
    path('system-messages/<int:message_id>/toggle/', utility_views.system_message_toggle, name='system_message_toggle'),
    
    # ============================================================================
    # DATA EXPORT HISTORY URLs
    # ============================================================================
    path('export-history/', utility_views.export_history_list, name='export_history'),
    path('export-history/<int:export_id>/', utility_views.export_history_detail, name='export_history_detail'),
    path('export-history/<int:export_id>/download/', utility_views.export_history_download, name='export_history_download'),
    path('export-history/<int:export_id>/delete/', utility_views.export_history_delete, name='export_history_delete'),
    
    # ============================================================================
    # ADMIN PREFERENCE URLs
    # ============================================================================
    path('preferences/', utility_views.admin_preference_view, name='preferences'),
    path('preferences/reset/', utility_views.admin_preference_reset, name='preference_reset'),
    path('preferences/api/', utility_views.admin_preference_api, name='preference_api'),
]

