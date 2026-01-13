from django.db import models

# Create your models here.
class RadarImages(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_title = models.CharField(max_length=100)
    image_url = models.CharField(max_length=500)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self): return self.image_url