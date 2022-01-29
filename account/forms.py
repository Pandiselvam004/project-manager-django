from django import forms
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.forms.models import ModelMultipleChoiceField
User = get_user_model()

formClass = "form-control form-control-lg form-control"


class PermissionModelChoices(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class RoleForm(forms.ModelForm):
    name = forms.CharField(
        error_messages={'required': 'Role Name field is required'},
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'Role Name'}), label=''
    )
    permissions = PermissionModelChoices(
        error_messages={'required': 'Select atleast one permission'},
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': formClass+" multi-select", })
    )

    class Meta:
        model = Group
        fields = '__all__'


class UserForm(forms.ModelForm):
    username = forms.CharField(
        error_messages={'required': 'User name field is required'},
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'User Name', 'autocomplete': 'new-password'}), label=''
    )
    groups = PermissionModelChoices(
        required=False,
        error_messages={'required': 'Role field is required'},
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': formClass+' multi-select'})
    )
    email = forms.CharField(
        validators=[validate_email],
        error_messages={'required': 'Email field is required'},
        widget=forms.EmailInput(attrs={'class': formClass, 'placeholder': 'Email', 'autocomplete': 'new-password'}), label=''
    )
    first_name = forms.CharField(
        error_messages={'required': 'First Name field is required'},
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'First Name'}), label=''
    )
    last_name = forms.CharField(
        error_messages={'required': 'Last Name field is required'},
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'Last Name'}), label=''
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': formClass, 'placeholder': 'Password', 'autocomplete': 'new-password'}), label=''
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': formClass, 'placeholder': 'Confirm Password'}), label=''
    )
    profile_img = forms.ImageField(required=False, widget=forms.FileInput)
    is_active = forms.CharField(widget=forms.HiddenInput(), initial=1)

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not self.instance.id and not password:
            self.add_error('password', "Password field is required")

        if password and len(password) < 6:
            self.add_error('password', "Passwords must have 6 characters")

        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match !")

        if not password and password == '':
            del self.cleaned_data['password']
        else:
            self.cleaned_data['password'] = make_password(
                self.cleaned_data['password'])

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
