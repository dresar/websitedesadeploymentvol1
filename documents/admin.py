from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Document, DocumentCategory, DocumentComment, DocumentDownloadLog


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(SummernoteModelAdmin):
    """Admin untuk Kategori Dokumen"""
    summernote_fields = ('description',)
    list_display = ['name', 'category_type', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active', 'category_type']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']


@admin.register(Document)
class DocumentAdmin(SummernoteModelAdmin):
    """Admin untuk Dokumen"""
    summernote_fields = ('description', 'summary')
    list_display = ['title', 'document_number', 'category', 'document_year', 'status', 'is_public', 'download_count', 'created_at']
    list_filter = ['status', 'is_public', 'is_featured', 'document_year', 'category']
    search_fields = ['title', 'document_number', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['download_count', 'view_count', 'created_at', 'updated_at', 'published_at']
    date_hierarchy = 'created_at'
    ordering = ['-document_year', '-created_at']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'slug', 'category', 'document_number', 'document_year')
        }),
        ('Konten', {
            'fields': ('description', 'summary', 'tags')
        }),
        ('File', {
            'fields': ('file', 'thumbnail')
        }),
        ('Status & Publikasi', {
            'fields': ('status', 'is_public', 'is_featured', 'uploaded_by')
        }),
        ('Statistik', {
            'fields': ('download_count', 'view_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DocumentComment)
class DocumentCommentAdmin(admin.ModelAdmin):
    """Admin untuk Komentar Dokumen"""
    list_display = ['document', 'name', 'email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} komentar berhasil disetujui.')
    approve_comments.short_description = 'Setujui komentar terpilih'
    
    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} komentar berhasil ditolak.')
    unapprove_comments.short_description = 'Tolak komentar terpilih'


@admin.register(DocumentDownloadLog)
class DocumentDownloadLogAdmin(admin.ModelAdmin):
    """Admin untuk Log Download"""
    list_display = ['document', 'ip_address', 'downloaded_at']
    list_filter = ['downloaded_at']
    search_fields = ['document__title', 'ip_address']
    readonly_fields = ['document', 'ip_address', 'user_agent', 'downloaded_at']
    ordering = ['-downloaded_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
