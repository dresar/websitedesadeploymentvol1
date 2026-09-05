from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django_summernote.widgets import SummernoteWidget
from .models import CustomUser, Role, MenuPermission, UserRole, UserProfile, DatabaseResetConfig, WebsiteSettings

User = get_user_model()


class UserForm(forms.ModelForm):
    """Form for creating and editing users"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Minimal 8 karakter'
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Masukkan password yang sama untuk konfirmasi'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'position', 'address', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if self.is_edit:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].help_text = 'Kosongkan jika tidak ingin mengubah password'
        else:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if not self.is_edit and (not password1 or not password2):
            raise forms.ValidationError('Password harus diisi untuk user baru.')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Password tidak sama.')
            if len(password1) < 8:
                raise forms.ValidationError('Password minimal 8 karakter.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form - kept for backward compatibility"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    position = forms.CharField(max_length=100, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    is_village_staff = forms.BooleanField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'position', 'address', 'is_village_staff', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.position = self.cleaned_data['position']
        user.address = self.cleaned_data['address']
        user.is_village_staff = self.cleaned_data['is_village_staff']
        
        if commit:
            user.save()
        return user


class RoleForm(forms.ModelForm):
    """Form for creating and editing roles"""
    
    class Meta:
        model = Role
        fields = ['name', 'display_name', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Nama unik untuk role (huruf kecil, underscore)'
        self.fields['display_name'].help_text = 'Nama yang ditampilkan untuk role'
        self.fields['description'].help_text = 'Deskripsi singkat tentang role ini'


class RolePermissionForm(forms.ModelForm):
    """Form for managing role permissions"""
    menu_permissions = forms.ModelMultipleChoiceField(
        queryset=MenuPermission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Pilih permission yang akan diberikan kepada role ini'
    )
    
    class Meta:
        model = Role
        fields = ['menu_permissions']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['menu_permissions'].initial = self.instance.menu_permissions.all()
    
    def save(self, commit=True):
        role = super().save(commit=False)
        if commit:
            role.save()
            role.menu_permissions.set(self.cleaned_data['menu_permissions'])
        return role


class UserRoleForm(forms.ModelForm):
    """Form for managing user roles"""
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Pilih role yang akan diberikan kepada user ini'
    )
    
    class Meta:
        model = CustomUser
        fields = ['roles']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['roles'].initial = self.instance.roles.all()
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.roles.set(self.cleaned_data['roles'])
        return user


class UserProfileForm(forms.ModelForm):
    """Form for user profile"""
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'address', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserEditForm(forms.ModelForm):
    """Form for editing user basic information"""
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'position', 'address', 'is_village_staff', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Nama pengguna untuk login'
        self.fields['email'].help_text = 'Email address user'
        self.fields['is_village_staff'].help_text = 'Centang jika user adalah staff desa'
        self.fields['is_active'].help_text = 'Centang jika user dapat login'


class PermissionFilterForm(forms.Form):
    """Form for filtering permissions"""
    module = forms.ChoiceField(
        choices=[('', 'Semua Module')] + MenuPermission.MODULE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    action = forms.ChoiceField(
        choices=[('', 'Semua Action')] + MenuPermission.ACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'Semua Status'), (True, 'Aktif'), (False, 'Non-Aktif')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RoleFilterForm(forms.Form):
    """Form for filtering roles"""
    name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cari role...'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'Semua Status'), (True, 'Aktif'), (False, 'Non-Aktif')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class DatabaseResetConfigForm(forms.ModelForm):
    """Form for database reset configuration"""
    
    class Meta:
        model = DatabaseResetConfig
        fields = [
            'name', 'description', 'reset_type',
            'reset_penduduk', 'reset_dusun', 'reset_lorong', 'reset_rt_rw',
            'reset_keluarga', 'reset_pelajar', 'reset_disabilitas',
            'reset_beneficiaries', 'reset_business', 'reset_complaints',
            'reset_documents', 'reset_tourism', 'reset_posyandu',
            'reset_news', 'reset_organization', 'reset_layanan', 'reset_letters',
            'backup_before_reset', 'keep_users', 'keep_settings', 'keep_media'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reset_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Group fields for better organization
        self.fields['name'].help_text = 'Nama konfigurasi reset database'
        self.fields['description'].help_text = 'Deskripsi konfigurasi reset'
        self.fields['reset_type'].help_text = 'Tipe reset yang akan dilakukan'
        
        # Core modules
        self.fields['reset_penduduk'].help_text = 'Reset data penduduk'
        self.fields['reset_dusun'].help_text = 'Reset data dusun'
        self.fields['reset_lorong'].help_text = 'Reset data lorong'
        self.fields['reset_rt_rw'].help_text = 'Reset data RT/RW'
        self.fields['reset_keluarga'].help_text = 'Reset data keluarga'
        self.fields['reset_pelajar'].help_text = 'Reset data pelajar'
        self.fields['reset_disabilitas'].help_text = 'Reset data disabilitas'
        
        # External modules
        self.fields['reset_beneficiaries'].help_text = 'Reset data penerima bantuan'
        self.fields['reset_business'].help_text = 'Reset data usaha'
        self.fields['reset_complaints'].help_text = 'Reset data keluhan'
        self.fields['reset_documents'].help_text = 'Reset data dokumen'
        self.fields['reset_tourism'].help_text = 'Reset data wisata'
        self.fields['reset_posyandu'].help_text = 'Reset data posyandu'
        self.fields['reset_news'].help_text = 'Reset data berita'
        self.fields['reset_organization'].help_text = 'Reset data organisasi'
        self.fields['reset_layanan'].help_text = 'Reset data layanan'
        self.fields['reset_letters'].help_text = 'Reset data surat menyurat'
        
        # Options
        self.fields['backup_before_reset'].help_text = 'Buat backup sebelum reset'
        self.fields['keep_users'].help_text = 'Tetap simpan data pengguna'
        self.fields['keep_settings'].help_text = 'Tetap simpan pengaturan'
        self.fields['keep_media'].help_text = 'Tetap simpan file media'
    
    def clean(self):
        cleaned_data = super().clean()
        reset_type = cleaned_data.get('reset_type')
        
        # Validate that at least one module is selected for selective reset
        if reset_type == 'selective':
            module_fields = [
                'reset_penduduk', 'reset_dusun', 'reset_lorong', 'reset_rt_rw',
                'reset_keluarga', 'reset_pelajar', 'reset_disabilitas',
                'reset_beneficiaries', 'reset_business', 'reset_complaints',
                'reset_documents', 'reset_tourism', 'reset_posyandu',
                'reset_news', 'reset_organization', 'reset_layanan', 'reset_letters'
            ]
            
            if not any(cleaned_data.get(field) for field in module_fields):
                raise forms.ValidationError(
                    'Untuk reset selektif, minimal satu modul harus dipilih.'
                )
        
        return cleaned_data


class SEOForm(forms.ModelForm):
    """Form for SEO settings"""
    
    class Meta:
        model = WebsiteSettings
        fields = [
            'site_title', 'site_description', 'site_keywords', 'site_author', 'site_language',
            'og_title', 'og_description', 'og_image',
            'google_analytics_id', 'google_tag_manager_id', 'facebook_pixel_id', 'enable_facebook_tracking',
            'google_search_console', 'bing_webmaster',
            'enable_sitemap', 'enable_robots_txt', 'robots_content'
        ]
        widgets = {
            'site_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website Desa Pulo Sarok',
                'maxlength': '60'
            }),
            'site_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi singkat tentang website desa Pulo Sarok...',
                'maxlength': '160',
                'rows': '3'
            }),
            'site_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'desa, pulo sarok, aceh singkil, website, informasi',
                'maxlength': '200'
            }),
            'site_author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tim Website Pulo Sarok'
            }),
            'site_language': forms.Select(attrs={
                'class': 'form-control'
            }),
            'og_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website Desa Pulo Sarok - Aceh Singkil',
                'maxlength': '200'
            }),
            'og_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi untuk media sosial...',
                'rows': '3'
            }),
            'og_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'google_analytics_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GA-XXXXXXXXX',
                'maxlength': '50'
            }),
            'google_tag_manager_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GTM-XXXXXXX',
                'maxlength': '50'
            }),
            'facebook_pixel_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789012345',
                'maxlength': '50'
            }),
            'enable_facebook_tracking': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'google_search_console': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Verification code',
                'maxlength': '100'
            }),
            'bing_webmaster': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Verification code',
                'maxlength': '100'
            }),
            'enable_sitemap': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'enable_robots_txt': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'robots_content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /private/',
                'rows': '10'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default values for new instances
        if not self.instance.pk:
            self.fields['site_title'].initial = 'Website Desa Pulo Sarok - Aceh Singkil'
            self.fields['site_description'].initial = 'Website resmi Desa Pulo Sarok, Kecamatan Singkil, Kabupaten Aceh Singkil. Menyediakan informasi lengkap tentang desa, layanan administrasi, pantai wisata, hutan mangrove, dan kegiatan masyarakat.'
            self.fields['site_keywords'].initial = 'desa pulo sarok, aceh singkil, singkil, pantai pulo sarok, hutan mangrove, wisata aceh, website desa, layanan administrasi, kecamatan singkil, kabupaten aceh singkil'
            self.fields['site_author'].initial = 'Tim Website Pulo Sarok'
            self.fields['site_language'].initial = 'id'
            self.fields['og_title'].initial = 'Website Desa Pulo Sarok - Wisata Pantai & Hutan Mangrove Aceh Singkil'
            self.fields['og_description'].initial = 'Website resmi Desa Pulo Sarok yang menyediakan informasi lengkap tentang desa, layanan administrasi, pantai wisata dengan pasir putih, hutan mangrove, dan kegiatan masyarakat di Kecamatan Singkil, Kabupaten Aceh Singkil.'
            self.fields['robots_content'].initial = 'User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /private/\n\nSitemap: https://pulosarok.my.id/sitemap.xml'

    def clean_site_title(self):
        title = self.cleaned_data.get('site_title')
        if title and len(title) > 60:
            raise forms.ValidationError('Judul website maksimal 60 karakter.')
        return title

    def clean_site_description(self):
        description = self.cleaned_data.get('site_description')
        if description and len(description) > 160:
            raise forms.ValidationError('Deskripsi website maksimal 160 karakter.')
        return description


class MaintenanceModeForm(forms.ModelForm):
    """Form for maintenance mode settings"""
    
    class Meta:
        model = WebsiteSettings
        fields = ['enable_maintenance_mode', 'maintenance_message']
        widgets = {
            'maintenance_message': SummernoteWidget(attrs={
                'summernote': {
                    'height': 200,
                    'lang': 'id-ID',
                    'toolbar': [
                        ['style', ['style']],
                        ['font', ['bold', 'italic', 'underline', 'clear']],
                        ['fontname', ['fontname']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['table', ['table']],
                        ['insert', ['link', 'picture']],
                        ['view', ['fullscreen', 'codeview', 'help']]
                    ]
                }
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enable_maintenance_mode'].help_text = 'Aktifkan mode maintenance untuk menampilkan halaman maintenance kepada pengunjung'
        self.fields['maintenance_message'].help_text = 'Pesan yang akan ditampilkan kepada pengunjung saat mode maintenance aktif'

