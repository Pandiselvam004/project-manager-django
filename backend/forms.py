from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
formClass = "form-control form-control-lg form-control-solid"

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'Email','autocomplete' : 'new-password'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': formClass, 'placeholder': 'Password','autocomplete' : 'new-password'})
    )