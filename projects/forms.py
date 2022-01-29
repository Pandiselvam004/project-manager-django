from django import forms
from django.forms import ModelChoiceField
from projects.models import Project, Technology

formClass = "form-control form-control-lg form-control-solid"

class TechnologyChoiceField(ModelChoiceField):
    
    def label_from_instance(self, obj):
        return obj.name
    
    def to_python(self, value):
        if value in self.empty_values:
            return None
        return value


class ProjectFrom(forms.ModelForm):
    name = forms.CharField(
        error_messages={'required': 'Name field is required'},
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'Name',}), label=''
    )
    technologies = TechnologyChoiceField(
        empty_label = None,
        queryset=Technology.objects.all(),
        to_field_name='name',
        widget=forms.SelectMultiple(attrs={'class': 'form-select form-select-solid' ,'placeholder': 'Select an option',}), label=''
    )
    overview_document = forms.CharField(
        error_messages={'required': 'Document field is required'},
        widget=forms.Textarea(attrs={'class': formClass + ' kt_docs_ckeditor_classic'}), label=''
    )
    ssh_details = forms.CharField(
        error_messages={'required': 'SSH Details is required'},
        widget=forms.Textarea(attrs={'class': formClass+ ' kt_docs_ckeditor_classic'}), label=''
    )
    cpanel_details = forms.CharField(
        error_messages={'required': 'Cpanel Details is required'},
        widget=forms.Textarea(attrs={'class': formClass+ ' kt_docs_ckeditor_classic'}), label=''
    )
    ftp_details = forms.CharField(
        error_messages={'required': 'FTP Details is required'},
        widget=forms.Textarea(attrs={'class': formClass+ ' kt_docs_ckeditor_classic'}), label=''
    )
    key_link_url = forms.CharField(
        error_messages={'required': 'PEM Url field is required'},
        widget=forms.TextInput(attrs={'class': formClass, 'placeholder': 'PEM Url',}), label=''
    )
    
    class Meta:
        model = Project
        fields = '__all__'