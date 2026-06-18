from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['seller', 'main_photo']
        
        widgets = {
            'transport_type': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'imported_from': forms.Select(attrs={'class': 'form-select'}),
            'accident': forms.Select(attrs={'class': 'form-select'}),
            'conditioner': forms.Select(attrs={'class': 'form-select'}),
            'windows': forms.Select(attrs={'class': 'form-select'}),
            'interior_material': forms.Select(attrs={'class': 'form-select'}),
            'interior_color': forms.Select(attrs={'class': 'form-select'}),
            'steering_assist': forms.Select(attrs={'class': 'form-select'}),
            'steering_adjustment': forms.Select(attrs={'class': 'form-select'}),
            'spare_wheel': forms.Select(attrs={'class': 'form-select'}),
            'headlights': forms.Select(attrs={'class': 'form-select'}),
            'seat_height': forms.Select(attrs={'class': 'form-select'}),
            'seat_memory': forms.Select(attrs={'class': 'form-select'}),
            'seat_heating': forms.Select(attrs={'class': 'form-select'}),
            'seat_ventilation': forms.Select(attrs={'class': 'form-select'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
        }