# models.py

import os

from django.db import models
from django.conf import settings

def company_logo_upload_path(instance, filename):
    # Get original extension
    ext = os.path.splitext(filename)[1].lower()

    # Store as company/<id>/logo.ext
    return f"company/{instance.id}/logo{ext}"

class Company(models.Model):

    company_name    = models.CharField(max_length=255,unique=True)
    short_name      = models.CharField(max_length=100,blank=True,null=True)

    established_date = models.DateField(blank=True,null=True)

    logo            = models.ImageField(upload_to=company_logo_upload_path,blank=True,null=True)
    website         = models.URLField(blank=True, null=True)

    address_line1   = models.TextField(blank=True,null=True)
    address_line2   = models.TextField(blank=True,null=True)
    city            = models.TextField(blank=True,null=True)
    district        = models.TextField(blank=True,null=True)

    phone           = models.CharField(max_length=50, blank=True, null=True)
    email           = models.EmailField(blank=True,null=True)

    registration_number = models.CharField(max_length=100,blank=True,null=True,unique=True)
    tax_id_number = models.CharField(max_length=100,blank=True,null=True,unique=True)

    is_active       = models.BooleanField(default=True)

    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="company_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="company_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ["company_name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name

    