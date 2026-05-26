from django.db import models

class InventoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class DepartmentSection(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    short_name  = models.CharField(max_length=25, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Department Sections'

    def __str__(self):
        return self.name
    
class OfficeLocationPlacement(models.Model):

    name = models.CharField(max_length=150, unique=True)
    building = models.CharField(max_length=150, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        parts = [self.name]
        if self.building:
            parts.append(self.building)
        if self.room:
            parts.append(f"Room {self.room}")
        return " - ".join(parts)

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    
    STATUS_CHOICES = [
        ('1', 'Available'),
        ('2', 'In Use'),
        ('3', 'Under Maintenance'),
        ('4', 'Damaged'),
        ('5', 'Retired'),
    ]

    FLOOR_CHOICES = [
        ('1', 'Ground Floor'),
        ('2', 'Second Floor'),
        ('3', 'Third Floor'),
    ]
    
    device_label    = models.CharField(max_length=200)
    device_name     = models.CharField(max_length=200)
    device_type     = models.CharField(max_length=100, blank=True, null=True)
    
    assigned_user   = models.CharField(max_length=100, unique=True)
    placement       = models.ForeignKey(OfficeLocationPlacement,on_delete=models.SET_NULL,related_name='items',blank=True,null=True)
    department_section = models.ForeignKey(DepartmentSection, on_delete=models.SET_NULL, blank=True, null=True)
    floor_level     = models.CharField(max_length=100, choices=FLOOR_CHOICES, blank=True, null=True)
    category        = models.ForeignKey(InventoryCategory,on_delete=models.PROTECT,related_name='items')
    
    manufacturer    = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)
    model_number    = models.CharField(max_length=100, blank=True, null=True)
    service_tag     = models.CharField(max_length=30, blank=True, null=True)
    
    processor       = models.CharField(max_length=100, blank=True, null=True)
    ram             = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    disk            = models.CharField(max_length=100, blank=True, null=True)

    device_status   = models.IntegerField(max_length=20, choices=STATUS_CHOICES, default='1')
    serial_number   = models.CharField(max_length=150, blank=True, null=True)
    mac_address     = models.CharField(max_length=150, blank=True, null=True)
    ip_address      = models.CharField(max_length=150, blank=True, null=True)

    acquisition_date    = models.DateField(blank=True, null=True)
    date_issued         = models.DateField(blank=True, null=True)

    sponsor         = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''class Meta:
        ordering = ['device_label']
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'''

    def __str__(self):
        return f"{self.device_label} ({self.service_tag})"