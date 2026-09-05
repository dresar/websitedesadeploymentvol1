from django.contrib import admin
from .models import (
    BusinessCategory, Business, BusinessOwner, BusinessProduct, 
    BusinessFinance, UKM, Koperasi, BUMG, Aset, LayananJasa, 
    BusinessPageHeader, JenisKoperasi
)


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_type', 'status', 'category', 'created_at']
    list_filter = ['business_type', 'status', 'category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informasi Bisnis', {
            'fields': ('name', 'business_type', 'category', 'description', 'status', 'is_active')
        }),
        ('Kontak & Alamat', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Media', {
            'fields': ('image', 'logo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BusinessOwner)
class BusinessOwnerAdmin(admin.ModelAdmin):
    list_display = ['business', 'owner', 'ownership_percentage', 'is_primary']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['business__name', 'owner__nama']


@admin.register(BusinessProduct)
class BusinessProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'price', 'is_active']
    list_filter = ['is_active', 'business__business_type']
    search_fields = ['name', 'business__name', 'description']
    ordering = ['-created_at']


@admin.register(BusinessFinance)
class BusinessFinanceAdmin(admin.ModelAdmin):
    list_display = ['business', 'initial_capital', 'monthly_revenue', 'monthly_expenses']
    list_filter = ['created_at']
    search_fields = ['business__name']
    ordering = ['-created_at']


@admin.register(UKM)
class UKMAdmin(admin.ModelAdmin):
    list_display = ['nama_usaha', 'pemilik', 'jenis_usaha', 'skala_usaha', 'telepon', 'whatsapp', 'status']
    list_filter = ['status', 'skala_usaha', 'jenis_usaha']
    search_fields = ['nama_usaha', 'pemilik', 'jenis_usaha', 'produk_utama', 'telepon', 'whatsapp']
    ordering = ['-created_at']
    fieldsets = (
        ('Informasi Usaha', {
            'fields': ('nama_usaha', 'pemilik', 'nik_pemilik', 'jenis_usaha', 'skala_usaha', 'tanggal_mulai', 'nomor_izin')
        }),
        ('Alamat', {
            'fields': ('alamat_usaha', 'alamat_pemilik')
        }),
        ('Kontak', {
            'fields': ('telepon', 'whatsapp', 'email')
        }),
        ('Media', {
            'fields': ('foto_usaha', 'logo_usaha')
        }),
        ('Keuangan', {
            'fields': ('modal_awal', 'omzet_bulanan', 'jumlah_karyawan')
        }),
        ('Produk & Pasar', {
            'fields': ('produk_utama', 'target_pasar')
        }),
        ('Status', {
            'fields': ('status', 'keterangan')
        }),
    )


@admin.register(Koperasi)
class KoperasiAdmin(admin.ModelAdmin):
    list_display = ['nama', 'nomor_badan_hukum', 'ketua', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['nama', 'ketua', 'sekretaris', 'bendahara']
    ordering = ['-created_at']
    fieldsets = (
        ('Informasi Koperasi', {
            'fields': ('nama', 'nomor_badan_hukum', 'tanggal_berdiri', 'jenis_koperasi', 'status')
        }),
        ('Pengurus', {
            'fields': ('ketua', 'sekretaris', 'bendahara')
        }),
        ('Alamat & Kontak', {
            'fields': ('alamat', 'telepon', 'email')
        }),
        ('Media', {
            'fields': ('foto_koperasi', 'logo_koperasi')
        }),
        ('Keanggotaan & Modal', {
            'fields': ('jumlah_anggota', 'modal_dasar', 'modal_disetor')
        }),
        ('Keterangan', {
            'fields': ('keterangan',)
        }),
    )


@admin.register(BUMG)
class BUMGAdmin(admin.ModelAdmin):
    list_display = ['nama', 'nomor_sk', 'direktur', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['nama', 'direktur', 'nomor_sk']
    ordering = ['-created_at']
    fieldsets = (
        ('Informasi BUMG', {
            'fields': ('nama', 'nomor_sk', 'tanggal_sk', 'status')
        }),
        ('Pimpinan', {
            'fields': ('direktur', 'komisaris')
        }),
        ('Alamat & Kontak', {
            'fields': ('alamat', 'telepon', 'email', 'website')
        }),
        ('Media', {
            'fields': ('foto_bumg', 'logo_bumg')
        }),
        ('Usaha & Modal', {
            'fields': ('bidang_usaha', 'jumlah_karyawan', 'modal_dasar', 'modal_disetor')
        }),
        ('Keterangan', {
            'fields': ('keterangan',)
        }),
    )


@admin.register(Aset)
class AsetAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'value', 'is_active']
    list_filter = ['is_active', 'business__business_type']
    search_fields = ['name', 'business__name', 'description']
    ordering = ['-created_at']


@admin.register(LayananJasa)
class LayananJasaAdmin(admin.ModelAdmin):
    list_display = ['nama', 'penyedia', 'kategori', 'harga_min', 'status']
    list_filter = ['status', 'kategori']
    search_fields = ['nama', 'penyedia', 'kategori']
    ordering = ['-created_at']
    fieldsets = (
        ('Informasi Layanan', {
            'fields': ('nama', 'penyedia', 'kategori', 'deskripsi', 'status')
        }),
        ('Alamat & Kontak', {
            'fields': ('alamat', 'telepon', 'email', 'website')
        }),
        ('Media', {
            'fields': ('foto_layanan', 'logo_layanan')
        }),
        ('Harga & Tarif', {
            'fields': ('tarif_layanan', 'harga_min', 'harga_max', 'satuan_harga')
        }),
        ('Operasional', {
            'fields': ('jam_operasional', 'waktu_layanan', 'area_layanan', 'pengalaman')
        }),
        ('Kualitas & Sertifikasi', {
            'fields': ('rating', 'sertifikat', 'keunggulan', 'syarat_ketentuan')
        }),
        ('Keterangan', {
            'fields': ('keterangan',)
        }),
    )


@admin.register(BusinessPageHeader)
class BusinessPageHeaderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']


@admin.register(JenisKoperasi)
class JenisKoperasiAdmin(admin.ModelAdmin):
    list_display = ['nama', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nama', 'deskripsi']
