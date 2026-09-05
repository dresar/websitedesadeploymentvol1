from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import (
    BeneficiaryCategory,
    Beneficiary,
    Aid,
    AidDistribution,
    BeneficiaryVerification
)


class BeneficiaryCategoryForm(forms.ModelForm):
    class Meta:
        model = BeneficiaryCategory
        fields = ['name', 'description', 'criteria', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
            'criteria': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = [
            'person', 'category', 'registration_date', 'status', 'economic_status',
            'monthly_income', 'family_members_count', 'house_condition',
            'special_needs', 'verification_date', 'notes'
        ]
        widgets = {
            'person': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'economic_status': forms.Select(attrs={'class': 'form-control'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'family_members_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'house_condition': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
            'special_needs': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
            'verification_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
        }


class AidForm(forms.ModelForm):
    class Meta:
        model = Aid
        fields = [
            'name', 'aid_type', 'source', 'description', 'value_per_beneficiary',
            'total_budget', 'target_beneficiaries', 'start_date', 'end_date',
            'requirements', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama program bantuan'}),
            'aid_type': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'description': SummernoteWidget(attrs={'summernote': {'height': 250, 'lang': 'id-ID'}}),
            'value_per_beneficiary': forms.NumberInput(attrs={'class': 'form-control', 'step': '1000', 'min': '0'}),
            'total_budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '1000', 'min': '0', 'readonly': True}),
            'target_beneficiaries': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'requirements': SummernoteWidget(attrs={'summernote': {'height': 250, 'lang': 'id-ID'}}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nama Program',
            'aid_type': 'Jenis Bantuan',
            'source': 'Sumber Dana',
            'description': 'Deskripsi Program',
            'value_per_beneficiary': 'Nilai per Penerima (Rp)',
            'total_budget': 'Total Anggaran (Rp)',
            'target_beneficiaries': 'Target Penerima',
            'start_date': 'Tanggal Mulai',
            'end_date': 'Tanggal Berakhir',
            'requirements': 'Persyaratan Penerima',
            'is_active': 'Program Aktif',
        }


class AidDistributionForm(forms.ModelForm):
    class Meta:
        model = AidDistribution
        fields = [
            'aid', 'beneficiary', 'distribution_date', 'amount_received',
            'status', 'receipt_number', 'notes'
        ]
        widgets = {
            'aid': forms.Select(attrs={'class': 'form-control'}),
            'beneficiary': forms.Select(attrs={'class': 'form-control'}),
            'distribution_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount_received': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
        }


class BeneficiaryVerificationForm(forms.ModelForm):
    class Meta:
        model = BeneficiaryVerification
        fields = [
            'beneficiary', 'verification_date', 'verification_status',
            'verification_notes', 'documents_checked', 'field_visit_conducted',
            'field_visit_notes', 'next_verification_date'
        ]
        widgets = {
            'beneficiary': forms.Select(attrs={'class': 'form-control'}),
            'verification_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'verification_status': forms.Select(attrs={'class': 'form-control'}),
            'verification_notes': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
            'documents_checked': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'field_visit_conducted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'field_visit_notes': SummernoteWidget(attrs={'summernote': {'height': 200, 'lang': 'id-ID'}}),
            'next_verification_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }