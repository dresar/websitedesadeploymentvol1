from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import (
    VillageProfile, VillageGeography, VillageDemography,
    VillageOfficial, VillageFacility, VillageHistory, VillagePhoto
)


class VillageProfileForm(forms.ModelForm):
    """Form untuk mengelola profil desa"""
    
    class Meta:
        model = VillageProfile
        fields = [
            'name', 'code', 'district', 'regency', 'province', 'postal_code',
            'established_date', 'area', 'description', 'profile_description',
            'vision', 'mission', 'phone', 'email', 'website', 'logo', 'profile_image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Desa'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kode Desa'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Kecamatan'
            }),
            'regency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Kabupaten'
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Provinsi'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kode Pos'
            }),
            'established_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Luas wilayah dalam km²'
            }),
            'description': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi lengkap desa'
            }),
            'profile_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi singkat profil desa'
            }),
            'vision': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Visi desa'
            }),
            'mission': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Misi desa'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor telepon kantor desa'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email desa'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website desa'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'name': 'Nama Desa',
            'code': 'Kode Desa',
            'district': 'Kecamatan',
            'regency': 'Kabupaten',
            'province': 'Provinsi',
            'postal_code': 'Kode Pos',
            'established_date': 'Tanggal Berdiri',
            'area': 'Luas Wilayah (km²)',
            'description': 'Deskripsi Lengkap',
            'profile_description': 'Profil Singkat',
            'vision': 'Visi Desa',
            'mission': 'Misi Desa',
            'phone': 'Telepon Kantor',
            'email': 'Email Desa',
            'website': 'Website Desa',
            'logo': 'Logo Desa',
            'profile_image': 'Gambar Profil Desa'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['name'].required = True
        self.fields['code'].required = True
        self.fields['district'].required = True
        self.fields['regency'].required = True
        self.fields['province'].required = True
        
        # Configure Summernote for rich text fields
        self.fields['description'].widget = SummernoteWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Deskripsi lengkap desa'
        })
        self.fields['vision'].widget = SummernoteWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Visi desa'
        })
        self.fields['mission'].widget = SummernoteWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Misi desa'
        })


class VillageGeographyForm(forms.ModelForm):
    """Form untuk mengelola data geografis desa"""
    
    class Meta:
        model = VillageGeography
        fields = [
            'latitude', 'longitude', 'altitude', 'climate', 'rainfall',
            'temperature_min', 'temperature_max', 'topography', 'soil_type',
            'boundary_north', 'boundary_south', 'boundary_east', 'boundary_west'
        ]
        widgets = {
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0000001',
                'placeholder': 'Contoh: -4.5000000'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0000001',
                'placeholder': 'Contoh: 120.2000000'
            }),
            'altitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ketinggian dalam mdpl'
            }),
            'climate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Tropis'
            }),
            'rainfall': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Curah hujan dalam mm/tahun'
            }),
            'temperature_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Suhu minimum dalam °C'
            }),
            'temperature_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Suhu maksimum dalam °C'
            }),
            'topography': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Dataran rendah'
            }),
            'soil_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Alluvial'
            }),
            'boundary_north': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Batas utara'
            }),
            'boundary_south': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Batas selatan'
            }),
            'boundary_east': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Batas timur'
            }),
            'boundary_west': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Batas barat'
            })
        }
        labels = {
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'altitude': 'Ketinggian (mdpl)',
            'climate': 'Jenis Iklim',
            'rainfall': 'Curah Hujan (mm/tahun)',
            'temperature_min': 'Suhu Minimum (°C)',
            'temperature_max': 'Suhu Maksimum (°C)',
            'topography': 'Topografi',
            'soil_type': 'Jenis Tanah',
            'boundary_north': 'Batas Utara',
            'boundary_south': 'Batas Selatan',
            'boundary_east': 'Batas Timur',
            'boundary_west': 'Batas Barat'
        }
    
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise forms.ValidationError('Latitude harus antara -90 dan 90')
        return latitude
    
    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise forms.ValidationError('Longitude harus antara -180 dan 180')
        return longitude


class VillageDemographyForm(forms.ModelForm):
    """Form untuk mengelola data demografi desa"""
    
    class Meta:
        model = VillageDemography
        fields = [
            'total_population', 'male_population', 'female_population',
            'total_families', 'population_density', 'growth_rate', 'year',
            'age_0_14', 'age_15_64', 'age_65_plus', 'education_none',
            'education_elementary', 'education_junior', 'education_senior',
            'education_higher', 'employed'
        ]
        widgets = {
            'total_population': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total penduduk'
            }),
            'male_population': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah laki-laki'
            }),
            'female_population': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah perempuan'
            }),
            'total_families': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah kepala keluarga'
            }),
            'population_density': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Kepadatan penduduk per km²'
            }),
            'growth_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Tingkat pertumbuhan dalam %'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tahun data'
            }),
            'age_0_14': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usia 0-14 tahun'
            }),
            'age_15_64': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usia 15-64 tahun'
            }),
            'age_65_plus': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usia 65+ tahun'
            }),
            'education_none': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tidak sekolah'
            }),
            'education_elementary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'SD'
            }),
            'education_junior': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'SMP'
            }),
            'education_senior': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'SMA'
            }),
            'education_higher': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Perguruan Tinggi'
            }),
            'employed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bekerja'
            })
        }
        labels = {
            'total_population': 'Total Penduduk',
            'male_population': 'Laki-laki',
            'female_population': 'Perempuan',
            'total_families': 'Jumlah KK',
            'population_density': 'Kepadatan (jiwa/km²)',
            'growth_rate': 'Tingkat Pertumbuhan (%)',
            'year': 'Tahun Data',
            'age_0_14': 'Usia 0-14 tahun',
            'age_15_64': 'Usia 15-64 tahun',
            'age_65_plus': 'Usia 65+ tahun',
            'education_none': 'Tidak Sekolah',
            'education_elementary': 'SD',
            'education_junior': 'SMP',
            'education_senior': 'SMA',
            'education_higher': 'Perguruan Tinggi',
            'employed': 'Bekerja'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_population'].required = True
        self.fields['male_population'].required = True
        self.fields['female_population'].required = True
        self.fields['year'].required = True

    def clean(self):
        cleaned_data = super().clean()
        male = cleaned_data.get('male_population', 0)
        female = cleaned_data.get('female_population', 0)
        total = cleaned_data.get('total_population', 0)
        
        if male and female and total and (male + female) != total:
            raise forms.ValidationError(
                'Jumlah laki-laki + perempuan harus sama dengan total populasi'
            )
        
        year = cleaned_data.get('year')
        if year and (year < 1900 or year > 2100):
            raise forms.ValidationError('Tahun harus antara 1900 dan 2100')
        
        return cleaned_data


class VillageOfficialForm(forms.ModelForm):
    """Form untuk mengelola perangkat desa"""
    
    GENDER_CHOICES = [
        ('', 'Pilih Jenis Kelamin'),
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('', 'Pilih Status Perkawinan'),
        ('BELUM_KAWIN', 'Belum Kawin'),
        ('KAWIN', 'Kawin'),
        ('CERAI_HIDUP', 'Cerai Hidup'),
        ('CERAI_MATI', 'Cerai Mati'),
    ]
    
    class Meta:
        model = VillageOfficial
        fields = [
            'name', 'position', 'custom_position', 'phone', 'email', 'photo', 
            'nik', 'birth_date', 'birth_place', 'gender', 'religion', 'education',
            'occupation', 'marital_status', 'experience', 'mobile', 'address',
            'dusun', 'lorong', 'rt_number', 'rw_number', 'house_number', 'postal_code',
            'start_date', 'end_date', 'is_active', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama lengkap'
            }),
            'position': forms.Select(attrs={
                'class': 'form-control'
            }),
            'custom_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jabatan khusus (jika memilih Lainnya)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor telepon'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor handphone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'nik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor Induk Kependudukan',
                'maxlength': '16'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'birth_place': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tempat lahir'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'religion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Agama'
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pendidikan terakhir'
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pekerjaan'
            }),
            'marital_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pengalaman kerja'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Alamat lengkap'
            }),
            'dusun': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dusun'
            }),
            'lorong': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lorong'
            }),
            'rt_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RT'
            }),
            'rw_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RW'
            }),
            'house_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor rumah'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kode pos'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Urutan tampil'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': 'Nama Lengkap',
            'position': 'Jabatan',
            'custom_position': 'Jabatan Khusus',
            'phone': 'Telepon',
            'mobile': 'Handphone',
            'email': 'Email',
            'photo': 'Foto',
            'nik': 'NIK',
            'birth_date': 'Tanggal Lahir',
            'birth_place': 'Tempat Lahir',
            'gender': 'Jenis Kelamin',
            'religion': 'Agama',
            'education': 'Pendidikan',
            'occupation': 'Pekerjaan',
            'marital_status': 'Status Perkawinan',
            'experience': 'Pengalaman',
            'address': 'Alamat',
            'dusun': 'Dusun',
            'lorong': 'Lorong',
            'rt_number': 'RT',
            'rw_number': 'RW',
            'house_number': 'Nomor Rumah',
            'postal_code': 'Kode Pos',
            'start_date': 'Tanggal Mulai Jabatan',
            'end_date': 'Tanggal Berakhir Jabatan',
            'display_order': 'Urutan Tampil',
            'is_active': 'Status Aktif'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['position'].required = True
        self.fields['start_date'].required = True
        
        # Set choices for select fields
        self.fields['gender'].choices = self.GENDER_CHOICES
        self.fields['marital_status'].choices = self.MARITAL_STATUS_CHOICES


class VillageFacilityForm(forms.ModelForm):
    """Form untuk mengelola fasilitas desa"""
    
    class Meta:
        model = VillageFacility
        fields = [
            'name', 'type', 'condition', 'description', 'location', 'capacity',
            'image', 'manager', 'contact_person', 'contact_phone', 'operational_hours',
            'built_year', 'last_renovation', 'is_active', 'is_public'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama fasilitas'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi fasilitas'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lokasi fasilitas'
            }),
            'capacity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kapasitas'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'manager': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pengelola fasilitas'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Penanggung jawab'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor telepon kontak'
            }),
            'operational_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jam operasional (contoh: 08:00-17:00)'
            }),
            'built_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tahun dibangun'
            }),
            'last_renovation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': 'Nama Fasilitas',
            'type': 'Jenis Fasilitas',
            'condition': 'Kondisi',
            'description': 'Deskripsi',
            'location': 'Lokasi',
            'capacity': 'Kapasitas',
            'image': 'Gambar',
            'manager': 'Pengelola',
            'contact_person': 'Penanggung Jawab',
            'contact_phone': 'Telepon Kontak',
            'operational_hours': 'Jam Operasional',
            'built_year': 'Tahun Dibangun',
            'last_renovation': 'Renovasi Terakhir',
            'is_active': 'Status Aktif',
            'is_public': 'Fasilitas Umum'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['type'].required = True
        self.fields['condition'].required = True
        self.fields['description'].required = True
        self.fields['location'].required = True


class VillageHistoryForm(forms.ModelForm):
    """Form untuk mengelola sejarah desa"""
    
    class Meta:
        model = VillageHistory
        fields = [
            'title', 'history_type', 'year_start', 'year_end', 'summary',
            'content', 'featured_image', 'author', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul sejarah'
            }),
            'history_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'year_start': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tahun mulai'
            }),
            'year_end': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tahun selesai'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ringkasan sejarah'
            }),
            'content': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Konten lengkap sejarah'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Penulis'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Judul',
            'history_type': 'Jenis Sejarah',
            'year_start': 'Tahun Mulai',
            'year_end': 'Tahun Selesai',
            'summary': 'Ringkasan',
            'content': 'Konten',
            'featured_image': 'Gambar Utama',
            'author': 'Penulis',
            'is_featured': 'Featured',
            'is_active': 'Status Aktif'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['history_type'].required = True
        self.fields['year_start'].required = True


class VillagePhotoForm(forms.ModelForm):
    """Form untuk mengelola galeri foto desa"""
    
    class Meta:
        model = VillagePhoto
        fields = [
            'title', 'photo_type', 'description', 'image', 'is_featured',
            'is_active', 'display_order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul foto'
            }),
            'photo_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi foto'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Urutan tampil'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Judul Foto',
            'photo_type': 'Jenis Foto',
            'description': 'Deskripsi',
            'image': 'Gambar',
            'display_order': 'Urutan Tampil',
            'is_featured': 'Featured',
            'is_active': 'Status Aktif'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['photo_type'].required = True
        self.fields['image'].required = True