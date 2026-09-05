from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Business, BusinessCategory, UKM, Koperasi, BUMG, LayananJasa, BusinessRegistration, BusinessRegistrationImage
from .validators import validate_image_file, validate_logo_file

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'name', 'business_type', 'category', 'description', 'address', 
            'phone', 'email', 'website', 'status', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'business-form-control'}),
            'business_type': forms.Select(attrs={'class': 'business-form-control'}),
            'category': forms.Select(attrs={'class': 'business-form-control'}),
            'description': SummernoteWidget(),
            'address': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'business-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'business-form-control'}),
            'website': forms.URLInput(attrs={'class': 'business-form-control'}),
            'status': forms.Select(attrs={'class': 'business-form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'business-form-control'}),
        }

class UKMForm(forms.ModelForm):
    class Meta:
        model = UKM
        fields = [
            'nama_usaha', 'pemilik', 'nik_pemilik', 'alamat_usaha', 'alamat_pemilik',
            'jenis_usaha', 'skala_usaha', 'modal_awal', 'omzet_bulanan', 'jumlah_karyawan',
            'tanggal_mulai', 'nomor_izin', 'telepon', 'email', 'produk_utama', 'target_pasar',
            'foto_usaha', 'logo_usaha', 'status', 'keterangan'
        ]
        widgets = {
            'nama_usaha': forms.TextInput(attrs={'class': 'business-form-control'}),
            'pemilik': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'data-fill-nik': 'id_nik_pemilik',
                'data-fill-alamat': 'id_alamat_pemilik',
                'data-fill-telepon': 'id_telepon',
                'data-fill-email': 'id_email',
                'placeholder': 'Ketik nama atau NIK penduduk...',
                'autocomplete': 'off'
            }),
            'nik_pemilik': forms.TextInput(attrs={'class': 'business-form-control', 'readonly': 'readonly'}),
            'alamat_usaha': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2}),
            'alamat_pemilik': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2, 'readonly': 'readonly'}),
            'jenis_usaha': forms.TextInput(attrs={'class': 'business-form-control'}),
            'skala_usaha': forms.Select(attrs={'class': 'business-form-control'}),
            'modal_awal': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'omzet_bulanan': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'jumlah_karyawan': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'tanggal_mulai': forms.DateInput(attrs={'class': 'business-form-control', 'type': 'date'}),
            'nomor_izin': forms.TextInput(attrs={'class': 'business-form-control'}),
            'telepon': forms.TextInput(attrs={'class': 'business-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'business-form-control', 'readonly': 'readonly'}),
            'produk_utama': SummernoteWidget(),
            'target_pasar': SummernoteWidget(),
            'foto_usaha': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'logo_usaha': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'business-form-control'}),
            'keterangan': SummernoteWidget(),
        }

class KoperasiForm(forms.ModelForm):
    class Meta:
        model = Koperasi
        fields = [
            'nama', 'nomor_badan_hukum', 'tanggal_berdiri', 'alamat',
            'ketua', 'sekretaris', 'bendahara', 'jumlah_anggota', 
            'modal_dasar', 'modal_disetor', 'jenis_koperasi', 'jenis_usaha', 'bidang_usaha',
            'telepon', 'email', 'foto_koperasi', 'logo_koperasi', 'status', 'keterangan'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'business-form-control'}),
            'nomor_badan_hukum': forms.TextInput(attrs={'class': 'business-form-control'}),
            'tanggal_berdiri': forms.DateInput(attrs={'class': 'business-form-control', 'type': 'date'}),
            'alamat': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2}),
            'ketua': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'data-fill-telepon': 'id_telepon',
                'data-fill-email': 'id_email',
                'placeholder': 'Ketik nama atau NIK ketua...',
                'autocomplete': 'off'
            }),
            'sekretaris': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'placeholder': 'Ketik nama atau NIK sekretaris...',
                'autocomplete': 'off'
            }),
            'bendahara': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'placeholder': 'Ketik nama atau NIK bendahara...',
                'autocomplete': 'off'
            }),
            'jumlah_anggota': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'modal_dasar': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'modal_disetor': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'jenis_koperasi': forms.TextInput(attrs={'class': 'business-form-control'}),
            'jenis_usaha': forms.TextInput(attrs={'class': 'business-form-control'}),
            'bidang_usaha': forms.TextInput(attrs={'class': 'business-form-control'}),
            'telepon': forms.TextInput(attrs={'class': 'business-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'business-form-control'}),
            'foto_koperasi': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'logo_koperasi': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'business-form-control'}),
            'keterangan': SummernoteWidget(),
        }

class BUMGForm(forms.ModelForm):
    class Meta:
        model = BUMG
        fields = [
            'nama', 'nomor_sk', 'tanggal_sk', 'alamat', 'direktur', 'komisaris',
            'jumlah_karyawan', 'modal_dasar', 'modal_disetor', 'bidang_usaha', 'telepon', 'email', 
            'website', 'foto_bumg', 'logo_bumg', 'status', 'keterangan'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'business-form-control'}),
            'nomor_sk': forms.TextInput(attrs={'class': 'business-form-control'}),
            'tanggal_sk': forms.DateInput(attrs={'class': 'business-form-control', 'type': 'date'}),
            'alamat': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2}),
            'direktur': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'data-fill-telepon': 'id_telepon',
                'data-fill-email': 'id_email',
                'placeholder': 'Ketik nama atau NIK direktur...',
                'autocomplete': 'off'
            }),
            'komisaris': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'placeholder': 'Ketik nama atau NIK komisaris...',
                'autocomplete': 'off'
            }),
            'jumlah_karyawan': forms.NumberInput(attrs={
                'class': 'business-form-control',
                'min': '0',
                'max': '1000',
                'step': '1',
                'placeholder': 'Masukkan jumlah karyawan'
            }),
            'modal_dasar': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'modal_disetor': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'bidang_usaha': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2}),
            'telepon': forms.TextInput(attrs={'class': 'business-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'business-form-control'}),
            'website': forms.URLInput(attrs={'class': 'business-form-control'}),
            'foto_bumg': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'logo_bumg': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'business-form-control'}),
            'keterangan': SummernoteWidget(),
        }

class LayananJasaForm(forms.ModelForm):
    class Meta:
        model = LayananJasa
        fields = [
            'nama', 'penyedia', 'alamat', 'telepon', 'email', 'kategori', 'deskripsi',
            'pengalaman', 'harga_min', 'harga_max', 'satuan_harga', 'waktu_layanan', 
            'area_layanan', 'rating', 'website', 'keunggulan', 'syarat_ketentuan', 
            'sertifikat', 'foto_layanan', 'logo_layanan', 'status', 'keterangan'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'business-form-control'}),
            'penyedia': forms.TextInput(attrs={
                'class': 'business-form-control penduduk-autocomplete',
                'data-fill-alamat': 'id_alamat',
                'data-fill-telepon': 'id_telepon',
                'data-fill-email': 'id_email',
                'placeholder': 'Ketik nama atau NIK penyedia...',
                'autocomplete': 'off'
            }),
            'alamat': forms.Textarea(attrs={'class': 'business-form-control', 'rows': 2}),
            'telepon': forms.TextInput(attrs={'class': 'business-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'business-form-control'}),
            'kategori': forms.TextInput(attrs={'class': 'business-form-control'}),
            'deskripsi': SummernoteWidget(),
            'pengalaman': forms.TextInput(attrs={'class': 'business-form-control'}),
            'harga_min': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'harga_max': forms.NumberInput(attrs={'class': 'business-form-control'}),
            'satuan_harga': forms.TextInput(attrs={'class': 'business-form-control'}),
            'waktu_layanan': forms.TextInput(attrs={'class': 'business-form-control'}),
            'area_layanan': forms.TextInput(attrs={'class': 'business-form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'business-form-control', 'step': '0.1'}),
            'website': forms.URLInput(attrs={'class': 'business-form-control'}),
            'keunggulan': SummernoteWidget(),
            'syarat_ketentuan': SummernoteWidget(),
            'sertifikat': forms.FileInput(attrs={'class': 'business-form-control', 'accept': '.pdf,.png,.jpg,.jpeg'}),
            'foto_layanan': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'logo_layanan': forms.FileInput(attrs={'class': 'business-form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'business-form-control'}),
            'keterangan': SummernoteWidget(),
        }

# Business Registration Forms
class BusinessRegistrationForm(forms.ModelForm):
    """Form untuk pendaftaran bisnis online"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom validation
        self.fields['owner_nik'].widget.attrs.update({'pattern': '[0-9]{16}', 'title': 'NIK harus 16 digit angka'})
        self.fields['owner_phone'].widget.attrs.update({'pattern': '[0-9+\\-\\s()]{10,20}', 'title': 'Format: 08xx-xxxx-xxxx atau +62xxx'})
        self.fields['business_phone'].widget.attrs.update({'pattern': '[0-9+\\-\\s()]{10,20}', 'title': 'Format: 08xx-xxxx-xxxx atau +62xxx'})
    
    def clean_owner_nik(self):
        nik = self.cleaned_data.get('owner_nik')
        if nik:
            if not nik.isdigit():
                raise forms.ValidationError('NIK harus berupa angka')
            if len(nik) != 16:
                raise forms.ValidationError('NIK harus 16 digit')
        return nik
    
    def clean_owner_phone(self):
        phone = self.cleaned_data.get('owner_phone')
        if phone:
            # Remove spaces and special characters for validation
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) < 10:
                raise forms.ValidationError('Nomor telepon minimal 10 digit')
        return phone
    
    def clean_business_phone(self):
        phone = self.cleaned_data.get('business_phone')
        if phone:
            # Remove spaces and special characters for validation
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) < 10:
                raise forms.ValidationError('Nomor telepon minimal 10 digit')
        return phone
    
    def clean_owner_email(self):
        email = self.cleaned_data.get('owner_email')
        if email:
            if not email.endswith(('.com', '.co.id', '.id', '.org')):
                raise forms.ValidationError('Format email tidak valid')
        return email
    
    def clean_business_email(self):
        email = self.cleaned_data.get('business_email')
        if email:
            if not email.endswith(('.com', '.co.id', '.id', '.org')):
                raise forms.ValidationError('Format email tidak valid')
        return email
    
    class Meta:
        model = BusinessRegistration
        fields = [
            'registration_type', 'business_name', 'owner_name', 'owner_nik', 
            'owner_phone', 'owner_email', 'owner_address', 'business_address',
            'business_phone', 'business_email', 'business_description',
            'business_photo', 'business_logo', 'additional_documents',
            'business_video', 'facebook_url', 'instagram_url', 'twitter_url',
            'youtube_url', 'tiktok_url', 'website_url'
        ]
        widgets = {
            'registration_type': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'required': True}),
            'business_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'required': True, 'placeholder': 'Masukkan nama bisnis Anda'}),
            'owner_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'required': True, 'placeholder': 'Masukkan nama lengkap pemilik'}),
            'owner_nik': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'required': True, 'maxlength': '16', 'placeholder': 'Masukkan NIK pemilik'}),
            'owner_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'required': True, 'placeholder': 'Masukkan nomor telepon pemilik'}),
            'owner_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'Masukkan email pemilik'}),
            'business_address': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 resize-none', 'required': True, 'rows': 3, 'placeholder': 'Masukkan alamat lengkap bisnis'}),
            'business_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'Masukkan nomor telepon bisnis'}),
            'business_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'Masukkan email bisnis'}),
            'business_description': SummernoteWidget(),
            'business_photo': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100', 'accept': 'image/*'}),
            'business_logo': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100', 'accept': 'image/*'}),
            'additional_documents': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100', 'accept': '.pdf,.doc,.docx'}),
            'business_video': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100', 'accept': 'video/*'}),
            'facebook_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'https://facebook.com/yourbusiness'}),
            'instagram_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'https://instagram.com/yourbusiness'}),
            'twitter_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'https://twitter.com/yourbusiness'}),
            'youtube_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'https://youtube.com/c/yourbusiness'}),
            'tiktok_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'https://tiktok.com/@yourbusiness'}),
            'website_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-900', 'placeholder': 'https://yourbusiness.com'}),
        }
        labels = {
            'registration_type': 'Jenis Bisnis',
            'business_name': 'Nama Bisnis',
            'owner_name': 'Nama Pemilik',
            'owner_nik': 'NIK Pemilik',
            'owner_phone': 'No. Telepon',
            'owner_email': 'Email',
            'owner_address': 'Alamat Pemilik',
            'business_address': 'Alamat Bisnis',
            'business_phone': 'Telepon Bisnis',
            'business_email': 'Email Bisnis',
            'business_description': 'Deskripsi Bisnis',
            'business_photo': 'Foto Bisnis',
            'business_logo': 'Logo Bisnis',
            'additional_documents': 'Dokumen Tambahan',
            'business_video': 'Video Bisnis',
            'facebook_url': 'Facebook',
            'instagram_url': 'Instagram',
            'twitter_url': 'Twitter',
            'youtube_url': 'YouTube',
            'tiktok_url': 'TikTok',
            'website_url': 'Website',
        }

class UMKMRegistrationForm(BusinessRegistrationForm):
    """Form khusus untuk pendaftaran UMKM"""
    
    class Meta(BusinessRegistrationForm.Meta):
        fields = BusinessRegistrationForm.Meta.fields + ['skala_usaha', 'jenis_usaha']
        widgets = {
            **BusinessRegistrationForm.Meta.widgets,
            'skala_usaha': forms.Select(attrs={'class': 'form-control'}),
            'jenis_usaha': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            **BusinessRegistrationForm.Meta.labels,
            'skala_usaha': 'Skala Usaha',
            'jenis_usaha': 'Jenis Usaha',
        }

class KoperasiRegistrationForm(BusinessRegistrationForm):
    """Form khusus untuk pendaftaran Koperasi"""
    
    class Meta(BusinessRegistrationForm.Meta):
        fields = BusinessRegistrationForm.Meta.fields + ['ketua', 'sekretaris', 'bendahara', 'jumlah_anggota', 'modal_dasar']
        widgets = {
            **BusinessRegistrationForm.Meta.widgets,
            'ketua': forms.TextInput(attrs={'class': 'form-control'}),
            'sekretaris': forms.TextInput(attrs={'class': 'form-control'}),
            'bendahara': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_anggota': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'modal_dasar': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }
        labels = {
            **BusinessRegistrationForm.Meta.labels,
            'ketua': 'Ketua',
            'sekretaris': 'Sekretaris',
            'bendahara': 'Bendahara',
            'jumlah_anggota': 'Jumlah Anggota',
            'modal_dasar': 'Modal Dasar (Rp)',
        }

class BUMGRegistrationForm(BusinessRegistrationForm):
    """Form khusus untuk pendaftaran BUMG"""
    
    class Meta(BusinessRegistrationForm.Meta):
        fields = BusinessRegistrationForm.Meta.fields + ['direktur', 'komisaris', 'jumlah_karyawan', 'bidang_usaha']
        widgets = {
            **BusinessRegistrationForm.Meta.widgets,
            'direktur': forms.TextInput(attrs={'class': 'form-control'}),
            'komisaris': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_karyawan': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'bidang_usaha': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            **BusinessRegistrationForm.Meta.labels,
            'direktur': 'Direktur',
            'komisaris': 'Komisaris',
            'jumlah_karyawan': 'Jumlah Karyawan',
            'bidang_usaha': 'Bidang Usaha',
        }

class LayananJasaRegistrationForm(BusinessRegistrationForm):
    """Form khusus untuk pendaftaran Layanan Jasa"""
    
    class Meta(BusinessRegistrationForm.Meta):
        fields = BusinessRegistrationForm.Meta.fields + ['penyedia', 'kategori_layanan', 'tarif_layanan']
        widgets = {
            **BusinessRegistrationForm.Meta.widgets,
            'penyedia': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori_layanan': forms.TextInput(attrs={'class': 'form-control'}),
            'tarif_layanan': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }
        labels = {
            **BusinessRegistrationForm.Meta.labels,
            'penyedia': 'Penyedia',
            'kategori_layanan': 'Kategori Layanan',
            'tarif_layanan': 'Tarif Layanan (Rp)',
        }

class BusinessRegistrationImageForm(forms.ModelForm):
    """Form untuk upload gambar tambahan"""
    
    class Meta:
        model = BusinessRegistrationImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan gambar (opsional)'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'image': 'Gambar',
            'caption': 'Keterangan',
            'is_primary': 'Gambar Utama',
        }
