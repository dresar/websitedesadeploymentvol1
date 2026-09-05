from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
import os

User = get_user_model()


class DocumentCategory(models.Model):
    """Kategori Dokumen Transparansi Desa"""
    
    # Kategori Utama
    CATEGORY_CHOICES = [
        # Transparansi Anggaran
        ('apbdes', 'APBDES (Anggaran Pendapatan dan Belanja Desa)'),
        ('realisasi_anggaran', 'Laporan Realisasi Anggaran'),
        ('dana_desa', 'Info Dana Desa (DD & ADD)'),
        
        # Produk Hukum Desa
        ('perdes', 'Peraturan Desa (Perdes)'),
        ('perkades', 'Peraturan Kepala Desa (Perkades)'),
        ('sk_kades', 'Surat Keputusan Kepala Desa'),
        
        # Data dan Profil Desa
        ('profil_desa', 'Profil Desa & Kelurahan (Prodeskel)'),
        ('data_kependudukan', 'Data Kependudukan Agregat'),
        ('peta_desa', 'Peta Desa'),
        
        # Laporan
        ('lppd', 'Laporan Penyelenggaraan Pemerintahan Desa'),
        ('musdes', 'Notulensi Musyawarah Desa'),
        ('laporan_lainnya', 'Laporan Lainnya'),
        
        # Lainnya
        ('lainnya', 'Dokumen Lainnya'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Nama Kategori')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category_type = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        verbose_name='Jenis Kategori'
    )
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    icon = models.CharField(max_length=50, default='fa-file', verbose_name='Icon (FontAwesome)')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    display_order = models.IntegerField(default=0, verbose_name='Urutan Tampilan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Kategori Dokumen'
        verbose_name_plural = 'Kategori Dokumen'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Document(models.Model):
    """Dokumen Transparansi Desa"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Sedang Ditinjau'),
        ('published', 'Dipublikasikan'),
        ('archived', 'Diarsipkan'),
    ]
    
    # Informasi Dasar
    title = models.CharField(max_length=255, verbose_name='Judul Dokumen')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(
        DocumentCategory, 
        on_delete=models.CASCADE, 
        related_name='documents',
        verbose_name='Kategori'
    )
    
    # Nomor & Tahun Dokumen
    document_number = models.CharField(
        max_length=100, 
        blank=True, 
        default='',
        verbose_name='Nomor Dokumen',
        help_text='Contoh: 01/APBDES/2025 atau 05/PERDES/XII/2024'
    )
    document_year = models.IntegerField(
        default=2025,
        verbose_name='Tahun Dokumen',
        help_text='Tahun terbit dokumen'
    )
    
    # Deskripsi & Ringkasan
    description = models.TextField(
        default='', 
        verbose_name='Deskripsi'
    )
    summary = models.TextField(
        blank=True, 
        default='',
        verbose_name='Ringkasan',
        help_text='Ringkasan singkat untuk tampilan publik'
    )
    
    # File Upload
    file = models.FileField(
        upload_to='documents/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls'])],
        verbose_name='File Dokumen'
    )
    file_size = models.IntegerField(default=0, verbose_name='Ukuran File (bytes)')
    
    # Thumbnail/Cover (Optional)
    thumbnail = models.ImageField(
        upload_to='documents/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Thumbnail/Cover',
        help_text='Gambar cover untuk dokumen (opsional)'
    )
    
    # Status & Publikasi
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name='Status'
    )
    is_public = models.BooleanField(
        default=True, 
        verbose_name='Tampilkan di Public',
        help_text='Centang untuk menampilkan dokumen di halaman publik'
    )
    is_featured = models.BooleanField(
        default=False, 
        verbose_name='Dokumen Unggulan',
        help_text='Tampilkan di halaman utama'
    )
    
    # Metadata
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_documents',
        verbose_name='Diupload Oleh'
    )
    download_count = models.IntegerField(default=0, verbose_name='Jumlah Download')
    view_count = models.IntegerField(default=0, verbose_name='Jumlah Dilihat')
    
    # Tags untuk pencarian
    tags = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name='Tag',
        help_text='Pisahkan dengan koma. Contoh: anggaran, 2025, keuangan'
    )
    
    # Timestamps
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Tanggal Publikasi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Tanggal Diupdate')
    
    class Meta:
        verbose_name = 'Dokumen'
        verbose_name_plural = 'Dokumen'
        ordering = ['-document_year', '-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['document_year']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.document_number} - {self.title}" if self.document_number else self.title
    
    def save(self, *args, **kwargs):
        # Generate slug
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.document_year}")
        
        # Calculate file size
        if self.file and hasattr(self.file, 'size'):
            self.file_size = self.file.size
        
        # Set published_at
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def file_size_display(self):
        """Return human-readable file size"""
        if self.file_size == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = float(self.file_size)
        
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.2f} {size_names[i]}"
    
    @property
    def file_extension(self):
        """Return file extension"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower().replace('.', '')
        return ''
    
    @property
    def get_tags_list(self):
        """Return tags as list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class DocumentComment(models.Model):
    """Komentar pada Dokumen (untuk feedback publik)"""
    
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Dokumen'
    )
    name = models.CharField(max_length=100, verbose_name='Nama')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Komentar')
    is_approved = models.BooleanField(default=False, verbose_name='Disetujui')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal')
    
    class Meta:
        verbose_name = 'Komentar Dokumen'
        verbose_name_plural = 'Komentar Dokumen'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.document.title}"


class DocumentDownloadLog(models.Model):
    """Log untuk tracking download dokumen"""
    
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name='download_logs',
        verbose_name='Dokumen'
    )
    ip_address = models.GenericIPAddressField(verbose_name='IP Address')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    downloaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Download')
    
    class Meta:
        verbose_name = 'Log Download'
        verbose_name_plural = 'Log Download'
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.document.title} - {self.downloaded_at}"

