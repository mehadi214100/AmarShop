
from django import forms
from accounts.models import userProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['profile_picture','city', 'postcode', 'gender', 'address_line_1', 'address_line_2']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your postal code'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address_line_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address line 1'}),
            'address_line_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address line 2'}),
        }
