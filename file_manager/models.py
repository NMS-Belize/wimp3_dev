from django.db import models
from django.conf import settings
from django.utils import timezone

class FileCategory(models.Model):
    
    category_name   = models.CharField(max_length=150,unique=True)
    description     = models.TextField(blank=True,null=True)
    is_active       = models.BooleanField(default=True)

    class Meta:
        verbose_name = "File Category"
        verbose_name_plural = "File Categories"
        ordering = ["category_name"]

    def __str__(self):
        return self.category_name


class FileType(models.Model):

    file_type_name  = models.CharField(max_length=100,unique=True)
    description     = models.TextField(blank=True,null=True)
    is_active       = models.BooleanField(default=True)

    class Meta:
        verbose_name = "File Type"
        verbose_name_plural = "File Types"
        ordering = ["file_type_name"]

    def __str__(self):
        return self.file_type_name


class Files(models.Model):

    STATUS_CHOICES = ((0, "Draft"),(1, "Published"))

    file_title          = models.CharField(max_length=255)
    category            = models.ForeignKey(FileCategory,on_delete=models.PROTECT,related_name="files")
    publication_date    = models.DateField(blank=True,null=True)
    file_type           = models.ForeignKey(FileType,on_delete=models.SET_NULL,related_name="files",blank=True,null=True)
    file                = models.FileField(upload_to="file_manager/documents/")

    thumbnail_image     = models.ImageField(upload_to="file_manager/thumbnails/",blank=True,null=True)
    file_description    = models.TextField(blank=True,null=True)

    file_summary = models.TextField(blank=True,null=True)

    tags                = models.CharField(max_length=500,blank=True,null=True,help_text="Comma-separated tags")

    is_published        = models.BooleanField(default=False)

    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="file_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="file_updated")
    created_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ["-publication_date", "-created_datetime"]

    def __str__(self):
        return self.file_title

    @property
    def is_published(self):
        return self.is_published

    @property
    def filename(self):
        if self.file:
            return self.file.name.split("/")[-1]
        return ""

    @property
    def file_extension(self):
        if self.file:
            return self.file.name.rsplit(".", 1)[-1].lower()
        return ""