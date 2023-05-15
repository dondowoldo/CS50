from django import forms
from django.forms import ModelForm
from .models import User, PropertyType, Listing


class CreatePropType(ModelForm):
    class Meta:
        model = PropertyType
        fields = ("type",)

class DateInput(forms.DateInput):
    input_type = 'date'

class PropertyFilter(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertyFilter, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = Listing
        fields = ("type", "availability_from", "availability_to", "price_per_day")

        required = (
            'type',
            'availability_from',
            'availability_to',
            'price_per_day'
        )

        labels = {
                "type": 'Property Type ',
                "availability_from": 'From ',
                "availability_to": 'To ',
                "price_per_day": 'Max price per day '
        }
        
        widgets = {
            "type": forms.Select(attrs={'class':'form-control'}),
            "availability_from": DateInput(attrs={'class':'form-control'}),
            "availability_to": DateInput(attrs={'class':'form-control'}),
            "price_per_day": forms.NumberInput(attrs={'class':'form-control', 'placeholder': '$'})
        }
