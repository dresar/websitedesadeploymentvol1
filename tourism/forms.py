from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select, NumberInput, CheckboxInput, FileInput, ClearableFileInput
from django_summernote.widgets import SummernoteWidget
from .models import (
    TourismCategory, TourismLocation, TourismGallery, TourismPackageGallery,
    TourismReview, TourismRating, TourismEvent, 
    TourismPackage, TourismFAQ
)

class TourismCategoryForm(ModelForm):
    class Meta:
        model = TourismCategory
        fields = ['name', 'slug', 'description', 'icon', 'color', 'image', 'meta_title', 'meta_description', 'meta_keywords', 'is_active', 'is_featured']
        widgets = {
            'name': TextInput(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base',
                'placeholder': 'Masukkan nama kategori wisata'
            }),
            'description': SummernoteWidget(attrs={
                'summernote': {'height': 200, 'lang': 'id-ID'},
                'placeholder': 'Deskripsi kategori wisata'
            }),
            'icon': TextInput(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base',
                'placeholder': 'Contoh: fas fa-mountain'
            }),
            'color': TextInput(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base',
                'type': 'color'
            }),
            'meta_title': TextInput(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base',
                'placeholder': 'Judul untuk SEO (maksimal 60 karakter)',
                'maxlength': '60'
            }),
            'meta_description': Textarea(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base',
                'rows': 2,
                'placeholder': 'Deskripsi untuk SEO (maksimal 160 karakter)',
                'maxlength': '160'
            }),
            'meta_keywords': TextInput(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base',
                'placeholder': 'Kata kunci untuk SEO (pisahkan dengan koma)'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 sm:h-5 sm:w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'is_featured': CheckboxInput(attrs={
                'class': 'h-4 w-4 sm:h-5 sm:w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }

class TourismLocationForm(ModelForm):
    # Multiple images field
    gallery_images = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'accept': 'image/*'
        }),
        required=False,
        help_text='Pilih beberapa gambar untuk galeri (opsional)'
    )
    
    class Meta:
        model = TourismLocation
        fields = [
            'title', 'slug', 'category', 'location_type', 'short_description', 
            'full_description', 'address', 'latitude', 'longitude', 'opening_hours',
            'entry_fee', 'contact_phone', 'contact_email', 'website', 'facilities',
            'activities', 'status', 'featured', 'is_active', 'meta_title',
            'meta_description', 'meta_keywords', 'main_image', 'hero_image'
        ]
        widgets = {
            'title': TextInput(attrs={
                'class': 'w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base tourism-form',
                'placeholder': 'Judul lokasi wisata'
            }),
            'slug': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'slug-url-otomatis'
            }),
            'category': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'location_type': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'short_description': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Deskripsi singkat lokasi wisata'
            }),
            'full_description': SummernoteWidget(attrs={
                'summernote': {'height': 200, 'lang': 'id-ID'},
                'placeholder': 'Deskripsi lengkap lokasi wisata'
            }),
            'address': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Alamat lengkap lokasi wisata'
            }),
            'latitude': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': 'any',
                'placeholder': 'Latitude (opsional)'
            }),
            'longitude': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': 'any',
                'placeholder': 'Longitude (opsional)'
            }),
            'opening_hours': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Contoh: Senin-Jumat 08:00-17:00'
            }),
            'entry_fee': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Biaya masuk (opsional)'
            }),
            'contact_phone': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nomor telepon kontak'
            }),
            'contact_email': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'email',
                'placeholder': 'Email kontak'
            }),
            'website': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'url',
                'placeholder': 'Website resmi (opsional)'
            }),
            'facilities': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Fasilitas yang tersedia (JSON format)'
            }),
            'activities': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Aktivitas yang tersedia (JSON format)'
            }),
            'status': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'featured': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'meta_title': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'maxlength': 60,
                'placeholder': 'Meta title untuk SEO (maksimal 60 karakter)'
            }),
            'meta_description': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'maxlength': 160,
                'placeholder': 'Meta description untuk SEO (maksimal 160 karakter)'
            }),
            'meta_keywords': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Kata kunci untuk SEO (pisahkan dengan koma)'
            }),
            'main_image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'hero_image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            })
        }

class TourismGalleryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set media_type as not required (always use default 'image')
        if 'media_type' in self.fields:
            self.fields['media_type'].required = False
            # Hide media_type field since we only support images for now
            self.fields['media_type'].widget = self.fields['media_type'].hidden_widget()
    
    def clean(self):
        cleaned_data = super().clean()
        tourism_location = cleaned_data.get('tourism_location')
        image = cleaned_data.get('image')
        
        # Validate required fields
        if not tourism_location:
            raise forms.ValidationError('⚠️ Mohon pilih lokasi wisata terlebih dahulu.')
        
        # Validate image for new gallery (not editing)
        if not self.instance.pk and not image:
            raise forms.ValidationError('⚠️ Mohon upload gambar untuk gallery.')
        
        return cleaned_data
    
    class Meta:
        model = TourismGallery
        fields = [
            'tourism_location', 'media_type', 'title', 'description', 
            'image', 'alt_text', 'caption', 'is_featured', 'is_active', 'order'
        ]
        widgets = {
            'tourism_location': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'media_type': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'title': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Judul gambar'
            }),
            'description': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Deskripsi gambar'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'alt_text': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Alt text untuk aksesibilitas'
            }),
            'caption': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Caption gambar'
            }),
            'order': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Urutan tampilan'
            }),
            'is_featured': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            })
        }

class TourismPackageGalleryForm(ModelForm):
    class Meta:
        model = TourismPackageGallery
        fields = [
            'package', 'title', 'description', 
            'image', 'order', 'is_active'
        ]
        widgets = {
            'package': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'title': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Judul gambar'
            }),
            'description': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Deskripsi gambar'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'order': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Urutan tampilan'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            })
        }

class TourismReviewForm(ModelForm):
    class Meta:
        model = TourismReview
        fields = ['rating', 'title', 'comment', 'image', 'visit_date', 'visit_type']
        widgets = {
            'rating': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'title': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Judul review Anda'
            }),
            'comment': SummernoteWidget(attrs={
                'summernote': {'height': 200, 'lang': 'id-ID'},
                'placeholder': 'Bagikan pengalaman Anda mengunjungi tempat ini...'
            }),
            'image': FileInput(attrs={
                'class': 'w-full',
                'accept': 'image/*'
            }),
            'visit_date': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'visit_type': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
        }

class AnonymousReviewForm(forms.Form):
    """Form for anonymous reviews"""
    visitor_name = forms.CharField(
        max_length=100,
        widget=TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-dark-700 dark:text-white',
            'placeholder': 'Nama Anda'
        })
    )
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Bintang') for i in range(1, 6)],
        widget=Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-dark-700 dark:text-white'
        })
    )
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-dark-700 dark:text-white',
            'placeholder': 'Judul Review (opsional)'
        })
    )
    comment = forms.CharField(
        widget=SummernoteWidget(attrs={
            'summernote': {'height': 200, 'lang': 'id-ID'},
            'placeholder': 'Ceritakan pengalaman Anda...'
        })
    )
    image = forms.ImageField(
        required=False,
        widget=FileInput(attrs={
            'class': 'w-full',
            'accept': 'image/*'
        })
    )

class TourismRatingForm(ModelForm):
    class Meta:
        model = TourismRating
        fields = ['rating', 'cleanliness', 'accessibility', 'facilities', 'service', 'value']
        widgets = {
            'rating': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'cleanliness': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'accessibility': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'facilities': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'service': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'value': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
        }

class TourismEventForm(ModelForm):
    class Meta:
        model = TourismEvent
        fields = [
            'title', 'slug', 'tourism_location', 'event_type', 'description', 
            'start_date', 'end_date', 'start_time', 'end_time', 'organizer', 
            'contact_person', 'phone', 'email', 'contact_info',
            'registration_required', 'registration_deadline', 'max_participants',
            'registration_fee', 'registration_link', 'image', 'hero_image', 
            'hero_video', 'hero_youtube', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Judul event wisata'
            }),
            'slug': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'slug-url-otomatis'
            }),
            'tourism_location': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'event_type': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'description': SummernoteWidget(attrs={
                'summernote': {'height': 200, 'lang': 'id-ID'},
                'placeholder': 'Deskripsi lengkap event'
            }),
            'start_date': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'datetime-local'
            }),
            'end_date': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'datetime-local'
            }),
            'start_time': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'time'
            }),
            'end_time': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'time'
            }),
            'contact_person': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nama kontak person'
            }),
            'phone': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nomor telepon'
            }),
            'email': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'email',
                'placeholder': 'Email kontak'
            }),
            'registration_deadline': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'datetime-local'
            }),
            'max_participants': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': 1,
                'placeholder': 'Maksimal peserta'
            }),
            'registration_fee': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Biaya pendaftaran'
            }),
            'registration_link': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'url',
                'placeholder': 'Link pendaftaran'
            }),
            'organizer': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nama penyelenggara event'
            }),
            'contact_info': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Informasi kontak untuk event'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'hero_image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'hero_video': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'video/*'
            }),
            'hero_youtube': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'url',
                'placeholder': 'Link YouTube untuk hero section'
            }),
            'is_featured': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }

class TourismPackageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields optional (not required)
        self.fields['currency'].required = False
        self.fields['includes'].required = False
        self.fields['excludes'].required = False
        self.fields['itinerary'].required = False
    
    def clean_price(self):
        """Clean and validate price field - handle Rupiah format"""
        price = self.cleaned_data.get('price')
        
        if price:
            # Convert to string first
            price_str = str(price)
            
            # Remove any dots (thousand separators) and spaces
            price_str = price_str.replace('.', '').replace(' ', '').strip()
            
            # Try to convert to decimal
            try:
                from decimal import Decimal, InvalidOperation
                price_decimal = Decimal(price_str)
                
                # Validate positive value
                if price_decimal < 0:
                    raise forms.ValidationError('Harga tidak boleh negatif.')
                
                return price_decimal
            except (ValueError, InvalidOperation):
                raise forms.ValidationError('Format harga tidak valid. Gunakan angka saja (contoh: 150000).')
        
        return price
    
    class Meta:
        model = TourismPackage
        fields = [
            'title', 'slug', 'tourism_location', 'package_type', 'description', 
            'duration', 'price', 'currency', 'whatsapp', 'website',
            'image', 'video', 'youtube_link', 'hero_image', 'hero_video', 'hero_youtube',
            'includes', 'excludes', 'itinerary', 
            'max_participants', 'min_participants', 'booking_deadline', 
            'is_featured', 'is_active'
        ]
        widgets = {
            'title': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Judul paket wisata'
            }),
            'slug': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'slug-url-otomatis'
            }),
            'tourism_location': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'package_type': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'description': SummernoteWidget(attrs={
                'summernote': {'height': 200, 'lang': 'id-ID'},
                'placeholder': 'Deskripsi lengkap paket wisata'
            }),
            'duration': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Contoh: 2 hari 1 malam'
            }),
            'price': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Contoh: 150000 (akan otomatis diformat menjadi 150.000)',
                'inputmode': 'numeric'
            }),
            'currency': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'includes': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Yang termasuk dalam paket (JSON format)'
            }),
            'excludes': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Yang tidak termasuk dalam paket (JSON format)'
            }),
            'itinerary': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Itinerary perjalanan (JSON format)'
            }),
            'max_participants': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': 1,
                'placeholder': 'Maksimal peserta'
            }),
            'min_participants': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': 1,
                'placeholder': 'Minimal peserta'
            }),
            'booking_deadline': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': 1,
                'placeholder': 'Deadline booking dalam hari'
            }),
            'whatsapp': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nomor WhatsApp (contoh: 6281234567890)'
            }),
            'website': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'url',
                'placeholder': 'Website atau portofolio paket'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'video': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'video/*'
            }),
            'youtube_link': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'url',
                'placeholder': 'Link YouTube dokumentasi paket'
            }),
            'hero_image': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'hero_video': ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'video/*'
            }),
            'hero_youtube': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'url',
                'placeholder': 'Link YouTube untuk hero section'
            }),
            'is_featured': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }

class TourismFAQForm(ModelForm):
    class Meta:
        model = TourismFAQ
        fields = ['tourism_location', 'question', 'answer', 'category', 'order', 'is_active']
        widgets = {
            'tourism_location': Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'question': Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Pertanyaan yang sering diajukan'
            }),
            'answer': SummernoteWidget(attrs={
                'summernote': {'height': 200, 'lang': 'id-ID'},
                'placeholder': 'Masukkan jawaban lengkap untuk FAQ...'
            }),
            'category': TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Kategori FAQ (opsional)'
            }),
            'order': NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'min': 0,
                'placeholder': 'Urutan tampilan'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }
