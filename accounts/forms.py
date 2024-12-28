from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    college_email = forms.EmailField(required=True,label="College Email")
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'college_email']

        def clean_college_email(self):
            college_email = self.cleaned_data.get('college_email')
            allowed_domain = "rvce.edu.in"  # Replace with your college domain
            if not college_email.endswith(f"@{allowed_domain}"):
                raise forms.ValidationError(f"Please use your college email address ending with @{allowed_domain}.")
            return college_email


class CustomLoginPage(AuthenticationForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)