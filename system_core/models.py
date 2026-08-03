from django.db import models

# Create your models here.

class Months(models.Model):
    id = models.BigAutoField(primary_key=True)
    month_name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=3,null=True, blank=True)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Month"
        verbose_name_plural = "Months"

    def __str__(self): return self.short_name.upper()

class Zone(models.Model):
    id = models.BigAutoField(primary_key=True)
    zone_name = models.CharField(max_length=50)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self): return self.zone_name

class District(models.Model):
    district_name = models.CharField(max_length=100, unique=True)
    zone_id = models.ForeignKey(Zone, related_name='zone_id', on_delete=models.CASCADE,null=True)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ["district_name"]

    def __str__(self):
        return self.district_name

class AlertLevel(models.Model):
    description = models.CharField(max_length=20)
    color       = models.CharField(max_length=20,default="",null=True, blank=True)

    def __str__(self):
        return self.description

class RiskLevel(models.Model):
    description = models.CharField(max_length=20)
    color = models.CharField(max_length=20,default="",null=True, blank=True)

    def __str__(self):
        return f"{self.description}"

class Sectors(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=20)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"

    def __str__(self): return self.description

class DepartmentSection(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    short_name  = models.CharField(max_length=25, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Department Sections'

    def __str__(self):
        return self.name

class OfficeLocation(models.Model):

    FLOOR_CHOICES = [
        ('1', 'Ground Floor'),
        ('2', 'Second Floor'),
        ('3', 'Third Floor'),
    ]

    name = models.CharField(max_length=150, unique=True)
    floor     = models.CharField(max_length=100, choices=FLOOR_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        parts = [self.name]
        #if self.building:
        #    parts.append(self.building)
        if self.floor:
            parts.append(f"Floor {self.floor}")
        return " - ".join(parts)

class JobTitle(models.Model):
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['description']
        verbose_name_plural = 'Job Titles'

    def __str__(self):
        return self.description