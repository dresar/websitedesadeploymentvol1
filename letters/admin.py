from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    LetterType, Letter, LetterRecipient, LetterAttachment, 
    LetterTracking, LetterSettings, LetterTemplate
)

# Minimal admin configuration - focus on custom admin panel
# Django admin is kept for emergency access only

@admin.register(LetterType)
class LetterTypeAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'code', 'is_active', 'processing_time_days', 'fee_amount')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)

@admin.register(Letter)
class LetterAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'notes')
    list_display = ('letter_number', 'subject', 'applicant', 'letter_type', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'letter_type', 'created_at')
    search_fields = ('letter_number', 'subject', 'applicant__nama', 'applicant__nik')
    ordering = ('-created_at',)
    readonly_fields = ('letter_number', 'created_at', 'updated_at')

@admin.register(LetterTemplate)
class LetterTemplateAdmin(SummernoteModelAdmin):
    summernote_fields = ('content_template', 'header_template', 'footer_template')
    list_display = ('name', 'template_type', 'is_default', 'is_active', 'usage_count')
    list_filter = ('template_type', 'is_default', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-is_default', '-usage_count', 'name')

@admin.register(LetterSettings)
class LetterSettingsAdmin(admin.ModelAdmin):
    list_display = ('village_name', 'head_of_village_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('village_name', 'head_of_village_name')

@admin.register(LetterRecipient)
class LetterRecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipient_type', 'organization', 'is_primary', 'letter')
    list_filter = ('recipient_type', 'is_primary', 'delivery_method')
    search_fields = ('name', 'organization', 'letter__subject')

@admin.register(LetterAttachment)
class LetterAttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'attachment_type', 'letter', 'is_required', 'uploaded_at')
    list_filter = ('attachment_type', 'is_required', 'uploaded_at')
    search_fields = ('title', 'letter__subject')

@admin.register(LetterTracking)
class LetterTrackingAdmin(admin.ModelAdmin):
    list_display = ('letter', 'action', 'performed_by', 'performed_at', 'location')
    list_filter = ('action', 'performed_at', 'location')
    search_fields = ('letter__subject', 'description', 'performed_by__username')
    readonly_fields = ('performed_at',)

# Note: All letter models are managed through custom admin panel
# Django admin is kept minimal for emergency access only