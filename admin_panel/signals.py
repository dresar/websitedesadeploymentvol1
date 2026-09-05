"""
Signals untuk auto-create notifications
Trigger notifications berdasarkan events tertentu
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .utils import create_notification, notify_admins, create_activity_log

User = get_user_model()


# ============================================================================
# COMPLAINT NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender='complaints.Complaint')
def complaint_notification(sender, instance, created, **kwargs):
    """
    Trigger notification saat ada complaint baru atau status berubah
    """
    if created:
        # New complaint
        notify_admins(
            title='Keluhan Baru Diterima',
            message=f'Keluhan baru dari {instance.reporter_name or "Anonim"}: {instance.title}',
            notification_type='info',
            priority='medium'
        )
        
        # Also notify complaint handlers (if any role exists)
        handlers = User.objects.filter(is_staff=True, roles__name__in=['complaint_manager', 'admin', 'super_admin'])
        for handler in handlers:
            create_notification(
                title='Keluhan Baru Perlu Ditindaklanjuti',
                message=f'Keluhan: {instance.title}',
                recipient=handler,
                notification_type='warning',
                priority='high',
                action_url=f'/admin-panel/complaints/{instance.id}/',
                action_text='Lihat Keluhan'
            )
    else:
        # Status changed
        if instance.status == 'resolved':
            if instance.reporter_email:
                # Notify complaint sender (if possible via email)
                pass
            
            # Notify admin that complaint is resolved
            notify_admins(
                title='Keluhan Terselesaikan',
                message=f'Keluhan "{instance.title}" telah diselesaikan',
                notification_type='success',
                priority='low'
            )


# ============================================================================
# DATA IMPORT/EXPORT NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender='admin_panel.DataExportHistory')
def export_notification(sender, instance, created, **kwargs):
    """
    Notify user when export is completed
    """
    if created and instance.is_successful:
        create_notification(
            title='Export Data Selesai',
            message=f'Export {instance.get_module_display()} ({instance.record_count} records) ke {instance.export_format.upper()} telah selesai',
            recipient=instance.user,
            notification_type='success',
            priority='low',
            action_url=f'/admin-panel/utilities/export-history/{instance.id}/',
            action_text='Download File'
        )


# ============================================================================
# USER/ROLE NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender=User)
def user_creation_notification(sender, instance, created, **kwargs):
    """
    Notify when new user is created or role changed
    """
    if created and instance.is_staff:
        # Welcome notification for new admin
        create_notification(
            title='Selamat Datang di Admin Panel',
            message=f'Akun Anda telah dibuat. Silakan lengkapi profil Anda untuk memulai.',
            recipient=instance,
            notification_type='info',
            priority='medium',
            action_url='/admin-panel/profile/',
            action_text='Lengkapi Profil'
        )
        
        # Notify super admins
        super_admins = User.objects.filter(is_superuser=True).exclude(id=instance.id)
        for admin in super_admins:
            create_notification(
                title='User Baru Ditambahkan',
                message=f'User baru: {instance.get_full_name() or instance.username}',
                recipient=admin,
                notification_type='info',
                priority='low'
            )


# ============================================================================
# SYSTEM NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender='admin_panel.SystemMessage')
def system_message_broadcast(sender, instance, created, **kwargs):
    """
    Notify all admins when new system message is created
    """
    if created and instance.is_active:
        # Don't create notification for system message (they will see it on page)
        # But log the activity
        pass


# ============================================================================
# APPROVAL/VERIFICATION NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender='beneficiaries.Beneficiary')
def beneficiary_notification(sender, instance, created, **kwargs):
    """
    Notify when beneficiary needs approval or is approved
    """
    if created:
        # New beneficiary needs approval
        approvers = User.objects.filter(is_staff=True, roles__name__in=['beneficiary_manager', 'admin', 'super_admin'])
        for approver in approvers:
            create_notification(
                title='Penerima Bantuan Baru Perlu Diverifikasi',
                message=f'{instance.person.name} - {instance.category.name}',
                recipient=approver,
                notification_type='warning',
                priority='high',
                action_url=f'/admin-panel/beneficiaries/{instance.id}/',
                action_text='Verifikasi'
            )
    elif hasattr(instance, '_status_changed'):
        # Status changed (you need to add this tracking in model)
        if instance.status == 'approved':
            notify_admins(
                title='Penerima Bantuan Disetujui',
                message=f'{instance.name} telah disetujui untuk program {instance.program_name}',
                notification_type='success',
                priority='low'
            )


# ============================================================================
# DOCUMENT NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender='documents.Document')
def document_notification(sender, instance, created, **kwargs):
    """
    Notify when new document needs approval
    """
    # Check if document is in review status (needs approval)
    if created and instance.status == 'review':
        approvers = User.objects.filter(is_staff=True, is_superuser=True)
        for approver in approvers:
            create_notification(
                title='Dokumen Baru Perlu Persetujuan',
                message=f'{instance.title} - {instance.category.name if instance.category else "Dokumen"}',
                recipient=approver,
                notification_type='warning',
                priority='medium',
                action_url=f'/admin-panel/documents/{instance.id}/',
                action_text='Review Dokumen'
            )


# ============================================================================
# NEWS NOTIFICATIONS
# ============================================================================

@receiver(post_save, sender='news.News')
def news_published_notification(sender, instance, created, **kwargs):
    """
    Notify when news is published
    """
    if not created and instance.is_published() and instance.published_date:
        # News just published
        notify_admins(
            title='Berita Baru Dipublikasikan',
            message=f'{instance.title}',
            notification_type='success',
            priority='low',
            action_url=f'/news/{instance.slug}/',
            action_text='Lihat Berita'
        )

