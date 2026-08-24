from django.db import models
from django.conf import settings

# Create your models here.
class WebPages(models.Model):
    page_title          = models.CharField(max_length=20)
    page_content        = models.CharField(max_length=20)
    is_published        = models.BooleanField(default=False)

    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="webpages_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="webpages_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.page_title