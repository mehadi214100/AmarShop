from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password1 =  forms.CharField(widget=forms.PasswordInput)
    password2 =  forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','email','city','phone']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2',"Passwords do not match")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email