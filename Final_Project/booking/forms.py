from django import forms
from django.forms import ModelForm
from .models import PropertyType, Listing
from datetime import date, timedelta

class DateInput(forms.DateInput):
    input_type = 'date'

class PropertyFilter(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertyFilter, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = Listing
        fields = ("type", "availability_from", "availability_to", "price_per_night")

        required = (
            'type',
            'availability_from',
            'availability_to',
            'price_per_night'
        )

        labels = {
                "type": 'Property Type',
                "availability_from": 'From',
                "availability_to": 'To',
                "price_per_night": 'Max price per night'
        }
        
        widgets = {
            "type": forms.Select(attrs={'class':'form-control'}),
            "availability_from": DateInput(attrs={'class':'form-control'}),
            "availability_to": DateInput(attrs={'class':'form-control'}),
            "price_per_night": forms.NumberInput(attrs={'class':'form-control', 'placeholder': ''})
        }

    def clean(self):
        cleaned_data = super().clean()
        afrom = cleaned_data.get("availability_from")
        ato = cleaned_data.get("availability_to")
        price = cleaned_data.get("price_per_night")
        errors = []
        
        if price is not None and price <= 0:
                errors.append(forms.ValidationError("Invalid Price"))

        if afrom is not None and ato is not None and afrom > ato:
                errors.append(forms.ValidationError("Invalid date. Start date has to be before End date."))
        
        if afrom is not None and afrom < date.today() or ato is not None and ato < date.today():
             errors.append(forms.ValidationError("Invalid date. Can't select dates before today."))
        
        if errors:
            raise forms.ValidationError(errors)
        
        return cleaned_data


class AddProperty(ModelForm):
    class Meta:
        model = Listing
        fields = (
            "type",
            "title",
            "price_per_night",
            "imageurl",
            "location",
            "availability_from",
            "availability_to",
            "description"
            )
        
        labels = {
            "title": '',
            "type": 'Type of Property',
            "price_per_night": '',
            "imageurl": '',
            "location": '',
            "availability_from": 'Available from',
            "availability_to": 'Available to',
            "description": ''
        }

        widgets = {
            "type": forms.Select(attrs={'class': 'form-control'}),
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            "price_per_night": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price (for each night)'}),
            "imageurl": forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL with property photo'}),
            "location": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (Town) of the property'}),
            "availability_from": DateInput(attrs={'class': 'form-control'}),
            "availability_to": DateInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description...'})
        }