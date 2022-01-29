from django.db import models
from django.utils.translation import gettext_lazy as _
from encrypted_model_fields import fields

# Create your models here.
class Technology(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    class Meta:
        db_table = 'technologies'
        
class Project(models.Model):
    name = models.CharField(max_length=30, unique=True)
    technologies = models.ManyToManyField(
        Technology,
        verbose_name=_('technologies'),
        blank=True,
    )
    overview_document = fields.EncryptedTextField(max_length=500,null=True)
    ssh_details = fields.EncryptedTextField(max_length=100,null=True)
    cpanel_details = fields.EncryptedTextField(max_length=100,null=True)
    ftp_details = fields.EncryptedTextField(max_length=100,null=True)
    key_link_url=fields.EncryptedTextField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True,null=True)
    
    class Meta:
        db_table = 'projects'

    
    
    