"""
Admin registration for Admin Panel models
"""

from django.contrib import admin
from .models import (
    AdminActivityLog,
    AdminNotification,
    DashboardWidget,
    QuickAccess,
    SystemMessage,
    DataExportHistory,
    AdminPreference
)


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'module', 'description', 'created_at']
    list_filter = ['action', 'module', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'action', 'module', 'description', 'ip_address', 
                      'user_agent', 'old_value', 'new_value', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'type', 'priority', 'is_read', 'created_at']
    list_filter = ['type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('recipient', 'title', 'message', 'type', 'priority')
        }),
        ('Aksi', {
            'fields': ('action_url', 'action_text')
        }),
        ('Status', {
            'fields': ('is_read', 'is_archived', 'read_at', 'expires_at')
        }),
    )


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'widget_type', 'size', 'position', 'is_visible']
    list_filter = ['widget_type', 'size', 'is_visible']
    search_fields = ['title', 'user__username']
    ordering = ['position', 'title']


@admin.register(QuickAccess)
class QuickAccessAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'url', 'position', 'access_count', 'last_accessed']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'user__username', 'url']
    ordering = ['position']


@admin.register(SystemMessage)
class SystemMessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'message_type', 'display_location', 'is_active', 
                   'start_date', 'end_date', 'priority']
    list_filter = ['message_type', 'display_location', 'is_active', 'start_date']
    search_fields = ['title', 'message']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Konten Pesan', {
            'fields': ('title', 'message', 'message_type')
        }),
        ('Tampilan', {
            'fields': ('display_location', 'is_dismissible', 'priority')
        }),
        ('Jadwal', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )


@admin.register(DataExportHistory)
class DataExportHistoryAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'user', 'module', 'export_format', 'record_count', 
                   'file_size_mb', 'is_successful', 'created_at']
    list_filter = ['module', 'export_format', 'is_successful', 'created_at']
    search_fields = ['file_name', 'user__username']
    readonly_fields = ['user', 'module', 'export_format', 'file_name', 'file_size', 
                      'record_count', 'filters', 'is_successful', 'error_message', 
                      'ip_address', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AdminPreference)
class AdminPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'sidebar_state', 'items_per_page', 'updated_at']
    list_filter = ['theme', 'sidebar_state']
    search_fields = ['user__username']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Preferensi UI', {
            'fields': ('theme', 'sidebar_state', 'items_per_page')
        }),
        ('Preferensi Dashboard', {
            'fields': ('default_dashboard', 'show_welcome_message')
        }),
        ('Preferensi Notifikasi', {
            'fields': ('email_notifications', 'browser_notifications', 'sound_notifications')
        }),
        ('Custom Settings', {
            'fields': ('custom_settings',),
            'classes': ('collapse',)
        }),
    )
