# Tambahan model untuk sistem surat yang lebih canggih

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils import timezone

User = get_user_model()

# Import Penduduk from references app
try:
    from references.models import Penduduk
except ImportError:
    Penduduk = None

# Import LetterType from main models
try:
    from .models import LetterType, Letter
except ImportError:
    LetterType = None
    Letter = None

class LetterRequest(models.Model):
    """Model untuk permintaan surat dari penduduk"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Verifikasi'),
        ('verified', 'Terverifikasi'),
        ('in_progress', 'Sedang Diproses'),
        ('completed', 'Selesai'),
        ('rejected', 'Ditolak'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Rendah'),
        ('normal', 'Normal'),
        ('high', 'Tinggi'),
        ('urgent', 'Mendesak'),
    ]
    
    # Informasi dasar
    request_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name='Nomor Permintaan'
    )
    letter_type = models.ForeignKey(
        LetterType,
        on_delete=models.CASCADE,
        verbose_name='Jenis Surat'
    )
    applicant = models.ForeignKey(
        Penduduk,
        on_delete=models.CASCADE,
        verbose_name='Pemohon'
    )
    
    # Detail permintaan
    purpose = models.TextField(
        verbose_name='Tujuan Penggunaan',
        help_text='Jelaskan untuk apa surat ini digunakan'
    )
    detailed_purpose = models.TextField(
        blank=True,
        verbose_name='Detail Tujuan',
        help_text='Penjelasan lebih detail tentang penggunaan surat'
    )
    urgency_reason = models.TextField(
        blank=True,
        verbose_name='Alasan Urgensi',
        help_text='Jika mendesak, jelaskan alasannya'
    )
    
    # Status dan prioritas
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name='Prioritas'
    )
    
    # Verifikasi
    verification_notes = models.TextField(
        blank=True,
        verbose_name='Catatan Verifikasi'
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='verified_requests',
        verbose_name='Diverifikasi Oleh'
    )
    verification_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tanggal Verifikasi'
    )
    
    # Penolakan
    rejection_reason = models.TextField(
        blank=True,
        verbose_name='Alasan Penolakan'
    )
    rejected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='rejected_requests',
        verbose_name='Ditolak Oleh'
    )
    rejection_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tanggal Penolakan'
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tanggal Pengajuan'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Tanggal Update'
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tanggal Selesai'
    )
    
    # Link ke surat yang dihasilkan
    generated_letter = models.OneToOneField(
        'Letter',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='source_request',
        verbose_name='Surat yang Dihasilkan'
    )
    
    class Meta:
        verbose_name = 'Permintaan Surat'
        verbose_name_plural = 'Permintaan Surat'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.request_number} - {self.applicant.nama} ({self.letter_type.name})"
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = self.generate_request_number()
        super().save(*args, **kwargs)
    
    def generate_request_number(self):
        """Generate unique request number"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"REQ/{timestamp}{random_suffix}"


class SupportingDocument(models.Model):
    """Model untuk dokumen pendukung"""
    DOCUMENT_TYPES = [
        ('ktp', 'KTP'),
        ('kk', 'Kartu Keluarga'),
        ('akte', 'Akte Kelahiran'),
        ('ijazah', 'Ijazah'),
        ('surat_keterangan', 'Surat Keterangan'),
        ('foto', 'Foto'),
        ('other', 'Lainnya'),
    ]
    
    request = models.ForeignKey(
        LetterRequest,
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        verbose_name='Permintaan Surat'
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        verbose_name='Jenis Dokumen'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Judul Dokumen'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Deskripsi'
    )
    file = models.FileField(
        upload_to='supporting_documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])],
        verbose_name='File Dokumen'
    )
    file_size = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Ukuran File (bytes)'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tanggal Upload'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Diupload Oleh'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Terverifikasi'
    )
    verification_notes = models.TextField(
        blank=True,
        verbose_name='Catatan Verifikasi'
    )
    
    class Meta:
        verbose_name = 'Dokumen Pendukung'
        verbose_name_plural = 'Dokumen Pendukung'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.request.applicant.nama}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


# LetterTemplate sudah ada di models.py utama


class LetterWorkflow(models.Model):
    """Model untuk workflow surat"""
    name = models.CharField(
        max_length=200,
        verbose_name='Nama Workflow'
    )
    letter_type = models.ForeignKey(
        LetterType,
        on_delete=models.CASCADE,
        related_name='workflows',
        verbose_name='Jenis Surat'
    )
    steps = models.JSONField(
        default=list,
        verbose_name='Langkah-langkah',
        help_text='Daftar langkah dalam workflow'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktif'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tanggal Dibuat'
    )
    
    class Meta:
        verbose_name = 'Workflow Surat'
        verbose_name_plural = 'Workflow Surat'
        ordering = ['letter_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.letter_type.name})"


class LetterApproval(models.Model):
    """Model untuk persetujuan surat"""
    APPROVAL_TYPES = [
        ('auto', 'Otomatis'),
        ('manual', 'Manual'),
        ('committee', 'Komite'),
    ]
    
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name='approvals',
        verbose_name='Surat'
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Penyetuju'
    )
    approval_type = models.CharField(
        max_length=20,
        choices=APPROVAL_TYPES,
        default='manual',
        verbose_name='Tipe Persetujuan'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Disetujui'
    )
    approval_notes = models.TextField(
        blank=True,
        verbose_name='Catatan Persetujuan'
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tanggal Persetujuan'
    )
    
    class Meta:
        verbose_name = 'Persetujuan Surat'
        verbose_name_plural = 'Persetujuan Surat'
        ordering = ['-approved_at']
        unique_together = ['letter', 'approver']
    
    def __str__(self):
        return f"{self.letter.letter_number} - {self.approver.get_full_name()}"


class LetterNotification(models.Model):
    """Model untuk notifikasi surat"""
    NOTIFICATION_TYPES = [
        ('status_change', 'Perubahan Status'),
        ('approval_needed', 'Perlu Persetujuan'),
        ('document_uploaded', 'Dokumen Diupload'),
        ('deadline_reminder', 'Pengingat Deadline'),
        ('completion', 'Surat Selesai'),
    ]
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Penerima'
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Surat'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='Tipe Notifikasi'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Judul'
    )
    message = models.TextField(
        verbose_name='Pesan'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Sudah Dibaca'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tanggal Dibuat'
    )
    read_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Tanggal Dibaca'
    )
    
    class Meta:
        verbose_name = 'Notifikasi Surat'
        verbose_name_plural = 'Notifikasi Surat'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"
