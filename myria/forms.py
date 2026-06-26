from django import forms
from .models import Car
import datetime

def get_years_choices():
    current_year = datetime.date.today().year
    years = [(str(y), str(y)) for y in range(current_year, 1899, -1)]
    return [('', 'Оберіть')] + years

class CarForm(forms.ModelForm):
    transport_type = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    mileage = forms.IntegerField(
        min_value=0, 
        widget=forms.NumberInput(attrs={
            'placeholder': 'тис. км',
            'min': '0',       
            'step': '1',      
            'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'
        })
    )

    price = forms.DecimalField(
        min_value=1, 
        widget=forms.NumberInput(attrs={
            'min': '0',       
            'step': '1',      
            'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'
        })
    )
    
    class Meta:
        model = Car
        exclude = ['seller', 'main_photo']
        
        widgets = {
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
            'year': forms.Select(choices=get_years_choices()),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from .models import Brand
        existing_types = Brand.objects.values_list('transport_type', flat=True).distinct()
        dynamic_choices = [('', 'Оберіть')] + [(t, t) for t in existing_types if t]
        self.fields['transport_type'].choices = dynamic_choices
        
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = "Оберіть"
            
            elif isinstance(field, forms.ChoiceField) and field_name != 'transport_type' and field_name != 'year':
                if field.choices and field.choices[0][0] == '':
                    current_choices = list(field.choices)
                    current_choices[0] = ('', 'Оберіть')
                    field.choices = current_choices