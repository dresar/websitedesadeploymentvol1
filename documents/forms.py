from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Document, DocumentCategory, DocumentComment

class DocumentForm(forms.ModelForm):
    """Form untuk Create & Edit Dokumen Transparansi"""
    
    class Meta:
        model = Document
        fields = [
            'title', 'category', 'document_number', 'document_year',
            'description', 'summary', 'file', 'thumbnail',
            'status', 'is_public', 'is_featured', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: APBDES Tahun 2025'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 01/APBDES/2025 (opsional)'
            }),
            'document_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2025',
                'min': '2000',
                'max': '2100'
            }),
            'description': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi lengkap dokumen...'
            }),
            'summary': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Ringkasan singkat untuk tampilan publik (opsional)'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xlsx,.xls'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pisahkan dengan koma. Contoh: anggaran, 2025, keuangan'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default values for new documents
        if not self.instance.pk:
            self.fields['status'].initial = 'draft'
            self.fields['is_public'].initial = True
            self.fields['document_year'].initial = 2025


class DocumentCategoryForm(forms.ModelForm):
    """Form untuk Create & Edit Kategori Dokumen"""
    
    class Meta:
        model = DocumentCategory
        fields = ['name', 'category_type', 'description', 'icon', 'display_order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama kategori'
            }),
            'category_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': SummernoteWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi kategori (opsional)'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fa-file (FontAwesome icon class)'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class DocumentCommentForm(forms.ModelForm):
    """Form untuk Komentar Publik"""
    
    class Meta:
        model = DocumentComment
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tulis komentar atau feedback Anda...'
            }),
        }


class DocumentSearchForm(forms.Form):
    """Form untuk Pencarian Dokumen"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari dokumen...',
            'aria-label': 'Search'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False,
        empty_label='Semua Kategori',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Semua Status')] + Document.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tahun',
            'min': '2000',
            'max': '2100'
        })
    )
