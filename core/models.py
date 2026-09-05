from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
import os
import shutil
import json


class MenuPermission(models.Model):
    """Permission model for admin panel menu access"""
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
        ('reports', 'Laporan'),
        ('settings', 'Pengaturan'),
    ]
    
    ACTION_CHOICES = [
        ('view', 'Lihat'),
        ('add', 'Tambah'),
        ('change', 'Ubah'),
        ('delete', 'Hapus'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]
    
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    codename = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Menu Permission'
        verbose_name_plural = 'Menu Permissions'
        unique_together = ['module', 'action']
    
    def __str__(self):
        return f"{self.get_module_display()} - {self.get_action_display()}"


class Role(models.Model):
    """Role model for multi-role authentication system"""
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('data_manager', 'Data Manager'),
        ('beneficiary_manager', 'Manager Penerima Bantuan'),
        ('business_manager', 'Manager Usaha'),
        ('complaint_manager', 'Manager Keluhan'),
        ('document_manager', 'Manager Dokumen'),
        ('tourism_manager', 'Manager Wisata'),
        ('posyandu_manager', 'Manager Posyandu'),
        ('news_manager', 'Manager Berita'),
        ('village_profile_manager', 'Manager Profil Desa'),
        ('organization_manager', 'Manager Organisasi'),
        ('karang_taruna_manager', 'Manager Karang Taruna'),
        ('kepemudaan_manager', 'Manager Kepemudaan'),
        ('pkk_manager', 'Manager PKK'),
        ('lembaga_adat_manager', 'Manager Lembaga Adat'),
        ('perangkat_desa_manager', 'Manager Perangkat Desa'),
        ('village_staff', 'Staff Desa'),
        ('moderator', 'Moderator'),
        ('viewer', 'Viewer'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    menu_permissions = models.ManyToManyField(MenuPermission, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name
    
    def has_menu_permission(self, module, action):
        """Check if role has permission for module and action"""
        return self.menu_permissions.filter(module=module, action=action, is_active=True).exists()


class CustomUser(AbstractUser):
    """Extended user model for village staff"""
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_village_staff = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, through='UserRole', through_fields=('user', 'role'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.position}"
    
    def has_role(self, role_name):
        """Check if user has specific role"""
        return self.roles.filter(name=role_name, is_active=True).exists()
    
    def get_active_roles(self):
        """Get all active roles for user"""
        return self.roles.filter(is_active=True)
    
    def has_menu_permission(self, module, action):
        """Check if user has menu permission"""
        for role in self.get_active_roles():
            if role.has_menu_permission(module, action):
                return True
        return False
    
    def get_menu_permissions(self):
        """Get all menu permissions for user"""
        permissions = set()
        for role in self.get_active_roles():
            for perm in role.menu_permissions.filter(is_active=True):
                permissions.add(perm)
        return permissions


class UserRole(models.Model):
    """Through model for User-Role relationship"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'role']
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
    
    def __str__(self):
        return f"{self.user.username} - {self.role.display_name}"


class UserProfile(models.Model):
    """Additional profile information for users"""
    GENDER_CHOICES = [
        ('M', 'Laki-laki'),
        ('F', 'Perempuan'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_id = models.CharField(max_length=64, unique=True, blank=True, help_text="Secure unique profile identifier")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True, help_text="Foto profil pengguna")
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Nomor telepon")
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    def generate_secure_profile_id(self):
        """Generate a secure, unique profile ID"""
        import secrets
        import hashlib
        import time
        
        # Create a unique string combining user data and timestamp
        unique_string = f"{self.user.id}_{self.user.username}_{time.time()}_{secrets.token_hex(16)}"
        
        # Generate SHA-256 hash for security
        secure_id = hashlib.sha256(unique_string.encode()).hexdigest()
        
        # Add a prefix for identification
        return f"PROF_{secure_id[:32]}"
    
    def save(self, *args, **kwargs):
        """Override save to generate secure profile ID if not exists"""
        if not self.profile_id:
            self.profile_id = self.generate_secure_profile_id()
        super().save(*args, **kwargs)


class LoginHistory(models.Model):
    """Model untuk menyimpan riwayat login pengguna"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(help_text="Alamat IP saat login")
    user_agent = models.TextField(help_text="User agent browser")
    browser = models.CharField(max_length=50, blank=True, null=True, help_text="Nama browser")
    os = models.CharField(max_length=50, blank=True, null=True, help_text="Sistem operasi")
    device = models.CharField(max_length=50, blank=True, null=True, help_text="Jenis perangkat")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Lokasi berdasarkan IP")
    login_time = models.DateTimeField(auto_now_add=True, help_text="Waktu login")
    logout_time = models.DateTimeField(blank=True, null=True, help_text="Waktu logout")
    is_successful = models.BooleanField(default=True, help_text="Apakah login berhasil")
    failure_reason = models.CharField(max_length=200, blank=True, null=True, help_text="Alasan gagal login")

    class Meta:
        ordering = ['-login_time']
        verbose_name = 'Riwayat Login'
        verbose_name_plural = 'Riwayat Login'

    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%d/%m/%Y %H:%M')}"

    @property
    def session_duration(self):
        """Calculate session duration in minutes"""
        if self.logout_time and self.login_time:
            duration = self.logout_time - self.login_time
            return duration.total_seconds() / 60
        return None


class WebsiteSettings(models.Model):
    """Unified website settings model - minimal and efficient"""
    THEME_CHOICES = [
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
        ('auto', 'Auto (System)')
    ]
    
    LANGUAGE_CHOICES = [
        ('id', 'Bahasa Indonesia'),
        ('en', 'English'),
        ('jv', 'Bahasa Jawa')
    ]
    
    # Basic Website Info
    site_name = models.CharField(max_length=200, default='Website Desa Pulosarok')
    site_description = models.TextField(blank=True, null=True, help_text="Deskripsi singkat website yang akan ditampilkan di halaman utama")
    site_logo = models.ImageField(upload_to='website/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='website/', blank=True, null=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    # Appearance
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    primary_color = models.CharField(max_length=7, default='#3B82F6')
    secondary_color = models.CharField(max_length=7, default='#10B981')
    
    # Localization
    default_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='id')
    timezone = models.CharField(max_length=50, default='Asia/Jakarta')
    
    # SEO Settings
    site_title = models.CharField(max_length=200, default='Website Desa Pulosarok', verbose_name="Site Title")
    site_description = models.TextField(blank=True, null=True, help_text="Deskripsi singkat website yang akan ditampilkan di halaman utama", verbose_name="Site Description")
    site_keywords = models.TextField(blank=True, null=True, verbose_name="Site Keywords")
    site_author = models.CharField(max_length=200, default='Tim Website Pulosarok', verbose_name="Site Author")
    site_language = models.CharField(max_length=5, default='id', verbose_name="Site Language")
    
    # Open Graph Settings
    og_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="OG Title")
    og_description = models.TextField(blank=True, null=True, verbose_name="OG Description")
    og_image = models.ImageField(upload_to='website/og/', blank=True, null=True, verbose_name="OG Image")
    
    # Analytics & Tracking
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Google Analytics ID")
    google_tag_manager_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Google Tag Manager ID")
    facebook_pixel_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Facebook Pixel ID")
    enable_facebook_tracking = models.BooleanField(default=False, verbose_name="Enable Facebook Tracking")
    
    # Search Console
    google_search_console = models.CharField(max_length=100, blank=True, null=True, verbose_name="Google Search Console")
    bing_webmaster = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bing Webmaster")
    
    # Sitemap & Robots
    enable_sitemap = models.BooleanField(default=True, verbose_name="Enable Sitemap")
    enable_robots_txt = models.BooleanField(default=True, verbose_name="Enable robots.txt")
    robots_content = models.TextField(blank=True, null=True, verbose_name="Robots.txt Content")
    
    # System Settings
    enable_maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, null=True)
    allow_registration = models.BooleanField(default=False)
    max_file_upload_size = models.IntegerField(default=10)
    
    # Security Settings
    enable_ssl_redirect = models.BooleanField(default=True, verbose_name="Enable SSL Redirect")
    enable_hsts = models.BooleanField(default=True, verbose_name="Enable HSTS")
    hsts_max_age = models.IntegerField(default=31536000, verbose_name="HSTS Max Age")
    max_login_attempts = models.IntegerField(default=5, verbose_name="Max Login Attempts")
    login_timeout = models.IntegerField(default=15, verbose_name="Login Timeout (minutes)")
    enable_2fa = models.BooleanField(default=False, verbose_name="Enable 2FA")
    enable_captcha = models.BooleanField(default=False, verbose_name="Enable CAPTCHA")
    min_password_length = models.IntegerField(default=8, verbose_name="Min Password Length")
    require_uppercase = models.BooleanField(default=True, verbose_name="Require Uppercase")
    require_lowercase = models.BooleanField(default=True, verbose_name="Require Lowercase")
    require_numbers = models.BooleanField(default=True, verbose_name="Require Numbers")
    require_symbols = models.BooleanField(default=False, verbose_name="Require Symbols")
    password_expiry = models.IntegerField(default=90, verbose_name="Password Expiry (days)")
    security_level = models.CharField(max_length=10, default='medium', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], verbose_name="Security Level")
    
    # Notification Settings
    sms_notifications = models.BooleanField(default=False)
    
    # Cache Settings
    enable_cache = models.BooleanField(default=True, verbose_name="Enable Cache")
    cache_duration = models.IntegerField(default=300, verbose_name="Cache Duration (seconds)")
    enable_static_cache = models.BooleanField(default=True, verbose_name="Enable Static Cache")
    enable_gzip_compression = models.BooleanField(default=True, verbose_name="Enable GZIP Compression")
    enable_minify_css = models.BooleanField(default=False, verbose_name="Minify CSS")
    enable_minify_js = models.BooleanField(default=False, verbose_name="Minify JavaScript")
    enable_cdn = models.BooleanField(default=False, verbose_name="Enable CDN")
    cdn_url = models.URLField(blank=True, null=True, verbose_name="CDN URL")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website Settings'
    
    def __str__(self):
        return f"Website Settings - {self.site_name}"
    
    @classmethod
    def get_settings(cls):
        """Get or create website settings singleton"""
        settings, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'Website Desa Pulosarok'
            }
        )
        return settings


class DatabaseResetConfig(models.Model):
    """Model untuk konfigurasi reset database"""
    RESET_TYPE_CHOICES = [
        ('selective', 'Reset Selektif'),
        ('full', 'Reset Lengkap'),
        ('custom', 'Reset Kustom'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Menunggu'),
        ('running', 'Berjalan'),
        ('completed', 'Selesai'),
        ('failed', 'Gagal'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    name = models.CharField(max_length=200, help_text='Nama konfigurasi reset')
    description = models.TextField(blank=True, null=True, help_text='Deskripsi konfigurasi')
    reset_type = models.CharField(max_length=20, choices=RESET_TYPE_CHOICES, default='selective')
    
    # Data yang akan direset
    reset_penduduk = models.BooleanField(default=False, help_text='Reset data penduduk')
    reset_dusun = models.BooleanField(default=False, help_text='Reset data dusun')
    reset_lorong = models.BooleanField(default=False, help_text='Reset data lorong')
    reset_rt_rw = models.BooleanField(default=False, help_text='Reset data RT/RW')
    reset_keluarga = models.BooleanField(default=False, help_text='Reset data keluarga')
    reset_pelajar = models.BooleanField(default=False, help_text='Reset data pelajar')
    reset_disabilitas = models.BooleanField(default=False, help_text='Reset data disabilitas')
    reset_beneficiaries = models.BooleanField(default=False, help_text='Reset data penerima bantuan')
    reset_business = models.BooleanField(default=False, help_text='Reset data usaha')
    reset_complaints = models.BooleanField(default=False, help_text='Reset data keluhan')
    reset_documents = models.BooleanField(default=False, help_text='Reset data dokumen')
    reset_tourism = models.BooleanField(default=False, help_text='Reset data wisata')
    reset_posyandu = models.BooleanField(default=False, help_text='Reset data posyandu')
    reset_news = models.BooleanField(default=False, help_text='Reset data berita')
    reset_organization = models.BooleanField(default=False, help_text='Reset data organisasi')
    reset_layanan = models.BooleanField(default=False, help_text='Reset data layanan')
    reset_letters = models.BooleanField(default=False, help_text='Reset data surat menyurat')
    
    # Opsi tambahan
    backup_before_reset = models.BooleanField(default=True, help_text='Backup data sebelum reset')
    keep_users = models.BooleanField(default=True, help_text='Tetap simpan data pengguna')
    keep_settings = models.BooleanField(default=True, help_text='Tetap simpan pengaturan')
    keep_media = models.BooleanField(default=False, help_text='Tetap simpan file media')
    
    # Status dan tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_reset_configs')
    executed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='executed_reset_configs')
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Log dan hasil
    execution_log = models.TextField(blank=True, null=True, help_text='Log eksekusi reset')
    error_log = models.TextField(blank=True, null=True, help_text='Log error jika ada')
    records_deleted = models.JSONField(default=dict, help_text='Jumlah record yang dihapus per tabel')
    
    class Meta:
        verbose_name = 'Database Reset Configuration'
        verbose_name_plural = 'Database Reset Configurations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    def get_selected_modules(self):
        """Get list of selected modules for reset"""
        modules = []
        if self.reset_penduduk:
            modules.append('Penduduk')
        if self.reset_dusun:
            modules.append('Dusun')
        if self.reset_lorong:
            modules.append('Lorong')
        if self.reset_rt_rw:
            modules.append('RT/RW')
        if self.reset_keluarga:
            modules.append('Keluarga')
        if self.reset_pelajar:
            modules.append('Pelajar')
        if self.reset_disabilitas:
            modules.append('Disabilitas')
        if self.reset_beneficiaries:
            modules.append('Penerima Bantuan')
        if self.reset_business:
            modules.append('Usaha')
        if self.reset_complaints:
            modules.append('Keluhan')
        if self.reset_documents:
            modules.append('Dokumen')
        if self.reset_tourism:
            modules.append('Wisata')
        if self.reset_posyandu:
            modules.append('Posyandu')
        if self.reset_news:
            modules.append('Berita')
        if self.reset_organization:
            modules.append('Organisasi')
        if self.reset_layanan:
            modules.append('Layanan')
        if self.reset_letters:
            modules.append('Surat Menyurat')
        return modules
    
    def is_dangerous(self):
        """Check if this reset configuration is dangerous (affects critical data)"""
        dangerous_modules = [
            self.reset_penduduk,
            self.reset_dusun,
            self.reset_keluarga,
            self.reset_beneficiaries,
        ]
        return any(dangerous_modules)


class HeroImage(models.Model):
    """Model sederhana untuk gambar hero"""
    PAGE_CHOICES = [
        ('home', 'Homepage'),
        ('events', 'Kegiatan'),
        ('news', 'Berita'),
        ('tourism', 'Wisata'),
        ('umkm', 'UMKM'),
        ('organization', 'Organisasi'),
        ('correspondence', 'Surat Menyurat'),
        ('gallery', 'Galeri'),
        ('complaints', 'Keluhan'),
        ('layanan', 'Layanan'),
        ('posyandu', 'Posyandu'),
        ('bantuna', 'Bantuna'),
        ('business', 'Bisnis'),
        ('koperasi', 'Koperasi'),
        ('bumg', 'BUMG'),
        ('layanan_jasa', 'Layanan Jasa'),
    ]
    
    name = models.CharField(max_length=200, help_text='Nama gambar hero')
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, default='home', help_text='Halaman yang menggunakan gambar ini')
    image = models.ImageField(upload_to='hero_images/%Y/%m/%d/', help_text='Gambar hero')
    is_active = models.BooleanField(default=True, help_text='Status aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Image'
        verbose_name_plural = 'Hero Images'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_page_display()}"


class ActivityLog(models.Model):
    """Model untuk menyimpan log aktivitas sistem"""
    ACTION_CHOICES = [
        ('create', 'Tambah'),
        ('update', 'Ubah'),
        ('delete', 'Hapus'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'Lihat'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('reset', 'Reset'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
    ]
    
    MODULE_CHOICES = [
        ('user', 'User Management'),
        ('settings', 'Settings'),
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
        ('letters', 'Surat Menyurat'),
        ('system', 'Sistem'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    module = models.CharField(max_length=30, choices=MODULE_CHOICES)
    object_type = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.CharField(max_length=50, blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['module', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.get_module_display()}"
    
    @classmethod
    def log_activity(cls, user, action, module, object_type=None, object_id=None, 
                     object_repr=None, description=None, ip_address=None, 
                     user_agent=None, extra_data=None):
        """Helper method untuk membuat log aktivitas"""
        return cls.objects.create(
            user=user,
            action=action,
            module=module,
            object_type=object_type,
            object_id=object_id,
            object_repr=object_repr,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            extra_data=extra_data
        )
