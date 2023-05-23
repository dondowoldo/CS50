from django import forms
from django.forms import ModelForm
from .models import Listing, Comment, Booking
from datetime import timedelta, datetime
import geocoder
#import pytz

# Set timezone if necessary
# tz = pytz.timezone('Europe/Prague')

class DateInput(forms.DateInput):
    input_type = 'date'
    
    def get_context(self, name, value, attrs):
        attrs.setdefault('min', datetime.now().strftime('%Y-%m-%d'))
        return super().get_context(name, value, attrs)  


class PropertyFilter(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertyFilter, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = Listing
        fields = ("title", "type", "availability_from", "availability_to", "price_per_night")

        required = (
            'title',
            'type',
            'availability_from',
            'availability_to',
            'price_per_night'
        )

        labels = {
                "title": '',
                "type": 'Property Type',
                "availability_from": 'From',
                "availability_to": 'To',
                "price_per_night": 'Max price per night'
        }
        
        widgets = {
            "title": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search by title..'}),
            "type": forms.Select(attrs={'class':'form-control'}),
            "availability_from": DateInput(attrs={'class':'form-control'}),
            "availability_to": DateInput(attrs={'class':'form-control'}),
            "price_per_night": forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Maximum price / night'})
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
        
        if afrom is not None and afrom < datetime.now().date() or ato is not None and ato < datetime.now().date():
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
    
    def clean(self):
        cleaned_data = super().clean()
        afrom = cleaned_data.get("availability_from")
        ato = cleaned_data.get("availability_to")
        price = cleaned_data.get("price_per_night")
        location = cleaned_data.get("location")
        errors = []
        
        geocode = geocoder.osm(location)
        if not geocode:
                errors.append(forms.ValidationError("Not a Valid location"))              
        if price <= 0:
            errors.append(forms.ValidationError("Invalid Price"))

        if afrom > ato:
            errors.append(forms.ValidationError("Invalid date. Start date has to be before End date."))
        
        if afrom < datetime.now().date() or ato < datetime.now().date():
             errors.append(forms.ValidationError("Invalid date. Can't select dates before today."))
        
        if errors:
            raise forms.ValidationError(errors)
           
        return cleaned_data
    
class PostComment(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        labels = {"comment": '',}
        widgets = {"comment": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...', 'style':'resize:none;'})}

class MakeBooking(ModelForm):
    class Meta:
        model = Booking
        fields = ("startdate", "enddate")
        widgets = {
            "startdate": DateInput(attrs={'class': 'form-control', 'style': 'max-width:200px;'}),
            "enddate": DateInput(attrs={'class': 'form-control', 'style': 'max-width:200px;'})
            }
        
