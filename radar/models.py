from django.db import models

# Create your models here.
class RadarImages(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_title = models.CharField(max_length=100)
    image_url = models.CharField(max_length=500)
    web_directory = models.CharField(max_length=500, default='/media/radar/', null=True, blank=True)
    display_order = models.IntegerField(default=0, null=True, blank=True)
    is_published = models.BooleanField(default=False, null=True, blank=True)
    published_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Radar Image"
        verbose_name_plural = "Radar Images"

    def __str__(self): return self.image_url