from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import PosyanduLocation, PosyanduSchedule, HealthRecord, Immunization, NutritionData


class PosyanduLocationForm(forms.ModelForm):
    class Meta:
        model = PosyanduLocation
        fields = '__all__'
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'facilities': SummernoteWidget(),
            'image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control-file'}),
        }


class PosyanduScheduleForm(forms.ModelForm):
    class Meta:
        model = PosyanduSchedule
        fields = '__all__'
        widgets = {
            'schedule_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': SummernoteWidget(),
            'notes': SummernoteWidget(),
        }


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = '__all__'
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'next_visit': forms.DateInput(attrs={'type': 'date'}),
            'complaints': SummernoteWidget(),
            'diagnosis': SummernoteWidget(),
            'treatment': SummernoteWidget(),
        }


class ImmunizationForm(forms.ModelForm):
    class Meta:
        model = Immunization
        fields = '__all__'
        widgets = {
            'immunization_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'next_dose_date': forms.DateInput(attrs={'type': 'date'}),
            'side_effects': SummernoteWidget(),
        }


class NutritionDataForm(forms.ModelForm):
    class Meta:
        model = NutritionData
        fields = '__all__'
        widgets = {
            'measurement_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': SummernoteWidget(),
        }