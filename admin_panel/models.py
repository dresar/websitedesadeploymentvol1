"""
Admin Panel Utility Models
Models untuk membantu management, tracking, dan monitoring admin panel
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class AdminActivityLog(models.Model):
    """
    Model untuk tracking semua aktivitas admin
    Mencatat siapa, kapan, apa yang dilakukan
    """
    ACTION_CHOICES = [
        ('create', 'Tambah Data'),
        ('update', 'Ubah Data'),
        ('delete', 'Hapus Data'),
        ('view', 'Lihat Data'),
        ('export', 'Export Data'),
        ('import', 'Import Data'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('publish', 'Publish'),
        ('unpublish', 'Unpublish'),
        ('other', 'Lainnya'),
    ]
    
    MODULE_CHOICES = [
        ('dashboard', 'Dashboard'),
        ('references', 'Data Referensi'),
        ('beneficiaries', 'Penerima Bantuan'),
        ('business', 'Usaha'),
        ('complaints', 'Keluhan'),
        ('documents', 'Dokumen'),
        ('tourism', 'Wisata'),
        ('posyandu', 'Posyandu'),
        ('news', 'Berita'),
        ('village_profile', 'Profil Desa'),
        ('organization', 'Organisasi'),
        ('layanan', 'Layanan'),
        ('settings', 'Pengaturan'),
        ('users', 'Pengguna'),
        ('system', 'Sistem'),
    ]
    
    # User yang melakukan aktivitas
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="User"
    )
    
    # Detail aktivitas
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Aksi")
    module = models.CharField(max_length=50, choices=MODULE_CHOICES, verbose_name="Modul")
    description = models.TextField(verbose_name="Deskripsi")
    
    # Generic foreign key untuk referensi object yang dimodifikasi
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_repr = models.CharField(max_length=255, blank=True, null=True, verbose_name="Representasi Objek")
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    
    # Data sebelum dan sesudah (untuk audit)
    old_value = models.JSONField(null=True, blank=True, verbose_name="Data Lama")
    new_value = models.JSONField(null=True, blank=True, verbose_name="Data Baru")
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu")
    
    class Meta:
        verbose_name = "Log Aktivitas Admin"
        verbose_name_plural = "Log Aktivitas Admin"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['module', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.get_module_display()}"
    
    @property
    def duration_ago(self):
        """Berapa lama yang lalu aktivitas ini dilakukan"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} hari yang lalu"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600} jam yang lalu"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60} menit yang lalu"
        else:
            return "Baru saja"


class AdminNotification(models.Model):
    """
    Notifikasi khusus untuk admin
    Bisa berupa reminder, warning, atau info penting
    """
    TYPE_CHOICES = [
        ('info', 'Informasi'),
        ('warning', 'Peringatan'),
        ('success', 'Sukses'),
        ('danger', 'Bahaya'),
        ('reminder', 'Pengingat'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('urgent', 'Mendesak'),
    ]
    
    # Target notifikasi
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_notifications',
        null=True,
        blank=True,
        verbose_name="Penerima",
        help_text="Kosongkan untuk broadcast ke semua admin"
    )
    
    # Content notifikasi
    title = models.CharField(max_length=200, verbose_name="Judul")
    message = models.TextField(verbose_name="Pesan")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info', verbose_name="Tipe")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioritas")
    
    # Link terkait (optional)
    action_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="Link Aksi")
    action_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Text Tombol")
    
    # Status
    is_read = models.BooleanField(default=False, verbose_name="Sudah Dibaca")
    is_archived = models.BooleanField(default=False, verbose_name="Diarsipkan")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Dibaca Pada")
    
    # Auto-expire
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Kadaluarsa",
                                     help_text="Notifikasi akan otomatis hilang setelah tanggal ini")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diupdate")
    
    class Meta:
        verbose_name = "Notifikasi Admin"
        verbose_name_plural = "Notifikasi Admin"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient or 'Broadcast'}"
    
    def mark_as_read(self):
        """Mark notifikasi sebagai sudah dibaca"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @property
    def is_expired(self):
        """Check apakah notifikasi sudah expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def get_icon(self):
        """Get icon berdasarkan type"""
        icons = {
            'info': 'fa-info-circle',
            'warning': 'fa-exclamation-triangle',
            'success': 'fa-check-circle',
            'danger': 'fa-times-circle',
            'reminder': 'fa-clock',
        }
        return icons.get(self.type, 'fa-info-circle')
    
    def get_badge_class(self):
        """Get badge class berdasarkan type"""
        return f'badge-type-{self.type}'


class DashboardWidget(models.Model):
    """
    Widget yang bisa ditampilkan di dashboard admin
    Customizable per user
    """
    WIDGET_TYPES = [
        ('stats', 'Statistik'),
        ('chart', 'Grafik'),
        ('table', 'Tabel Data'),
        ('list', 'Daftar'),
        ('calendar', 'Kalender'),
        ('quick_actions', 'Aksi Cepat'),
        ('recent_activity', 'Aktivitas Terbaru'),
        ('alerts', 'Peringatan'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Kecil (1/4)'),
        ('medium', 'Sedang (1/2)'),
        ('large', 'Besar (3/4)'),
        ('full', 'Penuh (1/1)'),
    ]
    
    # Owner widget
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dashboard_widgets',
        null=True,
        blank=True,
        verbose_name="User",
        help_text="Kosongkan untuk widget default semua user"
    )
    
    # Widget info
    title = models.CharField(max_length=100, verbose_name="Judul Widget")
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPES, verbose_name="Tipe Widget")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='medium', verbose_name="Ukuran")
    
    # Configuration (JSON untuk flexibility)
    config = models.JSONField(default=dict, blank=True, verbose_name="Konfigurasi",
                              help_text="Konfigurasi widget dalam format JSON")
    
    # Display settings
    position = models.PositiveIntegerField(default=0, verbose_name="Posisi",
                                          help_text="Urutan tampil widget")
    is_visible = models.BooleanField(default=True, verbose_name="Tampilkan")
    is_collapsible = models.BooleanField(default=True, verbose_name="Bisa Dilipat")
    is_collapsed = models.BooleanField(default=False, verbose_name="Dilipat Default")
    
    # Refresh settings
    auto_refresh = models.BooleanField(default=False, verbose_name="Auto Refresh")
    refresh_interval = models.PositiveIntegerField(default=300, verbose_name="Interval Refresh (detik)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diupdate")
    
    class Meta:
        verbose_name = "Widget Dashboard"
        verbose_name_plural = "Widget Dashboard"
        ordering = ['position', 'title']
        unique_together = ['user', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.user or 'Default'}"
    
    def get_widget_icon(self):
        """Get icon berdasarkan widget type"""
        icons = {
            'stats': 'fa-chart-bar',
            'chart': 'fa-chart-line',
            'table': 'fa-table',
            'list': 'fa-list',
            'calendar': 'fa-calendar',
            'quick_actions': 'fa-bolt',
            'recent_activity': 'fa-clock',
            'alerts': 'fa-exclamation-triangle',
        }
        return icons.get(self.widget_type, 'fa-square')
    
    def get_widget_color(self):
        """Get color berdasarkan widget type"""
        colors = {
            'stats': 'primary',
            'chart': 'success',
            'table': 'info',
            'list': 'warning',
            'calendar': 'danger',
            'quick_actions': 'secondary',
            'recent_activity': 'info',
            'alerts': 'danger',
        }
        return colors.get(self.widget_type, 'secondary')


class QuickAccess(models.Model):
    """
    Menu akses cepat untuk admin
    Bisa di-customize per user untuk shortcut ke menu favorit
    """
    ICON_CHOICES = [
        ('fa-dashboard', 'Dashboard'),
        ('fa-users', 'Users'),
        ('fa-file', 'Documents'),
        ('fa-newspaper', 'News'),
        ('fa-briefcase', 'Business'),
        ('fa-heartbeat', 'Posyandu'),
        ('fa-mountain', 'Tourism'),
        ('fa-comments', 'Complaints'),
        ('fa-chart-bar', 'Reports'),
        ('fa-cog', 'Settings'),
    ]
    
    # Owner
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quick_access',
        verbose_name="User"
    )
    
    # Menu info
    title = models.CharField(max_length=100, verbose_name="Judul")
    url = models.CharField(max_length=500, verbose_name="URL")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-star', verbose_name="Icon")
    color = models.CharField(max_length=50, default='primary', verbose_name="Warna",
                            help_text="primary, success, warning, danger, info")
    
    # Display settings
    position = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    
    # Usage tracking
    access_count = models.PositiveIntegerField(default=0, verbose_name="Jumlah Akses")
    last_accessed = models.DateTimeField(null=True, blank=True, verbose_name="Terakhir Diakses")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat")
    
    class Meta:
        verbose_name = "Akses Cepat"
        verbose_name_plural = "Akses Cepat"
        ordering = ['position', 'title']
        unique_together = ['user', 'url']
    
    def __str__(self):
        return f"{self.title} - {self.user}"
    
    def increment_access(self):
        """Increment counter saat diakses"""
        self.access_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['access_count', 'last_accessed'])


class SystemMessage(models.Model):
    """
    Pesan broadcast sistem untuk admin
    Untuk announce maintenance, update, atau info penting
    """
    MESSAGE_TYPES = [
        ('announcement', 'Pengumuman'),
        ('maintenance', 'Maintenance'),
        ('update', 'Update Sistem'),
        ('warning', 'Peringatan'),
        ('info', 'Informasi'),
    ]
    
    DISPLAY_LOCATIONS = [
        ('dashboard', 'Dashboard'),
        ('all_pages', 'Semua Halaman'),
        ('login', 'Halaman Login'),
    ]
    
    # Message content
    title = models.CharField(max_length=200, verbose_name="Judul")
    message = models.TextField(verbose_name="Pesan")
    message_type = models.CharField(max_length=30, choices=MESSAGE_TYPES, verbose_name="Tipe Pesan")
    
    # Display settings
    display_location = models.CharField(max_length=30, choices=DISPLAY_LOCATIONS, 
                                       default='dashboard', verbose_name="Lokasi Tampil")
    is_dismissible = models.BooleanField(default=True, verbose_name="Bisa Ditutup")
    
    # Schedule
    start_date = models.DateTimeField(verbose_name="Mulai Tampil")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Selesai Tampil")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    priority = models.PositiveIntegerField(default=0, verbose_name="Prioritas",
                                          help_text="Semakin tinggi, semakin atas ditampilkan")
    
    # Created by
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Dibuat Oleh"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diupdate")
    
    class Meta:
        verbose_name = "Pesan Sistem"
        verbose_name_plural = "Pesan Sistem"
        ordering = ['-priority', '-start_date']
    
    def __str__(self):
        return f"{self.title} ({self.get_message_type_display()})"
    
    @property
    def is_currently_active(self):
        """Check apakah pesan sedang aktif berdasarkan schedule"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        if now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        return True


class DataExportHistory(models.Model):
    """
    History export data untuk tracking
    """
    EXPORT_FORMATS = [
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('pdf', 'PDF'),
        ('json', 'JSON'),
    ]
    
    MODULE_CHOICES = [
        ('references', 'Data Referensi'),
        ('beneficiaries', 'Penerima Bantuan'),
        ('business', 'Usaha'),
        ('complaints', 'Keluhan'),
        ('documents', 'Dokumen'),
        ('tourism', 'Wisata'),
        ('posyandu', 'Posyandu'),
        ('news', 'Berita'),
        ('organization', 'Organisasi'),
    ]
    
    # Export details
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="User"
    )
    module = models.CharField(max_length=50, choices=MODULE_CHOICES, verbose_name="Modul")
    export_format = models.CharField(max_length=20, choices=EXPORT_FORMATS, verbose_name="Format")
    
    # File info
    file_name = models.CharField(max_length=255, verbose_name="Nama File")
    file_size = models.PositiveIntegerField(default=0, verbose_name="Ukuran File (bytes)")
    record_count = models.PositiveIntegerField(default=0, verbose_name="Jumlah Data")
    
    # Filters used (optional)
    filters = models.JSONField(null=True, blank=True, verbose_name="Filter yang Digunakan")
    
    # Status
    is_successful = models.BooleanField(default=True, verbose_name="Berhasil")
    error_message = models.TextField(blank=True, null=True, verbose_name="Pesan Error")
    
    # IP tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Export")
    
    class Meta:
        verbose_name = "History Export Data"
        verbose_name_plural = "History Export Data"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['module', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_module_display()} - {self.file_name}"
    
    @property
    def file_size_mb(self):
        """Return file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)


class AdminPreference(models.Model):
    """
    Preferensi personal admin
    Untuk menyimpan settings UI/UX per user
    """
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    SIDEBAR_CHOICES = [
        ('expanded', 'Expanded'),
        ('collapsed', 'Collapsed'),
        ('auto', 'Auto'),
    ]
    
    # User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_preference',
        verbose_name="User"
    )
    
    # UI Preferences
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light', verbose_name="Tema")
    sidebar_state = models.CharField(max_length=20, choices=SIDEBAR_CHOICES, default='expanded', verbose_name="Sidebar")
    items_per_page = models.PositiveIntegerField(default=25, verbose_name="Item Per Halaman")
    
    # Dashboard preferences
    default_dashboard = models.CharField(max_length=100, default='main', verbose_name="Dashboard Default")
    show_welcome_message = models.BooleanField(default=True, verbose_name="Tampilkan Pesan Selamat Datang")
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True, verbose_name="Notifikasi Email")
    browser_notifications = models.BooleanField(default=True, verbose_name="Notifikasi Browser")
    sound_notifications = models.BooleanField(default=False, verbose_name="Notifikasi Suara")
    
    # Other preferences (JSON for flexibility)
    custom_settings = models.JSONField(default=dict, blank=True, verbose_name="Pengaturan Custom")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diupdate")
    
    class Meta:
        verbose_name = "Preferensi Admin"
        verbose_name_plural = "Preferensi Admin"
    
    def __str__(self):
        return f"Preferensi {self.user}"
